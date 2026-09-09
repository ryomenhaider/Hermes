import logging

import numpy as np
import polars as pl

from hermes.connectors.finnhub import FINNHUB
from hermes.connectors.sec import SECEDGAR
from hermes.connectors.sec.tags import SEC_TAG_MAP
from hermes.connectors.yfinance import Yfinance

logger = logging.getLogger(__name__)


def _to_float(value: object) -> float:
    return float(value)  # type: ignore


def _extract_periods(facts: dict, quarters: int) -> list[dict]:
    seen_periods: set[tuple[int, str]] = set()
    rows: list[dict] = []

    for field, tags in SEC_TAG_MAP.items():
        for tag in tags:
            if tag not in facts:
                continue
            tag_data = facts[tag]
            units = tag_data.get("units", {})
            for unit_type, entries in units.items():
                for entry in entries:
                    fy = entry.get("fy")
                    fp = entry.get("fp")
                    if fy is None or fp is None:
                        continue
                    period_key = (fy, fp)
                    if period_key in seen_periods:
                        continue
                    seen_periods.add(period_key)
                    rows.append(
                        {
                            "fiscal_year": fy,
                            "fiscal_period": fp,
                            "filing_date": entry.get("filed"),
                            "filing_type": entry.get("form"),
                        }
                    )
                break
            if rows:
                break
        if rows:
            break

    rows.sort(key=lambda r: (r["fiscal_year"], r["fiscal_period"]), reverse=True)
    return rows[:quarters]


def _extract_funds_per_period(facts: dict, periods: list[dict], symbol: str) -> list[dict]:
    result_rows: list[dict] = []

    for period in periods:
        period_facts: dict[str, object] = {}
        for field, tags in SEC_TAG_MAP.items():
            period_facts[field] = None
            for tag in tags:
                if tag not in facts:
                    continue
                tag_data = facts[tag]
                units = tag_data.get("units", {})
                for unit_type, entries in units.items():
                    for entry in entries:
                        if entry.get("fy") == period["fiscal_year"] and entry.get("fp") == period["fiscal_period"]:
                            period_facts[field] = entry.get("val")
                            break
                    if period_facts[field] is not None:
                        break
                if period_facts[field] is not None:
                    break

        r = period_facts.get("revenue")
        cor = period_facts.get("cost_of_revenue")
        oi = period_facts.get("operating_income")
        gp = period_facts.get("gross_profit")

        if gp is None and r is not None and cor is not None:
            try:
                period_facts["gross_profit"] = _to_float(r) - _to_float(cor)
            except (TypeError, ValueError):
                pass

        gp = period_facts.get("gross_profit")
        if period_facts.get("operating_expenses") is None and gp is not None and oi is not None:
            try:
                period_facts["operating_expenses"] = _to_float(gp) - _to_float(oi)
            except (TypeError, ValueError):
                pass

        result_rows.append(
            {
                "ticker": symbol,
                "filing_date": period["filing_date"],
                "fiscal_period": period["fiscal_period"],
                "fiscal_year": period["fiscal_year"],
                "filing_type": period["filing_type"],
                **period_facts,
            }
        )

    return result_rows


class CompanyFiling:
    def __init__(
        self,
        finnhub_api: str,
        sec_email: str,
        sec_username: str,
        fred_api: str,
    ):
        self.finn = FINNHUB(api=finnhub_api)
        self.sec = SECEDGAR(username=sec_username, email=sec_email)
        self.yf = Yfinance()

    async def get_candle_history(
        self,
        symbol: str,
        interval: str = "1d",
        years: int = 2,
    ) -> pl.DataFrame:
        from hermes.constants import FINNHUB_RESOLUTION_MAP, SUPPORTED_STOCK_FREQS

        if interval not in SUPPORTED_STOCK_FREQS:
            raise ValueError(f"Interval {interval!r} not supported for stocks. Supported: {SUPPORTED_STOCK_FREQS}")

        resolution = FINNHUB_RESOLUTION_MAP[interval]

        df_finn = await self.finn.fetch_candles_history(
            symbol=symbol,
            resolution=resolution,
            years=years,
        )

        if not df_finn.is_empty() and len(df_finn) > 100:
            df_finn = df_finn.with_columns(pl.lit(symbol).alias("symbol"), pl.lit(interval).alias("interval"))
            return df_finn

        logger.info(f"Finnhub returned {len(df_finn)} rows for {symbol}, falling back to yfinance")

        df_yf = await self.yf.fetch_history(
            symbol=symbol,
            interval=interval,
            years=years,
        )

        if not df_yf.is_empty():
            df_yf = df_yf.with_columns(pl.lit(symbol).alias("symbol"), pl.lit(interval).alias("interval"))

        return df_yf

    async def get_history(
        self,
        quarters: int = 8,
        symbols: list[str] | None = None,
    ) -> pl.DataFrame:
        from hermes.constants import TICKERS

        symbols = symbols or TICKERS
        all_dfs: list[pl.DataFrame] = []

        for symbol in symbols:
            try:
                raw = await self.sec.fetch(symbol=symbol)
            except Exception:
                logger.warning(f"Failed to fetch SEC data for {symbol}")
                continue

            if raw is None or not isinstance(raw, dict) or "facts" not in raw:
                continue

            facts = raw["facts"].get("us-gaap")
            if not facts:
                continue

            periods = _extract_periods(facts, quarters)
            if not periods:
                continue

            rows = _extract_funds_per_period(facts, periods, symbol)
            if rows:
                df_sym = pl.DataFrame(rows)
                df_sym = CompanyFiling._compute_fundamental_features(df_sym)
                all_dfs.append(df_sym)

        if not all_dfs:
            return pl.DataFrame()

        return pl.concat(all_dfs)

    @staticmethod
    def _compute_fundamental_features(df: pl.DataFrame) -> pl.DataFrame:
        if df.is_empty() or df.height < 2:
            return df

        df = df.sort(["fiscal_year", "fiscal_period"])
        df = df.with_row_index("_row_idx")
        df = df.with_columns((pl.col("fiscal_year") - 1).alias("_key"))

        prev = df.select(
            pl.col("fiscal_year"),
            pl.col("fiscal_period"),
            pl.col("_row_idx").alias("_prev_idx"),
        )
        df = df.join(
            prev,
            left_on=["_key", "fiscal_period"],
            right_on=["fiscal_year", "fiscal_period"],
            how="left",
        )

        def _safe_div(a: pl.Expr, b: pl.Expr) -> pl.Expr:
            return pl.when(b > 0).then(a / b).otherwise(np.nan)

        def _yoy(col_expr: pl.Expr) -> pl.Expr:
            current = col_expr
            prev_val = current.gather(pl.col("_prev_idx"))
            return (
                pl.when(pl.col("_prev_idx").is_not_null() & prev_val.is_not_null() & (prev_val != 0))
                .then((current - prev_val) / prev_val.abs())
                .otherwise(np.nan)
            )

        r = pl.col("revenue").cast(pl.Float64)
        gp = pl.col("gross_profit").cast(pl.Float64)
        oi = pl.col("operating_income").cast(pl.Float64)
        ni = pl.col("net_income").cast(pl.Float64)
        ocf = pl.col("operating_cash_flow").cast(pl.Float64)
        ca = pl.col("current_assets").cast(pl.Float64)
        cl = pl.col("current_liabilities").cast(pl.Float64)
        ta = pl.col("total_assets").cast(pl.Float64)
        eq = pl.col("equity").cast(pl.Float64)
        cash = pl.col("cash").cast(pl.Float64)
        inv = pl.col("inventory").cast(pl.Float64)
        ar = pl.col("accounts_receivable").cast(pl.Float64)
        ltd = pl.col("long_term_debt").cast(pl.Float64)
        std_ = pl.col("short_term_debt").cast(pl.Float64)
        capex = pl.col("capital_expenditure").cast(pl.Float64)
        ie = pl.col("interest_expense").cast(pl.Float64).fill_null(0)
        eps_d = pl.col("eps_diluted").cast(pl.Float64)
        shares = pl.col("shares_outstanding").cast(pl.Float64)
        divs = pl.col("dividends").cast(pl.Float64).fill_null(0)
        bbs = pl.col("buybacks").cast(pl.Float64).fill_null(0)
        total_debt = std_ + ltd
        net_debt = total_debt - cash
        fcf = ocf - capex
        working_capital = ca - cl

        out = df.with_columns(
            [
                _yoy(r).alias("revenue_growth_yoy"),
                _yoy(gp).alias("gross_profit_growth_yoy"),
                _yoy(oi).alias("operating_income_growth_yoy"),
                _yoy(ni).alias("net_income_growth_yoy"),
                _yoy(eps_d).alias("eps_growth_yoy"),
                _yoy(ocf).alias("operating_cash_flow_growth_yoy"),
                _safe_div(gp, r).alias("gross_margin"),
                _safe_div(oi, r).alias("operating_margin"),
                _safe_div(ni, r).alias("net_margin"),
                _safe_div(ocf, r).alias("ocf_margin"),
                _safe_div(ca, cl).alias("current_ratio"),
                _safe_div(ca - inv, cl).alias("quick_ratio"),
                _safe_div(cash, cl).alias("cash_ratio"),
                _safe_div(cash, ta).alias("cash_to_assets"),
                _safe_div(total_debt, eq).alias("debt_to_equity"),
                _safe_div(total_debt, ta).alias("debt_to_assets"),
                _safe_div(total_debt, total_debt + eq).alias("debt_to_capital"),
                net_debt.alias("net_debt"),
                _safe_div(total_debt - cash, eq).alias("net_debt_to_equity"),
                _yoy(total_debt).alias("debt_growth_yoy"),
                _safe_div(std_, total_debt).alias("short_term_debt_ratio"),
                _safe_div(ltd, total_debt).alias("long_term_debt_ratio"),
                fcf.alias("free_cash_flow"),
                _safe_div(fcf, r).alias("fcf_margin"),
                _safe_div(capex, r).alias("capex_to_revenue"),
                _safe_div(ocf, ni).alias("ocf_to_net_income"),
                _safe_div(ar, r).alias("receivables_to_revenue"),
                _safe_div(inv, r).alias("inventory_to_revenue"),
                _yoy(ar).alias("receivables_growth_yoy"),
                _yoy(inv).alias("inventory_growth_yoy"),
                working_capital.alias("working_capital"),
                _safe_div(ca - cl, r).alias("working_capital_to_revenue"),
                _yoy(ta).alias("asset_growth_yoy"),
                _yoy(eq).alias("equity_growth_yoy"),
                _yoy(cash).alias("cash_growth_yoy"),
                _yoy(capex).alias("capex_growth_yoy"),
                _yoy(fcf).alias("free_cash_flow_growth_yoy"),
                _yoy(shares).alias("share_count_change_yoy"),
                _yoy(bbs).alias("buyback_change_yoy"),
                _yoy(divs).alias("dividend_change_yoy"),
                _safe_div(bbs, ni).alias("buyback_to_net_income"),
                _safe_div(divs, ni).alias("dividend_to_net_income"),
                _safe_div(oi, ie).alias("interest_coverage"),
            ]
        )

        out = out.drop([c for c in ["_row_idx", "_prev_idx", "_key"] if c in out.columns])

        return out
