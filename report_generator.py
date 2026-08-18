from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = Path("sample_data.xlsx")
OUTPUT_FILE = Path("generated_report.xlsx")
CHART_FILE = Path("sales_by_region.png")

def main():
    df = pd.read_excel(INPUT_FILE)

    total_sales = df["Sales"].sum()
    total_orders = df["Orders"].sum()
    avg_sales = df["Sales"].mean()

    region_summary = (
        df.groupby("Region", as_index=False)
        .agg(Total_Sales=("Sales", "sum"), Total_Orders=("Orders", "sum"))
        .sort_values("Total_Sales", ascending=False)
    )

    category_summary = (
        df.groupby("Category", as_index=False)
        .agg(Total_Sales=("Sales", "sum"), Total_Orders=("Orders", "sum"))
        .sort_values("Total_Sales", ascending=False)
    )

    kpi_summary = pd.DataFrame({
        "Metric": ["Total Sales", "Total Orders", "Average Daily Sales"],
        "Value": [total_sales, total_orders, round(avg_sales, 2)],
    })

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Raw Data", index=False)
        kpi_summary.to_excel(writer, sheet_name="Summary", index=False)
        region_summary.to_excel(writer, sheet_name="Region Analysis", index=False)
        category_summary.to_excel(writer, sheet_name="Category Analysis", index=False)

    plt.figure(figsize=(8, 5))
    plt.bar(region_summary["Region"], region_summary["Total_Sales"])
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig(CHART_FILE, dpi=160)
    plt.close()

    print("Report generated successfully!")
    print(f"Created: {OUTPUT_FILE}")
    print(f"Created: {CHART_FILE}")

if __name__ == "__main__":
    main()
