class BaseFile():
    def __init__(self,name="",type ="",dir="",size="",data=""):
        self.name = name
        self.dir = dir
        self.type = type
        self.size = size
        self.data = data

    def __str__(self):
        return self.dir + self.name + self.type

    def __repr__(self):
        return str(self)

