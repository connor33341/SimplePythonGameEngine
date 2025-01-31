# Connor33341

from OpenGL.GL import *
from glfw.GLFW import *
from glfw import _GLFWwindow as GLFWwindow
from PIL import Image

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
            Logger.info("Finished")

        except Exception as Error:
            Logger.error(Error)
    def SetFramebufferSizeCallback(self,Callback) -> None:
        glfwSetFramebufferSizeCallback(self.Window, Callback)
    
    def SetCursorPosCallback(self,Callback) -> None:
        glfwSetCursorPosCallback(self.Window, Callback)
    
    def SetScrollCallback(self,Callback) -> None:
        glfwSetScrollCallback(self.Window, Callback)