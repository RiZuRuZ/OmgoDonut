from machine import Pin, PWM, Timer
import utime
import select
import sys

# Define stepper motor connections
dir_pin = Pin(0, Pin.OUT)
step_pin = Pin(1, Pin.OUT)

# Set the maximum speed and acceleration parameters
max_speed = 3000  # Maximum speed in steps per second
acceleration = 500  # Acceleration in steps per second^2

# Timer for step interval
timer = Timer()

current_position = 0
target_position = 0
step_interval = 1 / max_speed


def step_motor(timer):
    global current_position
    if current_position == 0:
        dir_pin.on()  # Change to dir_pin.off() if you need the opposite direction
    if current_position < target_position:
        step_pin.on()
        utime.sleep(step_interval / 2)
        step_pin.off()
        utime.sleep(step_interval / 2)
        current_position += 1
    else:
        print("Target position reached")
        current_position = 0  # Reset position for the next run
        timer.deinit()


servo = PWM(Pin(16))  # Replace 15 with your GPIO pin number
servo.freq(50)


def set_servo_angle(angle):
    # Convert the angle to a duty cycle
    duty = int((angle / 180 * 1023) + 26)  # For a 0-180 degree servo
    servo.duty_u16(duty)


# Define the LED pin
led1 = Pin(15, Pin.OUT)

# Define duty cycle values for different angles
duty_cycle_0_degrees = 1638  # 0.5 ms
duty_cycle_45_degrees = 3194  # 0.975 ms
duty_cycle_180_degrees = 7864  # 2.4 ms

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


def set_display(number):
    for i, pin in enumerate(segments_pins):
        pin.value(display_patterns[number][i])


while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.readline()
        data = ch.strip()  # Ensure to strip newline characters
        match data:
            case "Red":
                countdown_time = 3
                while countdown_time >= 0:
                    print("Countdown:", countdown_time)
                    set_display(countdown_time)
                    utime.sleep(1)
                    countdown_time -= 1
                if countdown_time < 0:
                    target_position = 3250  # 700*2.5
                    timer.init(freq=max_speed, mode=Timer.PERIODIC, callback=step_motor)
                    set_servo_angle(0)  # Move to 0 degrees
                    utime.sleep(1 / 16)
                    set_servo_angle(90)  # Move to 90 degrees
                    utime.sleep(1 / 16)
                    set_servo_angle(180)  # Move to 180 degrees
                    utime.sleep(1 / 16)

            case "Green":
                countdown_time = 3
                while countdown_time >= 0:
                    print("Countdown:", countdown_time)
                    set_display(countdown_time)
                    utime.sleep(1)
                    countdown_time -= 1
                if countdown_time < 0:
                    target_position = 5525  # 1300*2.5
                    timer.init(freq=max_speed, mode=Timer.PERIODIC, callback=step_motor)

            case "Violet":
                countdown_time = 3
                while countdown_time >= 0:
                    print("Countdown:", countdown_time)
                    set_display(countdown_time)
                    utime.sleep(1)
                    countdown_time -= 1
                if countdown_time < 0:
                    target_position = 3250  # 700*2.5
                    timer.init(freq=max_speed, mode=Timer.PERIODIC, callback=step_motor)
                utime.sleep(2)
                while countdown_time >= 0:
                    print("Countdown:", countdown_time)
                    set_display(countdown_time)
                    utime.sleep(1)
                    countdown_time -= 1
                if countdown_time < 0:
                    target_position = 2275  # 1300*2.5
                    timer.init(freq=max_speed, mode=Timer.PERIODIC, callback=step_motor)

            case "0":
                led1.off()
                print("Hello world")

            case _:
                print("Unknown command")

    utime.sleep(1)
