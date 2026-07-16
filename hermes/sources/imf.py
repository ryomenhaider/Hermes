# I never got that much headache when cleaning and validating IMF data, like tf bro learn from world how clean data they have!
# You fkin kill people bcz of money and you cant even take a moment to clean your OWN fkin data
# it took me 4 fkin hours just to get to the real data and please it have have one working API instead of 3 retarted one

import httpx
import pandas as pd
import json
import time
import logging

logger = logging.getLogger(__name__)

base_url = 'https://api.imf.org/external/sdmx/3.0'

class IMFLogic:

    def fetch_imf(
        self,
        agency: str,
        dataflow_id: str,
        key: str,
        version = '~',
    ):
        url = f'{base_url}/data/dataflow/{agency}/{dataflow_id}/{version}/{key}'
        r = httpx.get(url, headers={"Accept": "application/json"})
        return r.json()

    def transform(
        self,
        data: json
    ) -> pd.DataFrame :

        struct = data["data"]["structures"][0]
        dims = {d["id"]: d for d in struct["dimensions"]["series"]}
        tps = struct["dimensions"]["observation"][0]["values"]

        country = dims["COUNTRY"]["values"][0]["id"]
        indicator = f'{dims["INDEX_TYPE"]["values"][0]["id"]}.{dims["COICOP_1999"]["values"][0]["id"]}'

        rows = []
        for sv in data["data"]["dataSets"][0]["series"].items():
            for ok, ov in sv["observations"].items():
                rows.append({
                    "date": tps[int(ok)]["value"],
                    "country_iso3": country,
                    "indicator_id": indicator,
                    "value": float(ov[0]),
                    "source": "IMF",
                })

        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"])

        return df
    
    def validate(
        self,
        data: pd.DataFrame
    ) -> bool:
        df = data.to_dict(orient='records')
        issues = 0
        check = ['date', 'country_iso3', 'indicator_id', 'value', 'source']
        
        for idx, d in enumerate(df):  
            for c in check:
                if c not in d:
                    logger.warning(f'{c} not at {idx}')
                    issues += 1

        if issues != 0:
            logger.error(f'The Data has {issues} issues')
            return False
        else:
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

class IMF:

    def __init__(self):
        self.imf = IMFLogic()

    def find_key_structure(self, dataflow: str, agency: str = "IMF.STA") -> dict:
        url = f"{base_url}/structure/dataflow/{agency}/{dataflow}/~"
        r = httpx.get(
            url,
            headers={"Accept": "application/json"},
            params={"references": "all"},
            follow_redirects=True,
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()["data"]

        ds = data["dataStructures"][0]
        dims = ds["dataStructureComponents"]["dimensionList"]["dimensions"]
        dims_sorted = sorted(dims, key=lambda d: d["position"])
        dimension_order = [d["id"] for d in dims_sorted]

        dim_to_codelist_id = {}
        
        for d in dims_sorted:
            local_rep = d.get("localRepresentation", {})
            enum = local_rep.get("enumeration")
            if not enum:
                continue
            if isinstance(enum, dict):
                enum_str = enum.get("id") or enum.get("ref") or str(enum)
            else:
                enum_str = str(enum)
        
            codelist_id = enum_str.split("=")[-1].split("(")[0].split(":")[-1]
            dim_to_codelist_id[d["id"]] = codelist_id

        codelists_raw = {cl["id"]: cl for cl in data.get("codelists", [])}
        codelists = {}
        for dim_id, cl_id in dim_to_codelist_id.items():
            cl = codelists_raw.get(cl_id)
            if not cl:
                continue
            raw_codes = cl.get("codes") or cl.get("items") or []
            codes = {}
            for code in raw_codes:
                code_id = code.get("id")
                name = code.get("name")
                if isinstance(name, dict):  # sometimes localized {"en": "..."}
                    name = name.get("en", str(name))
                codes[code_id] = name
            codelists[dim_id] = codes

        return {
            "dataflow": dataflow,
            "dimension_order": dimension_order,
            "codelists": codelists,
            "_raw_codelist_ids_found": list(codelists_raw.keys()),
        }


    def build_key(self, structure: dict, **dimension_values: str) -> str:
        return ".".join(dimension_values.get(dim, "") for dim in structure["dimension_order"])


    def explore(self, dataflow: str, agency: str = "IMF.STA", show: int = 5) -> dict:
        
        structure = self.find_key_structure(dataflow, agency=agency)

        print("Dataflow:", structure["dataflow"])
        print("Dimension order:", structure["dimension_order"])
        print()

        if not structure["codelists"]:
            print("(no codelists parsed — raw codelist ids found in response:)")
            print(structure["_raw_codelist_ids_found"])
            print()

        for dim, codes in structure["codelists"].items():
            print(f"--- {dim} ({len(codes)} valid codes, showing first {show}) ---")
            for code, name in list(codes.items())[:show]:
                print(f"  {code}: {name}")
            print()

        return structure
    
    
    def get_dataflowid():
    
        with httpx.Client(timeout=httpx.Timeout(45.0, connect=15.0), follow_redirects=True) as client:
            r = client.get(
                f'{base_url}/structure/dataflow', 
                headers={"Accept": "application/json"}
            )
            r.raise_for_status()
            data = r.json()
            
            flows = data["data"]["dataflows"]
            dataflows = {f["id"]: f["name"] for f in flows}
            
            return dataflows
    
    def get_agency():
        agency_ids = ["IMF", "IMF.STA", "IMF.RES", "IMF.FAD", "SDMX", "ESTAT", "OECD", "BIS"]
        return agency_ids
    
    def get_data(
        self,
        agency: str,
        dataflow_id: str,
        key: str,
        filetype: str | None = None,
        export: bool | None = None,
        version = '~'
    ):
        if not dataflow_id:
            raise ValueError('No dataflow_id is provided you can call get_dataflowid() to get all the IDs')
        elif not agency:
            raise ValueError('No Agency was provided call get_agency() to all agencies')
        elif not key:
            raise ValueError('No key was provided call explore(dataflow, agency), to get all the Keys')
        
        
        raw = self.imf.fetch_imf(
            agency=agency,
            dataflow_id=dataflow_id,
            key=key,
            version=version,
        )

        transformed_data = self.imf.transform(raw)

        vl = self.imf.validate(data=transformed_data)
        if vl:
            logger.info('The data if validated')
            if export:
                try:
                    exp = self.imf.export(data=transformed_data, filetype=filetype)
                    logger.info(f'The data is exported at {exp}')
                except Exception as e:
                    raise LookupError(f'Error: {e}')