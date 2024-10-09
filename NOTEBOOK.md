# RSI Scalping

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

## RSI Scalping + Candlestick patterns

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
