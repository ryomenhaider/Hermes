import httpx
import pandas as pd
import json
import time

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

        # 1. dimension order, straight from the DSD
        ds = data["dataStructures"][0]
        dims = ds["dataStructureComponents"]["dimensionList"]["dimensions"]
        dims_sorted = sorted(dims, key=lambda d: d["position"])
        dimension_order = [d["id"] for d in dims_sorted]

        # 2. map each dimension -> its codelist id (if it has one)
        dim_to_codelist_id = {}
        for d in dims_sorted:
            enum = d.get("localRepresentation", {}).get("enumeration")
            if enum:
                # enum is usually a URN like "...Codelist=IMF.STA:CL_INDEX_TYPE(1.0)"
                codelist_id = enum.split("=")[-1].split("(")[0].split(":")[-1]
                dim_to_codelist_id[d["id"]] = codelist_id

        codelists_raw = {cl["id"]: cl for cl in data.get("codelists", [])}
        codelists = {}
        for dim_id, cl_id in dim_to_codelist_id.items():
            cl = codelists_raw.get(cl_id)
            if not cl:
                continue
            codes = {}
            for code in cl.get("codes", []):
                code_id = code.get("id")
                name = code.get("name")
                if isinstance(name, dict):
                    name = name.get("en", str(name))
                codes[code_id] = name
            codelists[dim_id] = codes

        return {
            "dataflow": dataflow,
            "dimension_order": dimension_order,
            "codelists": codelists,
        }


    def build_key(self, structure: dict, **dimension_values: str) -> str:
        return ".".join(dimension_values.get(dim, "") for dim in structure["dimension_order"])


class IMF:

    pass

if __name__ == '__main__':
    imf = IMFLogic()
    structure = imf.find_key_structure("BOP", agency="IMF.STA")

    print("Dataflow:", structure["dataflow"])
    print("Dimension order:", structure["dimension_order"])
    print()

    for dim, codes in structure["codelists"].items():
        print(f"--- {dim} ({len(codes)} valid codes, showing first 5) ---")
        for code, name in list(codes.items())[:5]:
            print(f"  {code}: {name}")
        print()
        