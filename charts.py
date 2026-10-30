import io
import matplotlib.pyplot as plt
import pandas as pd

# 1. Load the data
csv_data = """name,department,salary
arun,sales,30000
priya,HR,45000
rahul,IT,60000
divya,IT,75000
karthik,Finance,90000"""

df = pd.read_csv(io.StringIO(csv_data))

# Format names to look clean (Capitalise first letter)
df["name"] = df["name"].str.capitalize()
df["department"] = df["department"].str.upper()

# Set up the visualization window for 2 side-by-side charts
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- CHART 1: Individual Salaries (Bar Chart) ---
colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]
bars = ax1.bar(
    df["name"], df["salary"], color=colors[: len(df)], edgecolor="black"
)

ax1.set_title("Salary Distribution by Employee", fontsize=14, fontweight="bold")
ax1.set_ylabel("Salary (₹)", fontsize=12)
ax1.set_xlabel("Employee Name", fontsize=12)
ax1.grid(axis="y", linestyle="--", alpha=0.7)

# Add value labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        yval + 1500,
        f"₹{yval:,}",
        ha="center",
        va="bottom",
        fontweight="bold",
    )


# --- CHART 2: Salary Budget by Department (Pie Chart) ---
dept_salary = df.groupby("department")["salary"].sum()

ax2.pie(
    dept_salary,
    labels=dept_salary.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=["#FF9999", "#66B3FF", "#99FF99", "#FFCC99"],
    wedgeprops={"edgecolor": "black", "linewidth": 1},
    textprops={"fontsize": 11, "fontweight": "bold"},
)
ax2.set_title("Salary Budget Share by Department", fontsize=14, fontweight="bold")


# Render layout smoothly
plt.tight_layout()
plt.show()
