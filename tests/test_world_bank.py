from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from hermes.connectors.world_bank import World_bank


def _mock_aiohttp_response(json_data, status=200):
    """Create a mock aiohttp response."""
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
    """Create a mock aiohttp ClientSession that returns the given response."""
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    return mock_session


class TestWorldBank:
    async def test_fetch_success(self):
        wb = World_bank(cache=None)
        mock_response = [
            {"page": 1, "pages": 1, "per_page": 1000, "total": 1},
            [
                {
                    "indicator": {"id": "NY.GDP.MKTP.KD.ZG", "value": "GDP growth"},
                    "countryiso3code": "USA",
                    "date": "2023",
                    "value": 2.5,
                }
            ],
        ]
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.world_bank.connector.aiohttp.ClientSession", return_value=mock_session):
            df = await wb._fetch("USA", "NY.GDP.MKTP.KD.ZG")
            assert not df.is_empty()
            assert df["value"].item(0) == 2.5
            assert df["country"].item(0) == "USA"
            assert df["source"].item(0) == "World_Bank"

    async def test_fetch_no_data(self):
        wb = World_bank(cache=None)
        mock_response = [{"page": 1, "pages": 1}, []]
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.world_bank.connector.aiohttp.ClientSession", return_value=mock_session):
            df = await wb._fetch("XYZ", "SOME.IND")
            assert df.is_empty()

    async def test_fetch_http_error(self):
        wb = World_bank(cache=None)
        mock_resp = _mock_aiohttp_response({}, status=404)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.world_bank.connector.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(aiohttp.ClientResponseError):
                await wb._fetch("USA", "BAD")

    async def test_fetch_retry_on_timeout(self):
        wb = World_bank(cache=None)
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(side_effect=aiohttp.ClientError("timeout"))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("hermes.connectors.world_bank.connector.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(aiohttp.ClientError):
                await wb._fetch("USA", "NY.GDP.MKTP.KD.ZG", retries=1)

    async def test_public_fetch_uses_cache(self, tmp_cache):
        wb = World_bank(cache=tmp_cache)
        mock_response = [
            {"page": 1, "pages": 1, "per_page": 1000, "total": 1},
            [
                {
                    "indicator": {"id": "GDP.PROT", "value": "Test"},
                    "countryiso3code": "USA",
                    "date": "2023",
                    "value": 3.0,
                }
            ],
        ]
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.world_bank.connector.aiohttp.ClientSession", return_value=mock_session):
            df1 = await wb.fetch("USA", "GDP.PROT")
            df2 = await wb.fetch("USA", "GDP.PROT")
            assert mock_session.get.call_count == 1
            assert not df1.is_empty()
            assert not df2.is_empty()
