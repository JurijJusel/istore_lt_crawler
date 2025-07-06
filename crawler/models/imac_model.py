from models.base_model import BaseItemModel


class ImacItemModel(BaseItemModel):
    proc: str
    ram: str
    disc: str
    gpu: str
    system: str
    color: str
