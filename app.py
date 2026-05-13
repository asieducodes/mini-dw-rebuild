from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Seth Mini DW Jupyter Rebuild", page_icon="📊", layout="wide")

# 2. Header
st.title("📊 Seth Mini Data Warehouse — Jupyter Rebuild")
st.caption("Seth Mini Data Warehouse Project")

# 3. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("datasets/processed/cleaned_records.csv")
    df["record_date"] = pd.to_datetime(df["record_date"])
    # Time-based features for the new heatmap
    df['day_of_week'] = df['record_date'].dt.day_name()
    df['month'] = df['record_date'].dt.month_name()
    return df

records = load_data()

# 4. Metrics Row
# 4. Top Row: Enhanced KPI Cards
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 5px solid #3498db;
    }
    .metric-label {
        font-size: 14px;
        color: #7f8c8d;
        font-weight: bold;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 24px;
        color: #2c3e50;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Calculate values
total_records = len(records)
revenue = records[records['normal_sign'] == 1.0]['raw_value'].sum()
expenses = records[records['normal_sign'] == -1.0]['raw_value'].sum()
net_value = records['signed_value'].sum()

# Display Cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Total Records</div><div class="metric-value">{total_records:,}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card" style="border-left-color: #2ecc71;"><div class="metric-label">Total Revenue</div><div class="metric-value">GHS {revenue:,.2f}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card" style="border-left-color: #e74c3c;"><div class="metric-label">Total Expenses</div><div class="metric-value">GHS {expenses:,.2f}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card" style="border-left-color: #9b59b6;"><div class="metric-label">Net Value</div><div class="metric-value">GHS {net_value:,.2f}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Primary Charts (Financial & Regional)
a, b = st.columns(2)
with a:
    st.subheader("Daily Net Financial Performance")
    daily = records.groupby("record_date")["signed_value"].sum().reset_index()
    st.line_chart(daily, x="record_date", y="signed_value")
with b:
    st.subheader("Cumulative Growth (Mountain Chart)")
    records_sorted = records.sort_values("record_date")
    records_sorted['cumulative_net'] = records_sorted['signed_value'].cumsum()
    st.area_chart(records_sorted, x="record_date", y="cumulative_net", color="#9b59b6")

# 6. Regional & Heatmap Row
col_region, col_heat = st.columns(2)
with col_region:
    st.subheader("Regional Contribution")
    region = records.groupby("region")["signed_value"].sum().reset_index()
    st.bar_chart(region, x="region", y="signed_value")

with col_heat:
    st.subheader("Activity Heatmap (Month vs Day)")
    heatmap_data = records.groupby(['day_of_week', 'month']).size().reset_index(name='count')
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    fig_heat = px.density_heatmap(heatmap_data, x="month", y="day_of_week", z="count",
                                  category_orders={"day_of_week": days_order},
                                  color_continuous_scale="YlGnBu", text_auto=True)
    st.plotly_chart(fig_heat, use_container_width=True)

# 7. Cleaned Records Section (Restored to original style)
st.subheader("Cleaned Records")
st.dataframe(records, use_container_width=True)

# 8. Static Reports Section
st.subheader("Generated Report Images")
reports_dir = Path("visualizations/reports")
images = sorted(reports_dir.glob("*.png")) if reports_dir.exists() else []
if images:
    for image in images:
        st.image(str(image), caption=image.name)
else:
    st.info("Run `python src/visualizations.py` to generate chart images.")