#!/usr/bin/env python
#import roslib; roslib.load_manifest('control_amigo')
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty

msg = """s to start
p to immediate stop

CTRL-C to quit"""

start = 's'
stop = 'p'

class Move(object):
    def __init__(self, repeat, x, rotation):
             self.repeat = repeat
             self.x = x
             self.rotation = rotation

#create an empty list
baseTrajectory = [

#rotation 1 repeat = 10 degree
#forward 1 repeat <> 10cm
		#	  time, x, z
		#Move(x, 0, -1),
        Move(3, 1, 1),
		Move(2, 1, 0),
		Move(3, 1, -1),
		Move(2, 1, 0),
		Move(5, 0, 0), #stop

		Move(7, -1, 0), #backwards
		Move(4, -1, 1),
		Move(4, 1, 0),
		Move(2, -1, -1),
		Move(1, -1, 0),

		Move(10, 0, 0), #stop
		Move(4, 1, 0),
]

currentMove = -1
repeatedIteration = -1


moveBindings = {
		'u':(1,0,0,1),
		'i':(1,0,0,0),
		'o':(1,0,0,-1),

		'j':(0,0,0,1),
        #k stop
		'l':(0,0,0,-1),

		'm':(-1,0,0,-1),
		',':(-1,0,0,0),
		'.':(-1,0,0,1),
       }
speedBindings={
		'q':(1.1,1.1),
		'z':(.9,.9),
		'w':(1.1,1),
		'x':(.9,1),
		'e':(1,1.1),
		'c':(1,.9),
	      }

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)

	pub = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size = 1)
	rospy.init_node('control_amigo')

	speed = rospy.get_param("~speed", 0.5)
	turn = rospy.get_param("~turn", 1.0)
	x = 0
	y = 0
	z = 0
	th = 0
	status = 0

	try:
		print msg
		#print vels(speed,turn)
		while(1):

			key = getKey()
			print key
			if key == start:
				print "start"

				for move in baseTrajectory:
					print move

					for i in range(0, move.repeat):
						for j in range(0, 6720):
							twist = Twist()
							twist.linear.x = move.x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
							twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = move.rotation*turn
							pub.publish(twist)
							#print "publish"

				print "public stop"
				twist = Twist()
				twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
				twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
				pub.publish(twist)
			else:
				if (key == '\x03'):
					break

	except Exception as e:
		print e

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

		print "finally"

		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
