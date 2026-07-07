import asyncio
import logging
from datetime import datetime

from src.hermes.database.database import delete_many_async, save_many_async, save_one_async
from src.hermes.models.fred_model import FredMetaData, FredObs

logger = logging.getLogger(__name__)


class FredRepo:
    def upsert_metadata(self, metadata: dict) -> None:
        try:
            indicator = FredMetaData(
                id=metadata['id'],
                title=metadata['title'],
                frequency=metadata['frequency'],
                units=metadata['units'],
                source=metadata.get('source', 'FRED')
            )
            asyncio.run(save_one_async(indicator))
            logger.info("Metadata upserted for %s", indicator.id)
        except Exception as exc:
            logger.error("Error upserting metadata: %s", exc)

    def upsert_obs(self, series_id: str, observations: list[dict]) -> None:
        try:
            asyncio.run(delete_many_async(FredObs, series_id=series_id))

            rows = []
            for obs in observations:
                rows.append(
                    FredObs(
                        series_id=series_id,
                        period=datetime.fromisoformat(obs['period']).date(),
                        value=obs['value']
                    )
                )

            if rows:
                asyncio.run(save_many_async(rows))
            logger.info("%s observations stored", series_id)
        except Exception as exc:
            logger.error("Error upserting observations for %s: %s", series_id, exc)