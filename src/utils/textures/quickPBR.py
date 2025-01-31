from values.pbr.pbrTexture import PBRTexture
import os

DEFAULT = "src\\assets"
def ReturnDefault() -> str:
    return DEFAULT

class QuickPBR:
    def __init__(self,TextureName: str,TextureDirectory: str = f"{DEFAULT}\\pbr\\",TextureExtension: str = ".png",AutoLoad: bool = True) -> None: #PBRTexture:
        self.TextureDirectory = TextureDirectory
        self.TextureName = TextureName
        self.TexturePath = os.path.join(TextureDirectory,TextureName)+"\\"
        self.Texture = PBRTexture(self.TexturePath+"albedo"+TextureExtension,self.TexturePath+"normal"+TextureExtension,self.TexturePath+"metallic"+TextureExtension,self.TexturePath+"roughness"+TextureExtension,self.TexturePath+"ao"+TextureExtension)
        if AutoLoad:
            self.Load()
    def Load(self) -> None:
        self.Texture.LoadTextures()
    def GetTexture(self) -> PBRTexture:
        return self.Texture
