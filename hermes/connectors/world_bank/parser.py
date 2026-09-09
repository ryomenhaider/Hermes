import polars as pl


def records_to_dataframe(records: list) -> pl.DataFrame:
    data = [
        {
            "date": record["date"],
            "indicator_id": record["indicator"]["id"],
            "indicator_name": record["indicator"]["value"],
            "country": record["countryiso3code"],
            "value": record["value"],
            "source": "World_Bank",
        }
        for record in records
    ]

    data = pl.DataFrame(data)

    data = data.sort("date", descending=True)
    return data


__all__ = ["records_to_dataframe"]
