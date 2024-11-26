# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
from operator import length_hint
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from typing import Dict, Optional, Union, Tuple

from technical.vendor.qtpylib.indicators import crossed_above

from freqtrade.strategy import (
    IStrategy,
    Trade,
    Order,
    PairLocks,
    informative,  # @informative decorator
    # Hyperopt Parameters
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
    RealParameter,
    # timeframe helpers
    timeframe_to_minutes,
    timeframe_to_next_date,
    timeframe_to_prev_date,
    # Strategy helper functions
    merge_informative_pair,
    stoploss_from_absolute,
    stoploss_from_open,
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib

# --------------------------------
# Backtesting
from functools import reduce


class SC_RSI_Engulfing_V2(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = "1m"

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {"0": 0.5}

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.05
    use_custom_stoploss = True

    # Trailing stoploss
    # trailing_stop = True
    # trailing_only_offset_is_reached = True
    # trailing_stop_positive = 0.003
    # trailing_stop_positive_offset = 0.005  # Disabled / not configured

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 50

    # Define the parameter spaces
    rsi = IntParameter(2, 20, default=14)
    candlestick_patterns = ["engulfing"]

    # Indicators
    atr_multiplier = 6
    atr_length = 14

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    plot_config = {
        # Main plot indicators (Moving averages, ...)
        "main_plot": {},
        "subplots": {
            # Subplots - each dict defines one additional plot
            "RSI": {
                f"rsi": {"color": "red"},
            },
            "Stoploss": {
                "stoploss_percent": {"color": "red"},
            },
        },
    }

    # no trailing stoploss!!!!!!!!!!
    def custom_stoploss(
        self,
        pair: str,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        after_fill: bool,
        **kwargs,
    ) -> Optional[float]:
        """
        Custom stoploss logic, returning the new distance relative to current_rate (as ratio).
        e.g. returning -0.05 would create a stoploss 5% below current_rate.
        The custom stoploss can never be below self.stoploss, which serves as a hard maximum loss.

        For full documentation please go to https://www.freqtrade.io/en/latest/strategy-advanced/

        When not implemented by a strategy, returns the initial stoploss value.
        Only called when use_custom_stoploss is set to True.

        :param pair: Pair that's currently analyzed
        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
        :param current_profit: Current profit (as ratio), calculated based on current_rate.
        :param after_fill: True if the stoploss is called after the order was filled.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return float: New stoploss value, relative to the current_rate
        """
        trade_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)

        # only adjust the stoploss at the beginning of the trade.
        # stoploss is set to what the value of stoploss_percent is on trade entry
        if current_time == trade_date:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            last_candle = dataframe.iloc[-1].squeeze()
            stoploss_percent = last_candle["stoploss_percent"]

            return stoploss_percent

        # don't update stoploss value
        return None

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Generate all indicators used by the strategy"""

        # RSI
        dataframe[f"rsi"] = pta.rsi(dataframe["close"], length=self.rsi.value)

        # candlestick_patterns
        dataframe[self.candlestick_patterns] = pta.cdl_pattern(
            open_=dataframe["open"],
            high=dataframe["high"],
            low=dataframe["low"],
            close=dataframe["close"],
            name=self.candlestick_patterns,
        )

        dataframe[f"atr"] = pta.atr(
            high=dataframe["high"],
            low=dataframe["low"],
            close=dataframe["close"],
            length=self.atr_length,
            mamode="sma",
        )

        dataframe[f"stoploss_percent"] = (
            dataframe["atr"] / dataframe["close"] * self.atr_multiplier * -1
        )

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions_long = []

        conditions_long.append(dataframe["rsi"] < 20)
        conditions_long.append(dataframe[self.candlestick_patterns].any(axis=1))

        # Check that volume is not 0
        conditions_long.append(dataframe["volume"] > 0)

        if conditions_long:
            dataframe.loc[reduce(lambda x, y: x & y, conditions_long), "enter_long"] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions_long = []

        conditions_long.append((dataframe["rsi"] > 70))

        # Check that volume is not 0
        conditions_long.append(dataframe["volume"] > 0)

        if conditions_long:
            dataframe.loc[reduce(lambda x, y: x & y, conditions_long), "exit_long"] = 1
        return dataframe
