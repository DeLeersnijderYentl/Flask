import mysql.connector as connector


class DbClass:
    def __init__(self):
        pass

    @staticmethod
    def connection():
        config = {
            "user": "root",
            "password": "root",
            "host": "localhost",
            "port": 3306,
            "database": "database_input"
        }
        try:
            c = connector.connect(**config)
            return c
        except:
            print("connection error")
            exit(1)

    @staticmethod
    def get_input():
        # Query zonder parameters
        cn = DbClass.connection()
        cur = cn.cursor()
        query = "SELECT  * FROM input ORDER BY ID_INPUT DESC LIMIT 1"
        cur.execute(query)
        result = cur.fetchone()
        cur.close()
        cn.close()
        return result

    @staticmethod
    def new_input(temp_set, automatic_set, element_power_set, element_heat_cool_set):
        cn = DbClass.connection()
        cur = cn.cursor()
        query = "INSERT INTO input VALUES(NULL," + str(temp_set) + "," + str(automatic_set) + "," + str(element_power_set) + "," + str(element_heat_cool_set) + ")"
        cur.execute(query)
        cn.commit()
        cur.close()
        cn.close()

    @staticmethod
    def get_sensors():
        cn = DbClass.connection()
        cur = cn.cursor()
        query = "SELECT M.ID_SENSOR, M.TEMPERATURE,M.DATE_TIME FROM micontrol AS C JOIN measurement AS M ON M.ID_MEASUREMENT = C.ID_MEASUREMENT ORDER BY M.DATE_TIME DESC LIMIT 4"
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        cn.close()
        return result

    @staticmethod
    def get_sensors_temp_graph():
        cn = DbClass.connection()
        cur = cn.cursor()
        query = "SELECT M.ID_SENSOR, M.TEMPERATURE,M.DATE_TIME FROM micontrol AS C JOIN measurement AS M ON M.ID_MEASUREMENT = C.ID_MEASUREMENT ORDER BY M.DATE_TIME DESC LIMIT 200"
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        cn.close()
        return result

    @staticmethod
    def get_peltier_status():
        cn = DbClass.connection()
        cur = cn.cursor()
        query = "SELECT M.DATE_TIME,C.ID_PELTIER_STATUS FROM micontrol AS C JOIN measurement AS M ON M.ID_MEASUREMENT = C.ID_MEASUREMENT ORDER BY M.DATE_TIME DESC LIMIT 200"
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        cn.close()
        return result

