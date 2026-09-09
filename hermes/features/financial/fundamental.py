from hermes.connectors.finnhub import FINNHUB
from hermes.connectors.fred import FRED
from hermes.connectors.sec import SECEDGAR
from hermes.connectors.sec.tags import SEC_TAG_MAP
from hermes.connectors.yfinance import Yfinance
from hermes.features.financial.models.fundamental import CompanyFundamental


class FAfeatures:
    def __init__(
        self,
        finnhub_api: str,
        sec_email: str,
        sec_username: str,
        fred_api: str,
    ):
        self.finn_api = finnhub_api
        self.sec_email = sec_email
        self.sec_username = sec_username
        self.finn: FINNHUB = FINNHUB(api=finnhub_api)
        self.sec: SECEDGAR = SECEDGAR(username=sec_username, email=sec_email)
        self.fred: FRED = FRED(api=fred_api)
        self._yf = Yfinance()

    def extract_funds_sec(self, data: dict) -> dict:
        facts = data["facts"]["us-gaap"]
        result: dict[str, object] = {}

        for field, tags in SEC_TAG_MAP.items():
            result[field] = None

            for tag in tags:
                if tag in facts:
                    tag_data = facts[tag]
                    units = tag_data.get("units", {})
                    for unit_type, entries in units.items():
                        if entries:
                            result[field] = entries[-1].get("val")
                            break
                    break

        return result

    def extract_filing_meta(self, data: dict) -> dict:
        facts = data["facts"]["us-gaap"]

        for tag, tag_data in facts.items():
            units = tag_data.get("units", {})
            for unit_type, entries in units.items():
                if entries:
                    latest = entries[-1]
                    return {
                        "filing_date": latest.get("filed"),
                        "fiscal_year": latest.get("fy"),
                        "fiscal_period": latest.get("fp"),
                        "filing_type": latest.get("form"),
                    }

        return {
            "filing_date": None,
            "fiscal_year": None,
            "fiscal_period": None,
            "filing_type": None,
        }

    async def _yf_data(self, symbol: str):
        _earnings = await self._yf.fetch(endpoint="earnings_history", symbol=symbol)
        earnings = _earnings["surprisePercent"]
        _eps = await self._yf.fetch(endpoint="eps_estimate", symbol=symbol)
        eps = _eps["avg"]["0q"]
        _rev = await self._yf.fetch(symbol=symbol, endpoint="revenue_estimate")
        rev = _rev["avg"]["0y"]
        return {"earnings_surprise": next(iter(earnings.values())), "eps_estimate": eps, "revenue_estimate": rev}

    async def finn_profile(self, symbol: str):
        data = await self.finn.fetch(endpoint="profile", symbol=symbol)
        return data

    async def company_peers(self, symbol: str):
        data = await self.finn.fetch(endpoint="peers", symbol=symbol)
        return data

    async def finn_metrics(self, symbol: str):
        data = await self.finn.fetch(endpoint="metric", symbol=symbol)
        return data.get("metric", data)

    async def finn_qoute(self, symbol: str):
        qoute = await self.finn.fetch(endpoint="quote", symbol=symbol)
        return qoute["c"]

    async def macro(self):
        macro_gdp = await self.fred.fetch(series_id="GDPC1")
        macro_gdp_growth = await self.fred.fetch(series_id="A191RL1Q225SBEA")
        macro_inflation = await self.fred.fetch(series_id="CPIAUCSL")
        macro_interest_rates = await self.fred.fetch(series_id="FEDFUNDS")
        macro_unemployment = await self.fred.fetch(series_id="UNRATE")
        macro_government_debt = await self.fred.fetch(series_id="GFDEBTN")
        macro_exchange_rates = await self.fred.fetch(series_id="RTWEXBGS")

        return {
            "macro_gdp": float(macro_gdp["value"].iloc[0]),
            "macro_gdp_growth": float(macro_gdp_growth["value"].iloc[0]),
            "macro_inflation": float(macro_inflation["value"].iloc[0]),
            "macro_interest_rates": float(macro_interest_rates["value"].iloc[0]),
            "macro_unemployment": float(macro_unemployment["value"].iloc[0]),
            "macro_government_debt": float(macro_government_debt["value"].iloc[0]),
            "macro_exchange_rates": float(macro_exchange_rates["value"].iloc[0]),
        }

    async def get_fundamentels(self, symbol: str):

        raw_sec = await self.sec.fetch(symbol=symbol)
        if not isinstance(raw_sec, dict):
            raise TypeError(f"Expected dict from SEC, got {type(raw_sec)}")
        sec_funds = self.extract_funds_sec(data=raw_sec)
        filing_meta = self.extract_filing_meta(data=raw_sec)
        metric = await self.finn_metrics(symbol=symbol)
        macro = await self.macro()
        yf_data = await self._yf_data(symbol=symbol)

        return CompanyFundamental(
            symbol=symbol,
            filing_date=filing_meta["filing_date"],
            fiscal_period=filing_meta["fiscal_period"],
            fiscal_year=filing_meta["fiscal_year"],
            filing_type=filing_meta["filing_type"],
            pre_tax_income=sec_funds["pretax_income"],
            revenue=sec_funds["revenue"],
            cost_of_revenue=sec_funds["cost_of_revenue"],
            gross_profit=sec_funds["gross_profit"],
            operating_expenses=sec_funds["operating_expenses"],
            operating_income=sec_funds["operating_income"],
            interest_expense=sec_funds["interest_expense"],
            income_tax_expense=sec_funds["income_tax_expense"],
            net_income=sec_funds["net_income"],
            eps_basic=sec_funds["eps_basic"],
            eps_diluted=sec_funds["eps_diluted"],
            cash=sec_funds["cash"],
            short_term_investments=sec_funds["short_term_investments"],
            accounts_receivable=sec_funds["accounts_receivable"],
            inventory=sec_funds["inventory"],
            current_assets=sec_funds["current_assets"],
            total_assets=sec_funds["total_assets"],
            current_liabilities=sec_funds["current_liabilities"],
            short_term_debt=sec_funds["short_term_debt"],
            long_term_debt=sec_funds["long_term_debt"],
            total_liabilities=sec_funds["total_liabilities"],
            equity=sec_funds["equity"],
            operating_cash_flow=sec_funds["operating_cash_flow"],
            investing_cash_flow=sec_funds["investing_cash_flow"],
            financing_cash_flow=sec_funds["financing_cash_flow"],
            capital_expenditure=sec_funds["capital_expenditure"],
            shares_outstanding=sec_funds["shares_outstanding"],
            weighted_average_shares=sec_funds["weighted_average_shares_basic"],
            dividends=sec_funds["dividends"],
            buybacks=sec_funds["buybacks"],
            current_price=await self.finn_qoute(symbol=symbol),
            market_cap=metric["marketCapitalization"],
            pe_ratio=metric["peTTM"],
            ps_ratio=metric["psTTM"],
            pb_ratio=metric["pb"],
            ev_ebitda=metric["evEbitdaTTM"],
            roe=metric["roeRfy"],
            roa=metric["roaRfy"],
            debt_equity=metric.get("totalDebt/totalEquityAnnual"),
            earnings=metric["peTTM"],
            eps_estimates=yf_data["eps_estimate"],
            revenue_estimates=yf_data["revenue_estimate"],
            earnings_surprise=yf_data["earnings_surprise"],
            revenue_surprise=(sec_funds["revenue"] - yf_data["revenue_estimate"]) / yf_data["revenue_estimate"],
            company_peers=await self.company_peers(symbol=symbol),
            macro_gdp=macro["macro_gdp"],
            macro_gdp_growth=macro["macro_gdp_growth"],
            macro_inflation=macro["macro_inflation"],
            macro_interest_rates=macro["macro_interest_rates"],
            macro_unemployment=macro["macro_unemployment"],
            macro_government_debt=macro["macro_government_debt"],
            macro_exchange_rates=macro["macro_exchange_rates"],
        )
