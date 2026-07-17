import httpx
import pandas as pd
import json
import logging
import time
from io import StringIO

from typing import Literal, Optional

logger = logging.getLogger(__name__)

BASE_URL = 'https://stats.bis.org/api/v1'

OBS_COLS = {'TIME_PERIOD', 'OBS_VALUE', 'OBS_STATUS', 'OBS_CONF', 'OBS_PRE_BREAK'}

FLOWS = [
    "BIS_REL_CAL", "WS_CBPOL", "WS_CBS_PUB", "WS_CBTA",
    "WS_CPMI_CASHLESS", "WS_CPMI_CT1", "WS_CPMI_CT2",
    "WS_CPMI_DEVICES", "WS_CPMI_INSTITUT", "WS_CPMI_MACRO",
    "WS_CPMI_PARTICIP", "WS_CPMI_SYSTEMS", "WS_CPP",
    "WS_CREDIT_GAP", "WS_DEBT_SEC2_PUB", "WS_DER_OTC_TOV",
    "WS_DPP", "WS_DSR", "WS_EER", "WS_GLI", "WS_LBS_D_PUB",
    "WS_LONG_CPI", "WS_NA_SEC_C3", "WS_NA_SEC_DSS",
    "WS_OTC_DERIV2", "WS_SPP", "WS_TC", "WS_XRU", "WS_XTD_DERIV"
]


class BISLogic:

    def fetch(
        self,
        flow: str,
        key: str = "all",
        format: Literal["csv", "json", "xml"] = "csv",
        start_period: Optional[str] = None,
        end_period: Optional[str] = None,
        first_n: Optional[int] = None,
        last_n: Optional[int] = None,
        detail: Optional[Literal["full", "dataonly", "serieskeysonly", "nodata"]] = None,
    ) -> pd.DataFrame:
        url = f'{BASE_URL}/data/{flow}/{key}'

        params = {"format": format}
        if start_period:
            params["startPeriod"] = start_period
        if end_period:
            params["endPeriod"] = end_period
        if first_n:
            params["firstNObservations"] = first_n
        if last_n:
            params["lastNObservations"] = last_n
        if detail:
            params["detail"] = detail

        resp = httpx.get(url, params=params, timeout=120)
        resp.raise_for_status()

        if format == "csv":
            return pd.read_csv(StringIO(resp.text))
        else:
            return self._parse_sdmx_json(resp.json(), flow)

    def _parse_sdmx_json(self, data: dict, flow: str) -> pd.DataFrame:
        try:
            struct = data["data"]["structures"][0]
            dims = {d["id"]: d for d in struct["dimensions"]["series"]}
            tps = struct["dimensions"]["observation"][0]["values"]

            dim_ids = sorted(dims.keys())

            rows = []
            for sv_key, sv in data["data"]["dataSets"][0]["series"].items():
                key_parts = sv_key.split(":")
                per_series_dims = {
                    dim_id: key_parts[i] if i < len(key_parts) else ""
                    for i, dim_id in enumerate(dim_ids)
                }

                indicator_id = ".".join([flow] + [per_series_dims[d] for d in dim_ids])

                for ok, ov in sv["observations"].items():
                    rows.append({
                        "date": pd.to_datetime(tps[int(ok)]["value"]),
                        "country_iso3": per_series_dims.get("REF_AREA", ""),
                        "indicator_id": indicator_id,
                        "value": float(ov[0]),
                        "source": "BIS",
                    })

            df = pd.DataFrame(rows)
            return df.sort_values(["country_iso3", "date"]).reset_index(drop=True)

        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Failed to parse SDMX JSON: {e}")
            return pd.DataFrame(columns=["date", "country_iso3", "indicator_id", "value", "source"])

    def transform(self, data: pd.DataFrame, flow: str) -> pd.DataFrame:
        if data.empty:
            return pd.DataFrame(columns=["date", "country_iso3", "indicator_id", "value", "source"])

        dim_cols = [c for c in data.columns if c not in OBS_COLS]

        df = data

        text_cols = {"TITLE_TS", "TITLE", "SUPP_INFO", "SUPP_INFO_BREAKS", "SOURCE_REF", "COMPILATION"}
        indicator_cols = [c for c in dim_cols if c not in text_cols]

        df["indicator_id"] = df.apply(
            lambda row: ".".join(
                [flow] + [str(row[c]) if pd.notna(row[c]) else "" for c in indicator_cols]
            ),
            axis=1
        )

        country_cols = {"REF_AREA", "BORROWERS_CTY", "COUNTRY", "REFERENCE_AREA"}
        country_col = next((c for c in country_cols if c in df.columns), None)
        if country_col:
            df["country_iso3"] = df[country_col].fillna("").astype(str)
            df["country_iso3"] = df["country_iso3"].replace("nan", "")
        else:
            df["country_iso3"] = ""

        df["date"] = pd.to_datetime(df["TIME_PERIOD"], format="mixed")

        df["value"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")

        df["source"] = "BIS"

        result = df[["date", "country_iso3", "indicator_id", "value", "source"]].copy()
        result = result.dropna(subset=["value"])
        result = result.sort_values(["country_iso3", "date"]).reset_index(drop=True)

        return result

    def validate(self, data: pd.DataFrame) -> bool:
        if not isinstance(data, pd.DataFrame):
            logger.error('Data must be a pandas DataFrame')
            return False

        required = {"date", "country_iso3", "indicator_id", "value", "source"}
        missing = required - set(data.columns)

        if missing:
            logger.error(f'DataFrame missing columns: {missing}')
            return False

        issues = 0
        records = data.to_dict(orient='records')
        for idx, row in enumerate(records):
            for col in required:
                if col not in row:
                    logger.warning(f'{col} missing at row {idx}')
                    issues += 1
                elif pd.isna(row[col]):
                    logger.warning(f'{col} is na at row {idx}')
                    issues += 1

        if issues:
            logger.error(f'The Data has {issues} issues')
            return False

        return True

    def export(self, data: pd.DataFrame, filetype: str) -> str:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        ts = time.time()
        path = f'data/{ts}.{filetype}'

        if filetype == 'json':
            records = data.reset_index().to_dict(orient='records')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(records, f, default=str)
        elif filetype == 'csv':
            data.to_csv(path, date_format='iso')
        elif filetype == 'parquet':
            data.to_parquet(path)
        elif filetype == 'pickle':
            data.to_pickle(path)
        else:
            raise ValueError(f"Unsupported filetype: {filetype!r}")

        logger.info(f'Exported to {path}')
        return path


class BIS:

    def __init__(self):
        self.bis = BISLogic()

    def get_flows(self) -> list[dict]:
        return [{"id": f, "name": FLOW_NAMES.get(f, "")} for f in FLOWS]

    def explore(
        self,
        flow: str,
        key: str = "all",
        n: int = 5,
        **kwargs,
    ) -> pd.DataFrame:
        kwargs.setdefault("last_n", n)
        raw = self.bis.fetch(flow=flow, key=key, **kwargs)
        if raw.empty:
            print(f"No data returned for {flow}")
            return raw

        print(f"=== {flow} ===")
        print(f"Columns: {list(raw.columns)}")
        print(f"Shape: {raw.shape}")
        print(f"--- First {n} rows ---")
        print(raw.head(n))
        print()

        dim_cols = [c for c in raw.columns if c not in OBS_COLS]
        print(f"Dimension columns (define a series): {dim_cols}")
        if not raw.empty:
            print(f"Unique series: {raw[dim_cols].drop_duplicates().shape[0]}")
        print()

        return raw

    def get_data(
        self,
        flow: str,
        key: str = "all",
        start_period: Optional[str] = None,
        end_period: Optional[str] = None,
        first_n: Optional[int] = None,
        last_n: Optional[int] = None,
        export: Optional[bool] = None,
        filetype: str = 'csv',
    ) -> pd.DataFrame:
        raw = self.bis.fetch(
            flow=flow,
            key=key,
            start_period=start_period,
            end_period=end_period,
            first_n=first_n,
            last_n=last_n,
        )

        transformed = self.bis.transform(raw, flow=flow)

        valid = self.bis.validate(transformed)
        if not valid:
            raise RuntimeError('The Data is not valid for application')

        if export:
            self.bis.export(transformed, filetype=filetype)

        return transformed


FLOW_NAMES = {
    "BIS_REL_CAL": "BIS Release Calendar",
    "WS_CBPOL": "Central bank policy rates",
    "WS_CBS_PUB": "Consolidated banking",
    "WS_CBTA": "Central bank total assets",
    "WS_CPMI_CASHLESS": "CPMI cashless payments",
    "WS_CPMI_CT1": "CPMI comparative tables type 1",
    "WS_CPMI_CT2": "CPMI comparative tables type 2",
    "WS_CPMI_DEVICES": "CPMI payment devices",
    "WS_CPMI_INSTITUT": "CPMI institutions",
    "WS_CPMI_MACRO": "CPMI macro",
    "WS_CPMI_PARTICIP": "CPMI participants",
    "WS_CPMI_SYSTEMS": "CPMI systems",
    "WS_CPP": "Commercial property prices",
    "WS_CREDIT_GAP": "Credit-to-GDP gaps",
    "WS_DEBT_SEC2_PUB": "International debt securities",
    "WS_DER_OTC_TOV": "OTC derivatives turnover",
    "WS_DPP": "Detailed residential property prices",
    "WS_DSR": "Debt service ratios",
    "WS_EER": "Effective exchange rates",
    "WS_GLI": "Global liquidity indicators",
    "WS_LBS_D_PUB": "Locational banking",
    "WS_LONG_CPI": "Consumer prices statistics",
    "WS_NA_SEC_C3": "BIS debt securities statistics",
    "WS_NA_SEC_DSS": "Debt securities statistics",
    "WS_OTC_DERIV2": "OTC derivatives outstanding",
    "WS_SPP": "Selected residential property prices",
    "WS_TC": "Total credit",
    "WS_XRU": "US dollar exchange rates",
    "WS_XTD_DERIV": "Exchange-traded derivatives",
}
