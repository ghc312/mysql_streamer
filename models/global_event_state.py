# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.types import Enum

from models.database import Base
from models.database import UnixTimeStampType
from models.database import default_now


class EventType(object):

    SCHEMA_EVENT = 'schema_event'
    DATA_EVENT = 'data_event'


class GlobalEventState(Base):
    """GlobalEventState is used to save information about latest event for recovery.
    For clean shutdowns, we will just resume from the recorded gtid, otherwise,
    we will perform recovery procedures for schema event or data event
    according to the event type.
    """

    __tablename__ = 'global_event_state'

    gtid = Column(String, primary_key=True)
    is_clean_shutdown = Column(Integer, nullable=False)
    event_type = Column(
        Enum(
            EventType.SCHEMA_EVENT,
            EventType.DATA_EVENT,
            name='event_type'
        ),
        nullable=False
    )
    time_updated = Column(UnixTimeStampType, default=default_now, onupdate=default_now)
