# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       Vivaan                                                       #
#   Created:      2/24/2026, 9:21:32 AM                                        #
#   Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Brain should be defined by default
brain = Brain()
global remote_control_code_enabled
remote_control_code_enabled = True
# The internal EXP inertial sensor
brain_inertial = Inertial()

# The controller
controller = Controller()
bumper_a = Bumper(brain.three_wire_port.a)
bumper_b = Bumper(brain.three_wire_port.b)

# Drive motors
left_drive_2 = Motor(Ports.PORT6, False)
right_drive_2 = Motor(Ports.PORT10, True)

# Arm and claw motors will have brake mode set to hold
# Claw motor will have max torque limited
claw_motor = Motor(Ports.PORT4, False)
arm_motor = Motor(Ports.PORT3, False)


arm_motor.set_stopping(HOLD)
claw_motor.set_stopping(HOLD)

# Max motor speed (percent) for motors controlled by buttons

#
# All motors are controlled from this function which is run as a separate thread
#
def drive_task():

    # setup the claw motor
    def on_L1_pressed():
        global remote_control_code_enabled
        if remote_control_code_enabled:
        # Spinning the arm_motor in forward raises the Arm
            arm_motor.spin(FORWARD)

    # Wait until buttonL1 is released
            while controller.buttonL1.pressing():
                wait(20, MSEC)
            arm_motor.stop()

    # Callback function when Controller buttonL2 is pressed
    def on_L2_pressed():
        # Spinning the arm_motor in reverse lowers the Arm
        global remote_control_code_enabled
        if remote_control_code_enabled:
            arm_motor.spin(REVERSE)

    # Wait until buttonL2 is released
            while controller.buttonL2.pressing():
                wait(20, MSEC)

            arm_motor.stop()

    # Callback function when Controller buttonR1 is pressed
    def on_R1_pressed():
        global remote_control_code_enabled
        if remote_control_code_enabled:
            claw_motor.spin(FORWARD)

    # Wait until buttonR1 is released
            while controller.buttonR1.pressing():
                wait(20, MSEC)

            claw_motor.stop()

    # Callback function when Controller buttonR2 is pressed
    def on_R2_pressed():
        global remote_control_code_enabled
        if remote_control_code_enabled:
        # Spinning the claw_motor in reverse opens the Claw
            claw_motor.spin(REVERSE)

    # Wait until buttonR2 is released
            while controller.buttonR2.pressing():
                wait(20, MSEC)
            claw_motor.stop()
    def bumper_a_pressed_callback_0():
        global remote_control_code_enabled
        remote_control_code_enabled = False
        right_drive_2.stop()
        left_drive_2.stop()
        claw_motor.spin(REVERSE)
        arm_motor.spin(FORWARD)
        for repeat_count in range(20):
            brain.screen.print("FREEZE")
            brain.screen.next_row()
            wait(1, SECONDS)
            wait(5, MSEC)
        remote_control_code_enabled = True
        brain.screen.clear_screen()

    def bumper_b_pressed_callback_0():
        global myVariable, remote_control_code_enabled
        remote_control_code_enabled = False
        left_drive_2.stop()
        right_drive_2.stop()
        claw_motor.spin(REVERSE)
        arm_motor.spin(FORWARD)
        for repeat_count2 in range(20):
            brain.screen.print("FREEZE")
            brain.screen.next_row()
            wait(1, SECONDS)
            wait(5, MSEC)
            remote_control_code_enabled = True
            brain.screen.clear_screen()


# Register event handlers and pass callback functions
    controller.buttonL1.pressed(on_L1_pressed)
    controller.buttonL2.pressed(on_L2_pressed)
    controller.buttonR1.pressed(on_R1_pressed)
    controller.buttonR2.pressed(on_R2_pressed)
    bumper_a.pressed(bumper_a_pressed_callback_0)
    bumper_b.pressed(bumper_b_pressed_callback_0)

    # add 15ms delay to make sure events are registered correctly.
    wait(15, MSEC)

    # loop forever
    while True:
        
        # buttons
        # Three values, max, 0 and -max.
        #

        # joystick tank control
        y = controller.axis3.position()
        x = controller.axis1.position()

        # threshold the variable channels so the drive does not
        # move if the joystick axis does not return exactly to 0
        deadband = 15
        if abs(x) < deadband:
            x = 0
        if abs(y) < deadband:
            y = 0

        # Now send all drive values to motors
        leftPower   = max(min(y + x, 100), -100)
        rightPower   = max(min(y - x, 100), -100)

        if remote_control_code_enabled == False:
            leftPower   = 0
            rightPower   = 0
        # The drivetrain
        left_drive_2.spin(FORWARD, leftPower, PERCENT)
        right_drive_2.spin(FORWARD, rightPower, PERCENT)

        # Claw and Arm motors
 
        # and the auxilary motors

        # No need to run too fast
        sleep(10)

# Run the drive code
drive = Thread(drive_task)

# Python now drops into REPL
    