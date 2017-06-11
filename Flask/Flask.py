from flask import Flask, render_template, request, redirect
from static.DbClass import DbClass


app = Flask(__name__)

current_set = 25.0
temperature_1 = 0.0
temperature_2 = 0.0
temperature_3 = 0.0
temperature_4 = 0.0
avg_temperature = 0.0
automatic_status = 0  # Automatic = 0, Manual = 1
element_power_status = 0  # ON = 1, OFF = 0
element_heat_cool_status = 1  # HEATING = 0, COOLING = 1
pomp = 5
peltier_dir = 17
peltier_pwm = 27

times = [0, 1, 2, 3, 4, 5, 6, 7, 8]
values = [10, 11, 12, 1, 14, 3, 16, 22, 18, 19, 20]


def write_input(temp_set, automatic_set, element_power_set, element_heat_cool_set):
    DbClass.new_input(temp_set, automatic_set, element_power_set, element_heat_cool_set)


temp_graph_1_values = []
temp_graph_2_values = []
temp_graph_3_values = []
temp_graph_4_values = []

temp_graph_1_times = []
temp_graph_2_times = []
temp_graph_3_times = []
temp_graph_4_times = []


def get_temp_graph_data():
    global temp_graph_1_values, temp_graph_2_values, temp_graph_3_values, temp_graph_4_values
    global temp_graph_1_times, temp_graph_2_times, temp_graph_3_times, temp_graph_4_times
    sensors = DbClass.get_sensors_temp_graph()
    temp_graph_1_values = []
    temp_graph_2_values = []
    temp_graph_3_values = []
    temp_graph_4_values = []
    temp_graph_1_times = []
    temp_graph_2_times = []
    temp_graph_3_times = []
    temp_graph_4_times = []
    for sensor in sensors:
        if sensor[0] == 1:
            temp_graph_1_times.append(sensor[2])
            temp_graph_1_values.append(sensor[1])
        elif sensor[0] == 2:
            temp_graph_2_values.append(sensor[1])
            temp_graph_2_times.append(sensor[2])
        elif sensor[0] == 3:
            temp_graph_3_values.append(sensor[1])
            temp_graph_3_times.append(sensor[2])
        elif sensor[0] == 4:
            temp_graph_4_values.append(sensor[1])
            temp_graph_4_times.append(sensor[2])
    temp_graph_1_values.reverse()
    temp_graph_2_values.reverse()
    temp_graph_3_values.reverse()
    temp_graph_4_values.reverse()
    temp_graph_1_times.reverse()
    temp_graph_2_times.reverse()
    temp_graph_3_times.reverse()
    temp_graph_4_times.reverse()


def get_temps():
    global temperature_1, temperature_2, temperature_3, temperature_4, avg_temperature
    sensors = DbClass.get_sensors()
    for sensor in sensors:
        if sensor[0] == 1:
            temperature_1 = sensor[1]
        elif sensor[0] == 2:
            temperature_2 = sensor[1]
        elif sensor[0] == 3:
            temperature_3 = sensor[1]
        elif sensor[0] == 4:
            temperature_4 = sensor[1]
    avg_temperature = float(round((temperature_1 + temperature_2 + temperature_3 + temperature_4) / 4, 2))


@app.route('/')
def home():
    global avg_temperature, element_heat_cool_status, element_power_status, automatic_status
    get_temps()
    return render_template('Home.html', avg_temperature=avg_temperature, element_power_status=element_power_status, element_heat_cool_status=element_heat_cool_status, automatic_status=automatic_status, times=times, values=values)


@app.route('/set', methods=['POST'])
def handle_data():
    global automatic_status, element_power_status, element_heat_cool_status, current_set
    new_set = str(request.form['temp_set'])
    try:
        new_set = float(new_set)
        print('this is a number ' + str(new_set))
        current_set = new_set
        write_input(current_set, automatic_status, element_power_status, element_heat_cool_status)
        return redirect('Temperature')
    except ValueError:
        print('this is not a number ' + str(new_set))
        return redirect('Temperature')


@app.route('/buttons', methods=['GET', 'POST'])
def handle_data_buttons():
    global automatic_status, element_power_status, element_heat_cool_status, current_set
    try:
        if request.form.get('slider1') is None:
            print('empty 1')
            automatic_status = 0
        else:
            print(request.form.get('slider1'))
            automatic_status = 1

        if request.form.get('slider2') is None:
            print('empty 2')
            element_power_status = 0
        else:
            print(request.form.get('slider2'))
            element_power_status = 1

        if request.form.get('slider3') is None:
            print('empty 3')
            element_heat_cool_status = 0
        else:
            print(request.form.get('slider3'))
            element_heat_cool_status = 1
        write_input(current_set, automatic_status, element_power_status, element_heat_cool_status)
        return redirect('Heating_Cooling')
    except:
        return redirect('')


@app.route('/Temperature')
def temperature():
    global temperature_1, temperature_2, temperature_3, temperature_4, avg_temperature, current_set
    global temp_graph_1_values, temp_graph_2_values, temp_graph_3_values, temp_graph_4_values
    global temp_graph_1_times, temp_graph_2_times, temp_graph_3_times, temp_graph_4_times
    get_temps()
    get_temp_graph_data()
    return render_template('Temperature.html', current_set=current_set, temperature_1=temperature_1, temperature_2=temperature_2, temperature_3=temperature_3, temperature_4=temperature_4, avg_temperature=avg_temperature,
                           sensor_1_values=temp_graph_1_values, sensor_1_times=temp_graph_1_times, sensor_2_values=temp_graph_2_values, sensor_2_times=temp_graph_2_times, sensor_3_values=temp_graph_3_values, sensor_3_times=temp_graph_3_times,
                           sensor_4_values=temp_graph_4_values, sensor_4_times=temp_graph_4_times, )


@app.route('/Heating_Cooling')
def heating_cooling():
    global element_power_status, element_heat_cool_status, automatic_status
    data_input = DbClass.get_input()
    automatic_status = data_input[2]
    current_set = data_input[1]
    element_power_status = data_input[3]
    element_heat_cool_status = data_input[4]
    return render_template('Heating_Cooling.html', element_power_status=element_power_status, element_heat_cool_status=element_heat_cool_status, automatic_status=automatic_status, times=times, values=values)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
