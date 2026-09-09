from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from hermes.connectors.fred import FRED


def _mock_aiohttp_response(json_data, status=200):
    mock_resp = AsyncMock()
    mock_resp.status = status
    mock_resp.json = AsyncMock(return_value=json_data)
    mock_resp.raise_for_status = MagicMock()

    if status >= 400:
        mock_resp.raise_for_status.side_effect = aiohttp.ClientResponseError(
            request_info=MagicMock(),
            history=(),
            status=status,
        )
    return mock_resp


def _mock_session(mock_resp):
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    return mock_session


class TestFRED:
    async def test_fetch_success(self):
        fred = FRED(api="test-key", cache=None)
        mock_response = {
            "observations": [
                {
                    "realtime_start": "2024-01-01",
                    "realtime_end": "2024-01-01",
                    "date": "2023-10-01",
                    "value": "27360.863",
                },
                {
                    "realtime_start": "2024-01-01",
                    "realtime_end": "2024-01-01",
                    "date": "2023-07-01",
                    "value": "27061.152",
                },
            ],
            "units": "Billions of Dollars",
        }
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.fred.connector.aiohttp.ClientSession", return_value=mock_session):
            df = await fred._fetch(series_id="GDPC1")
            assert not df.is_empty()
            assert df["value"].item(0) == "27360.863"
            assert df["series_id"].item(0) == "GDPC1"
            assert df["unit"].item(0) == "Billions of Dollars"

    async def test_fetch_404(self):
        fred = FRED(api="test-key", cache=None)
        mock_resp = _mock_aiohttp_response({}, status=404)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.fred.connector.aiohttp.ClientSession", return_value=mock_session):
            result = await fred._fetch(series_id="BAD_SERIES")
            assert result is None

    async def test_fetch_http_error(self):
        fred = FRED(api="test-key", cache=None)
        mock_resp = _mock_aiohttp_response({}, status=500)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.fred.connector.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(aiohttp.ClientResponseError):
                await fred._fetch(series_id="GDPC1")

    async def test_fetch_retry_on_timeout(self):
        fred = FRED(api="test-key", cache=None)
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(side_effect=TimeoutError("timeout"))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("hermes.connectors.fred.connector.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(TimeoutError):
                await fred._fetch(series_id="GDPC1", retries=1)

    async def test_fetch_uses_cache(self, tmp_cache):
        fred = FRED(api="test-key", cache=tmp_cache)
        mock_response = {
            "observations": [
                {
                    "realtime_start": "2024-01-01",
                    "realtime_end": "2024-01-01",
                    "date": "2023-10-01",
                    "value": "27360.863",
                },
            ],
            "units": "Billions of Dollars",
        }
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.fred.connector.aiohttp.ClientSession", return_value=mock_session):
            df1 = await fred.fetch(series_id="GDPC1")
            df2 = await fred.fetch(series_id="GDPC1")
            assert mock_session.get.call_count == 1
            assert not df1.is_empty()
            assert not df2.is_empty()
