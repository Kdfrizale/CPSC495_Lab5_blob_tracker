#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.subscriber_state import SubscriberState
from flexbe_states.wait_state import WaitState
from flexbe_states.operator_decision_state import OperatorDecisionState
from cpsc495_flexbe_flexbe_states.kyle_twist_state import KyleTwistState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Mar 29 2017
@author: Kyle Frizzell
'''
class Lab5_State_MachineSM(Behavior):
	'''
	Main State Machine for Lab 5
	'''


	def __init__(self):
		super(Lab5_State_MachineSM, self).__init__()
		self.name = 'Lab5_State_Machine'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1162 y:100, x:318 y:599
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:102 y:130
			OperatableStateMachine.add('GetTwistCommand',
										SubscriberState(topic="/makethisupvel", blocking=True, clear=False),
										transitions={'received': 'getang', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'velocitymy'})

			# x:471 y:488
			OperatableStateMachine.add('simpleWait',
										WaitState(wait_time=.01),
										transitions={'done': 'GetTwistCommand'},
										autonomy={'done': Autonomy.Off})

			# x:864 y:316
			OperatableStateMachine.add('Should_Robot_Finish',
										OperatorDecisionState(outcomes=["yes", "no"], hint="Should the Robot Stop?", suggestion=None),
										transitions={'yes': 'finished', 'no': 'simpleWait'},
										autonomy={'yes': Autonomy.Off, 'no': Autonomy.Off})

			# x:441 y:214
			OperatableStateMachine.add('mvoe',
										KyleTwistState(cmd_topic='/turtlebot/stamped_cmd_vel_mux/input/navi'),
										transitions={'done': 'Should_Robot_Finish', 'getNewMove': 'GetTwistCommand'},
										autonomy={'done': Autonomy.Off, 'getNewMove': Autonomy.Off},
										remapping={'input_velocity': 'velocitymy', 'input_rotation_rate': 'angularmy'})

			# x:249 y:85
			OperatableStateMachine.add('getang',
										SubscriberState(topic="/makethisupang", blocking=True, clear=False),
										transitions={'received': 'mvoe', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'angularmy'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
