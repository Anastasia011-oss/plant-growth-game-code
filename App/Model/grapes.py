from .plant_base import Plant, PlantModel

class GrapesModel(PlantModel):
    def __init__(self):
        super().__init__(Plant(2, "Виноград", 4000))