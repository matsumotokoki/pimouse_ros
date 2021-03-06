#!/bin/bash -xve

#required packages
curl -kL https://bootstrap.pypa.io/get-pip.py | python
echo "empy install start"
pip install empy
echo "pyyaml install start"
pip install pyyaml
echo "rospkg install start"
pip install rospkg
echo "catkin_pkg install start"
pip install catkin_pkg

#ros install
cd ..
git clone https://github.com/ryuichiueda/ros_setup_scripts_Ubuntu14.04_server.git
ls
cd ./ros_setup_scripts_Ubuntu14.04_server
bash ./step0.bash
bash ./step1.bash

#catkin setup
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
source /opt/ros/indigo/setup.bash
catkin_init_workspace
cd ~/catkin_ws
catkin_make
