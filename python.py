import pulp

# Problem
prob = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Data
costs = [[2,3,1,4],
         [3,2,5,1],
         [4,3,2,2]]

supply = [20,30,25]
demand = [10,25,20,20]

rows = range(len(supply))
cols = range(len(demand))

# Decision variables
x = pulp.LpVariable.dicts("ship", (rows, cols), lowBound=0)

# Objective
prob += pulp.lpSum(costs[i][j] * x[i][j] for i in rows for j in cols)

# Supply constraints
for i in rows:
    prob += pulp.lpSum(x[i][j] for j in cols) == supply[i]

# Demand constraints
for j in cols:
    prob += pulp.lpSum(x[i][j] for i in rows) == demand[j]

# Solve
prob.solve()

# Output
print("Status:", pulp.LpStatus[prob.status])
for i in rows:
    for j in cols:
        print(f"Ship from W{i+1} to S{j+1}: {x[i][j].varValue}")

print("Total Cost =", pulp.value(prob.objective))