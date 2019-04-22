
from ClassTagRfid import RfidTag
import math
class RfIDCategory(object):
    
    def __init__(self, nameID):
        self.nameID=nameID
        self.RFIDList=[]
        self.XCM=0
        self.YCM=0
        self.AVGDIST=0
        self.MAXDIST=0
        
    def GETCM(self):
        SumX=0
        SumY=0
        
        for rfid in self.RFIDList:
            SumX=rfid.xpos+SumX
            SumY=rfid.ypos+SumY
        try:         
            self.XCM=SumX/len(self.RFIDList)
            self.YCM=SumY/len(self.RFIDList)
        except:
            self.XCM=0
            self.YCM=0
        
    def GetAvgDistCM(self):
        DistSum=0
        for rfid in self.RFIDList:
          DistSum=DistSum+math.sqrt(((rfid.xpos-self.XCM)*(rfid.xpos-self.XCM))+((rfid.ypos-self.YCM)*(rfid.ypos-self.YCM)))  
        try: 
            self.AVGDIST=DistSum/len(self.RFIDList) 
        except:
            self.AVGDIST=0
           
        
    def GetMaxDistCM(self):
        MaxDist=0
        for rfid in self.RFIDList:  
            Dist=sqrt(((rfid.xpos-self.XCM)*(rfid.xpos-self.XCM))+((rfid.ypos-self.YCM)*(rfid.ypos-self.YCM)))  
            if (MaxDist<Dist):
                MaxDist=Dist
        try:       
            self.MAXDIST=MaxDist
        except:
            self.MAXDIST=0
               
                
        
        
    

