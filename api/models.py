from pydantic import BaseModel
from typing import Optional, Dict


class RawEvent(BaseModel):
    event_type: str
    event_timestamp: int
    received_timestamp: int
    payload: Dict
    dedup_hash: Optional[str]


class Transaction(BaseModel):
    event_type: str

    item_type: str
    item_snbt: Optional[str]

    quantity: float
    price_per_item: float
    total_value: float

    location_world: Optional[str]
    location_x: Optional[int]
    location_y: Optional[int]
    location_z: Optional[int]

    timestamp: int

    payload: Optional[Dict]