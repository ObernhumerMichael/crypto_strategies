# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
from math import degrees
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


class SC_RSI_VOLUME(IStrategy):
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
    stoploss = -0.5

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
    startup_candle_count: int = 30

    # Define the parameter spaces
    rsi = IntParameter(2, 20, default=14)
    obv_len = IntParameter(1, 20, default=5)

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
            "OBV": {
                f"obv": {"color": "blue"},
                f"obv_ln": {"color": "orange"},
            },
            "OBV_an": {
                f"angle": {"color": "blue"},
            },
            "OBV_r2": {
                f"r2": {"color": "green"},
            },
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Generate all indicators used by the strategy"""

        # RSI
        dataframe[f"rsi"] = pta.rsi(dataframe["close"], length=self.rsi.value)
        dataframe["obv"] = pta.obv(dataframe["close"], dataframe["volume"])
        dataframe["obv_ln"] = pta.linreg(dataframe["obv"])
        dataframe["angle"] = pta.linreg(dataframe["obv"], angle=True)
        dataframe["r"] = pta.linreg(dataframe["obv"], r=True)
        dataframe["r2"] = dataframe["r"] * dataframe["r"]
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions_long = []

        conditions_long.append(dataframe["rsi"] < 20)

        # conditions_long.append(dataframe["obv"] > dataframe["obv"].shift(1))

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
