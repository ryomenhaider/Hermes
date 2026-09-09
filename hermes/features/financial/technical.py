import math
from datetime import UTC, datetime

import numpy as np
import polars as pl

from hermes.connectors.binance import Binance
from hermes.features.financial.models.technical import TechnicalSnapshot


class TAfeatures:
    def __init__(self):
        self.binance = Binance()

    @staticmethod
    def _safe_div(a, b):
        if b is None or b == 0:
            return float("nan")
        return a / b

    @staticmethod
    def _returns(closes):
        closes = np.asarray(closes, dtype=float)
        return np.log(closes[1:] / closes[:-1])

    @staticmethod
    def _sma(values, period):
        if len(values) < period:
            return float("nan")
        return float(np.mean(values[-period:]))

    @staticmethod
    def _ema(values, period):
        if len(values) < period:
            return float("nan")

        series = pl.Series(values, dtype=pl.Float64)
        return float(series.ewm_mean(span=period, adjust=False)[-1])

    @staticmethod
    def _zscore(values):
        values = np.asarray(values, dtype=float)

        if len(values) < 2:
            return float("nan")

        std = np.std(values, ddof=1)

        if std == 0:
            return 0.0

        return float((values[-1] - np.mean(values)) / std)

    async def ohlcv(self, symbol: str, market: str = "future", interval: str = "1h", limit: int = 250):

        data = await self.binance.fetch(
            mode=market,
            endpoint="ohlcv",
            symbol=symbol,
            interval=interval,
            limit=limit,
        )

        return data

    def calculate_price_features(self, candles):

        opens = np.array([float(x[1]) for x in candles])
        highs = np.array([float(x[2]) for x in candles])
        lows = np.array([float(x[3]) for x in candles])
        closes = np.array([float(x[4]) for x in candles])
        volumes = np.array([float(x[5]) for x in candles])
        quote_volumes = np.array([float(x[7]) for x in candles])

        current_open = opens[-1]
        current_high = highs[-1]
        current_low = lows[-1]
        current_close = closes[-1]
        current_volume = volumes[-1]

        ret_1b = self._safe_div(current_close, closes[-2]) - 1
        ret_5b = self._safe_div(current_close, closes[-6]) - 1
        ret_10b = self._safe_div(current_close, closes[-11]) - 1
        ret_60b = self._safe_div(current_close, closes[-61]) - 1

        ret_open_to_close = self._safe_div(current_close, current_open) - 1

        hl_range = self._safe_div(
            current_high - current_low,
            current_close,
        )

        body_range = self._safe_div(
            abs(current_close - current_open),
            current_close,
        )

        sma20 = self._sma(closes, 20)
        sma50 = self._sma(closes, 50)
        sma200 = self._sma(closes, 200)

        dist_sma_20 = self._safe_div(
            current_close - sma20,
            sma20,
        )

        dist_sma_50 = self._safe_div(
            current_close - sma50,
            sma50,
        )

        dist_sma_200 = self._safe_div(
            current_close - sma200,
            sma200,
        )

        ema9 = self._ema(closes, 9)
        ema21 = self._ema(closes, 21)
        ema50 = self._ema(closes, 50)

        ema_diff_9_21 = self._safe_div(
            ema9 - ema21,
            ema21,
        )

        ema_diff_21_50 = self._safe_div(
            ema21 - ema50,
            ema50,
        )

        log_returns = self._returns(closes)

        vol_20 = float(np.std(log_returns[-20:], ddof=1)) if len(log_returns) >= 20 else float("nan")

        vol_60 = float(np.std(log_returns[-60:], ddof=1)) if len(log_returns) >= 60 else float("nan")

        previous_close = closes[:-1]

        tr = np.maximum(
            highs[1:] - lows[1:],
            np.maximum(
                abs(highs[1:] - previous_close),
                abs(lows[1:] - previous_close),
            ),
        )

        atr14 = float(np.mean(tr[-14:])) if len(tr) >= 14 else float("nan")

        atr_14_norm = self._safe_div(
            atr14,
            current_close,
        )

        avg_volume_20 = np.mean(volumes[-20:]) if len(volumes) >= 20 else float("nan")

        volume_rel_20 = self._safe_div(
            current_volume,
            avg_volume_20,
        )

        taker_buy_volumes = np.array([float(x[9]) for x in candles])

        taker_buy_volume = taker_buy_volumes[-1]

        taker_buy_vol_ratio = self._safe_div(
            taker_buy_volume,
            current_volume,
        )

        return {
            "open": current_open,
            "high": current_high,
            "low": current_low,
            "close": current_close,
            "volume": current_volume,
            "quote_volume": quote_volumes[-1],
            "ret_1b": ret_1b,
            "ret_5b": ret_5b,
            "ret_10b": ret_10b,
            "ret_60b": ret_60b,
            "ret_open_to_close": ret_open_to_close,
            "hl_range": hl_range,
            "body_range": body_range,
            "dist_sma_20": dist_sma_20,
            "dist_sma_50": dist_sma_50,
            "dist_sma_200": dist_sma_200,
            "ema_diff_9_21": ema_diff_9_21,
            "ema_diff_21_50": ema_diff_21_50,
            "vol_20": vol_20,
            "vol_60": vol_60,
            "atr_14_norm": atr_14_norm,
            "volume_rel_20": volume_rel_20,
            "taker_buy_vol_ratio": taker_buy_vol_ratio,
        }

    async def trade_features(
        self,
        symbol: str,
        market: str = "future",
        limit: int = 1000,
    ):

        trades = await self.binance.fetch(
            mode=market,
            endpoint="trades",
            symbol=symbol,
            limit=limit,
        )

        if not trades:
            return {}

        quantities = np.array([float(t["qty"]) for t in trades])

        prices = np.array([float(t["price"]) for t in trades])

        quote_values = prices * quantities

        # Binance:
        # isBuyerMaker=True  -> seller initiated
        # isBuyerMaker=False -> buyer initiated

        buy_mask = np.array([not t["isBuyerMaker"] for t in trades])

        buy_volume = quantities[buy_mask].sum()
        total_volume = quantities.sum()

        threshold = np.percentile(
            quantities,
            95,
        )

        large_volume = quantities[quantities >= threshold].sum()

        return {
            "trades_count": len(trades),
            "trade_window_count": len(trades),
            "trade_window_vol_base": float(quantities.sum()),
            "trade_window_vol_quote": float(quote_values.sum()),
            "trade_buy_vol_ratio": self._safe_div(
                buy_volume,
                total_volume,
            ),
            "avg_trade_size": float(np.mean(quantities)),
            "median_trade_size": float(np.median(quantities)),
            "large_trade_vol_ratio": self._safe_div(
                large_volume,
                total_volume,
            ),
        }

    async def orderbook_features(
        self,
        symbol: str,
        market: str = "future",
        limit: int = 20,
    ):

        book = await self.binance.fetch(
            mode=market,
            endpoint="order_book",
            symbol=symbol,
            limit=limit,
        )

        bids = book["bids"]
        asks = book["asks"]

        bid_price = float(bids[0][0])
        bid_qty = float(bids[0][1])

        ask_price = float(asks[0][0])
        ask_qty = float(asks[0][1])

        spread_abs = ask_price - bid_price

        mid = (ask_price + bid_price) / 2

        spread_bps = (
            self._safe_div(
                spread_abs,
                mid,
            )
            * 10_000
        )

        top_book_imbalance = self._safe_div(
            bid_qty - ask_qty,
            bid_qty + ask_qty,
        )

        depth_bid_total = sum(float(x[1]) for x in bids)

        depth_ask_total = sum(float(x[1]) for x in asks)

        depth_imbalance = self._safe_div(
            depth_bid_total - depth_ask_total,
            depth_bid_total + depth_ask_total,
        )

        return {
            "bid_price": bid_price,
            "ask_price": ask_price,
            "bid_qty": bid_qty,
            "ask_qty": ask_qty,
            "spread_abs": spread_abs,
            "spread_bps": spread_bps,
            "top_book_imbalance": top_book_imbalance,
            "depth_bid_total": depth_bid_total,
            "depth_ask_total": depth_ask_total,
            "depth_imbalance": depth_imbalance,
        }

    async def day_features(
        self,
        symbol: str,
        market: str = "future",
    ):

        data = await self.binance.fetch(
            mode=market,
            endpoint="24hr",
            symbol=symbol,
        )

        high = float(data["highPrice"])
        low = float(data["lowPrice"])
        last = float(data["lastPrice"])

        range_24h = self._safe_div(
            high - low,
            last,
        )

        pos_in_range = self._safe_div(
            last - low,
            high - low,
        )

        return {
            "high_24h": high,
            "low_24h": low,
            "last_price_24h": last,
            "range_24h": range_24h,
            "pct_change_24h": float(data["priceChangePercent"]) / 100,
            "pos_in_24h_range": pos_in_range,
            "volume_24h": float(data["volume"]),
            "quote_volume_24h": float(data["quoteVolume"]),
        }

    async def funding_features(
        self,
        symbol: str,
        market: str = "future",
        limit: int = 30,
    ):

        data = await self.binance.fetch(
            mode=market,
            endpoint="fundingRate",
            symbol=symbol,
            limit=limit,
        )

        if not data:
            return {}

        rates = np.array([float(x["fundingRate"]) for x in data])

        current = rates[-1]

        lag_3 = rates[-4] if len(rates) >= 4 else float("nan")

        previous = rates[-2] if len(rates) >= 2 else float("nan")

        change = current - previous if not math.isnan(previous) else float("nan")

        zscore = self._zscore(rates)

        return {
            "funding_rate": current,
            "funding_rate_lag_3": lag_3,
            "funding_rate_change": change,
            "funding_rate_zscore": zscore,
        }

    async def oi_features(
        self,
        symbol: str,
        market: str = "future",
    ):

        current = await self.binance.fetch(
            mode=market,
            endpoint="openInterest",
            symbol=symbol,
        )

        oi = float(current["openInterest"])

        history = await self.binance.fetch(
            mode=market,
            endpoint="openInterestHist",
            symbol=symbol,
            period="1h",
            limit=25,
        )

        if not history:
            return {
                "open_interest": oi,
            }

        values = np.array([float(x["sumOpenInterest"]) for x in history])

        oi_1h = values[-2] if len(values) >= 2 else float("nan")
        oi_24h = values[0] if len(values) >= 25 else float("nan")

        oi_change_1h = self._safe_div(oi - oi_1h, oi_1h) if not math.isnan(oi_1h) else float("nan")

        oi_change_24h = self._safe_div(oi - oi_24h, oi_24h) if not math.isnan(oi_24h) else float("nan")

        return {
            "open_interest": oi,
            "oi_change_1h": oi_change_1h,
            "oi_change_24h": oi_change_24h,
        }

    async def funding_time(
        self,
        symbol: str,
    ):

        data = await self.binance.fetch(
            mode="future",
            endpoint="premiumIndex",
            symbol=symbol,
        )

        next_funding = int(data["nextFundingTime"])

        now = int(datetime.now(UTC).timestamp() * 1000)

        return {"time_to_next_funding_min": max(0, (next_funding - now) / 60_000)}

    async def positioning_features(
        self,
        symbol: str,
        period: str = "1h",
        limit: int = 30,
    ):

        long_short = await self.binance.fetch(
            mode="future",
            endpoint="longShortRatio",
            symbol=symbol,
            period=period,
            limit=limit,
        )

        top_accounts = await self.binance.fetch(
            mode="future",
            endpoint="topLongShortAccountRatio",
            symbol=symbol,
            period=period,
            limit=limit,
        )

        top_positions = await self.binance.fetch(
            mode="future",
            endpoint="topLongShortPositionRatio",
            symbol=symbol,
            period=period,
            limit=limit,
        )

        ls_ratio = float(long_short[-1]["longShortRatio"]) if long_short else float("nan")

        top_acct_ratio = float(top_accounts[-1]["longShortRatio"]) if top_accounts else float("nan")

        top_pos_ratio = float(top_positions[-1]["longShortRatio"]) if top_positions else float("nan")

        return {
            "trend_score": ls_ratio - 1.0,
            "mean_reversion_score": (1.0 - abs(ls_ratio - 1.0)),
            "liquidity_score": self._safe_div(
                1.0,
                1.0 + abs(top_pos_ratio - 1.0),
            ),
            "order_flow_score": self._safe_div(
                top_pos_ratio - 1.0,
                1.0,
            ),
            "sentiment_score": self._safe_div(
                ls_ratio + top_acct_ratio + top_pos_ratio,
                3.0,
            )
            - 1.0,
        }

    async def build_snapshot(
        self,
        symbol: str,
        market: str = "future",
        interval: str = "1h",
    ):

        candles = await self.ohlcv(
            symbol=symbol,
            market=market,
            interval=interval,
            limit=250,
        )

        price = self.calculate_price_features(candles)

        trades = await self.trade_features(
            symbol=symbol,
            market=market,
        )

        orderbook = await self.orderbook_features(
            symbol=symbol,
            market=market,
        )

        day = await self.day_features(
            symbol=symbol,
            market=market,
        )

        funding = await self.funding_features(
            symbol=symbol,
            market=market,
        )

        oi = await self.oi_features(
            symbol=symbol,
            market=market,
        )

        funding_time = await self.funding_time(
            symbol=symbol,
        )

        positioning = await self.positioning_features(
            symbol=symbol,
        )

        return TechnicalSnapshot(
            symbol=symbol,
            timestamp_ms=int(candles[-1][0]),
            **price,
            **trades,
            **orderbook,
            **day,
            **funding,
            **oi,
            **funding_time,
            **positioning,
            oi_to_volume_24h=self._safe_div(
                oi.get("open_interest", 0.0),
                day.get("quote_volume_24h", 0.0),
            ),
        )

    async def get_technical(
        self,
        symbol: str,
        market: str = "future",
        interval: str = "1h",
    ):

        return await self.build_snapshot(
            symbol=symbol,
            market=market,
            interval=interval,
        )
