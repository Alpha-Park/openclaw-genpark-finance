---
name: genpark-finance
description: Basic financial modeling, DCF, and unit economics calculator.
version: 1.0.0
---

# genpark-finance

## Overview
This skill aids in business financial planning. It performs basic Discounted Cash Flow (DCF) modeling, analyzes product profit margins, and calculates unit economics to ensure profitability.

## Capabilities
1. **Unit Economics**: Calculate Customer Acquisition Cost (CAC), Lifetime Value (LTV), and gross margins per unit.
2. **DCF Modeling**: Build a basic 5-year cash flow projection based on user-provided growth assumptions and discount rates.
3. **Break-Even Analysis**: Determine the sales volume required to cover fixed and variable costs.

## Usage Instructions
When a user asks about profitability:
- Request fixed costs, variable sourcing costs (from `genpark-sourcing`), and expected sale price.
- Calculate the break-even point and display a simplified P&L (Profit and Loss) statement.
- For DCF requests, always state the assumed Terminal Value and Discount Rate for transparency.
