import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient
os.system ("sudo pigpiod") #Launching GPIO library
import pigpio #importing GPIO library

class MotorController:
    def __init__(self, speed=1000):
        self.speed = speed

        self.ESC_pin = 4
        self.pi = pigpio.pi()

        self.pi.set_servo_pulsewidth(self.ESC_pin, 0)
        time.sleep(0.5)
        self.pi.set_servo_pulsewidth(self.ESC_pin, self.speed)

    def update_speed(self, new_speed):
        self.speed = new_speed
        self.pi.set_servo_pulsewidth(self.ESC_pin, self.speed)
