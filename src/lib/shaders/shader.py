from OpenGL.GL import *

import glm
import logging
import io

Logger = logging.getLogger(__name__)

class Shader:
    def __init__(self, VertexPath: str, FragmentPath: str, GeometryPath: str = None) -> None:
        Logger.info(f"Compiling Shader")
        try:
            vShaderFile = io.open(VertexPath)
            fShaderFile = io.open(FragmentPath)

            VertexCode = vShaderFile.read()
            FragmentCode = fShaderFile.read()
            GeometryCode = None

            vShaderFile.close()
            fShaderFile.close()

            if (GeometryPath):
                gShaderFile = io.open(GeometryPath)
                GeometryCode = gShaderFile.read()
                gShaderFile.close()

            Vertex = glCreateShader(GL_VERTEX_SHADER)
            Fragment = glCreateShader(GL_FRAGMENT_SHADER)
            Geometry = None
            
            glShaderSource(Vertex, VertexCode)
            glShaderSource(Fragment, FragmentCode)

            if (GeometryPath):
                Geometry = glCreateShader(GL_GEOMETRY_SHADER)
                glShaderSource(Geometry, GeometryCode)

            Shaders = [
                [Geometry, "GEOMETRY"],
                [Vertex, "VERTEX"],
                [Fragment, "FRAGMENT"]
            ]

            self.ID = glCreateProgram()

            for ShaderList in Shaders:
                if ((ShaderList[1] == "GEOMETRY") and (GeometryPath)) or (ShaderList[1] != "GEOMETRY"):
                    UncompiledShader = ShaderList[0]
                    Name = ShaderList[1]
                    Logger.info(f"Loading ShaderType: {Name}")
                    glCompileShader(UncompiledShader)
                    self.CheckCompileErrors(UncompiledShader,Name)
                    glAttachShader(self.ID,UncompiledShader)
            
            glLinkProgram(self.ID)
            self.CheckCompileErrors(self.ID,"PROGRAM")

            glDeleteShader(Vertex)
            glDeleteShader(Fragment)

            if (GeometryPath):
                glDeleteShader(Geometry)

        except IOError:
            Logger.error("Error reading shader")
        except Exception as Error:
            Logger.error(Error)

    def UseShader(self) -> None:
        glUseProgram(self.ID)

    def SetBool(self, name: str, value: bool) -> None:
        glUniform1i(glGetUniformLocation(self.ID, name), int(value))

    def SetInt(self, name: str, value: int) -> None:
        glUniform1i(glGetUniformLocation(self.ID, name), value)

    def SetFloat(self, name: str, value: float) -> None:
        glUniform1f(glGetUniformLocation(self.ID, name), value)

    def SetVec2(self, name: str, *args) -> None:
        if (len(args) == 1 and type(args[0]) == glm.vec2):
            glUniform2fv(glGetUniformLocation(self.ID, name), 1, glm.value_ptr(args[0]))
        elif (len(args) == 2 and all(map(lambda x: type(x) == float, args))):
            glUniform2f(glGetUniformLocation(self.ID, name), *args)

    def SetVec3(self, name: str, *args) -> None:
        if (len(args) == 1 and type(args[0]) == glm.vec3):
            glUniform3fv(glGetUniformLocation(self.ID, name), 1, glm.value_ptr(args[0]))
        elif (len(args) == 3 and all(map(lambda x: type(x) == float, args))):
            glUniform3f(glGetUniformLocation(self.ID, name), *args)

    def SetVec4(self, name: str, *args) -> None:
        if (len(args) == 1 and type(args[0]) == glm.vec4):
            glUniform4fv(glGetUniformLocation(self.ID, name), 1, glm.value_ptr(args[0]))
        elif (len(args) == 3 and all(map(lambda x: type(x) == float, args))):
            glUniform4f(glGetUniformLocation(self.ID, name), *args)

    def SetMat2(self, name: str, mat: glm.mat2) -> None:
        glUniformMatrix2fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(mat))

    def SetMat3(self, name: str, mat: glm.mat3) -> None:
        glUniformMatrix3fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(mat))

    def SetMat4(self, name: str, mat: glm.mat4) -> None:
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(mat))

    def CheckCompileErrors(self, Shader: int, type: str) -> None:
        pass