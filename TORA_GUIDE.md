# TORA Optimization Guide: Retail Supply Chain

TORA (Temporary Operation Research Application) is a classic software for learning OR. While our Python script handles a large 10x50 matrix, TORA's UI is best suited for smaller matrices.

Below is a **5x5 subset** of our retail problem extracted for manual entry into TORA.

## 1. Problem Matrix (5 DCs x 5 Stores)

| | Store_01 | Store_02 | Store_03 | Store_04 | Store_05 | **Supply** |
|---|---|---|---|---|---|---|
| **DC_01** | 9.07 | 10.37 | 5.86 | 6.72 | 8.87 | **2126** |
| **DC_02** | 6.46 | 9.01 | 11.23 | 5.08 | 7.92 | **1459** |
| **DC_03** | 7.15 | 8.54 | 11.29 | 10.31 | 10.15 | **2291** |
| **DC_04** | 7.62 | 9.47 | 10.02 | 11.66 | 8.44 | **2604** |
| **DC_05** | 6.55 | 9.87 | 11.02 | 9.17 | 10.87 | **2023** |
| **Demand**| **496** | **221** | **314** | **120** | **421** | |

*(Note: These costs and capacities are sampled from the generated `data/` files for consistency)*

## 2. Steps to Solve in TORA

1. **Launch TORA.exe** and select **Transportation Model** from the Main Menu.
2. Click **Go to Input Screen**.
3. **Problem Title**: Retail Distribution Subset.
4. **Number of Sources (Supply)**: 5.
5. **Number of Destinations (Demand)**: 5.
6. **Input Data**:
    - Enter the cost values in the matrix cells.
    - Enter the Supply capacities in the right-most column.
    - Enter the Demand requirements in the bottom-most row.
7. Click **Solve Menu** -> **Solve Problem**.
8. Select **Starting Solution Method**:
    - Choose **Vogel's Approximation Method (VAM)** (Recommended for best initial results).
9. Click **Output Summary** to see the optimal allocation.

## 3. Interpreting Results
- TORA will show a table where cells contain values like `X(1,3) = 314`. This means 314 units should be shipped from DC_01 to Store_03.
- The **Total Cost** in TORA for this subset should be significantly lower than the full Python model because it only considers 5 stores.

## 4. Comparison: Python vs TORA
| Feature | Python (PuLP) | TORA |
|---|---|---|
| **Capacity** | Scalable (Thousands of rows/cols) | Limited (Small Educational Matrices) |
| **Speed** | Instant (< 1s) | Manual Data Entry |
| **Visualization** | Custom Network Graphs | Tabular results only |
| **Method** | Simplex/CBC Solver | VAM, North-West, Least-Cost |
