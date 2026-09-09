from __future__ import annotations

from unittest.mock import AsyncMock, patch

import polars as pl
import pytest

from hermes.features.country_risk_features.pipeline import pipeline


class TestPipeline:
    @pytest.fixture
    def mock_eco(self):
        mock = AsyncMock()
        mock.gdp_growth_yoy.return_value = 2.5
        mock.gdp_growth_qoq.return_value = 0.6
        mock.industrial_production_yoy.return_value = 3.1
        mock.inflation_cpi_yoy.return_value = 2.0
        mock.inflation_volatility_12m.return_value = 0.5
        mock.ppi_yoy.return_value = 1.8
        mock.unemployment_rate.return_value = 4.0
        mock.youth_unemployment.return_value = 8.0
        mock.labor_force_participation.return_value = 62.0
        mock.current_account_gdp_ratio.return_value = -3.0
        mock.fx_reserves_months_import.return_value = 6.0
        mock.external_debt_gdp_ratio.return_value = 35.0
        mock.fiscal_deficit_gdp.return_value = -2.0
        mock.government_debt_gdp.return_value = 120.0
        mock.reer_misalignment.return_value = 50
        mock.inflation_yoy.return_value = 2.1
        mock.banking_sector_health.return_value = 0.85
        mock.gdp_per_capita_ppp.return_value = 65000
        return mock

    @pytest.fixture
    def mock_geo(self):
        mock = AsyncMock()
        mock.conflict_event_count_30d.return_value = 5
        mock.conflict_event_count_90d.return_value = 15
        mock.conflict_trend.return_value = "stable"
        mock.goldstein_scale_avg_30d.return_value = -2.0
        mock.goldstein_scale_trend.return_value = 0.5
        mock.battle_deaths_30d.return_value = 10
        mock.battle_deaths_90d.return_value = 30
        mock.protest_event_count_30d.return_value = 20
        mock.protest_violence_level.return_value = 0.3
        mock.diplomatic_event_count_30d.return_value = 8
        mock.diplomatic_intensity_avg.return_value = 4.5
        mock.sanctions_count_active.return_value = 3
        mock.sanctions_new_30d.return_value = 1
        mock.sanctions_sector_coverage.return_value = 0.4
        mock.governance_wgi_composite.return_value = 1.2
        mock.corruption_perception_index.return_value = 67
        mock.rule_of_law_score.return_value = 1.5
        mock.regulatory_quality.return_value = 1.3
        mock.democracy_index.return_value = 0.85
        mock.regime_type.return_value = "democracy"
        mock.press_freedom_score.return_value = 75
        return mock

    @pytest.fixture
    def mock_sec(self):
        mock = AsyncMock()
        mock.military_spending_gdp.return_value = 3.5
        mock.military_spending_growth_yoy.return_value = 2.0
        mock.alliance_strength_score.return_value = 0.9
        mock.arms_imports_12m.return_value = 500
        mock.arms_exports_12m.return_value = 2000
        mock.peacekeeping_troops.return_value = 100
        mock.nato_member.return_value = True
        return mock

    @pytest.fixture
    def mock_soc(self):
        mock = AsyncMock()
        mock.social_stability_index.return_value = 0.75
        mock.human_rights_score.return_value = 0.8
        mock.fragile_state_index.return_value = 30.0
        mock.human_development_index.return_value = 0.92
        mock.gini_coefficient.return_value = 41.0
        mock.poverty_headcount_ratio.return_value = 10.0
        return mock

    @pytest.fixture
    def mock_env(self):
        mock = AsyncMock()
        mock.climate_vulnerability_score.return_value = 0.3
        mock.climate_readiness_score.return_value = 0.8
        mock.natural_disaster_risk.return_value = 0.4
        mock.food_price_index_change_yoy.return_value = 2.5
        mock.energy_dependence_ratio.return_value = 0.2
        mock.water_stress_index.return_value = 0.6
        return mock

    @pytest.fixture
    def pipe(self, mock_eco, mock_env, mock_geo, mock_sec, mock_soc):
        with patch.multiple(
            "hermes.features.country_risk_features.pipeline",
            economic_features=lambda: mock_eco,
            enviromental_features=lambda: mock_env,
            geopolitical_features=lambda os_api=None: mock_geo,
            security_features=lambda: mock_sec,
            social_features=lambda: mock_soc,
        ):
            p = pipeline(os_api="test-key")
            yield p

    async def test_get_country_risk_features_schema(self, pipe):
        result = await pipe.get_country_risk_features("USA")
        assert isinstance(result, dict)
        assert result["country"] == "USA"
        assert "economic" in result
        assert "geopolitical" in result
        assert "security" in result
        assert "social" in result
        assert "environmental" in result
        assert "metadata" in result
        assert result["economic"]["gdp_growth_yoy"] == 2.5
        assert result["geopolitical"]["regime_type"] == "democracy"
        assert result["security"]["nato_member"] is True
        assert result["social"]["human_development_index"] == 0.92
        assert result["environmental"]["climate_vulnerability_score"] == 0.3

    async def test_build_training_panel(self, pipe):
        async def fn(c, mode="ML"):
            return pl.DataFrame({"date": ["2023", "2024"], "value": [2.5, 1.9]})

        fns = [fn]
        result = await pipe.build_training_panel(fns, ["USA"])
        assert isinstance(result, pl.DataFrame)
        assert not result.is_empty()

    async def test_build_training_panel_multiple_countries(self, pipe):
        fns = [
            pipe.eco.gdp_growth_yoy,
            pipe.eco.inflation_cpi_yoy,
        ]
        result = await pipe.build_training_panel(fns, ["USA", "GBR"])
        assert isinstance(result, pl.DataFrame)

    async def test_build_training_panel_no_countries(self, pipe):
        result = await pipe.build_training_panel([], [])
        assert result.is_empty()
