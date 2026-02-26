# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Vivaan                                                       #
# 	Created:      2/24/2026, 9:21:32 AM                                        #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Brain should be defined by default
brain = Brain()

# The internal EXP inertial sensor
brain_inertial = Inertial()

# The controller
controller = Controller()

# Drive motors
left_drive_2 = Motor(Ports.PORT6, False)
right_drive_2 = Motor(Ports.PORT10, True)

# Arm and claw motors will have brake mode set to hold
# Claw motor will have max torque limited
claw_motor = Motor(Ports.PORT4, False)
arm_motor = Motor(Ports.PORT3, False)

smartdrive = SmartDrive(left_drive_2, right_drive_2, brain_inertial, units=DistanceUnits.IN)
# Max motor speed (percent) for motors controlled by buttons

#
# All motors are controlled from this function which is run as a separate thread
#
def drive_task():
    drive_left = 0
    drive_right = 0

    # setup the claw motor
    def on_L1_pressed():
        # Spinning the arm_motor in forward raises the Arm
        arm_motor.spin(FORWARD)

    # Wait until buttonL1 is released
        while controller.buttonL1.pressing():
            wait(20, MSEC)

        arm_motor.stop()

    # Callback function when Controller buttonL2 is pressed
    def on_L2_pressed():
        # Spinning the arm_motor in reverse lowers the Arm
        arm_motor.spin(REVERSE)

    # Wait until buttonL2 is released
        while controller.buttonL2.pressing():
            wait(20, MSEC)

        arm_motor.stop()

    # Callback function when Controller buttonR1 is pressed
    def on_R1_pressed():
        # Spinning the claw_motor forward closes the Claw
        claw_motor.spin(FORWARD)

    # Wait until buttonR1 is released
        while controller.buttonR1.pressing():
            wait(20, MSEC)

        claw_motor.stop()

    # Callback function when Controller buttonR2 is pressed
    def on_R2_pressed():
        # Spinning the claw_motor in reverse opens the Claw
        claw_motor.spin(REVERSE)

    # Wait until buttonR2 is released
        while controller.buttonR2.pressing():
            wait(20, MSEC)

        claw_motor.stop()


# Register event handlers and pass callback functions
    # add 15ms delay to make sure events are registered correctly.
    smartdrive.set_drive_velocity(25, PERCENT)
    # loop forever
    smartdrive.drive_for(FORWARD, 12, wait=True)
    smartdrive.turn_to_heading(90)

# Run the drive code
drive = Thread(drive_task)

# Python now drops into REPL
