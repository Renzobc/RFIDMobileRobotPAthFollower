#! /usr/bin/env python

from rfid_path_msg.srv import  path
import rospy

import json


from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Quaternion
from nav_msgs.msg import Path 

def handlePathRequest(req):
    rfid_plan=Generate_rfid_path()
    
    return rfid_plan


def Generate_rfid_path():
    rfid_plan=Path()

    rfid_plan.header.seq=0
    rfid_plan.header.stamp=rospy.Time.now()
    rfid_plan.header.frame_id="base"

    txt_file=read_txt()
    rospy.loginfo(txt_file)
    for e in txt_file: 
        p=GetNextPose(e)
        #rospy.loginfo(p)
        rfid_plan.poses.append(p)
    
    rospy.loginfo([rfid_plan, True])
    return [rfid_plan, True]

def read_txt():
    result=[]
    file=open("/home/renzo/pompeu_ws/src/packages/rfid_path/path.txt","r")
    rospy.loginfo(file.readlines)
    
    for line in file:
        
        
        l=line.split()
        
        point={'x':l[1], 'y':l[2], 'th':l[3]} 
        
        #rospy.loginfo(point)
        
        result.append(point)
        
    return result

def GetNextPose(e):
    
    #rospy.loginfo(e)
    
    pose=PoseStamped()
    
    #rospy.loginfo(pose)

    pose.header.stamp=rospy.Time.now()
    pose.header.frame_id="base"
    pose.pose.position.x=float(e['x'])
    pose.pose.position.y=float(e['y'])
    pose.pose.position.z=0

    (pose.pose.orientation.x, pose.pose.orientation.y, pose.pose.orientation.z, pose.pose.orientation.w )= quaternion_from_euler(0,0,float(e['th']))

    #rospy.loginfo(pose)
    return pose

def pathserver():
    rospy.init_node('rfid_path_server_node', anonymous=False)
    rospy.Service('rfid_path', path, handlePathRequest)
    rospy.loginfo('Service path is up')
    rospy.spin()

if __name__=='__main__':
    pathserver()
    
    
    