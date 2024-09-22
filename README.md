<!--toc:start-->

- [This is my strategy portfolio](#this-is-my-strategy-portfolio)
- [Template](#template)
- [Strategies](#strategies)
- [Notations](#notations)
- [Lexica](#lexica)
<!--toc:end-->

# This is my strategy portfolio

In here I document various strategy and testing results.

The strategies should be documented according to the following template.

# Template

```
# Strategy:

<!--toc:start-->

- [Strategy: AwesomeStrategy](#strategy-awesomestrategy)
- [Description](#description)
- [Strategy](#strategy)
  - [Variables](#variables)
  - [Calculations](#calculations)
    - [Buy](#buy)
    - [Sell](#sell)
- [Backtesting Results](#backtesting-results)
<!--toc:end-->

# Description

**Short Description**:\

**Trading Style**:

**Market:**

**Timeframe:**

**Can Short:**

# Strategy

[Strategy code file](./AwesomeStrategy.py)

## Variables

<!--also including ROI and stoploss-->

## Calculations

### Buy

$

$

**Triggers:**

**Guards:**

### Sell

**Triggers:**

**Guards:**

# Backtesting Results

**Timerange:**

**Symbols:** BTC/USDT

**Start Capital:** 1000

**Summary:**
```

# Strategies

- Examples:
  - [AwesomeStrategy](./strategys/example/AwesomeStrategy.md)

# Notations

- $A \uparrow B$: A crosses above B
- $A \downarrow B$: A crosses below B

# Lexica

1. **CAGR (Compound Annual Growth Rate)**

   - **Definition**: CAGR measures the mean annual growth rate of an investment over a specified time period longer than one year.
   - **Interpretation**: A CAGR of 101.833% means that the investment or portfolio grew at an average rate of 101.833% per year over the period being measured.
     It shows the smoothed growth rate, ignoring volatility during the period.

1. **Sharpe Ratio**

   - **Definition**: The Sharpe Ratio measures the risk-adjusted return of a portfolio, where risk is defined by standard deviation.
   - **Interpretation**: A Sharpe Ratio of 2.02 means the portfolio generates 2.02 units of return for every unit of risk.
     Generally, a Sharpe Ratio greater than 1 is considered good, and above 2 is very good.

1. **Sortino Ratio**

   - **Definition**: The Sortino Ratio is a variation of the Sharpe Ratio, but it differentiates harmful volatility (downside deviation) from total volatility.
   - **Interpretation**: A Sortino Ratio of 8.61 indicates that the portfolio generates returns 8.61 times higher than the downside risk (negative volatility).
     A higher ratio implies better risk-adjusted returns, focusing only on downside risk.

1. **Calmar Ratio**

   - **Definition**: The Calmar Ratio is a performance metric that compares the annualized rate of return to the maximum drawdown (the largest peak-to-trough decline).
   - **Interpretation**: A Calmar Ratio of 61.93 is extremely high, indicating that the returns are significantly larger than the worst drawdown the portfolio experienced.
     High Calmar ratios suggest strong returns with limited downside.

1. **Expectancy (Ratio)**

   - **Definition**: Expectancy is a measure of the average return per trade, taking both the probability of winning and losing trades into account.
   - **Interpretation**: An expectancy of 2.41 means that on average, each trade is expected to return 2.41 units of profit.

1. **Profit Factor**

   - **Definition**: The Profit Factor is the ratio of gross profits to gross losses. It helps assess the profitability of a trading system or strategy.
   - **Interpretation**: A profit factor of 1.395 means that for every unit of risk (loss), the system generates 1.395 units of profit.
     A profit factor above 1.0 indicates a profitable system, though the higher, the better.
