# Strategy: AwesomeStrategy

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
This is an example strategy that uses SMAs as triggers and RSIs as guards.

**Trading Style**: swing trading

**Market:** trading range

**Timeframe:** 15m

**Can Short:** No

# Strategy

[Strategy code file](./AwesomeStrategy.py)

## Variables

<!--including ROI and stoploss-->

```python
minimal_roi = {"0": 0.10}

stoploss = -0.02
trailing_stop = False

sma_short = 50
sma_long = 200

rsi_border = 50
rsi_upper_bound = 70
rsi_lower_bound = 30
```

## Calculations

### Buy

$
SMA_{short} \uparrow SMA_{long}\\
RSI > RSI_{border}\\
RSI < RSI_{upper\ bound} \\
VOLUME > 0\\
$

**Triggers:**

- The SMAs are the main indicators that should indicate a change in trend.\

**Guards:**

- $RSI > RSI_{border}$ is used to filter out signals that happen due to volatility.
- $RSI < RSI_{upper\ bound}$ to avoid buying at an overbought scenario.

### Sell

```latex
SMA_{short} \downarrow SMA_{long}\\
RSI < RSI_{border}\\
RSI > RSI_{lower\ bound}\\
VOLUME > 0\\
```

**Triggers:**

- The SMAs are the main indicators that should indicate a change in trend.\

**Guards:**

- $RSI > RSI_{border}$ is used to filter out signals that happen due to volatility.
- $RSI > RSI_{upper\ lower}$ to avoid selling at an oversold scenario.

# Backtesting Results

**Timerange:** 20240801-20240922

**Symbols:** BTC/USDT

**Start Capital:** 1000

**Summary:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                      ┃ Value               ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Backtesting from            │ 2024-08-01 00:00:00 │
│ Backtesting to              │ 2024-09-22 00:00:00 │
│ Max open trades             │ 1                   │
│                             │                     │
│ Total/Daily Avg Trades      │ 5 / 0.1             │
│ Starting balance            │ 1000 USDT           │
│ Final balance               │ 1092.612 USDT       │
│ Absolute profit             │ 92.612 USDT         │
│ Total profit %              │ 9.26%               │
│ CAGR %                      │ 86.21%              │
│ Sortino                     │ 6.69                │
│ Sharpe                      │ 0.70                │
│ Calmar                      │ 63.51               │
│ Profit factor               │ 2.65                │
│ Expectancy (Ratio)          │ 18.52 (0.99)        │
│ Avg. daily profit %         │ 0.18%               │
│ Avg. stake amount           │ 1009.404 USDT       │
│ Total trade volume          │ 5047.021 USDT       │
│                             │                     │
│ Best Pair                   │ BTC/USDT 9.26%      │
│ Worst Pair                  │ BTC/USDT 9.26%      │
│ Best trade                  │ BTC/USDT 9.99%      │
│ Worst trade                 │ BTC/USDT -2.20%     │
│ Best day                    │ 98.397 USDT         │
│ Worst day                   │ -22.595 USDT        │
│ Days win/draw/lose          │ 2 / 29 / 3          │
│ Avg. Duration Winners       │ 4 days, 9:22:00     │
│ Avg. Duration Loser         │ 14:35:00            │
│ Max Consecutive Wins / Loss │ 1 / 3               │
│ Rejected Entry signals      │ 0                   │
│ Entry/Exit Timeouts         │ 0 / 0               │
│                             │                     │
│ Min balance                 │ 994.215 USDT        │
│ Max balance                 │ 1092.612 USDT       │
│ Max % of account underwater │ 5.36%               │
│ Absolute Drawdown (Account) │ 5.36%               │
│ Absolute Drawdown           │ 56.281 USDT         │
│ Drawdown high               │ 50.496 USDT         │
│ Drawdown low                │ -5.785 USDT         │
│ Drawdown Start              │ 2024-08-11 18:00:00 │
│ Drawdown End                │ 2024-09-04 00:45:00 │
│ Market change               │ -7.20%              │
└─────────────────────────────┴─────────────────────┘
```
