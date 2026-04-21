import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set Plotting Style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 300

def generate_visuals():
    data_dir = 'data/genuine/'
    visuals_dir = 'data/genuine/visuals/'
    
    if not os.path.exists(visuals_dir):
        os.makedirs(visuals_dir)

    print("Loading data for visualization...")
    orders = pd.read_csv(os.path.join(data_dir, 'OrderList.csv'))
    wh_cap = pd.read_csv(os.path.join(data_dir, 'WhCapacities.csv'))
    rates = pd.read_csv(os.path.join(data_dir, 'FreightRates.csv'))
    results = pd.read_csv(os.path.join(data_dir, 'optimal_genuine_results.csv'))

    # --- Chart A: Freight Rate vs. Weight Band (Constraint Analysis) ---
    print("Generating Chart A: Rate vs Weight...")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=rates, x='Max_Weight_Quant', y='Rate', hue='Mode_DSC', alpha=0.6)
    plt.title("Freight Rate vs. Maximum Weight Band", fontsize=14, fontweight='bold')
    plt.xlabel("Weight Band Limit (Units)", fontsize=12)
    plt.ylabel("Freight Rate ($ per unit)", fontsize=12)
    plt.xscale('log')
    plt.savefig(os.path.join(visuals_dir, 'freight_rate_bands.png'), bbox_inches='tight')
    plt.close()

    # --- Chart B: Capacity Utilization (Solver Performance) ---
    print("Generating Chart B: Capacity Utilization...")
    # Map allocated quantities back to plants
    allocated = results.groupby('Plant')['Allocated_Quantity'].sum().reset_index()
    capacity = wh_cap[['Plant_Code', 'Daily_Capacity']].copy()
    # Scale capacity by 10,000 to match the solver logic
    capacity['Max_Capacity'] = capacity['Daily_Capacity'] * 10000
    
    comparison = pd.merge(capacity, allocated, left_on='Plant_Code', right_on='Plant', how='left').fillna(0)
    comparison = comparison.sort_values(by='Max_Capacity', ascending=False)

    plt.figure(figsize=(12, 6))
    plt.bar(comparison['Plant_Code'], comparison['Max_Capacity'], color='lightgray', label='Max Scaled Capacity')
    plt.bar(comparison['Plant_Code'], comparison['Allocated_Quantity'], color='#2ecc71', label='Allocated Volume')
    plt.title("Plant Capacity Utilization (Optimal Solver Assignment)", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.ylabel("Total Units", fontsize=12)
    plt.legend()
    plt.savefig(os.path.join(visuals_dir, 'capacity_utilization.png'), bbox_inches='tight')
    plt.close()

    # --- Chart C: Demand Concentration by Product ---
    print("Generating Chart C: Demand Concentration...")
    product_demand = orders.groupby('Product_ID')['Unit_Quant'].sum().sort_values(ascending=False).head(15).reset_index()
    product_demand['Product_ID'] = product_demand['Product_ID'].astype(str)

    plt.figure(figsize=(10, 8))
    sns.barplot(data=product_demand, x='Unit_Quant', y='Product_ID', palette='viridis', hue='Product_ID', legend=False)
    plt.title("Top 15 Products by Demand Volume (5/26/13)", fontsize=14, fontweight='bold')
    plt.xlabel("Total Units Demanded", fontsize=12)
    plt.ylabel("Product ID", fontsize=12)
    plt.savefig(os.path.join(visuals_dir, 'demand_distribution.png'), bbox_inches='tight')
    plt.close()

    # --- Chart D: Mode & Service Level Analysis ---
    print("Generating Chart D: Service Type vs Cost...")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=rates, x='Mode_DSC', y='Rate', hue='Service_Level', palette='Set2')
    plt.title("Logistics Service Type vs. Freight Rate", fontsize=14, fontweight='bold')
    plt.xlabel("Transportation Mode", fontsize=12)
    plt.ylabel("Freight Rate ($ per unit)", fontsize=12)
    plt.savefig(os.path.join(visuals_dir, 'service_mode_tradeoff.png'), bbox_inches='tight')
    plt.close()

    # --- Chart E: Cost vs. Transit Time Tradeoff ---
    print("Generating Chart E: Cost vs Transit Time...")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=rates, x='TPT_Day_Count', y='Rate', errorbar='sd', marker='o')
    plt.title("Transit Time (Days) vs. Average Freight Rate", fontsize=14, fontweight='bold')
    plt.xlabel("Transit Time (Days)", fontsize=12)
    plt.ylabel("Average Freight Rate ($)", fontsize=12)
    plt.savefig(os.path.join(visuals_dir, 'cost_vs_transit.png'), bbox_inches='tight')
    plt.close()

    # --- Chart F: Carrier Price Benchmarking ---
    print("Generating Chart F: Carrier Benchmarking...")
    plt.figure(figsize=(10, 6))
    carrier_prices = rates.groupby('Carrier')['Rate'].mean().sort_values().reset_index()
    sns.barplot(data=carrier_prices, x='Rate', y='Carrier', palette='magma', hue='Carrier', legend=False)
    plt.title("Carrier Price Benchmarking (Average Rate)", fontsize=14, fontweight='bold')
    plt.xlabel("Average Rate ($ per unit)", fontsize=12)
    plt.ylabel("Carrier Registry ID", fontsize=12)
    plt.savefig(os.path.join(visuals_dir, 'carrier_benchmarking.png'), bbox_inches='tight')
    plt.close()

    print(f"Comprehensive visualization complete. 6 charts total in: {visuals_dir}")

if __name__ == "__main__":
    try:
        generate_visuals()
    except Exception as e:
        print(f"Error generating visuals: {e}")
