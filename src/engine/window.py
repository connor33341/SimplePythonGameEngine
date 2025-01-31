# Connor33341

from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image
from utils.shader.bulkLoad import BulkLoadShader
from engine.render import RenderCube

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

    def SetBulkShader(self,BulkShader: BulkLoadShader) -> None:
        self.BulkShader = BulkShader

    def CreateSkyBox(self,HDRTexture: int) -> None:
        Logger.info("Setting Up: EquirectangularToCubemapShader")
        self.EquirectangularToCubemapShader = self.BulkShader.GetByName("EquirectangularToCubemapShader")
        self.EquirectangularToCubemapShader.UseShader()
        self.EquirectangularToCubemapShader.SetInt("equirectangularMap",0)
        self.EquirectangularToCubemapShader.SetMat4("projection",self.CaptureProjection)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,HDRTexture)
        glViewport(0,0,512,512)
        glBindFramebuffer(GL_FRAMEBUFFER,self.CaptureFBO)
        Logger.info("Iterating")
        for i in range(6):
            logging.info(f"Index: {i}")
            self.EquirectangularToCubemapShader.SetMat4("view",self.CaptureViews[i])
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, self.ENVCubemap, 0)
            RenderCube()
        glBindFramebuffer(GL_FRAMEBUFFER,0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.ENVCubemap)
        glGenerateMipmap(GL_TEXTURE_CUBE_MAP)

    def SetupPBR(self) -> None:
        Logger.info("Setting up PBR")
        self.IrradianceMap = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.IrradianceMap)
        Logger.info("Iterating")
        for i in range(6):
            Logger.info(f"Index {i}")
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB16F, 32, 32, 0, GL_RGB, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindFramebuffer(GL_FRAMEBUFFER, self.CaptureFBO)
        glBindRenderbuffer(GL_RENDERBUFFER, self.CaptureRBO)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, 32, 32)
        Logger.info("Getting Irraidiance Shader")
        self.IrradianceShader = self.BulkShader.GetByName("IrradianceShader")
        self.IrradianceShader.UseShader()
        self.IrradianceShader.SetInt("enviornmentMap",0)
        self.IrradianceShader.SetMat4("projection",self.CaptureProjection)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.ENVCubemap)
        glViewport(0,0,32,32)
        glBindFramebuffer(GL_FRAMEBUFFER, self.CaptureFBO)
        Logger.info("Itterating")
        for i in range(6):
            Logger.info(f"Index: {i}")
            self.IrradianceShader.SetMat4("view", self.CaptureViews[i])
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, self.IrradianceMap, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            RenderCube()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        Logger.info("Creating pre-filter to cubemap")
        self.PrefilterMap = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.PrefilterMap)
        Logger.info("Iterating")
        for i in range(6):
            Logger.info(f"Index: {i}")
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB16F, 128, 128, 0, GL_RGB, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR) # be sure to set minification filter to mip_linear 
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # generate mipmaps for the cubemap so OpenGL automatically allocates the required memory.
        glGenerateMipmap(GL_TEXTURE_CUBE_MAP)
        Logger.info("Running quasi monte-carlo simulation on the environment lighting to create a prefilter")
        Logger.info("Getting Prefilter Shader")
        self.PrefilterShader = self.BulkShader.GetByName("PrefilterShader")
        self.PrefilterShader.UseShader()
        self.PrefilterShader.SetInt("environmentMap", 0)
        self.PrefilterShader.SetMat4("projection", self.CaptureProjection)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.ENVCubemap)
        glBindFramebuffer(GL_FRAMEBUFFER, self.CaptureFBO)
        self.MaxMipLevels = 5
        Logger.info(f"MaxMipLevels: {self.MaxMipLevels}")
        for Mip in range(self.MaxMipLevels):
            Logger.info(f"Index: {Mip}")
            MipWidth = int(128 * pow(0.5,Mip))
            MipHeight = int(128 * pow(0.5,Mip))
            glBindRenderbuffer(GL_RENDERBUFFER, self.CaptureRBO)
            glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, MipWidth, MipHeight)
            glViewport(0, 0, MipWidth, MipHeight)
            Roughness = Mip/(self.MaxMipLevels - 1)
            self.PrefilterShader.SetFloat("roughness", Roughness)
            for i in range(6):
                Logger.info(f"SettingView: {i}")
                self.PrefilterShader.SetMat4("view", self.CaptureViews[i])
                glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, self.PrefilterMap, Mip)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                RenderCube()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        Logger.info("Generate 2D LUST from BRDF equations used")
        self.BRDFLUTTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.BRDFLUTTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RG16F, 512, 512, 0, GL_RG, GL_FLOAT, None)
        # be sure to set wrapping mode to GL_CLAMP_TO_EDGE
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        Logger.info("Re-configure framebuffer object and render screen-space quad with BRDF shader")
        glBindFramebuffer(GL_FRAMEBUFFER, self.CaptureFBO)
        glBindRenderbuffer(GL_RENDERBUFFER, self.CaptureRBO)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, 512, 512)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.BRDFLUTTexture, 0)

        glViewport(0, 0, 512, 512)
        #brdfShader.use()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #renderQuad()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)



