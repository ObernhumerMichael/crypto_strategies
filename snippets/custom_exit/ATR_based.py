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

    # Indicators
    atr_multiplier = 6
    atr_length = 14

    @property
    def plot_config(self):
        return {
            # Main plot indicators (Moving averages, ...)
            "main_plot": {},
            "subplots": {
                "Percent": {
                    "roi_percent": {"color": "green"},
                },
            },
        }

    # Takes a muliple of the ATR at the beginning of the trade and uses it as the ROI
    def custom_exit(
        self,
        pair: str,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        **kwargs,
    ):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        trade_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)
        trade_candle = dataframe.loc[dataframe["date"] == trade_date].squeeze()
        roi_percent = trade_candle["roi_percent"]

        if current_profit >= roi_percent:
            return "custom_roi_exit"

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe[f"atr"] = pta.atr(
            high=dataframe["high"],
            low=dataframe["low"],
            close=dataframe["close"],
            length=self.atr_length,
            mamode="sma",
        )

        dataframe[f"roi_percent"] = (
            dataframe["atr"] / dataframe["close"] * self.atr_multiplier
        )
        return dataframe
