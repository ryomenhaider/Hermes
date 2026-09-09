class ParserEngine:
    def detect_format(self, source: object) -> str:
        raise NotImplementedError()

    def parse(self, raw_data: object, format: str | None = None) -> object:
        raise NotImplementedError()

    def parse_csv(self, raw_data: object) -> object:
        raise NotImplementedError()

    def parse_json(self, raw_data: object) -> object:
        raise NotImplementedError()

    def parse_parquet(self, raw_data: object) -> object:
        raise NotImplementedError()

    def parse_xml(self, raw_data: object) -> object:
        raise NotImplementedError()
