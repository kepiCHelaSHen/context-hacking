"""
CHP Kill Switch — Memory Guardian for Time Sprint
Monitors a child process and terminates it if RSS exceeds LIMIT_GB.
Also enforces a wall-clock timeout.

Usage:
    python kill_switch.py <script.py> [args...] --limit-gb 4.0 --timeout 120

Returns exit code 0 if child completed normally, 1 if killed for memory,
2 if killed for timeout.
"""

import argparse
import subprocess
import sys
import time

import psutil


def monitor_process(cmd: list, limit_gb: float, timeout_s: float) -> dict:
    """Run cmd as subprocess, kill if it exceeds memory or time limits.

    Returns dict with:
        status: 'completed' | 'memory_killed' | 'timeout_killed' | 'error'
        peak_memory_gb: float
        elapsed_s: float
        stdout: str
        stderr: str
    """
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    start = time.time()
    peak_memory_gb = 0.0
    status = "completed"

    try:
        ps_proc = psutil.Process(proc.pid)
    except psutil.NoSuchProcess:
        proc.wait()
        return {
            "status": "error",
            "peak_memory_gb": 0,
            "elapsed_s": time.time() - start,
            "stdout": proc.stdout.read().decode(errors="replace") if proc.stdout else "",
            "stderr": proc.stderr.read().decode(errors="replace") if proc.stderr else "",
        }

    while proc.poll() is None:
        elapsed = time.time() - start

        # Check timeout
        if elapsed > timeout_s:
            print(f"KILL SWITCH: Timeout ({timeout_s}s) exceeded at {elapsed:.1f}s. "
                  f"Terminating PID {proc.pid}.")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            status = "timeout_killed"
            break

        # Check memory
        try:
            mem_info = ps_proc.memory_info()
            mem_gb = mem_info.rss / (1024 ** 3)
            if mem_gb > peak_memory_gb:
                peak_memory_gb = mem_gb
            if mem_gb > limit_gb:
                print(f"KILL SWITCH: Memory limit ({limit_gb}GB) exceeded at "
                      f"{mem_gb:.2f}GB. Terminating PID {proc.pid}.")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                status = "memory_killed"
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        time.sleep(0.5)

    elapsed = time.time() - start
    stdout = proc.stdout.read().decode(errors="replace") if proc.stdout else ""
    stderr = proc.stderr.read().decode(errors="replace") if proc.stderr else ""

    return {
        "status": status,
        "peak_memory_gb": peak_memory_gb,
        "elapsed_s": elapsed,
        "stdout": stdout,
        "stderr": stderr,
        "returncode": proc.returncode,
    }


def main():
    # Split on '--' to separate kill switch args from child args
    argv = sys.argv[1:]
    if "--" in argv:
        ks_args = argv[:argv.index("--")]
        child_args = argv[argv.index("--") + 1:]
    else:
        # Auto-detect: first positional arg is script, everything after is child args
        ks_args = []
        child_args = []
        script = None
        i = 0
        while i < len(argv):
            if argv[i] == "--limit-gb" and i + 1 < len(argv):
                ks_args.extend([argv[i], argv[i + 1]])
                i += 2
            elif argv[i] == "--timeout" and i + 1 < len(argv):
                ks_args.extend([argv[i], argv[i + 1]])
                i += 2
            elif argv[i] in ("-h", "--help"):
                ks_args.append(argv[i])
                i += 1
            elif script is None:
                script = argv[i]
                i += 1
            else:
                child_args.append(argv[i])
                i += 1
        if script:
            ks_args.insert(0, script)

    parser = argparse.ArgumentParser(description="CHP Kill Switch — Memory & Time Guardian")
    parser.add_argument("script", help="Python script to run")
    parser.add_argument("--limit-gb", type=float, default=4.0,
                        help="Memory limit in GB (default: 4.0)")
    parser.add_argument("--timeout", type=float, default=120.0,
                        help="Wall-clock timeout in seconds (default: 120)")
    args = parser.parse_args(ks_args)

    cmd = [sys.executable, args.script] + child_args
    print(f"KILL SWITCH: Monitoring {' '.join(cmd)}")
    print(f"KILL SWITCH: Memory limit = {args.limit_gb}GB, Timeout = {args.timeout}s")
    print("=" * 60)

    result = monitor_process(cmd, args.limit_gb, args.timeout)

    print("=" * 60)
    print(f"KILL SWITCH REPORT:")
    print(f"  Status:      {result['status']}")
    print(f"  Peak memory: {result['peak_memory_gb']:.3f} GB")
    print(f"  Elapsed:     {result['elapsed_s']:.2f}s")

    if result["status"] == "memory_killed":
        print(f"  DEAD_END: Memory Limit Exceeded ({result['peak_memory_gb']:.2f}GB > {args.limit_gb}GB)")
        sys.exit(1)
    elif result["status"] == "timeout_killed":
        print(f"  DEAD_END: Timeout Exceeded ({result['elapsed_s']:.1f}s > {args.timeout}s)")
        sys.exit(2)
    elif result.get("returncode", 0) != 0:
        print(f"  ERROR: Process exited with code {result.get('returncode')}")
        if result["stderr"]:
            print(f"  STDERR: {result['stderr'][:500]}")
        sys.exit(3)
    else:
        print(f"  SUCCESS: Completed normally")
        if result["stdout"]:
            # Print last 20 lines of stdout
            lines = result["stdout"].strip().split("\n")
            for line in lines[-20:]:
                try:
                    print(f"  > {line}")
                except UnicodeEncodeError:
                    print(f"  > {line.encode('ascii', errors='replace').decode()}")
        sys.exit(0)


if __name__ == "__main__":
    main()
