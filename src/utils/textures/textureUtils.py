from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
import imageio
import numpy
import glm
import os

class ImageUtils():
    def __init__(self,IMAGE_RESOURCE_PATH: str) -> None:
        self.IMAGE_RESOURCE_PATH = IMAGE_RESOURCE_PATH
        self.LOAD_IMAGE = lambda name: Image.open(os.path.join(IMAGE_RESOURCE_PATH, name)).transpose(Image.FLIP_TOP_BOTTOM)
        self.LOAD_HDR_IMAGE = lambda name: imageio.imread(os.path.join(IMAGE_RESOURCE_PATH, name), format="HDR-FI")
