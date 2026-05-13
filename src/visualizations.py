import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
viz_path = "./visualizations/reports/"
if not os.path.exists(viz_path):
    os.makedirs(viz_path)

def save_viz(filename):
    full_path = os.path.join(viz_path, f"{filename}.png")
    plt.savefig(full_path, bbox_inches="tight", dpi=300)
    print(f"Chart saved to: {full_path}")

records = pd.read_csv("./datasets/processed/cleaned_records.csv")
branches = pd.read_csv("./datasets/processed/cleaned_branches.csv")
categories = pd.read_csv("./datasets/processed/cleaned_categories.csv")
sources = pd.read_csv("./datasets/processed/cleaned_sources.csv")
records["record_date"] = pd.to_datetime(records["record_date"])

revenue = records[records["normal_sign"] == 1.0]["raw_value"].sum()
expenses = records[records["normal_sign"] == -1.0]["raw_value"].sum()

plt.figure(figsize=(10, 6))
plt.bar(["Total Revenue", "Total Expenses"], [revenue, expenses], color=["#2ecc71", "#e74c3c"])
plt.title("Total Revenue vs Total Expenses", fontsize=14)
plt.ylabel("Value (GHS)")
save_viz("revenue_vs_expenses_bar")
plt.show()

daily_trend = records.groupby("record_date")["signed_value"].sum()
plt.figure(figsize=(12, 6))
plt.plot(daily_trend.index, daily_trend.values, color="#3498db", linewidth=2)
plt.axhline(0, color="black", lw=1, linestyle="--")
plt.title("Daily Net Financial Performance", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Net Value (GHS)")
save_viz("daily_performance_trend")
plt.show()

region_perf = records.groupby("region")["signed_value"].sum().sort_values()
plt.figure(figsize=(10, 6))
region_perf.plot(kind="barh", color="#9b59b6")
plt.title("Net Value Contribution by Region", fontsize=14)
save_viz("regional_contribution_h_bar")
plt.show()

counts = records["category_name"].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=140, pctdistance=0.85)
center_circle = plt.Circle((0,0), 0.70, fc="white")
fig = plt.gcf()
fig.gca().add_artist(center_circle)
plt.title("Composition of Records by Category", fontsize=14)
plt.show()
save_viz("composition_of_records_by_category")

records = records.sort_values("record_date")
daily_trend = records.groupby("record_date")["signed_value"].sum()
plt.figure(figsize=(12, 6))
plt.plot(daily_trend.index, daily_trend.values, color="#3498db", marker=".", linestyle="-")
plt.fill_between(daily_trend.index, daily_trend.values, color="#3498db", alpha=0.2)
plt.axhline(0, color="black", lw=1)
plt.title("Daily Net Value Impact", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)
save_viz("daily_net_value_impact")
plt.show()



counts = records['category_name'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85)
# Add a circle at the center to make it a donut
center_circle = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(center_circle)
plt.title('Composition of Records by Category', fontsize=14)
save_viz('composition_of_records_by_category')
plt.show()




# Prepare data: Extract Day of Week and Month
records['day_of_week'] = records['record_date'].dt.day_name()
records['month'] = records['record_date'].dt.month_name()

# Create a pivot table for the heatmap
heatmap_data = records.pivot_table(index='day_of_week', 
                                   columns='month', 
                                   values='record_id', 
                                   aggfunc='count').fillna(0)

# Sort days correctly
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data = heatmap_data.reindex(days_order)
plt.figure(figsize=(12, 7))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': 'Transaction Count'})
plt.title('Business Activity Heatmap: Day of Week vs Month', fontsize=14)
save_viz('activity_heatmap')
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x='region', y='raw_value', data=records, palette="Set3")
plt.yscale('log') # Using log scale if you have massive price differences
plt.title('Distribution of Transaction Values by Region (Log Scale)', fontsize=14)
plt.ylabel('Value (GHS)')
plt.grid(axis='y', alpha=0.3)
save_viz('value_distribution_boxplot')
plt.show()

# Calculate cumulative sum of net value
#records = records.sort_values('record_date')
records['cumulative_net'] = records['signed_value'].cumsum()

plt.figure(figsize=(12, 6))
plt.fill_between(records['record_date'], records['cumulative_net'], color="skyblue", alpha=0.4)
plt.plot(records['record_date'], records['cumulative_net'], color="Slateblue", alpha=0.6, linewidth=2)
plt.title('Cumulative Net Growth Over Time', fontsize=14)
plt.xlabel('Timeline')
plt.ylabel('Running Total (GHS)')
plt.grid(True, alpha=0.2)
save_viz('cumulative_growth_mountain')
plt.show()

