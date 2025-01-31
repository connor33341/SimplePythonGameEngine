import logging

from lib.shaders.shader import Shader
from values.shader.shaderConfig import ShaderConfig

Logger = logging.getLogger(__name__)

class BuildShader:
    def __init__(self, Config: ShaderConfig) -> None:
        Logger.info("Building Shader")
        self.ShaderClass = Shader(Config.VertexPath,Config.FragmentPath,Config.GeometryPath)
        self.ShaderClass.UseShader()
        for ShaderValues in Config.ShaderValues:
            if ShaderValues != []:
                ShaderType: str = ShaderValues[0]
                Name = ShaderValues[1]
                Value = ShaderValues[2]
                if ShaderType == "INT":
                    self.ShaderClass.SetInt(Name,Value)
    
    def GetShader(self) -> Shader:
        return self.ShaderClass
        