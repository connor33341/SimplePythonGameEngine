from lib.textures.loadTexture import LoadTexture
import logging

Logger = logging.getLogger(__name__)
class PBRTexture:
    def __init__(self,AbedoMap: str = "", NormalMap: str = "", MetallicMap: str = "", RoughnessMap: str = "", AOMap: str = "") -> None:
        Logger.info("Adding New PBR Texture")
        self.AbedoMap = AbedoMap
        self.NormalMap = NormalMap
        self.MetallicMap = MetallicMap
        self.RoughnessMap = RoughnessMap
        self.AOMap = AOMap

    def LoadTextures(self) -> None:
        Logger.info("Loading PBR Textures")
        self.LoadedAbedoMap = LoadTexture(self.AbedoMap)
        self.LoadedNormalMap = LoadTexture(self.NormalMap)
        self.LoadedMetallicMap = LoadTexture(self.MetallicMap)
        self.LoadedRoughnessMap = LoadTexture(self.RoughnessMap)
        self.LoadedAOMap = LoadTexture(self.AOMap)