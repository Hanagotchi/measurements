from fastapi import HTTPException, status


class PlantNotFound(HTTPException):
    def __init__(self, plant_id: int):
        status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(
            status_code=status_code,
            detail=f"Could not found any plant with id: {plant_id}"
        )
