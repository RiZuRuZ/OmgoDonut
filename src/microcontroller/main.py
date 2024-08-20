from machine import Pin, PWM, Timer
import utime
import select
import sys

# Set the maximum speed and acceleration parameters
max_speed = 3000  # Maximum speed in steps per second
acceleration = 500  # Acceleration in steps per second^2

# Timer for step interval
timer = Timer()


class StepMotor:
    """Step Motor Object
    """
    def __init__(self, dir_pin, step_pin, max_speed, acceleration):
        """Initialize Step Motor Object

        Args:
            dir_pin (int): DIR pin
            step_pin (int): STEP pin
            max_speed (int): Maximum speed in steps per second
            acceleration (int): Acceleration in steps per second^2
        """
        self.current_position = 0
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.target_position = 0

    def turn_timer(self, timer):
        """Turn step motor to `target_position`

        Args:
            timer (Timer): Timer object from Timer.init()
        """
        step_interval = 1 / self.max_speed

        if self.current_position == 0:
            self.dir_pin.on()  # Change to dir_pin.off() if you need the opposite direction
        if self.current_position < self.target_position:
            self.step_pin.on()
            utime.sleep(step_interval / 2)
            self.step_pin.off()
            utime.sleep(step_interval / 2)
            self.current_position += 1
        else:
            print("Target position reached")
            self.current_position = 0  # Reset position for the next run
            timer.deinit()
    def turn(self,timer):
        """Turn step motor using `Timer` provided

        Args:
            timer (Timer): Timer object
        """        
        timer.init(
            freq=max_speed, mode=Timer.PERIODIC, callback=self.turn
        )
    def set_target_position(self, angle):
        """set `target_position`

        Args:
            angle (int): angle to turn to when called StepMotor.turn(timer)
        """
        self.target_position = angle


# Define stepper motor connections
dir_pin = Pin(0, Pin.OUT)
step_pin = Pin(1, Pin.OUT)

step_motor = StepMotor(dir_pin, step_pin, max_speed, acceleration)


servo = PWM(Pin(16))  # Replace 15 with your GPIO pin number
servo.freq(50)


def set_servo_angle(angle):
    """Turn servo to the specified angle

    Args:
        angle (int): angle in degrees
    """
    duty = int((angle / 180 * 1023) + 26)  # For a 0-180 degree servo
    servo.duty_u16(duty)


# Define the LED pin
led1 = Pin(15, Pin.OUT)

# Define duty cycle values for different angles
duty_cycle_0_degrees = 1638  # 0.5 ms
duty_cycle_45_degrees = 3194  # 0.975 ms
duty_cycle_180_degrees = 7864  # 2.4 ms


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


while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.readline()
        data = ch.strip()  # Ensure to strip newline characters
        match data:
            case "Red":
                wait_countdown(3)
                step_motor.set_target_position(3250)  # 700*2.5
                step_motor.turn(timer)
                set_servo_angle(0)  # Move to 0 degrees
                utime.sleep(1 / 16)
                set_servo_angle(90)  # Move to 90 degrees
                utime.sleep(1 / 16)
                set_servo_angle(180)  # Move to 180 degrees
                utime.sleep(1 / 16)

            case "Green":
                wait_countdown(3)
                step_motor.set_target_position(5525)  # 1300*2.5
                step_motor.turn(timer)

            case "Violet":
                wait_countdown(3)
                step_motor.set_target_position(3250)  # 700*2.5
                step_motor.turn(timer)
                wait_countdown(2)
                step_motor.set_target_position(2275)  # 1300*2.5
                step_motor.turn(timer)

            case "0":
                led1.off()
                print("Hello world")

            case _:
                print("Unknown command")

    utime.sleep(1)
