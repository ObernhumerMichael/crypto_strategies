class Strategy(IStrategy):
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

    # Backup Stoploss (should not be set too small)
    # This attribute will be overridden with custom_stoploss in runtime when entering a trade
    stoploss = -0.5
    # MUST BE SET TO TRUE otherwise the custom_stoploss will be ignored
    use_custom_stoploss = True

    # Trailing stoploss
    trailing_stop = False

    # Indicators
    atr_multiplier = 6
    atr_length = 14

    order_types = {
        "stoploss_on_exchange": True,
    }

    @property
    def plot_config(self):
        return {
            # Main plot indicators (Moving averages, ...)
            "main_plot": {},
            "subplots": {
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
