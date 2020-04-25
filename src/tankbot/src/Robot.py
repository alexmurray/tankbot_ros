# Simple two DC motor robot class.  Exposes a simple LOGO turtle-like API for
# moving a robot forward, backward, and turning.  See RobotTest.py for an
# example of using this class.
# Author: Tony DiCola
# License: MIT License https://opensource.org/licenses/MIT
import atexit

from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor


class Robot(object):
    def __init__(self, addr=0x6f, left_id=3, right_id=2, left_trim=0, right_trim=0,
                 stop_at_exit=True):
        """Create an instance of the robot.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x6f.
         - left_id: The ID of the left motor, default is 3.
         - right_id: The ID of the right motor, default is 2.
         - left_trim: Amount to offset the speed of the left motor, can be positive
                      or negative and use useful for matching the speed of both
                      motors.  Default is 0.
         - right_trim: Amount to offset the speed of the right motor (see above).
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        """
        # Initialize motor HAT and left, right motor.
        self._mh = Raspi_MotorHAT(addr)
        self._left = self._mh.getMotor(left_id)
        self._right = self._mh.getMotor(right_id)
        self._left_trim = int(left_trim)
        self._right_trim = int(right_trim)
        # Start with motors turned off.
        self._left.run(Raspi_MotorHAT.RELEASE)
        self._right.run(Raspi_MotorHAT.RELEASE)
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)

    def _left_speed(self, speed):
        """Set the speed of the left motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed %d must be a value between 0 to 255 inclusive!' % speed
        speed += self._left_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._left.setSpeed(speed)

    def _right_speed(self, speed):
        """Set the speed of the right motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed %d must be a value between 0 to 255 inclusive!' % speed
        speed += self._right_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._right.setSpeed(speed)

    def stop(self):
        """Stop all movement."""
        self._left.run(Raspi_MotorHAT.RELEASE)
        self._right.run(Raspi_MotorHAT.RELEASE)

    def right(self, speed_percent):
        """Drive right motor at speed_percent"""
        # Set motor speed and move both forward.
        dir = Raspi_MotorHAT.FORWARD if speed_percent >= 0 else Raspi_MotorHAT.BACKWARD
        self._right.run(dir)
        self._right_speed(max(0, min(100, int(abs(speed_percent) * 255 / 100))))

    def left(self, speed_percent):
        """Drive left motor at speed_percent"""
        # Set motor speed and move both forward.
        dir = Raspi_MotorHAT.FORWARD if speed_percent >= 0 else Raspi_MotorHAT.BACKWARD
        self._left.run(dir)
        self._left_speed(max(0, min(100, int(abs(speed_percent) * 255 / 100))))
