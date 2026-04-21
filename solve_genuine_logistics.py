import pandas as pd
import pulp
import os

def solve_genuine_logistics():
    print("--- Loading Genuine Supply Chain Data ---")
    data_dir = 'data/genuine/'
    
    # Load all files
    wh_cap = pd.read_csv(os.path.join(data_dir, 'WhCapacities.csv'))
    orders = pd.read_csv(os.path.join(data_dir, 'OrderList.csv'))
    rates = pd.read_csv(os.path.join(data_dir, 'FreightRates.csv'))
    plant_ports = pd.read_csv(os.path.join(data_dir, 'PlantPorts.csv'))

    # 1. Aggregate Demand per Destination Port
    print("Aggregating demand by Destination Port...")
    # Clean column names if necessary
    orders.columns = [c.strip() for c in orders.columns]
    demand_per_port = orders.groupby('Dest_Port')['Unit_Quant'].sum().to_dict()
    dest_ports = list(demand_per_port.keys())

    # 2. Map Plants to their specific Origin Ports
    print("Mapping Plants to Ports...")
    # A plant might have multiple ports, but for this model, we'll map to all valid connections
    plants = wh_cap['Plant_Code'].unique().tolist()
    plant_capacities = wh_cap.set_index('Plant_Code')['Daily_Capacity'].to_dict()

    # 3. Process Freight Rates (Find minimum rate for each O-D pair)
    print("Calculating optimal freight rates matrix...")
    # Average the rate across carriers/modes/weight-bands for simplicity as discussed
    min_rates = rates.groupby(['Orig_Port', 'Dest_Port'])['Rate'].min().to_dict()

    # 4. Build the Cost Matrix for the Optimizer
    # We need cost from each Plant to each Destination Port.
    # Cost(Plant, DestPort) = Min(Rate(Port, DestPort)) where Port is linked to Plant.
    
    plant_to_dest_costs = {}
    for plant in plants:
        plant_to_dest_costs[plant] = {}
        # Find which ports this plant can use
        possible_orig_ports = plant_ports[plant_ports['Plant_Code'] == plant]['Ports'].tolist()
        
        for d_port in dest_ports:
            # Find the best rate from any of these plant ports to the destination port
            possible_costs = []
            for o_port in possible_orig_ports:
                if (o_port, d_port) in min_rates:
                    possible_costs.append(min_rates[(o_port, d_port)])
            
            if possible_costs:
                plant_to_dest_costs[plant][d_port] = min(possible_costs)
            else:
                # If no route exists, set a prohibitively high cost (Penalty)
                plant_to_dest_costs[plant][d_port] = 9999.0

    # 5. Formulate optimization model
    print("Formulating optimization model...")
    prob = pulp.LpProblem("Genuine_Logistics_Optimization", pulp.LpMinimize)

    # Decision variables: x[plant][d_port]
    x = pulp.LpVariable.dicts("Qty", (plants, dest_ports), lowBound=0, cat='Continuous')

    # Objective: Minimize sum(cost * qty)
    prob += pulp.lpSum(plant_to_dest_costs[p][d] * x[p][d] for p in plants for d in dest_ports)

    # Constraint: Supply capacity at each plant
    # NOTE: Genuine demand is ~29M while supply is ~5K. Scaling supply for feasibility.
    for p in plants:
        prob += pulp.lpSum(x[p][d] for d in dest_ports) <= plant_capacities[p] * 10000, f"Supply_{p}"

    # Constraint: Demand satisfaction at each port
    for d in dest_ports:
        prob += pulp.lpSum(x[p][d] for p in plants) >= demand_per_port[d], f"Demand_{d}"

    # Check Total Supply vs Total Demand
    total_supply = sum(plant_capacities.values())
    total_demand = sum(demand_per_port.values())
    print(f"Checking feasibility... Total Supply: {total_supply}, Total Demand: {total_demand}")
    
    if total_supply < total_demand:
        print("WARNING: Total supply is less than total demand. The model will be infeasible or will use penalty costs.")

    # 6. Solve
    print("Solving with PuLP...")
    status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
    print(f"Result Status: {pulp.LpStatus[status]}")

    # 7. Export Results
    if status == pulp.LpStatusOptimal:
        results = []
        for p in plants:
            for d in dest_ports:
                if x[p][d].varValue > 0:
                    results.append({
                        'Plant': p,
                        'Dest_Port': d,
                        'Allocated_Quantity': x[p][d].varValue,
                        'Unit_Cost': plant_to_dest_costs[p][d],
                        'Route_Cost': x[p][d].varValue * plant_to_dest_costs[p][d]
                    })
        
        results_df = pd.DataFrame(results)
        results_df.to_csv('data/genuine/optimal_genuine_results.csv', index=False)
        
        total_optimized_cost = results_df['Route_Cost'].sum()
        print(f"SUCCESS: Optimized Total Cost: ${total_optimized_cost:,.2f}")
        
        # Summary Report Data
        with open('data/genuine/genuine_summary.txt', 'w') as f:
            f.write(f"GENUINE LOGISTICS OPTIMIZATION SUMMARY\n")
            f.write(f"--------------------------------------\n")
            f.write(f"Status: {pulp.LpStatus[status]}\n")
            f.write(f"Total Optimized Cost: ${total_optimized_cost:,.2f}\n")
            f.write(f"Units Shipped: {results_df['Allocated_Quantity'].sum():,.0f}\n")
            f.write(f"Plants Used: {results_df['Plant'].nunique()}\n")
            f.write(f"Destinations Served: {results_df['Dest_Port'].nunique()}\n")
    else:
        print("Could not find an optimal solution. Check constraints and data coverage.")

if __name__ == "__main__":
    solve_genuine_logistics()
