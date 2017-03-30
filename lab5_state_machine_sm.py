#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.subscriber_state import SubscriberState
from flexbe_states.calculation_state import CalculationState
from flexbe_states.decision_state import DecisionState
from cpsc495_flexbe_flexbe_states.timed_twist_state import TimedTwistState
from flexbe_states.wait_state import WaitState
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
			# x:409 y:290
			OperatableStateMachine.add('GetTwistCommand',
										SubscriberState(topic=makethisup, blocking=True, clear=False),
										transitions={'received': 'Move_The_Robot', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'myTwistCommand'})

			# x:293 y:51
			OperatableStateMachine.add('Calculate_DIFF_FROM_DESIRED',
										CalculationState(calculation=lambda x: x +2),
										transitions={'done': 'IS_ROBOT_CENTERED'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'BALL_XY', 'output_value': 'DISTANCE_FROM_BALL'})

			# x:538 y:128
			OperatableStateMachine.add('IS_ROBOT_CENTERED',
										DecisionState(outcomes=["centered", "not_centered"], conditions=DISTANCE_FROM_BALL),
										transitions={'centered': 'Stay Still', 'not_centered': 'MOVE_ROBOT'},
										autonomy={'centered': Autonomy.Off, 'not_centered': Autonomy.Off},
										remapping={'input_value': 'DISTANCE_FROM_BALL'})

			# x:739 y:161
			OperatableStateMachine.add('MOVE_ROBOT',
										TimedTwistState(target_time=5, velocity=5, rotation_rate=5, cmd_topic='cmd_vel'),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:719 y:72
			OperatableStateMachine.add('Stay Still',
										TimedTwistState(target_time=0, velocity=0, rotation_rate=0, cmd_topic='cmd_vel'),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:660 y:328
			OperatableStateMachine.add('Move_The_Robot',
										TimedTwistState(target_time=.1, velocity=myTwistCommand.linear, rotation_rate=myTwistCommand.angular, cmd_topic='cmd_vel'),
										transitions={'done': 'simpleWait'},
										autonomy={'done': Autonomy.Off})

			# x:471 y:488
			OperatableStateMachine.add('simpleWait',
										WaitState(wait_time=.01),
										transitions={'done': 'GetTwistCommand'},
										autonomy={'done': Autonomy.Off})

			# x:178 y:31
			OperatableStateMachine.add('Get_Ball_XY',
										SubscriberState(topic=/mine/makethisup, blocking=True, clear=False),
										transitions={'received': 'Calculate_DIFF_FROM_DESIRED', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'BALL_XY'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
