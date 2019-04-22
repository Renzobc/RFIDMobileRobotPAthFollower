class RfidTag(object):
    
    def __init__(self, TagID, Stamp, LeftAntenna, RightAntenna, Category):
        self.TagID=TagID
        self.Stamp=Stamp
        self.LeftAntenna=LeftAntenna
        self.RightAntenna=RightAntenna
        self.Category=Category
        
    def set_XPos(self, x):
        self.xpos=x
        
    def set_YPos(self, y):
        self.ypos=y