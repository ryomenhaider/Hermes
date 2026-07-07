import logging
from datetime import datetime

from src.hermes.database.database import get_db
from src.hermes.models.fred_model import FredMetaData, FredObs

logger = logging.getLogger(__name__)

class FredRepo:

    def upsert_metadata(self, metadata: dict):
        db = get_db()
        try:
            indicator = FredMetaData(
                id=metadata['id'],
                title=metadata['title'],
                frequency=metadata['frequency'],
                units=metadata['units'],
                source=metadata.get('source', 'FRED')
            )
            db.merge(indicator)
            db.commit()

        except Exception as e:
            logger.error(f'Error upserting metadata: {e}')
            db.rollback()

    def upsert_obs(self, series_id: str, observations: list[dict]):
        db = get_db()

        try:
            rows = []
            for obs in observations:
                rows.append(
                    FredObs(
                        series_id=series_id,
                        period=datetime.fromisoformat(obs['period']).date(),
                        value=obs['value']
                    )
                )

            db.add_all(rows)
            db.commit()
                
        except Exception as e:
            logger.error(f'Error upserting observations for {series_id}: {e}')
            db.rollback()