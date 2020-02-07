#!/bin/bash -xve

#required packages
echo "pyyaml install start"
pip install pyyaml
echo "rospkg install start"
pip install rospkg
echo "empy install start"
pip install empy
echo "catkin_pkg install start"
pip install catkin_pkg

#ros install
cd ..
git clone https://github.com/ryuichiueda/ros_setup_scripts_Ubuntu14.04_server.git
cd ./ros_setup_scripts_Ubintu14.04_server
bash ./setup0.bash
bash ./setip1.bash

#catkin setup
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
source /opt/ros/indigo/setup.bash
catkin_init_workspace
cd ~/catkin_ws
catkin_make
