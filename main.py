from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)

def connection():
    # Establece los parámetros de conexión a la base de datos SQL Server
    server= "191.239.122.127"#"10.0.0.4"
    database="FNA"
    username="FNA"
    password="D0cUm3nT2024*."
    driver = '{SQL Server}'

    # Crea una cadena de conexión utilizando los parámetros anteriores
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Conecta a la base de datos
    connectionsql = pyodbc.connect(conn_str)

    return connectionsql

@app.route('/')
def root():
    return 'Hola :), Alex trabaje'

@app.route('/data/<cedula>')
def getByCedula(cedula):
    # Establece la conexión a la base de datos
    connectionql = connection()
    cursor = connectionql.cursor()

    # Ejecuta la consulta SQL para obtener los datos
    query = f"SELECT inv_number, d_asunto, d_number FROM inventoryview WHERE d_number like '%{cedula}%'"  # Asegúrate de cambiar 'tabla' por el nombre correcto de tu tabla
    cursor.execute(query)

    # Obtiene los resultados de la consulta
    data = cursor.fetchall()

    # Convierte los resultados en un formato JSON
    result = []
    for row in data:
        result.append({
            'inv_number': row.inv_number,  # Reemplaza 'columna1' con el nombre de tus columnas
            'd_asunto': row.d_asunto,  # Reemplaza 'columna2' con el nombre de tus columnas
            'd_number': row.d_number
            # Agrega más columnas según sea necesario
        })

    # Cierra la conexión a la base de datos
    cursor.close()
    connectionql.close()

    # Devuelve los datos en formato JSON
    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)
