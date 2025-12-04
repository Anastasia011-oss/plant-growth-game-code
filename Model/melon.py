from .plant_base import Plant, PlantModel

class MelonModel(PlantModel):
    def __init__(self):
        super().__init__(Plant(5, "Дыня", 8000))