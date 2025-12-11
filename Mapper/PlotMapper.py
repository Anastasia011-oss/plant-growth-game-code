from Model.plot_entity import PlotEntity
from DTO.plot_dto import PlotDTO

class PlotMapper:
    @staticmethod
    def to_dto(entity: PlotEntity):
        return PlotDTO(
            index=entity.index,
            state=entity.state,
            plant_id=entity.plant_id,
            remaining=entity.remaining,
            fertilizer_count=entity.fertilizer_count
        )

    @staticmethod
    def from_dto(dto: PlotDTO):
        return PlotEntity(
            index=dto.index,
            state=dto.state,
            plant_id=dto.plant_id,
            remaining=dto.remaining,
            fertilizer_count=dto.fertilizer_count
        )