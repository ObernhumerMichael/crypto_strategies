<!--toc:start-->

- [General](#general)
  - [Freqtrade commands](#freqtrade-commands)
  - [ToDo](#todo)
  - [Ideas](#ideas)
  - [General](#general)
    - [SC RSI Strategies](#sc-rsi-strategies)
  - [Notations](#notations)
  - [Indicators](#indicators)
    - [Trend Indicators](#trend-indicators)
    - [Momentum Indicators](#momentum-indicators)
    - [Volatility Indicators](#volatility-indicators)
    - [Volume Indicators](#volume-indicators)
    - [Market Strength Indicators](#market-strength-indicators)
    - [Support and Resistance Indicators](#support-and-resistance-indicators)
  - [Metrics](#metrics)
  - [Trading Strategy Types](#trading-strategy-types)
- [Snippets](#snippets)
  - [Custom Stoploss](#custom-stoploss)
    - [Non trailing stoploss](#non-trailing-stoploss)
- [Strategies](#strategies)
  - [Scalping](#scalping)
    - [RSI](#rsi)
    - [RSI and Engulfing](#rsi-and-engulfing)
      - [RSI and Engulfing with custom stoploss](#rsi-and-engulfing-with-custom-stoploss)
    - [RSI and OBV](#rsi-and-obv)
    - [Linear Regression and RSI](#linear-regression-and-rsi)
  - [Trend Following](#trend-following)
    - [SMA and RSI](#sma-and-rsi)
      - [SMA and RSI with custom stoploss](#sma-and-rsi-with-custom-stoploss)
      - [Bidirectional SMA and RSI with custom stoploss](#bidirectional-sma-and-rsi-with-custom-stoploss)
      - [SMA and RSI with ATR based stoploss and ROI](#sma-and-rsi-with-atr-based-stoploss-and-roi)
      - [SMA and RSI with ATR based position adjustment](#sma-and-rsi-with-atr-based-position-adjustment)
    - [EMA Crossover + MACD Confirmation](#ema-crossover-macd-confirmation)
- [Final Thoughts](#final-thoughts)
<!--toc:end-->

# General

This is my notebook about crypto trading.
It contains my experience with various trading strategies.
All the strategy files are written for [freqtrade](https://www.freqtrade.io/en/stable/).

## Freqtrade commands

Start the webserver:

```sh
freqtrade webserver
```

To download the data for pairs specified in the config.json

```sh
freqtrade download-data -c ./user_data/config.json --days 365 --timeframes 1m 5m 15m 1h
```

## ToDo

- [ ] Make use of the derived strategy feature.

## Ideas

## General

- Use custom ROI with the help of `custom_exit`.
  Maybe use a multiple of ATR similar to `non_trailing_stoploss`.
- Implement a risk-reward system using `custom_stoploss` and `custom_exit (ROI)`.

### SC RSI Strategies

- Adjust the ATR multiplier.
- Use small ROI but on many coins.
- Use simple RSI scalping but with ATR base stoploss/ROI.

## Notations

- $A \uparrow B$: A crosses above B
- $A \downarrow B$: A crosses below B
- TF = Trend Following
- SC = Scalping

## Indicators

### Trend Indicators

Show the direction of the market..

- **Moving Averages (MA):** Simple Moving Average (SMA), Exponential Moving Average (EMA) – Smooth out price data to show the overall direction of the trend.
- **Moving Average Convergence Divergence (MACD):** Measures the relationship between two EMAs to show trend direction and strength.
- **Average Directional Index (ADX):** Indicates the strength of a trend but not its direction.
- **Parabolic SAR:** Highlights potential reversal points by showing dots on the chart above or below price.

### Momentum Indicators

Reveal the strength of price movement.

- **Relative Strength Index (RSI):** Measures the speed and change of price movements, typically to identify overbought or oversold conditions.
- **Stochastic Oscillator:** Compares a specific closing price to a range of its prices over time, showing potential reversal points.
- **Commodity Channel Index (CCI):** Measures how far a price has deviated from its average, used to identify momentum and potential reversals.
- **Rate of Change (ROC):** Measures the percentage change between the current price and a price from a certain number of periods ago.

### Volatility Indicators

Highlight the intensity of price fluctuations.

- **Bollinger Bands:** Use standard deviations to show volatility; when the bands widen, volatility increases.
- **Average True Range (ATR):** Measures the average range between high and low prices to gauge volatility.
- **Keltner Channels:** Similar to Bollinger Bands but based on ATR, highlighting volatility.
- **Donchian Channels:** Highlight the highest and lowest prices over a specific period, showing volatility and potential breakout points.

### Volume Indicators

Confirm the strength behind price trends.

- **On-Balance Volume (OBV):** Combines price and volume to show the cumulative buying and selling pressure.
- **Volume Price Trend (VPT):** Similar to OBV but includes the percentage change in price.
- **Chaikin Money Flow (CMF):** Measures buying and selling pressure using price and volume.
- **Accumulation/Distribution (A/D) Line:** Looks at volume and price to assess whether a stock is being accumulated (buying) or distributed (selling).

### Market Strength Indicators

Track overall market movement.

- **Advance/Decline Line (A/D Line):** Tracks the number of advancing vs. declining stocks to gauge overall market strength.
- **McClellan Oscillator:** A breadth indicator that looks at the rate of change between advancing and declining issues.
- **Arms Index (TRIN):** Measures the relationship between advancing and declining stocks and their volume.

### Support and Resistance Indicators

Identify key price levels.

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

## Trading Strategy Types

1. **Scalping**  
    A short-term trading strategy that focuses on making small, quick profits from minor price movements.
   Traders often place multiple trades within minutes or seconds.

1. **Day Trading**  
    Buying and selling assets within the same trading day to capitalize on short-term price movements.
   Day traders do not hold positions overnight.

1. **Swing Trading**  
    A medium-term strategy where traders aim to profit from price swings over days or weeks.
   They typically use technical analysis to identify entry and exit points.

1. **Position Trading**  
   A long-term approach where traders hold positions for weeks, months, or even years, relying on fundamental analysis to predict future price movements.

1. **Momentum Trading**  
    Traders focus on assets showing strong trends, entering trades when momentum is high and exiting when it begins to fade.
   It relies heavily on technical indicators like RSI or MACD.

1. **Trend Following**  
    A strategy that follows the prevailing market direction.
   Traders go long when markets are trending upward and short when they are trending downward.

1. **Arbitrage**  
    Exploiting price differences of the same asset on different exchanges or markets.
   It involves buying low in one market and selling high in another almost simultaneously.

1. **Mean Reversion**  
    Based on the idea that prices tend to revert to their average or mean over time.
   Traders buy when prices are low (below average) and sell when they are high (above average).

1. **Breakout Trading**  
   Traders buy or sell assets when prices break through significant resistance or support levels, hoping to capitalize on the strong move that follows.

1. **Reversal Trading**  
    A strategy focused on identifying potential trend reversals, typically after a strong trend.
   Traders aim to enter as soon as the market shifts direction.

1. **Carry Trade**  
   Commonly used in forex, it involves borrowing funds in a currency with a low interest rate and investing in a currency with a higher rate, profiting from the difference.

1. **News-Based Trading**  
    Traders react to major economic announcements, earnings reports, or geopolitical events.
   They attempt to predict market moves based on the news impact.

1. **Options Trading**  
    Involves buying and selling options contracts, giving the trader the right (but not the obligation) to buy or sell an asset at a specified price within a set timeframe.
   Strategies include hedging or leveraging positions.

1. **Pairs Trading**  
    Involves trading two correlated assets by going long on one and short on the other.
   The goal is to profit from the divergence or convergence of their prices.

1. **Grid Trading**  
   Traders place buy and sell orders at predefined intervals (grid) around a set price to profit from market fluctuations, especially in sideways markets.

# Snippets

## Custom Stoploss

### Non trailing stoploss

**Snippet:** [non_trailing_stoploss](./snippets/custom_stoploss/non_trailing_stoploss.py)

**Explanation:** This sets the stoploss to a value defined in `populate_indicators` at trade entry.

**Possible use case:** Giving more/less breathing room for the market depending on the situation.
This can possible improve the chance for good signals to take effect and limit the losses of false signals.

**Example**:
Using a multiple of ATR as the stoploss. _see [volatility-indicators](#volatility-indicators)_

$$ stoploss=ATR \* multiplier / CLOSE $$

> [!NOTE]
> The stoploss must be in percent. eg: 1% = 0.01

# Strategies

## Scalping

### RSI

**Result:** loss

**time frame:** 1-15m

$$ Buy: RSI \downarrow 30 $$
$$ Sell: RSI \uparrow 70 $$

**Pros:**

- The strategy works rather well if it closes without hitting a stop loss, it almost always produces a profit.
- It works under most conditions.

**Cons:**

- It produces many wrong signals in strongly trending situations.
  This leads to overall losses.

**Notes:**

- Adjusting the limits (e.g. 30 $\rightarrow$ 20) according to volatility helps.
- Adjusting the stop loss can also help but the strategy needs some breathing room.
- The strategy produces to much wrong signals in trending situations.
- Works best in 15m time frame.

### RSI and Engulfing

**Result:** profit

**time frame:** 1m

**Strategy:** [SC_RSI_Engulfing](./strategies/SC_RSI_Engulfing.py)

**Buy:**

$$ RSI \downarrow 20 $$
$$ Kline \rightarrow Engulfing $$

**Sell:**

$$RSI \uparrow 70 $$

**Pros:** The candlestick pattern filters out most false signals \
**Cons:** The candlestick patterns filters out too many signals which leads to small profits

**Notes:**

- Adjusting the limits (e.g. 20 $\rightarrow$ 30) produces too many false signals.
- Adding multiple candlestick patterns as triggers has not brought any significant improvement
  - But this has to be tested out more in the future on a broader timerange.

#### RSI and Engulfing with custom stoploss

Same as [RSI and Engulfing](#rsi-and-engulfing) but uses ATR to make custom stoplosses.

**Result:** profit --

**Strategy:** [SC_RSI_Engulfing_V2](./strategies/SC_RSI_Engulfing_V2.py)

**Notes:**

- This does not improve the trading results as the custom stoploss sets the breathing room to tight.
- The candlestick patter already filters out most false signals.
- The stoploss cancels the good signals too early resulting in smaller profits.

### RSI and OBV

**Strategy:** [SC_RSI_VOLUME](./strategies/SC_RSI_VOLUME.py)

I couldn't really find a way to use the OBV to reduce false entry signals.

Because of the nature of RSI scalping the OBV is naturally low when the RSI indicates an oversold situation.
This also means that the angle of the linear regression from the OBV is negative.

The fault lies at the tight condition of $RSI < 20$ for buying.
Because this condition mostly occurs at the bottom of a downtrend or during a strong and long downtrend.

**Note:**
Other types of applications of the OBV have not been explored yet.

**Untested potential use cases:**

- exit signal
- supporting guard signal indicating a weakening in trend

### Linear Regression and RSI

**Result:** loss

**time frame:** 1m

**Strategy:** [SC_linreg](./strategies/SC_linreg.py)

**Buy:**

$$ angle \uparrow 0 $$
$$ r < 0.01 $$
$$ RSI > 50 $$
$$ RSI < 60 $$

**Sell:**

$$RSI \uparrow 70 $$

**Pros:**

- One is able to identify stronger trends relatively well
- Able to determine the direction of the trend.
- Able to check how valid the linear regression is.
- Able to determine possible reversals.

**Cons:**

- Produces many false signals
- Has problems when there is not much market movement

**Notes:**

- Angle cross has to be relatively sharp to be more or less valid
- Possible application as trend indicator $\rightarrow$ must be tested
- Possible application in validating other indicators

## Trend Following

### SMA and RSI

**Result:** profit

**time frame:** 15m

**Strategy:** [TF_SMA_RSI](./strategies/TF_SMA_RSI.py)

**Buy:**

$$SMA_{short} \uparrow SMA_{long}$$
$$RSI > 50$$
$$RSI < 70$$

**Sell:**

$$SMA_{short} \downarrow SMA_{long}$$
$$RSI < 50$$
$$RSI > 30$$

**Pros:**

- Catches most major price swings.
- The RSI filters out several false signals.

**Cons:**

- Performs rather badly in side ways markets.
- The RSI guards filter out some correct signals.

**Notes:**

- A rather solid trading strategy for strongly trending markets.

#### SMA and RSI with custom stoploss

Same as the default but uses ATR to make custom stoplosses.

**Strategy:** [TF_SMA_RSI_V2](./strategies/TF_SMA_RSI_V2.py)

**Result:** profit ++

**Notes:**

- This improves the trading results significantly.
- The custom stoploss helps to minimize the losses on false signals.
- The custom stoploss gives the indicator more breathing room when needed.

#### Bidirectional SMA and RSI with custom stoploss

Same as [SMA and RSI with custom stoploss](#sma-and-rsi-with-custom-stoploss) but it also allows short positions.
The short conditions are the inverse to the long positions.

**Strategy:** [TF_SMA_RSI_V3](./strategies/TF_SMA_RSI_V3.py)

**Result:** profit --

**Notes:**

- This does NOT improve the original strategy.
- There are more false signals on short trades than long ones, which leads to smaller profits.

#### SMA and RSI with ATR based stoploss and ROI

Same as [SMA and RSI with custom stoploss](#sma-and-rsi-with-custom-stoploss) but it also introduces a custom ROI based on ATR.

**Strategy:** [TF_SMA_RSI_V4](./strategies/TF_SMA_RSI_V4.py)

**Result:** profit --

**Notes:**

- This does NOT improve the original strategy.
- The custom ROI takes away the meaning of trend following.
- It closes most trades either through ROI or Stoploss.

#### SMA and RSI with ATR based position adjustment

Same as [SMA and RSI with custom stoploss](#sma-and-rsi-with-custom-stoploss),
but it also introduces a halfing of the position when the profit reaches a certain amount based on an ATR multiple.

**Strategy:** [TF_SMA_RSI_V5](./strategies/TF_SMA_RSI_V5.py)

**Result:** profit --

**Notes:**

- This does not improve the original strategy in terms of profit.
- I increases the win rate of the strategy and reduces risks.
- With properly adjusted parameters I think this type of adjustment can help with risk management.

### EMA Crossover + MACD Confirmation

**Strategy:** [TF_EMA_MACD](./strategies/TF_EMA_MACD.py)

**Result:** loss

Stoploss is ATR based.

**Buy:**
$$EMA_{short} \uparrow EMA_{long}$$
$$MACD_{positive}$$
$$MACD_{-1} < MACD$$
$$ADX > 25$$

**Sell:**
$$EMA_{short} \downarrow EMA_{long}$$

**Pros:**
Strong in trending markets (e.g., ETH during a breakout).

**Cons:**
Whipsaws in choppy markets.

**When to Use:**
During strong uptrends/downtrends (check with ADX > 25).

# Final Thoughts

This only contains my own personal experience.
**ALWAYS** do your own research.
I am in no way responsible for any trading results.
