class ShaderConfig:
    def __init__(self,VertexPath: str = "",FragmentPath: str = "",GeometryPath: str = ""):
        self.VertexPath = VertexPath
        self.FragmentPath = FragmentPath
        self.GeometryPath = GeometryPath
        self.ShaderValues = {} #Type,Name,Position