from sqlalchemy import Column, Date, Float, Integer, String

from hermes.database.database import Base


class FredMetaData(Base):

    __tablename__ = "fred_metadata"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    units = Column(String, nullable=False)
    source = Column(String, nullable=False)

class FredObs(Base):

    __tablename__ = "fred_obs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    series_id = Column(String, nullable=False, index=True)
    period = Column(Date, nullable=False, index=True)
    value = Column(Float, nullable=False)