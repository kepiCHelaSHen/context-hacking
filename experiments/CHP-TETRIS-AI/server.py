"""CHP-TETRIS-AI WebSocket server."""
import asyncio
import json
import logging
import webbrowser
from pathlib import Path

from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from starlette.responses import JSONResponse

_log = logging.getLogger(__name__)
EXPERIMENT_DIR = Path(__file__).parent


# ============================================================================
# TetrisServer
# ============================================================================


class TetrisServer:
    def __init__(self):
        self.clients: set = set()               # connected WebSocket clients
        self.state: list[dict] = []             # all messages (for reconnection)
        self.running: bool = False              # is a run in progress?
        self.mode: str = "demo"                 # "demo" or "live"
        self.speed: float = 5.0                 # replay speed multiplier
        self._task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()

    # ------------------------------------------------------------------
    # broadcast
    # ------------------------------------------------------------------

    async def broadcast(self, message: dict) -> None:
        """Append message to state history and send to all connected clients.

        Disconnected clients are silently removed from the set.
        """
        self.state.append(message)
        encoded = json.dumps(message)
        dead: set = set()
        for ws in self.clients:
            try:
                await ws.send_text(encoded)
            except Exception:
                dead.add(ws)
        self.clients -= dead

    # ------------------------------------------------------------------
    # websocket_endpoint
    # ------------------------------------------------------------------

    async def websocket_endpoint(self, websocket: WebSocket) -> None:
        """Accept a WebSocket connection, replay existing state, then listen."""
        await websocket.accept()
        self.clients.add(websocket)
        _log.info("WebSocket client connected (%d total)", len(self.clients))

        # Replay all messages accumulated so far (reconnection support)
        for msg in self.state:
            try:
                await websocket.send_text(json.dumps(msg))
            except Exception:
                break

        # Keep the connection alive and listen for incoming messages
        try:
            while True:
                data = await websocket.receive_text()
                # Future: handle client->server commands here
                _log.debug("Received from client: %s", data)
        except Exception:
            pass
        finally:
            self.clients.discard(websocket)
            _log.info("WebSocket client disconnected (%d remaining)", len(self.clients))

    # ------------------------------------------------------------------
    # start_live
    # ------------------------------------------------------------------

    async def start_live(self, config_path: str) -> None:
        """Start the live optimizer loop, passing broadcast as the broadcast_fn."""
        if self.running:
            _log.warning("start_live called while already running — ignoring")
            return

        self._stop_event.clear()
        self.running = True
        self.mode = "live"

        async def _live_runner():
            try:
                import sys
                sys.path.insert(0, str(EXPERIMENT_DIR))
                from optimizer import run_loop  # noqa: PLC0415
                await run_loop(config_path, self.broadcast)
            except Exception as e:
                _log.error("Live optimizer error: %s", e)
                await self.broadcast({"type": "error", "message": str(e)})
            finally:
                self.running = False

        self._task = asyncio.create_task(_live_runner())

    # ------------------------------------------------------------------
    # start_demo
    # ------------------------------------------------------------------

    async def start_demo(self, history_path: str) -> None:
        """Replay run_history.json with delays based on timestamps."""
        if self.running:
            _log.warning("start_demo called while already running — ignoring")
            return

        self._stop_event.clear()
        self.running = True
        self.mode = "demo"

        async def _demo_runner():
            try:
                history_file = Path(history_path)
                if not history_file.exists():
                    _log.warning("run_history.json not found at %s — demo aborted", history_path)
                    await self.broadcast({
                        "type": "error",
                        "message": f"run_history.json not found: {history_path}",
                    })
                    return

                messages: list[dict] = json.loads(history_file.read_text(encoding="utf-8"))
                if not messages:
                    _log.warning("run_history.json is empty")
                    return

                # Determine time deltas between messages
                prev_ts: float | None = None
                for msg in messages:
                    if self._stop_event.is_set():
                        _log.info("Demo stopped by stop_event")
                        break

                    ts = msg.get("ts") or msg.get("timestamp")
                    if ts is not None and prev_ts is not None:
                        raw_delay = float(ts) - float(prev_ts)
                        # Apply speed multiplier (clamp to reasonable bounds)
                        delay = max(0.0, raw_delay) / max(self.speed, 0.1)
                        delay = min(delay, 5.0)  # cap at 5 s regardless of speed
                        if delay > 0:
                            try:
                                await asyncio.wait_for(
                                    self._stop_event.wait(),
                                    timeout=delay,
                                )
                                # If we get here the event was set — stop
                                break
                            except asyncio.TimeoutError:
                                pass  # Normal — just means the delay elapsed

                    prev_ts = ts
                    await self.broadcast(msg)

                _log.info("Demo replay complete")
                await self.broadcast({"type": "demo_complete"})
            except FileNotFoundError:
                _log.warning("run_history.json not found (FileNotFoundError)")
                await self.broadcast({"type": "error", "message": "run_history.json not found"})
            except Exception as e:
                _log.error("Demo runner error: %s", e)
                await self.broadcast({"type": "error", "message": str(e)})
            finally:
                self.running = False

        self._task = asyncio.create_task(_demo_runner())

    # ------------------------------------------------------------------
    # stop
    # ------------------------------------------------------------------

    async def stop(self) -> None:
        """Signal the running task to stop and cancel it."""
        self._stop_event.set()
        if self._task is not None and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except (asyncio.CancelledError, Exception):
                pass
        self.running = False
        self._task = None
        _log.info("Server stopped")

    # ------------------------------------------------------------------
    # reset
    # ------------------------------------------------------------------

    async def reset(self) -> None:
        """Stop, clear all accumulated state, and notify clients."""
        await self.stop()
        self.state.clear()
        await self.broadcast({"type": "reset"})
        _log.info("Server reset")


# ============================================================================
# Singleton server instance
# ============================================================================

server = TetrisServer()


# ============================================================================
# API route handlers
# ============================================================================


async def api_start(request):
    body = await request.json()
    mode = body.get("mode", "demo")
    if mode == "live":
        await server.start_live(str(EXPERIMENT_DIR / "config.yaml"))
    else:
        await server.start_demo(str(EXPERIMENT_DIR / "run_history.json"))
    return JSONResponse({"status": "started", "mode": mode})


async def api_stop(request):
    await server.stop()
    return JSONResponse({"status": "stopped"})


async def api_reset(request):
    await server.reset()
    return JSONResponse({"status": "reset"})


async def api_speed(request):
    body = await request.json()
    speed = float(body.get("speed", server.speed))
    server.speed = speed
    return JSONResponse({"status": "ok", "speed": speed})


# ============================================================================
# Startup handler
# ============================================================================


async def on_startup():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    url = "http://localhost:8080"
    _log.info("CHP-TETRIS-AI server running at %s", url)
    _log.info("WebSocket endpoint: ws://localhost:8080/ws")
    # Optionally open browser (comment out if running headless)
    # webbrowser.open(url)


# ============================================================================
# Starlette app
# ============================================================================

app = Starlette(
    on_startup=[on_startup],
    routes=[
        WebSocketRoute("/ws", server.websocket_endpoint),
        Route("/api/start", api_start, methods=["POST"]),
        Route("/api/stop", api_stop, methods=["POST"]),
        Route("/api/reset", api_reset, methods=["POST"]),
        Route("/api/speed", api_speed, methods=["POST"]),
        Mount("/", StaticFiles(directory=str(EXPERIMENT_DIR / "dashboard"), html=True)),
    ],
)
