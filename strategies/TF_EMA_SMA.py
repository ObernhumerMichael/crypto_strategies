# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from typing import Dict, Optional, Union, Tuple

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
from functools import reduce


class TF_EMA_SMA(IStrategy):
    """
    This is a strategy template to get you started.
    More information in https://www.freqtrade.io/en/latest/strategy-customization/

    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy

    You must keep:
    - the lib in the section "Do not remove these libs"
    - the methods: populate_indicators, populate_entry_trend, populate_exit_trend
    You should keep:
    - timeframe, minimal_roi, stoploss, trailing_*
    """

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = "1m"

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {"0": 0.025}

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.02
    use_custom_stoploss = False

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = True
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.01  # Disabled / not configured

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    # Strategy parameters
    ema_short = 50
    ema_long = 200
    sma = 24 * 5
    adx_guard = 25
    atr_multiplier = 6
    atr_length = 14

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Optional order time in force.
    order_time_in_force = {"entry": "GTC", "exit": "GTC"}

    @property
    def plot_config(self):
        return {
            # Main plot indicators (Moving averages, ...)
            "main_plot": {
                "ema_short": {"color": "blue"},
                "ema_long": {"color": "yellow"},
                "sma_1h": {"color": "green"},
            },
            "subplots": {
                # Subplots - each dict defines one additional plot
                "ADX": {
                    "adx": {"color": "red"},
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
        The custom stoploss can never be below self.stoploss, which serves as a hard maximum loss.
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

    @informative("1h")
    def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["sma"] = ta.SMA(dataframe, timeperiod=self.sma)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """
        # ATR
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

        # ADX
        dataframe["adx"] = ta.ADX(dataframe)

        # MA
        dataframe[f"ema_short"] = ta.EMA(dataframe, timeperiod=self.ema_short)
        dataframe[f"ema_long"] = ta.EMA(dataframe, timeperiod=self.ema_long)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        conditions = []
        # Trigger
        conditions.append(
            qtpylib.crossed_above(
                dataframe[f"ema_short"],
                dataframe[f"ema_long"],
            )
        )

        # Guard
        conditions.append(dataframe["adx"] > self.adx_guard)

        # Check that volume is not 0
        conditions.append(dataframe["volume"] > 0)
        conditions.append(dataframe["sma_1h"] > 0)

        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with exit columns populated
        """
        conditions = []
        # Trigger
        conditions.append(
            qtpylib.crossed_below(
                dataframe[f"close"],
                dataframe[f"sma_1h"],
            )
        )

        # Check that volume is not 0
        conditions.append(dataframe["volume"] > 0)

        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions), "exit_long"] = 1
        return dataframe
