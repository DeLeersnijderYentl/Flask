class DS18B20:
    def __init__(self, adres_1='28-0516a2d372ff', adres_2='28-0316a2ed4eff', adres_3='28-0316a2d7aeff', adres_4='28-0516a2e15dff'):
        self.__Sensor_Adressen = []
        self.__Sensors = []
        if adres_1 != '':
            self.__Sensor_Adressen.append(str(adres_1))
        if adres_2 != '':
            self.__Sensor_Adressen.append(str(adres_2))
        if adres_3 != '':
            self.__Sensor_Adressen.append(str(adres_3))
        if adres_4 != '':
            self.__Sensor_Adressen.append(str(adres_4))
        self.__sensor_Setup()

    def __sensor_Setup(self):
        for adres in self.__Sensor_Adressen:
            self.__Sensors.append('/sys/bus/w1/devices/' + str(adres) + '/w1_slave')

    def __read_temp_raw(self):
        lines = []
        waarde = []
        counter = 0
        for sensor in self.__Sensors:
            f = open(sensor, 'r')
            waarde.append(f.readlines())
            # print(waarde)
            lines.append(waarde[counter][1])
            # print('read temp raw: ' + str(lines))
            f.close()
            counter += 1
        return lines

    def __read_temps(self):
        lines = self.__read_temp_raw()
        temperatuur_list = []
        for data in lines:
            equals_pos = data.find('t=')
            # print('equals pos: ' + str(equals_pos))
            if equals_pos != -1:
                temp = data
                # print('Temp list location: ' + str(i))
                temp = temp[29:34]
                # print('Temp string: ' + str(temp))
                temperatuur_list.append(int(temp) / 1000.0)
                # print('Temp List: ' + str(temperatuur_list))
        return temperatuur_list

    def __read_temp_raw_one(self, number=0):
        line = []
        waarde = []
        f = open(self.__Sensors[number], 'r')
        waarde.append(f.readlines())
        line.append(waarde[0][1])
        f.close()
        return line

    def read_average_temps(self):
        average = 0
        for i in self.__read_temps():
            average += i
        return round(average / 4, 2)

    def read_one_sensor(self, sensor_number=0):
        temperatuur = 0
        line = self.__read_temp_raw_one(sensor_number)
        for data in line:
            equals_pos = data.find('t=')
            if equals_pos != -1:
                temp = data[29:34]
                temperatuur = int(temp) / 1000.0

        # equals_pos = line.find('t=')
        # if equals_pos != -1:
        #     temp = line[29:34]
        #     temperatuur.append(int(temp) / 1000.0)
        return temperatuur

# try:
#     temp_sensors = DS18B20('28-0516a2d372ff', '28-0316a2ed4eff', '28-0316a2d7aeff', '28-0516a2e15dff')
#     while True:
#         print('AVG: ' + str(temp_sensors.read_average_temps()))
#         print('1: '+str(temp_sensors.read_one_sensor(0)))
#         print('2:'+str(temp_sensors.read_one_sensor(1)))
#         print('3:'+str(temp_sensors.read_one_sensor(2)))
#         print('4: '+str(temp_sensors.read_one_sensor(3)))
#         print('\n')
# except KeyboardInterrupt:
#     print('\nSTOPPED')
