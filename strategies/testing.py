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


class Testing(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = "5m"

    # Can this strategy go short?
    can_short: bool = True

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
    startup_candle_count: int = 500

    # Define the parameter spaces
    rsi = IntParameter(2, 20, default=14)
    sma_short = IntParameter(3, 50, default=150)
    sma_long = IntParameter(1, 50, default=500)

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    plot_config = {
        # Main plot indicators (Moving averages, ...)
        "main_plot": {
            "bb_upperband": {
                "color": "orange",
                "fill_to": "bb_lowerband",
            },
            "bb_middleband": {"color": "orange"},
            "bb_lowerband": {"color": "orange"},
            "sma_short": {"color": "blue"},
            "sma_long": {"color": "yellow"},
        },
        "subplots": {
            # Subplots - each dict defines one additional plot
            "RSI": {
                f"rsi_{rsi.value}": {"color": "red"},
            },
            "BB_width": {
                "bb_width": {"color": "orange"},
            },
            "BB_percent": {
                "bb_percent": {"color": "blue"},
            },
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Generate all indicators used by the strategy"""

        # RSI
        dataframe[f"rsi_{self.rsi.value}"] = pta.rsi(
            dataframe["close"], length=self.rsi.value
        )

        # Bollinger Bands
        # bollinger = qtpylib.bollinger_bands(
        #     qtpylib.typical_price(dataframe), window=20, stds=2
        # )
        # dataframe["bb_lowerband"] = bollinger["lower"]
        # dataframe["bb_middleband"] = bollinger["mid"]
        # dataframe["bb_upperband"] = bollinger["upper"]
        # dataframe["bb_percent"] = (dataframe["close"] - dataframe["bb_lowerband"]) / (
        #     dataframe["bb_upperband"] - dataframe["bb_lowerband"]
        # )
        # dataframe["bb_width"] = (
        #     dataframe["bb_upperband"] - dataframe["bb_lowerband"]
        # ) / dataframe["bb_middleband"]

        # SMA
        dataframe[f"sma_short"] = pta.sma(
            dataframe["close"], length=self.sma_short.value
        )
        dataframe[f"sma_long"] = pta.sma(dataframe["close"], length=self.sma_long.value)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions_long = []

        conditions_long.append(
            qtpylib.crossed_above(dataframe["sma_short"], dataframe["sma_long"])
        )

        # Check that volume is not 0
        conditions_long.append(dataframe["volume"] > 0)

        if conditions_long:
            dataframe.loc[reduce(lambda x, y: x & y, conditions_long), "enter_long"] = 1

        # -----------short----------------
        conditions_short = []

        conditions_short.append(
            qtpylib.crossed_above(dataframe["sma_long"], dataframe["sma_short"])
        )
        # Check that volume is not 0
        conditions_short.append(dataframe["volume"] > 0)

        if conditions_short:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions_short), "enter_short"
            ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions_long = []

        conditions_long.append(
            qtpylib.crossed_above(dataframe["sma_long"], dataframe["sma_short"])
        )
        # Check that volume is not 0
        conditions_long.append(dataframe["volume"] > 0)

        if conditions_long:
            dataframe.loc[reduce(lambda x, y: x & y, conditions_long), "exit_long"] = 1

        # -----------short----------------
        conditions_short = []

        conditions_short.append(
            qtpylib.crossed_above(dataframe["sma_short"], dataframe["sma_long"])
        )
        # Check that volume is not 0
        conditions_short.append(dataframe["volume"] > 0)

        if conditions_short:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions_short), "exit_short"
            ] = 1

        return dataframe
