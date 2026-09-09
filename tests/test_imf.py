from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from hermes.connectors.imf import IMF
from hermes.entities.countries import iso3_to_iso2


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


@pytest.fixture
def sample_sdmx_response():
    return {
        "data": {
            "structures": [
                {
                    "dimensions": {
                        "series": [
                            {"id": "FREQ", "values": [{"id": "A", "name": "Annual"}]},
                            {"id": "INDICATOR", "values": [{"id": "PPI.IX.A", "name": "PPI"}]},
                            {"id": "COUNTRY", "values": [{"id": "USA", "name": "United States"}]},
                        ],
                        "observation": [
                            {
                                "id": "TIME_PERIOD",
                                "values": [
                                    {"id": "2023", "name": "2023", "value": "2023"},
                                    {"id": "2022", "name": "2022", "value": "2022"},
                                ],
                            },
                        ],
                    }
                }
            ],
            "dataSets": [
                {
                    "series": {
                        "0:0:0": {
                            "observations": {
                                "0": [110.5],
                                "1": [107.2],
                            }
                        }
                    }
                }
            ],
        }
    }


class TestIso3ToIso2:
    def test_valid(self):
        assert iso3_to_iso2("USA") == "US"

    def test_invalid(self):
        assert iso3_to_iso2("ZZZ") == "Not Found"


class TestIMF:
    async def test_fetch_success(self, sample_sdmx_response):
        imf = IMF(cache=None)
        mock_resp = _mock_aiohttp_response(sample_sdmx_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.imf.connector.aiohttp.ClientSession", return_value=mock_session):
            df = await imf._fetch("USA", "IMF.STA", "PPI", "PPI.IX.A")
            assert not df.is_empty()
            assert df["value"].item(0) == 110.5
            assert df["country"].item(0) == "USA"
            assert df["source"].item(0) == "IMF"

    async def test_fetch_no_series(self):
        imf = IMF(cache=None)
        mock_response = {
            "data": {
                "structures": [
                    {
                        "dimensions": {
                            "series": [],
                            "observation": [{"id": "TIME_PERIOD", "values": []}],
                        }
                    }
                ],
                "dataSets": [{}],
            }
        }
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.imf.connector.aiohttp.ClientSession", return_value=mock_session):
            df = await imf._fetch("USA", "IMF.STA", "PPI", "PPI.IX.A")
            assert df.is_empty()

    async def test_fetch_404(self):
        imf = IMF(cache=None)
        mock_resp = _mock_aiohttp_response({}, status=404)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.imf.connector.aiohttp.ClientSession", return_value=mock_session):
            df = await imf._fetch("USA", "IMF.STA", "BAD", "X")
            assert df.is_empty()

    async def test_fetch_http_error(self):
        imf = IMF(cache=None)
        mock_resp = _mock_aiohttp_response({}, status=500)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.imf.connector.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(aiohttp.ClientResponseError):
                await imf._fetch("USA", "IMF.STA", "PPI", "PPI.IX.A")
