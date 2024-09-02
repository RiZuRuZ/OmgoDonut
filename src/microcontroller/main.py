from machine import Pin, PWM, Timer
from stepper import Stepper
import utime
import select
import sys

# Set the maximum speed and acceleration parameters
max_speed = 3000  # Maximum speed in steps per second
acceleration = 500  # Acceleration in steps per second^2

# Timer for step interval
# timer = Timer()

# Define stepper motor connections
dir_pin = Pin(0, Pin.OUT)
step_pin = Pin(1, Pin.OUT)

# step_motor = StepMotor(step_pin, dir_pin , max_speed, acceleration)
step_motor = Stepper(step_pin, dir_pin , steps_per_rev = 16000, speed_sps = 8000)

servo2 = PWM(Pin(16))  
servo1 = PWM(Pin(17))

servo1.freq(50)
servo2.freq(50)


def set_servo_angle(servo, angle):
    """Turn servo to the specified angle

    Args:
        angle (int): angle in degrees
    """
    min_pulse_width = (544 * 0.001) / 1000
    max_pulse_width = (2400 * 0.001) / 1000
    frame_width = 20 / 1000
    duty_factor = 65535
    min_duty = int((min_pulse_width / frame_width) * duty_factor)
    max_duty = int((max_pulse_width / frame_width) * duty_factor)
    min_angle = 0
    max_angle = 180
    factor = (max_duty - min_duty) / (max_angle - min_angle)
    duty = int((angle - min_angle) * factor) + min_duty
    servo.duty_u16(duty)

def set_display(number):
    """display the specified number

    Args:
        number (int): number from 0-9
    """
    # Define the 7-segment display pins
    segments_pins = [Pin(pin_num, Pin.OUT) for pin_num in range(9, 2, -1)]
    display_patterns = [
        [1, 1, 1, 1, 1, 1, 0],  # 0
        [0, 1, 1, 0, 0, 0, 0],  # 1
        [1, 1, 0, 1, 1, 0, 1],  # 2
        [1, 1, 1, 1, 0, 0, 1],  # 3
        [0, 1, 1, 0, 0, 1, 1],  # 4
        [1, 0, 1, 1, 0, 1, 1],  # 5
        [1, 0, 1, 1, 1, 1, 1],  # 6
        [1, 1, 1, 0, 0, 0, 0],  # 7
        [1, 1, 1, 1, 1, 1, 1],  # 8
        [1, 1, 1, 1, 0, 1, 1],  # 9
    ]
    for i, pin in enumerate(segments_pins):
        pin.value(display_patterns[number][i])


def wait_countdown(seconds):  # type:  (int) -> None
    """Countdown timer and show to screen

    Args:
        seconds (int): seconds to count down
    """
    while seconds >= 0:
        print("Countdown:", seconds)
        set_display(seconds)
        utime.sleep(1)
        seconds -= 1


def repeat_servo(servo, repeat): # repeat servo
    for _ in range(repeat):
        set_servo_angle(servo, 0)
        utime.sleep(0.1)
        set_servo_angle(servo, 45)
        utime.sleep(0.1)

while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.readline()
        data = ch.strip()  # Ensure to strip newline characters
        if data == "test":
            data = None
            # Red
#             step_motor.free_run(1)
#             utime.sleep(2.3)
#             step_motor.free_run(0)
#             utime.sleep(1)
#             repeat_servo(20)

            # Green
#             step_motor.free_run(1)
#             utime.sleep(3.5) 
#             step_motor.free_run(0)
#             utime.sleep(1)
#             repeat_servo(20)

            #violet
            step_motor.free_run(1)
            utime.sleep(2.3) 
            step_motor.free_run(0)
            utime.sleep(1)
            repeat_servo(servo1, 20)
            step_motor.free_run(1)
            utime.sleep(1.2)
            step_motor.free_run(0)
            utime.sleep(1)
            repeat_servo(servo2, 20)
            

            
            
        if data == "Red":
            data = None
            wait_countdown(3)
            step_motor.set_target_position(3250)  # 700*2.5
            step_motor.turn(timer)
            set_servo_angle(0)  # Move to 0 degrees
            utime.sleep(1 / 16)
            set_servo_angle(90)  # Move to 90 degrees
            utime.sleep(1 / 16)
            set_servo_angle(180)  # Move to 180 degrees
            utime.sleep(1 / 16)

        if data == "Green":
            data = None
            wait_countdown(3)
            step_motor.set_target_position(5525)  # 1300*2.5
            step_motor.turn(timer)

        if data == "Violet":
            data = None
            wait_countdown(3)
            step_motor.set_target_position(3250)  # 700*2.5
            step_motor.turn(timer)
            wait_countdown(2)
            step_motor.set_target_position(2275)  # 1300*2.5
            step_motor.turn(timer)

        if data == "0":
            data = None
            led1.off()
            print("Hello world")

        if data is not None:
            print("Unknown command")

    utime.sleep(1)
