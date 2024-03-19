
from app.models.servicoscloudtivit import ServicosCloudTivit

class PrecoServicosCloudTivitResponse:
    class Config:
        arbitrary_types_allowed = True
    count:int
    data:list[ServicosCloudTivit]