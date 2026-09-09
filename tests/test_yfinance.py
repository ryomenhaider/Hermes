from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pandas as pd
import pytest

from hermes.connectors.yfinance import Yfinance


class TestYfinance:
    async def test_fetch_eps_estimate(self):
        yf = Yfinance(cache=None)
        mock_df = pd.DataFrame({"avg": [1.50], "high": [1.60], "low": [1.40]})
        mock_ticker = MagicMock()
        mock_ticker.earnings_estimate = mock_df

        with patch("hermes.connectors.yfinance.connector.yf.Ticker", return_value=mock_ticker):
            result = await yf._fetch(endpoint="eps_estimate", symbol="AAPL")
            assert result is not None
            assert "avg" in result

    async def test_fetch_revenue_estimate(self):
        yf = Yfinance(cache=None)
        mock_df = pd.DataFrame({"avg": [90000000000], "high": [95000000000]})
        mock_ticker = MagicMock()
        mock_ticker.revenue_estimate = mock_df

        with patch("hermes.connectors.yfinance.connector.yf.Ticker", return_value=mock_ticker):
            result = await yf._fetch(endpoint="revenue_estimate", symbol="AAPL")
            assert result is not None
            assert "avg" in result

    async def test_fetch_earnings_history(self):
        yf = Yfinance(cache=None)
        mock_df = pd.DataFrame({"surprisePercent": [2.5, -1.0]})
        mock_ticker = MagicMock()
        mock_ticker.earnings_history = mock_df

        with patch("hermes.connectors.yfinance.connector.yf.Ticker", return_value=mock_ticker):
            result = await yf._fetch(endpoint="earnings_history", symbol="AAPL")
            assert result is not None
            assert "surprisePercent" in result

    async def test_fetch_unsupported_endpoint(self):
        yf = Yfinance(cache=None)
        mock_ticker = MagicMock()
        mock_ticker.info = {}

        with patch("hermes.connectors.yfinance.connector.yf.Ticker", return_value=mock_ticker):
            with pytest.raises(ValueError, match="Unsupported endpoint"):
                await yf._fetch(endpoint="bad_endpoint", symbol="AAPL")

    async def test_fetch_none_data_returns_none(self):
        yf = Yfinance(cache=None)
        mock_ticker = MagicMock()
        mock_ticker.earnings_estimate = None

        with patch("hermes.connectors.yfinance.connector.yf.Ticker", return_value=mock_ticker):
            result = await yf._fetch(endpoint="eps_estimate", symbol="AAPL")
            assert result is None

    async def test_fetch_empty_df_returns_none(self):
        yf = Yfinance(cache=None)
        mock_df = pd.DataFrame()
        mock_ticker = MagicMock()
        mock_ticker.earnings_estimate = mock_df

        with patch("hermes.connectors.yfinance.connector.yf.Ticker", return_value=mock_ticker):
            result = await yf._fetch(endpoint="eps_estimate", symbol="AAPL")
            assert result is None

    async def test_fetch_uses_cache(self, tmp_cache):
        yf = Yfinance(cache=tmp_cache)
        mock_df = pd.DataFrame({"avg": [1.50]})
        mock_ticker = MagicMock()
        mock_ticker.earnings_estimate = mock_df

        with patch("hermes.connectors.yfinance.connector.yf.Ticker", return_value=mock_ticker):
            r1 = await yf.fetch(endpoint="eps_estimate", symbol="AAPL")
            r2 = await yf.fetch(endpoint="eps_estimate", symbol="AAPL")
            assert mock_ticker.earnings_estimate is not None
            assert r1 == r2
