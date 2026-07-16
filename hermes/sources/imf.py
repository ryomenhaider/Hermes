import httpx
import pandas as pd
import json
import time

base_url = 'https://api.imf.org/external/sdmx/3.0'
class IMFLogic:

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




if __name__ == "__main__":

    imf = IMFLogic()

    print('========== BOP ==========')
    imf.explore('BOP')
    print('========== WEO ==========')
    imf.explore('WEO', agency='IMF.RES')