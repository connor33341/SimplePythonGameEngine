import glm
from OpenGL.GL import *
from glfw.GLFW import *
    
from glfw import _GLFWwindow as GLFWwindow
from utils.textures.textureUtils import ImageUtils
from PIL import Image

import imageio

import numpy
import logging

Logger = logging.getLogger(__name__)

def LoadTexture(Path: str, ResourcePath: str = "") -> int:
    ImageProcessing = ImageUtils(ResourcePath)
    Logger.info(f"Loading Texture: {Path}")
    TextureID = glGenTextures(1)

    try:
        Image = ImageProcessing.LOAD_IMAGE(Path)
        nrComponents = len(Image.getbands())
        Format = GL_RED if nrComponents == 1 else \
                 GL_RGB if nrComponents == 3 else \
                 GL_RGBA
        glBindTexture(GL_TEXTURE_2D, TextureID)
        glTexImage2D(GL_TEXTURE_2D, 0, Format, Image.width, Image.height, 0, Format, GL_UNSIGNED_BYTE, Image.tobytes())
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        Image.close()
        Logger.info("Loading Completed")
        
    except Exception as Error:
        Logger.error(Error)
    
    return TextureID