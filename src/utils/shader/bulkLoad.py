import logging

from lib.shaders.shader import Shader
from utils.shader.buildShader import BuildShader
from values.shader.shaderConfig import ShaderConfig

Logger = logging.getLogger(__name__)

class BulkLoadShader:
    def __init__(self,ShaderList) -> None:
        Logger.info(f"Bulk Importing: {ShaderList}")
        self.ShaderList = ShaderList
        self.LoadedShaders = {}

    def Load(self):
        Logger.info("Loading Bulk Import")
        i = -1
        for ShaderObject in self.ShaderList:
            i += 1
            #0: ShaderValues
            #1: ShaderName
            #2,3,4: Shaders
            ShaderObjectConfig = ShaderConfig(ShaderObject[2],ShaderObject[3],ShaderObject[4])
            ShaderObjectConfig.ShaderValues = ShaderObject[0]
            ShaderBuilder = BuildShader(ShaderObjectConfig)
            ShaderClass = ShaderBuilder.GetShader()
            self.LoadedShaders[i] = {ShaderObject[1],ShaderObjectConfig,ShaderClass}
    
    def GetByName(self,Name: str) -> Shader:
        for ShaderObject in self.LoadedShaders:
            if ShaderObject[0] == Name:
                return ShaderObject[2]