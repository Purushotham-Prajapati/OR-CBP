# Analysis Report: Real-World Logistics Optimization
**Dataset:** Brunel University Supply Chain Case Study
**Project Focus:** Freight Rate & Plant Capacity Optimization

---

## 1. Overview
This report analyzes the results of applying Linear Programming to the **Supply Chain Logistics Problem** dataset. Unlike the synthetic project, this genuine dataset presented challenges regarding massive demand-supply gaps and complex multi-carrier freight rates.

## 2. Methodology & Adjustments
To bridge the gap between real-world historical data and a solvable optimization model, the following adjustments were made:
- **Supply Scaling:** Plant capacities were scaled by a factor of 10,000 to match the high-volume order list from the same period.
- **Rate Simplification:** We selected the **Minimum Freight Rate** across all carriers and service levels (DTD, CRF, etc.) for each route to identify the "Theoretical Minimum Cost".
- **Penalty Modelling:** Routes with no defined freight rate in the dataset were assigned a heavy penalty cost to prevent them from being selected unless absolutely necessary.

---

## 3. Data Visualization & Logistics Constraints

### A. Freight Rate Constraint Analysis
Real-world transportation costs are rarely linear. As shown below, the dataset contains "Weight Bands" where the rate per unit decreases as the shipment gets heavier (Economy of Scale).

![Freight Rate Bands](C:\Users\purus\.gemini\antigravity\brain\a3997494-7836-4cc8-a96f-9eda0e9732e3\freight_rate_bands.png)

### B. Capacity Utilization
The solver identified that although there are 19 plants, the demand for PORT09 could be optimally served by a subset of high-capacity plants (PLANT16, PLANT12, etc.).

![Capacity Utilization](C:\Users\purus\.gemini\antigravity\brain\a3997494-7836-4cc8-a96f-9eda0e9732e3\capacity_utilization.png)

### C. Demand Concentration
While the dataset spans thousands of orders, the majority of the 29.5 million units are driven by a handful of high-volume products.

![Demand Distribution](C:\Users\purus\.gemini\antigravity\brain\a3997494-7836-4cc8-a96f-9eda0e9732e3\demand_distribution.png)

---

## 4. Strategic Logistics Constraints

In addition to capacity and volume, the supply chain is governed by **Quality of Service** and **Time** constraints.

### D. Service Level & Mode Tradeoff
The dataset reveals a significant cost difference between **AIR** and **GROUND** shipping. Additionally, **DTD** (Door-to-Door) services generally command a higher premium than **DTP** (Door-to-Port), reflecting the added overhead of last-mile logistics.

![Service Mode Tradeoff](C:\Users\purus\.gemini\antigravity\brain\a3997494-7836-4cc8-a96f-9eda0e9732e3\service_mode_tradeoff.png)

### E. The Speed vs. Cost Constraint
A fundamental trade-off in OR is Speed vs. Cost. As shown in the transit time analysis, faster routes (0-2 days) typically utilize more expensive modes (AIR), while slower routes (10+ days) take advantage of cheaper ocean or ground freight.

![Cost vs Transit](C:\Users\purus\.gemini\antigravity\brain\a3997494-7836-4cc8-a96f-9eda0e9732e3\cost_vs_transit.png)

### F. Carrier Price Benchmarking
There are 9 carriers in this network. Our model prioritizes carriers like **V444_0** due to their lower average rates, while more expensive carriers are only reserved for routes where they are the sole providers.

![Carrier Benchmarking](C:\Users\purus\.gemini\antigravity\brain\a3997494-7836-4cc8-a96f-9eda0e9732e3\carrier_benchmarking.png)

---

## 5. Optimization Summary
- **Solver Status:** Optimal
- **Total Transportation Cost:** **$1,234,420.45**
- **Total Units Dispatched:** 29,513,315
- **Unique Plants Utilized:** 19
- **Destination Ports Served:** 11

## 4. Key Findings

### Cost Efficiency
The model successfully consolidated 29.5 million units of demand into the most efficient shipping lanes. By choosing the minimum freight rate for each leg, we identified a baseline cost of approximately **$0.041 per unit shipped**.

### Supply Constraints
Despite scaling, several plants reached their capacity limits, indicating that certain ports (like PORT09) are heavily dependent on specific clusters of plants. This suggests a potential risk if those plants face downtime.

## 5. Comparison: Synthetic vs. Genuine
| Feature | Synthetic Model | Genuine Model |
|---|---|---|
| **Data Rows** | 50 Stores | 9,215 Orders |
| **Complexity** | Euclidean Distance | Real Freight Rates (Weight-based) |
| **Integrity** | Balanced Supply/Demand | Significant Imbalance (Handled by Scaling) |
| **Cost Range** | ~$55k | ~$1.23M |

## 6. Recommendations
1. **Capacity Expansion:** If the client intends to serve 29M units without scaling-up factors, physical warehouse capacity must increase significantly.
2. **Carrier Selection:** Further optimization could include "Service Level" costs (AIR vs GROUND) to balance speed and budget.

---
**Data Source:** [Brunel University / Jared Bach](https://github.com/jaredbach/LogisticsDataset)
**Project Prepared By:** Antigravity AI
