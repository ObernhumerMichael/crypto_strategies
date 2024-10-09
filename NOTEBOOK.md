<!--toc:start-->

- [General](#general)
  - [Indicators](#indicators)
  - [Metrics](#metrics)
- [Strategys](#strategys)
  - [RSI Scalping](#rsi-scalping)
    - [RSI Scalping + Candlestick patterns](#rsi-scalping-candlestick-patterns)
- [Other](#other)
<!--toc:end-->

# General

## Indicators

- **Trend Indicators** show the direction of the market.
- **Momentum Indicators** reveal the strength of the price movement.
- **Volatility Indicators** highlight the intensity of price fluctuations.
- **Volume Indicators** confirm the strength behind price trends.
- **Market Strength Indicators** track overall market movement.
- **Support/Resistance Indicators** identify key price levels.

## Metrics

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

# Strategys

## RSI Scalping

**Result:** loss

**Timeframe:** 1-15m

$$ Buy: RSI \downarrow 30 $$
$$ Sell: RSI \uparrow 70 $$

**Pros:**

- The strategy works rather well if it closes witout hitting a stoploss, it almost always produces a profit.
- It works under most conditions.

**Cons:**

- It produces many wrong signals in strongly trending situations.
  This leads to overall losses.

**Notes:**

- Adjusting the limits (eg 30 $\rightarrow$ 20) according to volatility helps.
- Adjusting the stoploss can also help but the strategy needs some breathing room.
- The strategy produces to much wrong signals in trending situations.
- Works best in 15m timeframe.

### RSI Scalping + Candlestick patterns

**Result:** profit

**Timeframe:** 1m

**Buy:**

$$ RSI \downarrow 20 $$
$$ Kline \rightarrow Engulfing $$

**Sell:**

$$RSI \uparrow 70 $$

**Pros:**

- The candlestick pattern filters out most false signals

**Cons:**

- The candlestick patterns filters out too many signals which leads to smaller profits

**Notes:**

- Adjusting the limits (eg 20 $\rightarrow$ 30) produces too many false signals.
- Adding multiple candlestick patterns as triggers has not brought any significant improvement

  - But this has to be tested out more in the future on a broader timerange.

  # Other

  _nothing to see here yet_
