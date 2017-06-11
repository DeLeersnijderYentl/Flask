import RPi.GPIO as GPIO
from CLASS_DS18B20 import DS18B20
from DbClass import DbClass
from threading import Timer
import atexit
from datetime import datetime
import time

GPIO.setmode(GPIO.BCM)
current_set = 16.0
temperature_1 = 0.0
temperature_2 = 0.0
temperature_3 = 0.0
temperature_4 = 0.0
avg_temperature = 0.0
automatic_status = 0  # Automatic = 0, Manual = 1
element_power_status = 0  # ON = 1, OFF = 0
element_heat_cool_status = 1  # HEATING = 0, COOLING = 1
pomp = 5
pump_status = 0
peltier_dir = 17
peltier_pwm = 27
counter = 0
data_input = []
GPIO.setup(peltier_pwm, GPIO.OUT)
GPIO.setup(peltier_dir, GPIO.OUT)
GPIO.setup(pomp, GPIO.OUT)
peltier = GPIO.PWM(peltier_pwm, 50)
peltier.start(0)
adres_1 = '28-0516a2d372ff'
adres_2 = '28-0316a2ed4eff'
adres_3 = '28-0316a2d7aeff'
adres_4 = '28-0516a2e15dff'


def read_all_temps():
    global avg_temperature, temperature_1, temperature_2, temperature_3, temperature_4, current_set, pump_status, element_heat_cool_status, element_power_status
    temperature_1 = temp_sensors.read_one_sensor(0)
    write_measurement(adres_1, temperature_1, current_set, element_power_status, element_heat_cool_status, pump_status)
    temperature_2 = temp_sensors.read_one_sensor(1)
    write_measurement(adres_2, temperature_2, current_set, element_power_status, element_heat_cool_status, pump_status)
    temperature_3 = temp_sensors.read_one_sensor(2)
    write_measurement(adres_3, temperature_3, current_set, element_power_status, element_heat_cool_status, pump_status)
    temperature_4 = temp_sensors.read_one_sensor(3)
    write_measurement(adres_4, temperature_4, current_set, element_power_status, element_heat_cool_status, pump_status)
    avg_temperature = float(round((temperature_1 + temperature_2 + temperature_3 + temperature_4) / 4, 2))
    # print(avg_temperature)


def time_out_1():
    read_all_temps()
    timer_start_1()  # restart timer


def timer_start_1():  # start timer
    t = Timer(13, time_out_1)  # set seconds for time out
    t.start()  # start timer on a different thread


def heating():
    global element_heat_cool_status, pump_status, element_power_status
    element_power_status = 1
    GPIO.output(pomp, GPIO.HIGH)
    pump_status = 1
    GPIO.output(peltier_dir, GPIO.LOW)
    element_heat_cool_status = 0
    peltier.ChangeDutyCycle(99)
    # print(current_set)
    print('heating ' + str(avg_temperature) + ' - ' + str(datetime.now().strftime("%H:%M:%S %d-%m-%Y ")))


def cooling():
    global element_heat_cool_status, pump_status, element_power_status
    element_power_status = 1
    GPIO.output(pomp, GPIO.HIGH)
    pump_status = 1
    GPIO.output(peltier_dir, GPIO.HIGH)
    element_heat_cool_status = 1
    peltier.ChangeDutyCycle(99)
    # print(current_set)
    print('cooling ' + str(avg_temperature) + ' - ' + str(datetime.now().strftime("%H:%M:%S %d-%m-%Y ")))


def off():
    global element_power_status, pump_status
    GPIO.output(pomp, GPIO.LOW)
    pump_status = 0
    peltier.ChangeDutyCycle(0)
    element_power_status = 0
    # print(current_set)
    print('off ' + str(avg_temperature) + ' - ' + str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))


def time_out_2():
    global data_input
    data_input = DbClass.get_input()
    timer_start_2()  # restart timer


def timer_start_2():  # start timer
    t = Timer(7, time_out_2)  # set seconds for time out
    t.start()  # start timer on a different thread


def exit_():
    GPIO.output(pomp, GPIO.LOW)
    peltier.ChangeDutyCycle(0)
    print('exit')
    GPIO.cleanup()


def write_measurement(sensor, temperature, set_temp, peltier_power, peltier_heat_cool, pump):
    # measurement
    if sensor == adres_1:
        ID_SENSOR = 1
    elif sensor == adres_2:
        ID_SENSOR = 2
    elif sensor == adres_3:
        ID_SENSOR = 3
    elif sensor == adres_4:
        ID_SENSOR = 4
    TEMPERATURE = temperature
    DATE_TIME = time.strftime('%Y-%m-%d %H:%M:%S')
    SET_TEMPERATURE = set_temp

    # micontrol
    if peltier_power == 1:
        if peltier_heat_cool == 1:
            ID_PELTIER_STATUS = 2
            # print('petlier status 2')
        elif peltier_heat_cool == 0:
            ID_PELTIER_STATUS = 1
            # print('petlier status 1')
    elif peltier_power == 0:
        ID_PELTIER_STATUS = 3
        # print('petlier status 3')

    if pump == 1:
        ID_PUMP = 1
    elif pump == 0:
        ID_PUMP = 2
    DbClass.measurement(ID_SENSOR, TEMPERATURE, DATE_TIME, float(SET_TEMPERATURE), ID_PELTIER_STATUS, ID_PUMP)


try:
    atexit.register(exit_)
    temp_sensors = DS18B20()
    data_input = DbClass.get_input()
    automatic_status = data_input[2]
    current_set = data_input[1]
    #print(data_input)
    read_all_temps()
    timer_start_2()
    timer_start_1()
    temp_old = 0
    input_data_old = []
    while True:
        automatic_status = data_input[2]
        current_set = data_input[1]
        if automatic_status == 0:
            if avg_temperature != temp_old:
                if avg_temperature < current_set - 2:
                    heating()
                elif avg_temperature > current_set:
                    cooling()
                elif current_set - 2 <= avg_temperature <= current_set:
                    off()
                temp_old = avg_temperature
        elif automatic_status == 1:
            current_set = data_input[1]
            element_power_status = data_input[3]
            element_heat_cool_status = data_input[4]
            if element_power_status == 1:
                if element_heat_cool_status == 0:
                    heating()
                elif element_heat_cool_status == 1:
                    cooling()
            elif element_power_status == 0:
                off()
except KeyboardInterrupt:
    GPIO.output(pomp, GPIO.LOW)
    peltier.ChangeDutyCycle(0)
    print('exit')
    GPIO.cleanup()
