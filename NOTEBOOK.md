<!--toc:start-->

- [General](#general)
  - [Ideas](#ideas)
  - [Indicators](#indicators)
    - [1. Trend Indicators (Show the direction of the market)](#1-trend-indicators-show-the-direction-of-the-market)
    - [2. Momentum Indicators (Reveal the strength of price movement)](#2-momentum-indicators-reveal-the-strength-of-price-movement)
    - [3. Volatility Indicators (Highlight the intensity of price fluctuations)](#3-volatility-indicators-highlight-the-intensity-of-price-fluctuations)
    - [4. Volume Indicators (Confirm the strength behind price trends)](#4-volume-indicators-confirm-the-strength-behind-price-trends)
    - [5. Market Strength Indicators (Track overall market movement)](#5-market-strength-indicators-track-overall-market-movement)
    - [6. Support/Resistance Indicators (Identify key price levels)](#6-supportresistance-indicators-identify-key-price-levels)
  - [Metrics](#metrics)
- [Strategys](#strategys)
  - [RSI Scalping](#rsi-scalping)
    - [RSI Scalping + Candlestick patterns](#rsi-scalping-candlestick-patterns)
    - [RSI scalping + OBV](#rsi-scalping-obv)
- [Other](#other)
<!--toc:end-->

# General

## Ideas

**Untested:**

- Apply a linear regression on close or an SMA and use the angle to define if a strong trend happens.
  - potential guard
  - dont forget $|R| > 0.8$
- Maybe focus more on the exit signals rather than the entry signals for RSI scalping.
  Because the entry signals are mostly right but often close too late.
  - dont just use stoploss

## Indicators

### 1. Trend Indicators (Show the direction of the market)

- **Moving Averages (MA):** Simple Moving Average (SMA), Exponential Moving Average (EMA) – Smooth out price data to show the overall direction of the trend.
- **Moving Average Convergence Divergence (MACD):** Measures the relationship between two EMAs to show trend direction and strength.
- **Average Directional Index (ADX):** Indicates the strength of a trend but not its direction.
- **Parabolic SAR:** Highlights potential reversal points by showing dots on the chart above or below price.

### 2. Momentum Indicators (Reveal the strength of price movement)

- **Relative Strength Index (RSI):** Measures the speed and change of price movements, typically to identify overbought or oversold conditions.
- **Stochastic Oscillator:** Compares a specific closing price to a range of its prices over time, showing potential reversal points.
- **Commodity Channel Index (CCI):** Measures how far a price has deviated from its average, used to identify momentum and potential reversals.
- **Rate of Change (ROC):** Measures the percentage change between the current price and a price from a certain number of periods ago.

### 3. Volatility Indicators (Highlight the intensity of price fluctuations)

- **Bollinger Bands:** Use standard deviations to show volatility; when the bands widen, volatility increases.
- **Average True Range (ATR):** Measures the average range between high and low prices to gauge volatility.
- **Keltner Channels:** Similar to Bollinger Bands but based on ATR, highlighting volatility.
- **Donchian Channels:** Highlight the highest and lowest prices over a specific period, showing volatility and potential breakout points.

### 4. Volume Indicators (Confirm the strength behind price trends)

- **On-Balance Volume (OBV):** Combines price and volume to show the cumulative buying and selling pressure.
- **Volume Price Trend (VPT):** Similar to OBV but includes the percentage change in price.
- **Chaikin Money Flow (CMF):** Measures buying and selling pressure using price and volume.
- **Accumulation/Distribution (A/D) Line:** Looks at volume and price to assess whether a stock is being accumulated (buying) or distributed (selling).

### 5. Market Strength Indicators (Track overall market movement)

- **Advance/Decline Line (A/D Line):** Tracks the number of advancing vs. declining stocks to gauge overall market strength.
- **McClellan Oscillator:** A breadth indicator that looks at the rate of change between advancing and declining issues.
- **Arms Index (TRIN):** Measures the relationship between advancing and declining stocks and their volume.

### 6. Support/Resistance Indicators (Identify key price levels)

- **Pivot Points:** Calculate potential support and resistance levels based on the previous period’s price action.
- **Fibonacci Retracement:** Shows potential levels of support or resistance by using Fibonacci ratios.
- **Price Action (candlestick patterns):** Certain candlestick formations can highlight support and resistance levels (e.g., hammer, engulfing).
- **Supply and Demand Zones:** Mark levels where price historically found support or resistance.

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

# Strategies

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

**Pros:** The candlestick pattern filters out most false signals \
**Cons:** The candlestick patterns filters out too many signals which leads to small profits

**Notes:**

- Adjusting the limits (eg 20 $\rightarrow$ 30) produces too many false signals.
- Adding multiple candlestick patterns as triggers has not brought any significant improvement
  - But this has to be tested out more in the future on a broader timerange.

### RSI scalping + OBV

I couldn't really find a way to use the OBV to reduce false entry signals.

Because of the nature of RSI scalping the OBV is naturally low when the RSI indicates an oversold situation.
This also means that the angle of the linear regression from the OBV is negative.

The fault lies at the tight condition of $RSI < 20$ for buying.
Because this condition mostly occures at the bottom of a downtrend or during a strong and long downtrend.

**Note:**
Other types of applications of the OBV have not been explored yet.

**Untested potential use cases:**

- exit signal
- supporting guard signal indicating a weakening in trend

# Other

_nothing to see here yet_
