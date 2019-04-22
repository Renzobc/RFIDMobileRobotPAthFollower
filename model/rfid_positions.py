#! /usr/bin/env python
from ClassCatetogyRfid import RfIDCategory
from ClassTagRfid import RfidTag
import sys
import ast




def Results():    
    tags = InferRfidPos(GetOdomrecordings(),GetRFIDReadings())
    
    (CatA, CatB, CatC)=CategorizeTags(tags)

    
    WriteCategoryOnFile(CatA)
    WriteCategoryOnFile(CatB)
    WriteCategoryOnFile(CatC)
    
                 
                
def GetRFIDReadings():
    file=open("/home/renzo/pompeu_ws/src/model/readings_data.csv", "r")
    dict=[]
    
    next(file)
    for e in file:
         
         e=e.split(",")
         tag=RfidTag(e[1],float(e[0]),MakeBool(e[2]),MakeBool(e[3]),e[4])             
         dict.append(tag) 
    
          
    return dict     
        
def GetOdomrecordings():
    file=open("/home/renzo/pompeu_ws/src/model/Odometryrecordings.txt","r")
    dict=[]
    
    for e in file:
        
        e=ast.literal_eval(e)
        
        if len(dict)==0 or e['time']!=dict[-1]['time']:
            dict.append(e)
            
    
    return dict
    
            
def MakeBool(str):
    if (str==""):
        return False
    else:
        if (str=="yes"):
            return True
        else:
            return False


def InferRfidPos(Positions, tags):
    #If the time stamps have the same "scond count" the rfid is considered to have that position of the robot
    start_Time=Positions[0]['time']
    
    result=[]
    for tag in tags: 
         
        for position in Positions:
            
            if (tag.Stamp==(position['time']-start_Time)):
                tag.set_XPos(position['x']+isVertical(position)*LeftRight(tag))
                tag.set_YPos(position['y']+isHorizontal(position)*LeftRight(tag))
                result.append(tag)
                
               
    return result
                
def isVertical(position):
    if position['vertical']:
        return -1
    else:  
        return 0
    
def isHorizontal(position): 
    if position['horizontal']:
         return 1   
    else:  
        return 0 

def LeftRight(tag):
    if tag.LeftAntenna:
        return 1
    if tag.RightAntenna:
        return -1 
        
def CategorizeTags(tags):
    CatA=RfIDCategory("A")
    CatB=RfIDCategory("B")
    CatC=RfIDCategory("C")
    
    cases={
        "A":lambda el: CatA.RFIDList.append(el),
        "B":lambda el: CatB.RFIDList.append(el),
        "C":lambda el: CatC.RFIDList.append(el)
    }
    
    for tag in tags:
       
        cases[tag.Category.strip()](tag)
              
    return [CatA, CatB, CatC]

def WriteCategoryOnFile(Cat):
    file=open("/home/renzo/pompeu_ws/src/model/TagbyCategory.txt", "a")
    file.write("Category %s\n"%Cat.nameID)
    Cat.GETCM()
    Cat.GetAvgDistCM()
    file.write("The Position of Category %s is: \n {'XCM':%4.2f,'YCM':%4.2f}\n"%(Cat.nameID,Cat.XCM,Cat.YCM))
    file.write("The Average distance of the tags of this category to its Category position is:%4.2f\n"%Cat.AVGDIST)
    for tag in Cat.RFIDList:
        file.write('{"TagID":%s, "X":%4.2f, "Y":%4.2f}\n'%(tag.TagID,tag.xpos,tag.ypos))
        
        
        
if __name__ == "__main__" : 
    Results()