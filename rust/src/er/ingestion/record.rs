use polars::prelude::*;

pub fn read_csv(path: PlRefPath) -> PolarsResult<LazyFrame> {
    LazyCsvReader::new(path).with_has_header(true).finish()
}

pub fn read_json(path: PlRefPath) -> PolarsResult<LazyFrame> {
    LazyJsonLineReader::new(path).finish()
}
