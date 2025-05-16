import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Rodri1705",
            database="dbahorro",
            port="3306"
        )

        return conexion
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
    
conectar()