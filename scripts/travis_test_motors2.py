#!/usr/bin/env python
#encoding: utf8
import sys, rospy, math
from pimouse_ros.msg import MotorFreqs
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse

class Motor():
	def setUp(self):
		rospy.wait_for_service('/motor_on')
		rospy.wait_for_service('/motor_off')
		on = rospy.ServiceProxy('/motor_on', Trigger)
		ret = on()

	def __init__(self):
		if not self.set_power(False): sys.exit(1)

		rospy.on_shutdown(self.set_power)
		self.sub_raw = rospy.Subscriber('motor_raw', MotorFreqs, self.callback_raw_freq)
		self.sub_cmd_vel = rospy.Subscriber('cmd_vel', Twist, self.callback_cmd_vel)
		self.srv_on = rospy.Service('motor_on', Trigger, self.callback_on)
		self.srv_off = rospy.Service('motor_off', Trigger, self.callback_off)
		self.last_time = rospy.Time.now()
		self.using_cmd_vel = False

	def set_power(self,onoff=False):
		en = "/dev/rtmotoren0"
		try:
			with open(en,'w') as f:
				f.write("1\n" if onoff else "0\n")
			self.is_on = onoff
			return True
		except:
			rospy.logerr("cannot write to " + en)

		return False

	def set_raw_freq(self,left_hz,right_hz):
		if not self.is_on:
			rospy.logerr("not enpowered")
			return

		try:
			with open("/dev/rtmotor_raw_l0",'w') as lf,\
				open("/dev/rtmotor_raw_r0",'w') as rf:
				lf.write(str(int(round(left_hz))) + "\n")
				rf.write(str(int(round(right_hz))) + "\n")
		except:
			rospy.logerr("cannot write to rtmotor_raw_*")

	def callback_raw_freq(self,message):
		self.set_raw_freq(message.left_hz,message.right_hz)

	def callback_cmd_vel(self,message):
		forward_hz = 80000.0*message.linear.x/(9*math.pi)
		rot_hz = 400.0*message.angular.z/math.pi
		self.set_raw_freq(forward_hz-rot_hz, forward_hz+rot_hz)
		self.using_cmd_vel = True
		self.last_time = rospy.Time.now()

	def onoff_response(self,onoff):
		d = TriggerResponse()
		d.success = self.set_power(onoff)
		d.message = "ON" if self.is_on else "OFF"
		return d

	def callback_on(self,message): return self.onoff_response(True)

	def callback_off(self,message): return self.onoff_response(False)

	def test_on_off(self):
		off = rospy.ServiceProxy('motor_off', Trigger)
		ret = off()
		self.assertEqual(ret.success, True, "motor off does not succeeded")
		self.assertEqual(ret.message, "OFF", "motor off wrong message")
		with open("/dev/rtmotoren0", "r") as f:
			data = f.readline()
			self.assertEqual(data,"0\n", "wrong value in rtmotor0 at motor off")

		on = rospy.ServiceProxy('/motor_on', Teigger)
		ret = on()
		self.assertEqual(ret.success, True, "motor on does not succeeded")
		self.assertEqual(ret.message, "ON", "motor on wrong message")
		with open("/dev/rtmotoren0", "r") as f:
			data = f.readline()
			self.assertEqual(data,"1\n", "wrong value in rtmotor0 at motor on")
		

if __name__ == '__main__':
		rospy.init_node('travis_test_motors')
		rostest.rosrun('pimouse_ros', 'travis_test_motors', MotorTest)
		m = Motor()

		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
				if m.using_cmd_vel and rospy.Time.now().to_sec() - m.last_time.to_sec() >= 1.0:
					m.set_raw_freq(0,0)
					m.using_cmd_vel = False
				rate.sleep()

