"""
utils/charts.py
Plotly chart helpers for the dashboard and results pages.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


_COLORS = {
    "accent":  "#6c63ff",
    "accent2": "#00d4ff",
    "accent3": "#ff6584",
    "success": "#00e676",
    "warning": "#ffab40",
    "bg":      "rgba(0,0,0,0)",
    "grid":    "rgba(255,255,255,0.06)",
    "text":    "#8888aa",
}


def _base_layout(title: str = "") -> dict:
    return dict(
        title=dict(text=title, font=dict(family="Syne", size=16, color="#f0f0f8")),
        paper_bgcolor=_COLORS["bg"],
        plot_bgcolor=_COLORS["bg"],
        font=dict(family="Inter", color=_COLORS["text"]),
        margin=dict(l=32, r=32, t=48, b=32),
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#f0f0f8")),
    )


def radar_chart(scores: dict) -> go.Figure:
    """Render a radar chart for technical/communication/confidence/overall scores."""
    categories = list(scores.keys())
    values = list(scores.values())
    values.append(values[0])   # close the loop
    categories.append(categories[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values, theta=categories, fill="toself",
        fillcolor="rgba(108,99,255,0.2)",
        line=dict(color=_COLORS["accent"], width=2),
        name="Score",
    ))
    fig.update_layout(
        **_base_layout("Performance Radar"),
        polar=dict(
            bgcolor="rgba(255,255,255,0.03)",
            radialaxis=dict(visible=True, range=[0, 100],
                            color=_COLORS["text"], gridcolor=_COLORS["grid"]),
            angularaxis=dict(color=_COLORS["text"], gridcolor=_COLORS["grid"]),
        ),
    )
    return fig


def score_bar_chart(scores: dict) -> go.Figure:
    """Horizontal bar chart for score breakdown."""
    labels = list(scores.keys())
    values = list(scores.values())
    colors = [_COLORS["success"] if v >= 70 else _COLORS["warning"] if v >= 50 else "#ff5252"
              for v in values]

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v}" for v in values],
        textposition="outside",
        textfont=dict(color="#f0f0f8"),
    ))
    fig.update_layout(
        **_base_layout("Score Breakdown"),
        xaxis=dict(range=[0, 110], gridcolor=_COLORS["grid"], color=_COLORS["text"]),
        yaxis=dict(gridcolor=_COLORS["grid"], color="#f0f0f8"),
    )
    return fig


def trend_line_chart(history: list[dict]) -> go.Figure:
    """Line chart showing overall score improvement over time."""
    if not history:
        fig = go.Figure()
        fig.update_layout(**_base_layout("Score Trend (no data yet)"))
        return fig

    df = pd.DataFrame(history)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["overall_score"],
        mode="lines+markers",
        line=dict(color=_COLORS["accent"], width=3, shape="spline"),
        marker=dict(size=8, color=_COLORS["accent2"],
                    line=dict(width=2, color=_COLORS["accent"])),
        fill="tozeroy",
        fillcolor="rgba(108,99,255,0.08)",
        name="Overall Score",
    ))
    fig.update_layout(
        **_base_layout("Score Improvement Trend"),
        xaxis=dict(gridcolor=_COLORS["grid"], color=_COLORS["text"]),
        yaxis=dict(range=[0, 105], gridcolor=_COLORS["grid"], color=_COLORS["text"]),
    )
    return fig


def pie_chart(labels: list, values: list, title: str) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=[_COLORS["accent"], _COLORS["accent2"],
                            _COLORS["accent3"], _COLORS["success"]],
                    line=dict(color="#0d0f1a", width=2)),
        textfont=dict(color="#f0f0f8"),
    ))
    fig.update_layout(**_base_layout(title))
    return fig


def ats_gauge(score: float) -> go.Figure:
    """Gauge chart for ATS score."""
    color = _COLORS["success"] if score >= 70 else _COLORS["warning"] if score >= 50 else "#ff5252"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "ATS Score", "font": {"size": 18, "color": "#f0f0f8", "family": "Syne"}},
        number={"font": {"size": 40, "color": color, "family": "Syne"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": _COLORS["text"]},
            "bar": {"color": color},
            "bgcolor": "rgba(255,255,255,0.04)",
            "bordercolor": "rgba(255,255,255,0.1)",
            "steps": [
                {"range": [0, 50],  "color": "rgba(255,82,82,0.1)"},
                {"range": [50, 70], "color": "rgba(255,171,64,0.1)"},
                {"range": [70, 100],"color": "rgba(0,230,118,0.1)"},
            ],
            "threshold": {
                "line": {"color": "#ffffff", "width": 2},
                "thickness": 0.75,
                "value": score,
            },
        },
    ))
    fig.update_layout(paper_bgcolor=_COLORS["bg"], font=dict(color=_COLORS["text"]),
                      margin=dict(l=24, r=24, t=48, b=24))
    return fig
