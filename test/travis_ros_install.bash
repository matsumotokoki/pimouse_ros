#!/bin/bash -xve

#required packages
pip2 install catkin_pkg
pip2 install empy
pip2 install pyyaml
pip2 install rospkg

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
