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
        cn = DbClass.connection()
        cur = cn.cursor()
        query = "SELECT  * FROM input ORDER BY ID_INPUT DESC LIMIT 1"
        cur.execute(query)
        result = cur.fetchone()
        cur.close()
        cn.close()
        return result

    @staticmethod
    def measurement(ID_SENSOR, TEMPERATURE, DATE_TIME_, SET_TEMPERATURE, ID_PELTIER_STATUS, ID_PUMP):
        cn = DbClass.connection()
        cur = cn.cursor()
        query = "INSERT INTO measurement VALUES(NULL,%s,%s,'%s',%s)" % (ID_SENSOR, TEMPERATURE, DATE_TIME_, SET_TEMPERATURE)
        cur.execute(query)
        cn.commit()
        query = 'SELECT ID_MEASUREMENT FROM measurement ORDER BY ID_MEASUREMENT DESC LIMIT 1'
        cur.execute(query)
        result = cur.fetchone()
        ID_MEASUREMENT = result[0]
        query = "INSERT INTO micontrol VALUES(NULL,%s,%s,%s)" % (ID_MEASUREMENT, ID_PELTIER_STATUS, ID_PUMP)
        cur.execute(query)
        cn.commit()
        cur.close()
        cn.close()

    @staticmethod
    def get_sensors():
        cn = DbClass.connection()
        cur = cn.cursor()
        query = "SELECT M.ID_SENSOR, M.TEMPERATURE,M.DATE_TIME from micontrol as C JOIN measurement as M on M.ID_MEASUREMENT = C.ID_MEASUREMENT ORDER BY M.DATE_TIME DESC LIMIT 4"
        cur.execute(query)
        result = cur.fetchall()
        print(result)
        cur.close()
        cn.close()
