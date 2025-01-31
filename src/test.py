from engine.window import GLWindowSettings, GLWindow
from values.shader.shaderConfig import ShaderConfig
from values.shader.defaultShaders import DefaultShaders
from utils.shader.bulkLoad import BulkLoadShader
from utils.textures.quickPBR import QuickPBR
import logging
import uuid

Logger = logging.getLogger(__name__)

if __name__ == "__main__":
    FileName = str(uuid.uuid4())
    LogFile = f"src\\logs\\{FileName}.log"
    print(LogFile)
    logging.basicConfig(filename=LogFile, level=logging.INFO)
    Logger.info("Started")
    Settings = GLWindowSettings()
    Window = GLWindow(Settings)
    BulkShader = BulkLoadShader(DefaultShaders)
    BulkShader.Load()
    GoldMaterial = QuickPBR("gold").GetTexture()
    
    Logger.info("Ended")