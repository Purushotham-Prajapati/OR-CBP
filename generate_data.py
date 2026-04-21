import pandas as pd
import numpy as np
import os

# Set seed for reproducibility
np.random.seed(42)

def generate_retail_data(num_dcs=10, num_stores=50):
    # 1. Create Directories
    if not os.path.exists('data'):
        os.makedirs('data')

    # 2. Generate Locations (Coordinates) to calculate distances/costs
    # Distribution Centers (Warehouses)
    dc_names = [f"DC_{i+1:02d}" for i in range(num_dcs)]
    dc_coords = np.random.rand(num_dcs, 2) * 100 # X, Y coordinates
    dc_supply = np.random.randint(1000, 3000, size=num_dcs)

    # Retail Stores
    store_names = [f"Store_{i+1:02d}" for i in range(num_stores)]
    store_coords = np.random.rand(num_stores, 2) * 100 # X, Y coordinates
    store_demand = np.random.randint(100, 500, size=num_stores)

    # Balance Supply vs Demand (Ensure supply >= demand)
    total_demand = np.sum(store_demand)
    total_supply = np.sum(dc_supply)
    
    if total_supply < total_demand:
        # Boost a few DCs to ensure feasibility
        dc_supply[0] += (total_demand - total_supply) + 500
        total_supply = np.sum(dc_supply)
    
    print(f"Total Supply: {total_supply} | Total Demand: {total_demand}")

    # 3. Calculate Transportation Cost Matrix
    # Using Euclidean distance as a proxy for cost ($ per unit per distance)
    costs = []
    for i in range(num_dcs):
        dc_row_costs = []
        for j in range(num_stores):
            dist = np.linalg.norm(dc_coords[i] - store_coords[j])
            # Cost = Base cost + distance-based cost
            cost = 2 + (dist * 0.1) 
            dc_row_costs.append(round(cost, 2))
        costs.append(dc_row_costs)

    # 4. Save to CSVs
    # Cost Matrix
    df_costs = pd.DataFrame(costs, index=dc_names, columns=store_names)
    df_costs.to_csv('data/transportation_costs.csv')

    # Supply and Demand
    df_supply = pd.DataFrame({'DC': dc_names, 'Supply': dc_supply, 'X': dc_coords[:,0], 'Y': dc_coords[:,1]})
    df_supply.to_csv('data/supply_capacities.csv', index=False)

    df_demand = pd.DataFrame({'Store': store_names, 'Demand': store_demand, 'X': store_coords[:,0], 'Y': store_coords[:,1]})
    df_demand.to_csv('data/demand_requirements.csv', index=False)

    print("Data generation complete. Files saved in 'data/' directory.")

if __name__ == "__main__":
    generate_retail_data()
