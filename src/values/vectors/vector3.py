import glm

class Vector3:
    def __init__(self,X: float = 0.0,Y: float = 0.0, Z: float = 0.0):
        self.X = X
        self.Y = Y
        self.Z = Z
    
    def ToGLM(self) -> glm.vec3:
        return glm.vec3(self.X, self.Y, self.Z)