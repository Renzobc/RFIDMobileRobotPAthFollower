# RFIDMobileRobotPathFollower
Simulation Using move_base Turtlebot on Ros

The Packages were tested using a Turtlebot, with the following launch files:
  roslaunch turtlebot_gazebo amcl_demo.launch. (Necessary so move_base actionserver is up)
  roslaunch turtlebot_gazebo turtlebot_world.launch (Any gazebo world will work)
  
To run the nodes:
  rosrun rfidpath path_rfid_service_server.py (Construct the path given in the pdf)
  rosrun followrfidpath make_path.py (Acts like a actionclient for the move_base action server)
  
The "make_path.py" makes the robot follow the desired path while records the /odom topic in a txt file which should be located in the model folder (same folder as "readings_data.csv" )
The results of the positions of the tags and the Position and radius of each tag category are made by a script locate in the "model" folder.
The script named "rfid_positions.py" produces a txt file located in the "model" folder where it provides of the following info:
  -Position of each tag
  -Position and radius of each category of tags.
