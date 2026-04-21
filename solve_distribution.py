import pandas as pd
import pulp
import matplotlib.pyplot as plt
import os

def solve_retail_transportation():
    # 1. Load Data
    print("Loading datasets...")
    costs_df = pd.read_csv('data/transportation_costs.csv', index_col=0) # Index is DC names
    supply_df = pd.read_csv('data/supply_capacities.csv')
    demand_df = pd.read_csv('data/demand_requirements.csv')

    # Re-align cost matrix index if necessary
    costs_df.index = costs_df.index.astype(str)
    
    # 2. Extract Names and Parameters
    dcs = list(costs_df.index)
    stores = list(costs_df.columns)
    
    supply = {row['DC']: row['Supply'] for _, row in supply_df.iterrows()}
    demand = {row['Store']: row['Demand'] for _, row in demand_df.iterrows()}
    
    # Map costs into a dictionary
    costs = {}
    for dc in dcs:
        costs[dc] = {}
        for store in stores:
            costs[dc][store] = costs_df.loc[dc, store]

    # 3. Formulate Linear Programming Problem
    print("Formulating optimization model...")
    prob = pulp.LpProblem("Retail_Supply_Chain_Optimization", pulp.LpMinimize)

    # Decision Variables: amount to ship from DC i to Store j
    x = pulp.LpVariable.dicts("Ship", (dcs, stores), lowBound=0, cat='Continuous')

    # Objective Function: Minimize total transportation cost
    prob += pulp.lpSum(costs[dc][store] * x[dc][store] for dc in dcs for store in stores), "Total_Transportation_Cost"

    # Constraints: Supply Outflow
    for dc in dcs:
        prob += pulp.lpSum(x[dc][store] for store in stores) <= supply[dc], f"Supply_Constraint_{dc}"

    # Constraints: Demand Inflow
    for store in stores:
        prob += pulp.lpSum(x[dc][store] for dc in dcs) >= demand[store], f"Demand_Constraint_{store}"

    # 4. Solve the Problem
    print("Solving with PuLP...")
    status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
    print(f"Solver Status: {pulp.LpStatus[status]}")

    # 5. Extract Results
    results = []
    for dc in dcs:
        for store in stores:
            if x[dc][store].varValue > 0:
                results.append({
                    'From_DC': dc,
                    'To_Store': store,
                    'Quantity': x[dc][store].varValue,
                    'Unit_Cost': costs[dc][store],
                    'Total_Segment_Cost': x[dc][store].varValue * costs[dc][store]
                })

    results_df = pd.DataFrame(results)
    results_df.to_csv('data/optimal_allocation.csv', index=False)

    total_cost = pulp.value(prob.objective)
    summary = f"""
    =========================================
    RETAIL SUPPLY CHAIN OPTIMIZATION SUMMARY
    =========================================
    Problem Status: {pulp.LpStatus[status]}
    Total Warehouses (DCs): {len(dcs)}
    Total Retail Stores: {len(stores)}
    Total Minimized Transportation Cost: ${total_cost:,.2f}
    Total Units Shipped: {results_df['Quantity'].sum():,.0f}
    =========================================
    """
    print(summary)
    with open('data/solution_summary.txt', 'w') as f:
        f.write(summary)

    # 6. Visualization
    print("Generating network visualization...")
    plt.figure(figsize=(12, 8))
    
    # Plot locations
    plt.scatter(supply_df['X'], supply_df['Y'], color='blue', label='Warehouses (DCs)', s=100, marker='s')
    plt.scatter(demand_df['X'], demand_df['Y'], color='red', label='Retail Stores', s=50, edgecolors='black')

    # Plot labels for DCs
    for idx, row in supply_df.iterrows():
        plt.text(row['X']+1, row['Y']+1, row['DC'], fontsize=9, color='blue', fontweight='bold')

    # Plot shipping lines (arrows or lines)
    max_q = results_df['Quantity'].max()
    for _, res in results_df.iterrows():
        dc_info = supply_df[supply_df['DC'] == res['From_DC']].iloc[0]
        store_info = demand_df[demand_df['Store'] == res['To_Store']].iloc[0]
        
        # Line width based on quantity
        lw = (res['Quantity'] / max_q) * 3
        plt.plot([dc_info['X'], store_info['X']], [dc_info['Y'], store_info['Y']], 
                 color='gray', alpha=0.3, linewidth=lw)

    plt.title("Optimized Retail Supply Chain Network", fontsize=15)
    plt.xlabel("X Coordinate (km)")
    plt.ylabel("Y Coordinate (km)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig('data/distribution_network.png')
    print("Visualization saved to 'data/distribution_network.png'.")

if __name__ == "__main__":
    try:
        solve_retail_transportation()
    except Exception as e:
        print(f"Error during optimization: {e}")
