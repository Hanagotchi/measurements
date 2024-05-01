from fastapi import Query
from typing import Optional


class DevicePlantQueryParams:
    def __init__(
        self,
        limit: Optional[int] = Query(10, ge=1, le=500),
        id_plant: Optional[int] = None
    ):
        self.limit = limit
        self.id_plant = id_plant

    def get_query_params(self):
        filters = {}
        if self.limit is not None:
            filters['limit'] = self.limit
        if self.id_plant is not None:
            filters['id_plant'] = self.id_plant
        return filters
