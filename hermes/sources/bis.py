import httpx
import pandas as pd
import pycountry
import logging
import json
import time
from io import StringIO
from typing import Any, Optional, Literal

logger = logging.getLogger(__name__)

BASE_URL = "https://stats.bis.org/api/v1"
OBS_COLS = {"TIME_PERIOD", "OBS_VALUE", "OBS_STATUS", "OBS_CONF", "OBS_PRE_BREAK"}
TEXT_COLS = {"TITLE_TS", "TITLE", "SUPP_INFO", "SUPP_INFO_BREAKS", "SOURCE_REF", "COMPILATION"}
SERIES_EXCLUDE = {"FREQ", "REF_AREA"}

FLOWS = [
    "BIS_REL_CAL", "WS_CBPOL", "WS_CBS_PUB", "WS_CBTA",
    "WS_CPMI_CASHLESS", "WS_CPMI_CT1", "WS_CPMI_CT2",
    "WS_CPMI_DEVICES", "WS_CPMI_INSTITUT", "WS_CPMI_MACRO",
    "WS_CPMI_PARTICIP", "WS_CPMI_SYSTEMS", "WS_CPP",
    "WS_CREDIT_GAP", "WS_DEBT_SEC2_PUB", "WS_DER_OTC_TOV",
    "WS_DPP", "WS_DSR", "WS_EER", "WS_GLI", "WS_LBS_D_PUB",
    "WS_LONG_CPI", "WS_NA_SEC_C3", "WS_NA_SEC_DSS",
    "WS_OTC_DERIV2", "WS_SPP", "WS_TC", "WS_XRU", "WS_XTD_DERIV",
]

DIM_ORDER_CACHE: dict[str, list[str]] = {}

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

_COUNTRY_CACHE: dict[str, str | None] = {}
_ISO2_OVERRIDES = {"XK": "XKX"}


def _alpha3(code: str) -> str:
    if len(code) != 2:
        return code
    if code in _COUNTRY_CACHE:
        return _COUNTRY_CACHE[code] or code
    upper = code.upper()
    if upper in _ISO2_OVERRIDES:
        _COUNTRY_CACHE[code] = _ISO2_OVERRIDES[upper]
        return _ISO2_OVERRIDES[upper]
    try:
        c = pycountry.countries.get(alpha_2=upper)
        result = c.alpha_3 if c else None
    except LookupError:
        result = None
    _COUNTRY_CACHE[code] = result
    return result or code


def _build_key(flow: str, filters: dict[str, str] | None = None) -> str:
    if not filters:
        return "all"
    if flow not in DIM_ORDER_CACHE:
        return ".".join(filters.values())
    order = DIM_ORDER_CACHE[flow]
    return ".".join(filters.get(d, "") for d in order)


def _transform_csv(df: pd.DataFrame, flow: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["date", "country_iso3", "indicator_id", "value", "source"])

    dim_cols = [c for c in df.columns if c not in OBS_COLS and c not in TEXT_COLS]
    ind_cols = [c for c in dim_cols if c not in SERIES_EXCLUDE]

    df["indicator_id"] = flow + "." + df[ind_cols].apply(
        lambda r: ".".join(str(v) if pd.notna(v) else "" for v in r), axis=1
    )

    df["country_iso3"] = df.get("REF_AREA", pd.Series("", index=df.index)).apply(
        lambda x: _alpha3(str(x).strip()) if pd.notna(x) else ""
    )
    df["date"] = pd.to_datetime(df["TIME_PERIOD"], format="mixed", errors="coerce")
    df["value"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
    df["source"] = "BIS"

    result = df[["date", "country_iso3", "indicator_id", "value", "source"]].copy()
    result = result.dropna(subset=["value"])
    return result.sort_values(["country_iso3", "date"]).reset_index(drop=True)


def _parse_sdmx_json(data: dict, flow: str) -> pd.DataFrame:
    rows = []
    try:
        s = data.get("data", {}).get("structures", [{}])[0]
        obs_dims = {d["id"]: d for d in s.get("dimensions", {}).get("observation", [])}
        obs_vals = obs_dims.get("TIME_PERIOD", {}).get("values", [])
        series_dims = list({d["id"]: d for d in s.get("dimensions", {}).get("series", [])}.keys())

        for dset in data.get("data", {}).get("dataSets", []):
            for sk, sv in dset.get("series", {}).items():
                parts = sk.split(":")
                sd = {k: parts[i] if i < len(parts) else "" for i, k in enumerate(series_dims)}
                ind = ".".join([flow] + [sd[d] for d in series_dims if d not in SERIES_EXCLUDE])
                cty = _alpha3(sd.get("REF_AREA", ""))
                for ok, ov in sv.get("observations", {}).items():
                    idx = int(ok)
                    rows.append({
                        "date": pd.to_datetime(obs_vals[idx]["id"], errors="coerce") if idx < len(obs_vals) else pd.NaT,
                        "country_iso3": cty,
                        "indicator_id": ind,
                        "value": float(ov[0]),
                        "source": "BIS",
                    })
    except (KeyError, IndexError, TypeError, ValueError) as e:
        logger.error("JSON parse error: %s", e)

    if not rows:
        return pd.DataFrame(columns=["date", "country_iso3", "indicator_id", "value", "source"])
    return pd.DataFrame(rows).sort_values(["country_iso3", "date"]).reset_index(drop=True)


class BISLogic:
    def __init__(self):
        self._client = httpx.Client(timeout=120, follow_redirects=True)

    def discover_dim_order(self, flow: str) -> list[str]:
        if flow in DIM_ORDER_CACHE:
            return DIM_ORDER_CACHE[flow]
        try:
            resp = self._get(f"{BASE_URL}/data/{flow}/all", params={"format": "csv", "detail": "serieskeysonly", "lastNObservations": 1})
            df = pd.read_csv(StringIO(resp.text))
            cols = [c for c in df.columns if c not in OBS_COLS and c not in TEXT_COLS]
            DIM_ORDER_CACHE[flow] = cols
            return cols
        except Exception:
            return []

    def _get(self, url: str, params: dict | None = None) -> httpx.Response:
        for attempt in range(3):
            try:
                r = self._client.get(url, params=params)
                r.raise_for_status()
                return r
            except (httpx.HTTPStatusError, httpx.RequestError, httpx.TimeoutException) as e:
                logger.warning("BIS request failed (attempt %d/3): %s", attempt + 1, e)
                if attempt < 2:
                    time.sleep(2 ** attempt)
        raise RuntimeError(f"BIS request failed after 3 attempts")

    def fetch_data(
        self,
        flow: str,
        key: str = "all",
        fmt: Literal["csv", "json", "xml"] = "csv",
        start_period: str | None = None,
        end_period: str | None = None,
        first_n: int | None = None,
        last_n: int | None = None,
    ) -> pd.DataFrame | dict | str:
        params: dict[str, Any] = {"format": fmt}
        if start_period: params["startPeriod"] = start_period
        if end_period: params["endPeriod"] = end_period
        if first_n is not None: params["firstNObservations"] = first_n
        if last_n is not None: params["lastNObservations"] = last_n
        resp = self._get(f"{BASE_URL}/data/{flow}/{key}", params=params)
        if fmt == "csv":
            return pd.read_csv(StringIO(resp.text))
        if fmt == "json":
            return resp.json()
        return resp.text

    def transform(self, data: Any, flow: str, fmt: str = "csv") -> pd.DataFrame:
        if fmt == "csv" and isinstance(data, pd.DataFrame):
            return _transform_csv(data, flow)
        if fmt == "json" and isinstance(data, dict):
            return _parse_sdmx_json(data, flow)
        if isinstance(data, str):
            return self._transform_xml(data, flow)
        raise ValueError(f"Unsupported format/type: {fmt}/{type(data).__name__}")

    @staticmethod
    def _transform_xml(xml: str, flow: str) -> pd.DataFrame:
        rows = []
        try:
            from xml.etree import ElementTree as ET
            root = ET.fromstring(xml)
            ns = {"g": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}
            for series in root.iter("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Series"):
                sk = {}
                for v in series.findall("g:SeriesKey/g:Value", ns):
                    sk[v.get("id")] = v.get("value")
                ind = ".".join([flow] + [v for k, v in sk.items() if k not in SERIES_EXCLUDE])
                cty = _alpha3(sk.get("REF_AREA", ""))
                for obs in series.iter("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs"):
                    tp = ""
                    ov = ""
                    o = obs.find("g:ObsDimension", ns)
                    if o is not None: tp = o.get("value", "")
                    v = obs.find("g:ObsValue", ns)
                    if v is not None: ov = v.get("value", "")
                    rows.append({
                        "date": pd.to_datetime(tp, errors="coerce"),
                        "country_iso3": cty,
                        "indicator_id": ind,
                        "value": pd.to_numeric(ov, errors="coerce"),
                        "source": "BIS",
                    })
        except Exception as e:
            logger.error("XML parse error: %s", e)
        if not rows:
            return pd.DataFrame(columns=["date", "country_iso3", "indicator_id", "value", "source"])
        return pd.DataFrame(rows).dropna(subset=["value"]).sort_values(["country_iso3", "date"]).reset_index(drop=True)

    @staticmethod
    def validate(df: pd.DataFrame) -> dict:
        report: dict[str, Any] = {"valid": True, "errors": [], "warnings": [], "stats": {}}
        if not isinstance(df, pd.DataFrame):
            return {"valid": False, "errors": ["Not a DataFrame"], "warnings": [], "stats": {}}
        report["stats"] = {"rows": len(df), "columns": list(df.columns)}
        req = {"date", "country_iso3", "indicator_id", "value", "source"}
        missing = req - set(df.columns)
        if missing:
            report["valid"] = False
            report["errors"].append(f"Missing columns: {missing}")
            return report
        if not (df["source"] == "BIS").all():
            report["warnings"].append("Some rows have source != BIS")
        nd = int(df["date"].isna().sum())
        if nd: report["warnings"].append(f"{nd} null dates")
        nv = int(df["value"].isna().sum())
        if nv:
            report["errors"].append(f"{nv} null values")
            report["valid"] = False
        report["stats"]["null_dates"] = nd
        report["stats"]["null_values"] = nv
        return report

    @staticmethod
    def export(df: pd.DataFrame, filetype: str = "csv") -> str:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("data must be a DataFrame")
        ts = time.time()
        path = f"data/bis{ts}.{filetype}"
        if filetype == "json":
            with open(path, "w", encoding="utf-8") as f:
                json.dump(df.reset_index().to_dict(orient="records"), f, default=str)
        elif filetype == "csv":
            df.to_csv(path, date_format="iso")
        elif filetype == "parquet":
            df.to_parquet(path)
        elif filetype == "pickle":
            df.to_pickle(path)
        else:
            raise ValueError(f"Unsupported filetype: {filetype!r}")
        logger.info("Exported to %s", path)
        return path


class BIS:
    def __init__(self):
        self._logic = BISLogic()

    def get_flows(self) -> pd.DataFrame:
        return pd.DataFrame([{"id": f, "name": FLOW_NAMES.get(f, "")} for f in FLOWS])

    def get_dimensions(self, flow: str) -> list[str]:
        """Discover dimension column order for a flow from BIS CSV headers."""
        return self._logic.discover_dim_order(flow)

    def get_data(
        self,
        flow: str,
        filters: dict[str, str] | None = None,
        key: str | None = None,
        start_period: str | None = None,
        end_period: str | None = None,
        first_n: int | None = None,
        last_n: int | None = None,
        fmt: Literal["csv", "json", "xml"] = "csv",
        export: bool | None = None,
        filetype: str = "csv",
        validate: bool = True,
    ) -> pd.DataFrame:
        if key is None and filters:
            self._logic.discover_dim_order(flow)
        k = key or _build_key(flow, filters)
        logger.info("BIS: flow=%s key=%s fmt=%s", flow, k, fmt)
        raw = self._logic.fetch_data(flow, k, fmt, start_period, end_period, first_n, last_n)
        transformed = self._logic.transform(raw, flow, fmt)
        if validate:
            report = self._logic.validate(transformed)
            if not report["valid"]:
                raise RuntimeError(f"BIS validation failed: {'; '.join(report['errors'])}")
        if export:
            self._logic.export(transformed, filetype)
        return transformed

    def explore(self, flow: str, filters: dict[str, str] | None = None, n: int = 5, **kwargs) -> pd.DataFrame:
        kwargs.setdefault("last_n", n)
        kwargs.setdefault("fmt", "csv")
        if filters:
            self._logic.discover_dim_order(flow)
        key = _build_key(flow, filters)
        raw = self._logic.fetch_data(flow, key, **kwargs)
        if isinstance(raw, pd.DataFrame):
            print(f"=== {flow} ===")
            print(f"Columns: {list(raw.columns)}")
            print(f"Shape: {raw.shape}")
            print(f"--- First {n} rows ---")
            print(raw.head(n))
            dims = [c for c in raw.columns if c not in OBS_COLS]
            print(f"\nDimension columns: {dims}")
        return raw

    def validate(self, data: pd.DataFrame) -> dict:
        return self._logic.validate(data)

    def export(self, data: pd.DataFrame, filetype: str = "csv") -> str:
        return self._logic.export(data, filetype)
