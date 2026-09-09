from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import numpy as np
import polars as pl
import pytest

from hermes.entities.countries import check_iso3, iso3_to_iso2
from hermes.features.country_risk_features.economic import economic_features
from hermes.features.country_risk_features.utils import adjust_year_range, check_empty, empty_result


class TestHelpers:
    def test_check_iso3_valid(self):
        check_iso3("USA")

    def test_check_iso3_invalid(self):
        with pytest.raises(RuntimeError, match="not iso3"):
            check_iso3("ZZZ")

    def test_empty_result_F(self):
        assert np.isnan(empty_result("F"))

    def test_empty_result_ML(self):
        result = empty_result("ML")
        assert isinstance(result, pl.Series)
        assert result.dtype == pl.Float64

    def test_check_empty_F(self):
        data = pl.DataFrame({"value": [1.0]})
        result = check_empty("F", data, "USA")
        assert not result.is_empty()

    def test_check_empty_empty(self):
        data = pl.DataFrame()
        result = check_empty("F", data, "USA")
        assert np.isnan(result)

    def test_adjust_year_range_fills_missing_years(self):
        df = pl.DataFrame({"year": [2020, 2022], "value": [1.0, 3.0]})
        result = adjust_year_range(df, "year", 2020, 2022)
        assert list(result["year"]) == [2020, 2021, 2022]
        assert result["value"].null_count() == 1

    def test_adjust_year_range_filters_outside_range(self):
        df = pl.DataFrame({"year": [2019, 2020, 2021, 2022], "value": [0.0, 1.0, 2.0, 3.0]})
        result = adjust_year_range(df, "year", 2020, 2021)
        assert list(result["year"]) == [2020, 2021]

    def test_adjust_year_range_fill_value(self):
        df = pl.DataFrame({"year": [2020, 2022], "value": [1.0, 3.0]})
        result = adjust_year_range(df, "year", 2020, 2022, fill_method="value", fill_value=0)
        assert result["value"].to_list() == [1.0, 0.0, 3.0]

    def test_adjust_year_range_fill_ffill(self):
        df = pl.DataFrame({"year": [2020, 2022], "value": [1.0, 3.0]})
        result = adjust_year_range(df, "year", 2020, 2022, fill_method="ffill")
        assert result["value"].to_list() == [1.0, 1.0, 3.0]

    def test_adjust_year_range_fill_bfill(self):
        df = pl.DataFrame({"year": [2020, 2022], "value": [1.0, 3.0]})
        result = adjust_year_range(df, "year", 2020, 2022, fill_method="bfill")
        assert result["value"].to_list() == [1.0, 3.0, 3.0]

    def test_adjust_year_range_fill_linear(self):
        df = pl.DataFrame({"year": [2020, 2022], "value": [1.0, 3.0]})
        result = adjust_year_range(df, "year", 2020, 2022, fill_method="linear")
        assert result["value"].to_list() == [1.0, 2.0, 3.0]


class TestEconomicFeatures:
    @pytest.fixture
    def eco(self):
        return economic_features()

    @pytest.fixture
    def mock_wb(self, eco, sample_wb_df):
        eco.wb = MagicMock()
        eco.wb.fetch = AsyncMock(return_value=sample_wb_df)
        return eco.wb

    @pytest.fixture
    def mock_wb_cpi(self, eco, sample_wb_cpi_df):
        eco.wb = MagicMock()
        eco.wb.fetch = AsyncMock(return_value=sample_wb_cpi_df)
        return eco.wb

    @pytest.fixture
    def mock_imf(self, eco, sample_imf_df):
        eco.imf = MagicMock()
        eco.imf.fetch = AsyncMock(return_value=sample_imf_df)
        return eco.imf

    async def test_gdp_growth_yoy_F(self, eco, mock_wb):
        result = await eco.gdp_growth_yoy("USA", mode="F")
        assert result == 2.5

    async def test_gdp_growth_yoy_ML(self, eco):
        eco.wb = MagicMock()
        eco.wb.fetch = AsyncMock(
            return_value=pl.DataFrame({"date": ["2021", "2022", "2023"], "value": [5.8, 1.9, 2.5]})
        )
        result = await eco.gdp_growth_yoy("USA", mode="ML")
        assert isinstance(result, pl.DataFrame)

    async def test_gdp_growth_yoy_empty(self, eco):
        eco.wb = MagicMock()
        eco.wb.fetch = AsyncMock(return_value=pl.DataFrame())
        val = await eco.gdp_growth_yoy("USA", mode="F")
        assert np.isnan(val)

    async def test_gdp_growth_qoq_F(self, eco, mock_wb):
        val = await eco.gdp_growth_qoq("USA", mode="F")
        assert isinstance(val, float)

    async def test_gdp_growth_qoq_empty(self, eco):
        eco.wb = MagicMock()
        eco.wb.fetch = AsyncMock(return_value=pl.DataFrame())
        val = await eco.gdp_growth_qoq("USA", mode="F")
        assert np.isnan(val)

    async def test_industrial_production_yoy_F(self, eco, mock_wb):
        val = await eco.industrial_production_yoy("USA", mode="F")
        assert val == 2.5

    async def test_industrial_production_yoy_empty_F(self, eco):
        eco.wb = MagicMock()
        eco.wb.fetch = AsyncMock(return_value=pl.DataFrame())
        val = await eco.industrial_production_yoy("USA", mode="F")
        assert np.isnan(val)

    async def test_inflation_cpi_yoy_F(self, eco, mock_wb):
        val = await eco.inflation_cpi_yoy("USA", mode="F")
        assert val == 2.5

    async def test_inflation_volatility_12m_F(self, eco, mock_wb_cpi):
        val = await eco.inflation_volatility_12m("USA", mode="F")
        assert isinstance(val, float)

    async def test_inflation_volatility_12m_empty(self, eco):
        eco.wb = MagicMock()
        eco.wb.fetch = AsyncMock(return_value=pl.DataFrame())
        val = await eco.inflation_volatility_12m("USA", mode="F")
        assert np.isnan(val)

    async def test_ppi_yoy_F(self, eco, mock_imf):
        val = await eco.ppi_yoy("USA", mode="F")
        assert val == 110.0

    async def test_inflation_yoy_F(self, eco, mock_imf):
        val = await eco.inflation_yoy("USA", mode="F")
        assert val == 110.0

    async def test_unemployment_rate_F(self, eco, mock_wb):
        val = await eco.unemployment_rate("USA", mode="F")
        assert val == 2.5

    async def test_youth_unemployment_F(self, eco, mock_wb):
        val = await eco.youth_unemployment("USA", mode="F")
        assert val == 2.5

    async def test_labor_force_participation_F(self, eco, mock_wb):
        val = await eco.labor_force_participation("USA", mode="F")
        assert val == 2.5

    async def test_current_account_gdp_ratio_F(self, eco, mock_wb):
        val = await eco.current_account_gdp_ratio("USA", mode="F")
        assert val == 2.5

    async def test_fx_reserves_months_import_F(self, eco, mock_wb):
        val = await eco.fx_reserves_months_import("USA", mode="F")
        assert val == 2.5

    async def test_external_debt_gdp_ratio_F(self, eco, mock_wb):
        val = await eco.external_debt_gdp_ratio("USA", mode="F")
        assert val == 2.5

    async def test_fiscal_deficit_gdp_F(self, eco, mock_imf):
        val = await eco.fiscal_deficit_gdp("USA", mode="F")
        assert val == 110.0

    async def test_government_debt_gdp_F(self, eco, mock_imf):
        val = await eco.government_debt_gdp("USA", mode="F")
        assert val == 110.0

    async def test_reer_misalignment_F(self, eco, mock_imf):
        val = await eco.reer_misalignment("USA", mode="F")
        assert val == 110.0

    async def test_banking_sector_health_F(self, eco, mock_wb):
        val = await eco.banking_sector_health("USA", mode="F")
        assert val == 2.5

    async def test_gdp_per_capita_ppp_F(self, eco, mock_wb):
        val = await eco.gdp_per_capita_ppp("USA", mode="F")
        assert val == 2.5
