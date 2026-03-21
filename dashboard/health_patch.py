"""
health_patch.py — Drop-in replacement for _render_protocol_health.
Import this after app.py imports and call patch() to replace the function.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
import streamlit as st


def render_protocol_health_contained(project_dir: Path) -> None:
    """Contained 2-column Protocol Health tab — max-width 960px, charts in pairs."""
    import plotly.graph_objects as go

    # Inject contained-width CSS once
    st.markdown("""
    <style>
    /* Contain the health tab to 960px centred */
    [data-testid="stVerticalBlock"] .health-outer {
        max-width: 960px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

    telemetry_path = project_dir / ".chp" / "telemetry.json"

    CHART = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FAFBFC",
        font=dict(family="IBM Plex Mono, monospace", color="#6B7280", size=10),
        margin=dict(l=44, r=16, t=32, b=32),
        height=195,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(family="IBM Plex Mono", size=9, color="#9CA3AF"),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        ),
    )
    AX = dict(
        gridcolor="#EEF0F6", linecolor="#E2E5EF", zerolinecolor="#E2E5EF",
        tickfont=dict(family="IBM Plex Mono", size=9, color="#9CA3AF"),
        showgrid=True,
    )

    # ── Header ────────────────────────────────────────────────────────
    st.markdown(
        '<div style="max-width:960px;margin:0 auto;">'
        '<div class="sh"><span class="sh-lbl">Protocol Health — Is the loop learning?</span>'
        '<div class="sh-line"></div></div>'
        '<p style="font-size:0.73rem;color:var(--t3);margin:-4px 0 14px;">'
        'Healthy loop: declining drift &nbsp;·&nbsp; improving gate scores &nbsp;·&nbsp; '
        'faster turns &nbsp;·&nbsp; fewer fix cycles</p>',
        unsafe_allow_html=True,
    )

    if not telemetry_path.exists():
        st.markdown(
            '<div style="font-family:var(--mono);font-size:0.68rem;color:var(--t4);'
            'text-align:center;padding:40px;border:1px dashed #C8CCDB;border-radius:4px;">'
            'awaiting telemetry<br>'
            '<span style="font-size:0.60rem;">run chp run --method api to record</span>'
            '</div></div>',
            unsafe_allow_html=True,
        )
        return

    try:
        data       = json.loads(telemetry_path.read_text(encoding="utf-8"))
        turns_data = data.get("turns", [])
    except Exception:
        st.error("Failed to load telemetry.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    if not turns_data:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # ── Summary stats ─────────────────────────────────────────────────
    total_tokens = sum(t.get("tokens_total", 0) for t in turns_data)
    total_lines  = sum(t.get("lines_written", 0) for t in turns_data)
    total_time   = sum(t.get("duration_seconds", 0) for t in turns_data)
    n_fp   = sum(1 for t in turns_data if t.get("false_positive_caught"))
    n_de   = sum(t.get("dead_ends_avoided", 0) for t in turns_data)
    tested = [t for t in turns_data
              if t.get("tests_passed", 0) + t.get("tests_failed", 0) > 0]
    ftr    = sum(1 for t in tested if t.get("tests_passed_first_try")) / max(len(tested), 1)
    tpl    = round(total_tokens / max(total_lines, 1), 1)

    # Primary stat cards — 4 col
    col1, col2, col3, col4 = st.columns(4)
    for col, lbl, val, sub in [
        (col1, "Tokens / Line",    f"{tpl}",     "lower = more efficient"),
        (col2, "False Pos. Caught",str(n_fp),    "killed before merge"),
        (col3, "Dead Ends Avoided",str(n_de),    "mistakes not repeated"),
        (col4, "First-Try Pass",   f"{ftr:.0%}", "no fix cycle needed"),
    ]:
        with col:
            st.markdown(
                f'<div class="sc" style="max-width:220px;">'
                f'<div class="sc-lbl">{lbl}</div>'
                f'<div class="sc-val">{val}</div>'
                f'<div class="sc-sub">{sub}</div></div>',
                unsafe_allow_html=True,
            )

    # Secondary row — smaller
    col5, col6, col7, col8 = st.columns(4)
    for col, lbl, val in [
        (col5, "Total Tokens", f"{total_tokens:,}"),
        (col6, "Lines Built",  f"{total_lines:,}"),
        (col7, "Total Time",   f"{total_time/60:.1f} min"),
        (col8, "Turns",        str(len(turns_data))),
    ]:
        with col:
            st.markdown(
                f'<div class="sc" style="border-top-color:#C8CCDB;padding:9px 14px;max-width:220px;">'
                f'<div class="sc-lbl">{lbl}</div>'
                f'<div class="sc-val" style="font-size:1.05rem;">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Section header ─────────────────────────────────────────────────
    st.markdown(
        '<div class="sh" style="max-width:960px;margin:18px auto 8px;">'
        '<span class="sh-lbl">Trends Over Time</span>'
        '<div class="sh-line"></div></div>',
        unsafe_allow_html=True,
    )

    turn_nums = [t.get("turn", i + 1) for i, t in enumerate(turns_data)]
    fp_turns  = [t["turn"] for t in turns_data if t.get("false_positive_caught")]

    def _add_fp_markers(fig: go.Figure) -> None:
        for tn in fp_turns:
            fig.add_vline(x=tn, line_color="#D97706", line_width=1, line_dash="dot")
            fig.add_annotation(
                x=tn, text="◆ FP", showarrow=False,
                font=dict(size=8, color="#D97706"),
                yref="paper", y=1.01,
            )

    # ── Row 1: Tokens | Gate scores ───────────────────────────────────
    left, right = st.columns(2)

    tokens = [t.get("tokens_total", 0) for t in turns_data]
    with left:
        if any(x > 0 for x in tokens):
            avgs = [
                sum(tokens[max(0, i-2):i+1]) / len(tokens[max(0, i-2):i+1])
                for i in range(len(tokens))
            ]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=turn_nums, y=tokens, name="tokens",
                mode="lines+markers",
                line=dict(color="#3B82F6", width=1.5), marker=dict(size=5),
            ))
            fig.add_trace(go.Scatter(
                x=turn_nums, y=avgs, name="3T avg",
                mode="lines", line=dict(color="#D97706", width=1, dash="dot"),
            ))
            _add_fp_markers(fig)
            fig.update_layout(title="Tokens per turn", xaxis=AX, yaxis=AX, **CHART)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                '<div style="height:195px;display:flex;align-items:center;'
                'justify-content:center;border:1px dashed #C8CCDB;border-radius:4px;'
                'font-family:\'IBM Plex Mono\',monospace;font-size:0.65rem;color:#9CA3AF;">'
                'no token data yet</div>',
                unsafe_allow_html=True,
            )

    g1 = [t.get("gate_1_frozen", 0) for t in turns_data]
    g3 = [t.get("gate_3_scientific", 0) for t in turns_data]
    with right:
        if any(x > 0 for x in g1):
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=turn_nums, y=g1, name="G1 Frozen",
                mode="lines+markers",
                line=dict(color="#10B981", width=1.5), marker=dict(size=5),
            ))
            fig.add_trace(go.Scatter(
                x=turn_nums, y=g3, name="G3 Scientific",
                mode="lines+markers",
                line=dict(color="#F59E0B", width=1.5), marker=dict(size=5),
            ))
            fig.add_hline(
                y=0.85, line_dash="dot", line_color="#D97706", line_width=1,
                annotation_text="0.85",
                annotation_font=dict(size=8, color="#D97706"),
                annotation_position="bottom right",
            )
            _add_fp_markers(fig)
            fig.update_layout(
                title="Critic gate scores",
                xaxis=AX,
                yaxis=dict(**AX, range=[0.5, 1.05]),
                **CHART,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                '<div style="height:195px;display:flex;align-items:center;'
                'justify-content:center;border:1px dashed #C8CCDB;border-radius:4px;'
                'font-family:\'IBM Plex Mono\',monospace;font-size:0.65rem;color:#9CA3AF;">'
                'no gate score data yet</div>',
                unsafe_allow_html=True,
            )

    # ── Row 2: Time lollipop | Key events ─────────────────────────────
    left2, right2 = st.columns(2)

    times = [t.get("duration_seconds", 0) for t in turns_data]
    with left2:
        if any(x > 0 for x in times):
            clrs = [
                "#10B981" if x < 300 else "#F59E0B" if x < 600 else "#EF4444"
                for x in times
            ]
            fig = go.Figure()
            for i, (tn, tv) in enumerate(zip(turn_nums, times)):
                fig.add_trace(go.Scatter(
                    x=[tn, tn], y=[0, tv / 60], mode="lines",
                    line=dict(color=clrs[i], width=2), showlegend=False,
                ))
            fig.add_trace(go.Scatter(
                x=turn_nums, y=[t / 60 for t in times], mode="markers",
                marker=dict(
                    color=clrs, size=9,
                    line=dict(width=1.5, color="white"),
                ),
                showlegend=False,
            ))
            fig.update_layout(title="Time per turn (min)", xaxis=AX, yaxis=AX, **CHART)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                '<div style="height:195px;display:flex;align-items:center;'
                'justify-content:center;border:1px dashed #C8CCDB;border-radius:4px;'
                'font-family:\'IBM Plex Mono\',monospace;font-size:0.65rem;color:#9CA3AF;">'
                'no timing data yet</div>',
                unsafe_allow_html=True,
            )

    with right2:
        st.markdown(
            '<div class="sh" style="margin-top:4px;">'
            '<span class="sh-lbl">Key Events</span>'
            '<div class="sh-line"></div></div>',
            unsafe_allow_html=True,
        )
        has_events = False
        for t in turns_data:
            n = t.get("turn", "?")
            if t.get("false_positive_caught"):
                has_events = True
                desc = t.get("false_positive_description", "see innovation log")
                # Truncate long descriptions
                if len(desc) > 120:
                    desc = desc[:117] + "..."
                st.markdown(
                    f'<div class="fp-box" style="padding:8px 12px;margin:4px 0;">'
                    f'<div class="fp-hdr" style="margin-bottom:2px;">'
                    f'◆ Turn {n} — False Positive Caught</div>'
                    f'<div class="fp-body" style="font-size:0.70rem;">{desc}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            if t.get("anomaly"):
                has_events = True
                st.markdown(
                    f'<div style="background:var(--failbg);border-left:3px solid '
                    f'var(--failbd);padding:7px 12px;margin:4px 0;border-radius:0 4px 4px 0;'
                    f'font-family:var(--mono);font-size:0.68rem;color:var(--fail);">'
                    f'Turn {n}: ANOMALY — sigma-gate failed</div>',
                    unsafe_allow_html=True,
                )
        if not has_events:
            st.markdown(
                '<div style="font-family:var(--mono);font-size:0.68rem;color:var(--t4);'
                'text-align:center;padding:24px;border:1px dashed #C8CCDB;border-radius:4px;">'
                'clean run<br><span style="font-size:0.60rem;">no anomalies or false positives</span>'
                '</div>',
                unsafe_allow_html=True,
            )

    # Close outer max-width wrapper
    st.markdown('</div>', unsafe_allow_html=True)
