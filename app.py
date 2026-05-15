# ─────────────────────────────────────────────────────────────────────────────
#  Seth Mini Data Warehouse — Professional Analytics Dashboard
#  app.py  |  Streamlit + Plotly  |  Pro Build
# ─────────────────────────────────────────────────────────────────────────────

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ── 1. PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Seth Mini DW · Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 2. GLOBAL CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── App background ── */
    .stApp {
        background: #0f1117;
        color: #e2e8f0;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #161b27 !important;
        border-right: 1px solid #2d3748;
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #63b3ed;
        font-size: 11px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    /* ── KPI Cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }
    .kpi-card {
        background: #161b27;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px 22px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
    }
    .kpi-card.blue::before  { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .kpi-card.green::before { background: linear-gradient(90deg, #10b981, #34d399); }
    .kpi-card.red::before   { background: linear-gradient(90deg, #ef4444, #f87171); }
    .kpi-card.purple::before{ background: linear-gradient(90deg, #8b5cf6, #a78bfa); }

    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        color: #718096;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #f7fafc;
        font-family: 'DM Mono', monospace;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 12px;
        color: #4a5568;
        margin-top: 6px;
    }

    /* ── Section headers ── */
    .section-header {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #718096;
        margin: 24px 0 12px;
        border-bottom: 1px solid #2d3748;
        padding-bottom: 8px;
    }

    /* ── Divider ── */
    hr { border-color: #2d3748 !important; }

    /* ── DataFrame ── */
    [data-testid="stDataFrame"] {
        border: 1px solid #2d3748;
        border-radius: 10px;
        overflow: hidden;
    }

    /* ── Filter pills (active indicator) ── */
    .filter-badge {
        display: inline-block;
        background: #1e3a5f;
        color: #63b3ed;
        border: 1px solid #2b6cb0;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 11px;
        font-weight: 600;
        margin: 2px 3px;
    }

    /* ── Plotly charts background ── */
    .js-plotly-plot .plotly .bg { fill: transparent !important; }

    /* ── Streamlit overrides ── */
    .stSelectbox label, .stMultiSelect label,
    .stDateInput label, .stFileUploader label {
        color: #a0aec0 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetric"] { display: none; }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ── 3. PLOTLY THEME ────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#a0aec0", size=12),
    margin=dict(l=16, r=16, t=36, b=16),
    xaxis=dict(gridcolor="#2d3748", linecolor="#2d3748", tickcolor="#4a5568"),
    yaxis=dict(gridcolor="#2d3748", linecolor="#2d3748", tickcolor="#4a5568"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#2d3748"),
    colorway=["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"],
)

DAYS_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ── 4. DATA LOADING ────────────────────────────────────────────────────────────
@st.cache_data
def load_default() -> pd.DataFrame:
    df = pd.read_csv("datasets/processed/cleaned_records.csv")
    return _prep(df)

def _prep(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["record_date"] = pd.to_datetime(df["record_date"])
    df["normal_sign"] = pd.to_numeric(df["normal_sign"], errors="coerce")
    if "day_of_week" not in df.columns:
        df["day_of_week"] = df["record_date"].dt.day_name()
    if "month" not in df.columns:
        df["month"] = df["record_date"].dt.month_name()
    df["month_num"] = df["record_date"].dt.month  # for correct month ordering
    return df

# ── 5. SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Seth Mini DW")
    st.markdown("<hr style='margin:8px 0 16px'>", unsafe_allow_html=True)

    # 5a. File uploader
    st.markdown("### 📁 Data Source")
    uploaded = st.file_uploader(
        "Upload new CSV (optional)",
        type=["csv"],
        help="Must have the same schema as cleaned_records.csv",
    )

    if uploaded:
        try:
            raw_df = pd.read_csv(uploaded)
            df_full = _prep(raw_df)
            st.success(f"✓ Loaded {len(df_full):,} rows from upload")
        except Exception as e:
            st.error(f"Parse error: {e}")
            df_full = load_default()
    else:
        df_full = load_default()

    st.markdown("<hr style='margin:12px 0'>", unsafe_allow_html=True)

    # 5b. Date range filter
    st.markdown("### 📅 Date Range")
    min_date = df_full["record_date"].min().date()
    max_date = df_full["record_date"].max().date()
    date_range = st.date_input(
        "Select range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.markdown("<hr style='margin:12px 0'>", unsafe_allow_html=True)

    # 5c. Category filter
    st.markdown("### 🏷️ Category")
    all_cats = sorted(df_full["category_name"].dropna().unique().tolist())
    sel_cats = st.multiselect(
        "Filter by category",
        options=all_cats,
        default=all_cats,
        placeholder="All categories",
    )

    st.markdown("<hr style='margin:12px 0'>", unsafe_allow_html=True)

    # 5d. Region filter
    st.markdown("### 🌍 Region")
    all_regions = sorted(df_full["region"].dropna().unique().tolist())
    sel_regions = st.multiselect(
        "Filter by region",
        options=all_regions,
        default=all_regions,
        placeholder="All regions",
    )

    st.markdown("<hr style='margin:12px 0'>", unsafe_allow_html=True)

    # 5e. Download
    st.markdown("### 💾 Export")

# ── 6. APPLY FILTERS ──────────────────────────────────────────────────────────
try:
    start_date, end_date = date_range[0], date_range[1]
except (TypeError, IndexError):
    start_date, end_date = min_date, max_date

df = df_full.copy()
df = df[
    (df["record_date"].dt.date >= start_date) &
    (df["record_date"].dt.date <= end_date)
]
if sel_cats:
    df = df[df["category_name"].isin(sel_cats)]
if sel_regions:
    df = df[df["region"].isin(sel_regions)]

# Sidebar download (uses filtered df)
with st.sidebar:
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download Filtered CSV",
        data=csv_bytes,
        file_name="filtered_records.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.markdown(f"<div style='color:#4a5568;font-size:11px;margin-top:8px;text-align:center'>{len(df):,} rows in current view</div>", unsafe_allow_html=True)

# ── 7. HEADER ─────────────────────────────────────────────────────────────────
st.markdown("## Seth Mini Data Warehouse")
st.markdown("<div style='color:#718096;font-size:13px;margin-bottom:4px'>Client Management & Consultation Analytics · Professional Dashboard</div>", unsafe_allow_html=True)

# Active filter pills
filter_parts = []
if start_date != min_date or end_date != max_date:
    filter_parts.append(f"📅 {start_date} → {end_date}")
if len(sel_cats) != len(all_cats):
    filter_parts.append(f"🏷️ {len(sel_cats)} categories")
if len(sel_regions) != len(all_regions):
    filter_parts.append(f"🌍 {len(sel_regions)} regions")

if filter_parts:
    pills = "".join(f'<span class="filter-badge">{p}</span>' for p in filter_parts)
    st.markdown(f"<div style='margin-bottom:12px'>Active filters: {pills}</div>", unsafe_allow_html=True)

st.markdown("<hr style='margin:8px 0 20px'>", unsafe_allow_html=True)

# ── 8. KPI CARDS ──────────────────────────────────────────────────────────────
if df.empty:
    st.warning("No data matches the current filters. Please adjust your selections.")
    st.stop()

total_records = len(df)
revenue       = df[df["normal_sign"] == 1]["raw_value"].sum()
expenses      = df[df["normal_sign"] == -1]["raw_value"].sum()
net_value     = df["signed_value"].sum()
net_margin    = (net_value / revenue * 100) if revenue else 0

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card blue">
    <div class="kpi-label">Total Records</div>
    <div class="kpi-value">{total_records:,}</div>
    <div class="kpi-sub">transactions in view</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">Total Revenue</div>
    <div class="kpi-value">GHS {revenue:,.0f}</div>
    <div class="kpi-sub">normal_sign = +1</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-label">Total Expenses</div>
    <div class="kpi-value">GHS {expenses:,.0f}</div>
    <div class="kpi-sub">normal_sign = −1</div>
  </div>
  <div class="kpi-card purple">
    <div class="kpi-label">Net Value</div>
    <div class="kpi-value">GHS {net_value:,.0f}</div>
    <div class="kpi-sub">margin {net_margin:.1f}%</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 9. ROW 1: Time-Series Charts ───────────────────────────────────────────────
st.markdown('<div class="section-header">Time Series Analysis</div>', unsafe_allow_html=True)
col_ts1, col_ts2 = st.columns(2)

with col_ts1:
    daily = df.groupby("record_date")["signed_value"].sum().reset_index()

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=daily["record_date"], y=daily["signed_value"],
        mode="lines+markers",
        line=dict(color="#3b82f6", width=2),
        marker=dict(size=4, color="#3b82f6"),
        fill="tozeroy",
        fillcolor="rgba(59,130,246,0.08)",
        name="Net Daily",
    ))
    fig_line.add_hline(y=0, line_dash="dot", line_color="#4a5568", line_width=1)
    fig_line.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Daily Net Financial Performance", font=dict(size=13, color="#e2e8f0")),
        height=300,
        showlegend=False,
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_ts2:
    df_sorted = df.sort_values("record_date")
    df_sorted["cumulative_net"] = df_sorted["signed_value"].cumsum()

    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(
        x=df_sorted["record_date"], y=df_sorted["cumulative_net"],
        mode="lines",
        line=dict(color="#8b5cf6", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(139,92,246,0.12)",
        name="Cumulative Net",
    ))
    fig_area.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Cumulative Net Growth (Mountain Chart)", font=dict(size=13, color="#e2e8f0")),
        height=300,
        showlegend=False,
    )
    st.plotly_chart(fig_area, use_container_width=True)

# ── 10. ROW 2: Regional & Revenue vs Expenses ─────────────────────────────────
st.markdown('<div class="section-header">Regional & Category Breakdown</div>', unsafe_allow_html=True)
col_r1, col_r2 = st.columns(2)

with col_r1:
    region_df = df.groupby("region")["signed_value"].sum().reset_index().sort_values("signed_value")
    colors = ["#ef4444" if v < 0 else "#10b981" for v in region_df["signed_value"]]

    fig_reg = go.Figure(go.Bar(
        x=region_df["signed_value"],
        y=region_df["region"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"GHS {v:,.0f}" for v in region_df["signed_value"]],
        textposition="outside",
        textfont=dict(size=10, color="#a0aec0"),
    ))
    fig_reg.add_vline(x=0, line_color="#4a5568", line_width=1)
    fig_reg.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Net Value Contribution by Region", font=dict(size=13, color="#e2e8f0")),
        height=320,
        showlegend=False,
        xaxis_title="Net Value (GHS)",
        yaxis_title=None,
    )
    st.plotly_chart(fig_reg, use_container_width=True)

with col_r2:
    rev_exp_df = pd.DataFrame({
        "Type": ["Revenue", "Expenses"],
        "Value": [revenue, abs(expenses)],
    })
    fig_rev = go.Figure(go.Bar(
        x=rev_exp_df["Type"],
        y=rev_exp_df["Value"],
        marker=dict(
            color=["#10b981", "#ef4444"],
            line=dict(width=0),
        ),
        text=[f"GHS {v:,.0f}" for v in rev_exp_df["Value"]],
        textposition="outside",
        textfont=dict(size=11, color="#a0aec0"),
    ))
    fig_rev.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Total Revenue vs Total Expenses", font=dict(size=13, color="#e2e8f0")),
        height=320,
        showlegend=False,
        yaxis_title="Value (GHS)",
    )
    st.plotly_chart(fig_rev, use_container_width=True)

# ── 11. ROW 3: Donut + Boxplot ─────────────────────────────────────────────────
st.markdown('<div class="section-header">Composition & Distribution</div>', unsafe_allow_html=True)
col_d1, col_d2 = st.columns(2)
donut_layout = PLOTLY_LAYOUT.copy()
donut_layout.pop("legend", None)
with col_d1:
    cat_counts = df["category_name"].value_counts().reset_index()
    cat_counts.columns = ["category_name", "count"]

    fig_donut = go.Figure(go.Pie(
        labels=cat_counts["category_name"],
        values=cat_counts["count"],
        hole=0.65,
        marker=dict(
            colors=["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"],
            line=dict(color="#0f1117", width=3),
        ),
        textinfo="label+percent",
        textfont=dict(size=11, color="#e2e8f0"),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    fig_donut.add_annotation(
        text=f"<b>{total_records:,}</b><br><span style='font-size:10px'>records</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="#f7fafc"),
        align="center",
    )
   # Separate margin from the rest of the donut layout to avoid conflicts
base_donut_layout = {k: v for k, v in donut_layout.items() if k != 'margin'}
base_margin = donut_layout.get("margin", {})

fig_donut.update_layout(
    **base_donut_layout,
    title=dict(text="Record Composition by Category", font=dict(size=13, color="#e2e8f0")),
    height=360,
    legend=dict(
        orientation="v", x=1.02, y=0.5,
        font=dict(size=11, color="#a0aec0"),
        bgcolor="rgba(0,0,0,0)",
    ),
    margin={
    **base_margin,  # Retain global margin settings
    "l": 16, "r": 120, "t": 36, "b": 16  # Override specific margins safely
},
 
)

with col_d2:
    fig_box = go.Figure()
    palette = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]
    for i, reg in enumerate(sorted(df["region"].unique())):
        sub = df[df["region"] == reg]["raw_value"]
        fig_box.add_trace(go.Box(
            y=sub,
            name=reg,
            marker=dict(color=palette[i % len(palette)], size=4),
            line=dict(color=palette[i % len(palette)], width=1.5),
            boxmean=True,
            fillcolor=f"rgba({int(palette[i % len(palette)][1:3], 16)},{int(palette[i % len(palette)][3:5], 16)},{int(palette[i % len(palette)][5:7], 16)},0.15)",
        ))
        
    # FIX: Separate the base layout keys from the conflicting yaxis key
    base_layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k != 'yaxis'}
    base_yaxis = PLOTLY_LAYOUT.get("yaxis", {})

    fig_box.update_layout(
        **base_layout,
        title=dict(text="Transaction Value Distribution by Region", font=dict(size=13, color="#e2e8f0")),
        height=360,
        showlegend=False,
        yaxis=dict(
            **base_yaxis,
            type="log",
            title="Value (GHS, log scale)",
        ),
    )
    st.plotly_chart(fig_box, use_container_width=True)

# ── 12. ROW 4: Heatmap ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Activity Heatmap</div>', unsafe_allow_html=True)

heat_df = df.groupby(["day_of_week", "month", "month_num"]).size().reset_index(name="count")
# Sort months chronologically
heat_pivot = heat_df.pivot_table(index="day_of_week", columns="month", values="count", aggfunc="sum").fillna(0)
heat_pivot = heat_pivot.reindex([d for d in DAYS_ORDER if d in heat_pivot.index])

# Order columns by month number
month_order = (
    heat_df[["month", "month_num"]]
    .drop_duplicates()
    .sort_values("month_num")["month"]
    .tolist()
)
heat_pivot = heat_pivot[[m for m in month_order if m in heat_pivot.columns]]

fig_heat = go.Figure(go.Heatmap(
    z=heat_pivot.values,
    x=heat_pivot.columns.tolist(),
    y=heat_pivot.index.tolist(),
    colorscale=[
        [0.0,  "#161b27"],
        [0.25, "#1e3a5f"],
        [0.5,  "#2563eb"],
        [0.75, "#3b82f6"],
        [1.0,  "#93c5fd"],
    ],
    text=heat_pivot.values.astype(int),
    texttemplate="%{text}",
    textfont=dict(size=11, color="#e2e8f0"),
    hovertemplate="<b>%{y}</b> · <b>%{x}</b><br>Transactions: %{z}<extra></extra>",
    showscale=True,
    colorbar=dict(
        title=dict(text="Count", font=dict(color="#a0aec0")),
        tickfont=dict(color="#a0aec0"),
        bgcolor="rgba(0,0,0,0)",
        bordercolor="#2d3748",
    ),
))
fig_heat.update_layout(
    {
        **PLOTLY_LAYOUT,
        "title": dict(text="Business Activity Heatmap — Day of Week × Month", font=dict(size=13, color="#e2e8f0")),
        "height": 320,
        "xaxis": {**PLOTLY_LAYOUT.get("xaxis", {}), "side": "bottom"},
        "margin": dict(l=80, r=80, t=46, b=16),
    }
)
st.plotly_chart(fig_heat, use_container_width=True)


# ── 13. CLEANED RECORDS TABLE ─────────────────────────────────────────────────
st.markdown('<div class="section-header">Cleaned Records</div>', unsafe_allow_html=True)
st.dataframe(
    df.drop(columns=["month_num"], errors="ignore"),
    use_container_width=True,
    height=400,
)

# ── 14. FOOTER ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#4a5568;font-size:11px;margin-top:40px;padding:20px 0;border-top:1px solid #2d3748">
  Seth Mini Data Warehouse · Professional Analytics Dashboard · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)