from hermes.core.result import Result


def list_datasets() -> Result:
    raise NotImplementedError()


def get_dataset(dataset_id: str) -> Result:
    raise NotImplementedError()


def search_datasets(query: str) -> Result:
    raise NotImplementedError()
