# Connor33341

from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
from utils.shader.bulkLoad import BulkLoadShader

import numpy
import glm
import platform
import ctypes
import os
import logging

Logger = logging.getLogger(__name__)

class GLWindowSettings():
    def __init__(self):
        self.ScreenWidth = 1280
        self.ScreenHeight = 720
        self.Name = "Window"

class GLWindow():
    def __init__(self,WindowSettings: GLWindowSettings) -> None:
        try:
            Logger.info("Creating Window")
            self.DeltaTime = 0.0
            self.LastFrame = 0.0
            glfwInit()
            glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
            glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
            glfwWindowHint(GLFW_SAMPLES, 4)
            glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
            if (platform.system() == "Darwin"): # Stupid apple users
                glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)
            self.Window = glfwCreateWindow(WindowSettings.ScreenWidth, WindowSettings.ScreenHeight, WindowSettings.Name, None, None)
            glfwMakeContextCurrent(self.Window)
            if (self.Window == None):
                Logger.error("Window Create Error")
                glfwTerminate()
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LEQUAL)
            glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)
            Logger.info("Setting up Buffers")
            self.CaptureFBO = glGenFramebuffers(1)
            self.CaptureRBO = glGenRenderbuffers(1)
            glBindFramebuffer(GL_FRAMEBUFFER,self.CaptureFBO)
            glBindRenderbuffer(GL_RENDERBUFFER,self.CaptureRBO)
            glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, 512, 512)
            glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.CaptureRBO)
            Logger.info("Setting cubemap to render")
            self.ENVCubemap = glGenTextures(1)
            glBindTexture(GL_TEXTURE_CUBE_MAP, self.ENVCubemap)
            Logger.info("Iterating")
            for i in range(6):
                Logger.info(f"CUBE_MAP_POSITIVE_X_OFFSET: {i}")
                glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB16F, 512, 512, 0, GL_RGB, GL_FLOAT, None)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            Logger.info(f"Setting up projection and view matrices")
            self.CaptureProjection = glm.perspective(glm.radians(90.0), 1.0, 0.1, 10.0)
            self.CaptureViews = glm.array(
                glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 1.0,  0.0,  0.0), glm.vec3(0.0, -1.0,  0.0)),
                glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3(-1.0,  0.0,  0.0), glm.vec3(0.0, -1.0,  0.0)),
                glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0,  1.0,  0.0), glm.vec3(0.0,  0.0,  1.0)),
                glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0, -1.0,  0.0), glm.vec3(0.0,  0.0, -1.0)),
                glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0,  0.0,  1.0), glm.vec3(0.0, -1.0,  0.0)),
                glm.lookAt(glm.vec3(0.0, 0.0, 0.0), glm.vec3( 0.0,  0.0, -1.0), glm.vec3(0.0, -1.0,  0.0))
            )

        except Exception as Error:
            Logger.error(Error)
    def SetFramebufferSizeCallback(self,Callback) -> None:
        glfwSetFramebufferSizeCallback(self.Window, Callback)
    
    def SetCursorPosCallback(self,Callback) -> None:
        glfwSetCursorPosCallback(self.Window, Callback)
    
    def SetScrollCallback(self,Callback) -> None:
        glfwSetScrollCallback(self.Window, Callback)

    def SetupEquirectangularToCubemapShader(self,BulkShader: BulkLoadShader, HDRTexture: int) -> None:
        self.EquirectangularToCubemapShader = BulkShader.GetByName("EquirectangularToCubemapShader")
        self.EquirectangularToCubemapShader.UseShader()
        self.EquirectangularToCubemapShader.SetInt("equirectangularMap",0)
        self.EquirectangularToCubemapShader.SetMat4("projection",self.CaptureProjection)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,HDRTexture)