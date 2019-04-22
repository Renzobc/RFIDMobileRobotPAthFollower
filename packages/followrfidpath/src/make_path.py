#! /usr/bin/env python
import rospy
import math
import actionlib
import actionlib_msgs
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from rfid_path_msg.srv import  path#, pathRequest, pathResponce
from tf.transformations import euler_from_quaternion

class Followpath(object):
    
    def __init__(self, name):
        self._name=name
        self._movebase_client=actionlib.SimpleActionClient('move_base',MoveBaseAction)
        
        path_srv=rospy.ServiceProxy('rfid_path', path)
        service_resp=path_srv(True)
        
        self._PATH=service_resp.path_planed
        
        rospy.loginfo("Waiting for move_base action server to come up...")
        self._movebase_client.wait_for_server()
        
        #Send a position to go to the robot
            #Subscribe to the service that gives the path.
            #Construct the goal to be sent
        
        #Start recording the odometry of the robot.
        self.RecordOdometryTopic()

        #Send every remaining pose on the path to be completed to the move_base action server. Wait to arrive to each point.
        for pose in self._PATH.poses:
            rospy.loginfo("Sending_goal")
            self._movebase_client.send_goal(self.ConstructGoal(pose))
            self._movebase_client.wait_for_result()
            rospy.loginfo(self._movebase_client.get_state)
                    
        rospy.loginfo('Succesfully completed path')
        
    def ConstructGoal(self, pose):   
        Robot_path_goal=MoveBaseGoal()
        Robot_path_goal.target_pose.header.stamp = rospy.Time.now()
        Robot_path_goal.target_pose.header.frame_id = "map"#pose.header.frame_id
        Robot_path_goal.target_pose.header.seq = pose.header.seq
        Robot_path_goal.target_pose.pose.position.x = pose.pose.position.x
        Robot_path_goal.target_pose.pose.position.y = pose.pose.position.y
        Robot_path_goal.target_pose.pose.position.z = 0.0
        Robot_path_goal.target_pose.pose.orientation.x = 0.0
        Robot_path_goal.target_pose.pose.orientation.y = 0.0
        Robot_path_goal.target_pose.pose.orientation.z = pose.pose.orientation.z
        Robot_path_goal.target_pose.pose.orientation.w = pose.pose.orientation.w
        
        return Robot_path_goal
        
    def RecordOdometryTopic(self):
        rospy.Subscriber('/odom',Odometry,self.record2txt)
        
      
    def record2txt(self, data):
        #rospy.loginfo(data)
        #At the end of the sesion we will have a recording of the position of the robot while it was executing the mission.
        (roll, pith, yaw)=euler_from_quaternion([data.pose.pose.orientation.x, data.pose.pose.orientation.y,
                                                 data.pose.pose.orientation.z, data.pose.pose.orientation.w])
        axis=self.OrientationAxis(yaw)        
        file=open('/home/renzo/pompeu_ws/src/model/Odometryrecordings.txt',"a")
        file.write('{"time":%4.2f, "x":%4.2f, "y":%4.2f, "th":%4.2f, "vertical":%s, "horizontal":%s}\n'%(data.header.stamp.secs, data.pose.pose.position.x, data.pose.pose.position.y, yaw, axis[0], axis[1]))
        file.close()
        
        
    def OrientationAxis(self, yaw):
        vertical=False
        horizontal=False
        if (abs(yaw) > math.pi/4) and (abs(yaw) <(3*math.pi/4)):
            vertical=True
            horizontal=False
        else:
            vertical=False
            horizontal=True        
        return [vertical, horizontal]        
            

if __name__=="__main__":
    rospy.init_node('followpathnode')
    Followpath('followpathnode')
    
    