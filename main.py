from flask import Flask, jsonify, request
import pyodbc
import os

app = Flask(__name__)

# Configuración de la base de datos utilizando variables de entorno
DATABASE_CONFIG = {
    'server': os.getenv('DB_SERVER', '191.239.122.127'),
    'database': os.getenv('DB_NAME', 'FNA'),
    'username': os.getenv('DB_USERNAME', 'FNA'),
    'password': os.getenv('DB_PASSWORD', 'D0cUm3nT2024*.'),
    'driver': '{SQL Server}'
}

def connection():
    # Establece los parámetros de conexión a la base de datos SQL Server
    conn_str = f"DRIVER={DATABASE_CONFIG['driver']};SERVER={DATABASE_CONFIG['server']};DATABASE={DATABASE_CONFIG['database']};UID={DATABASE_CONFIG['username']};PWD={DATABASE_CONFIG['password']}"

    # Conecta a la base de datos
    connectionsql = pyodbc.connect(conn_str)

    return connectionsql

@app.route('/data/<cedula>')
def getByCedula(cedula):
    try:
        # Establece la conexión a la base de datos
        connectionql = connection()
        cursor = connectionql.cursor()

        # Ejecuta la consulta SQL parametrizada para obtener los datos
        query = "SELECT inv_number, d_asunto, d_number FROM inventoryview WHERE d_number LIKE ?"
        cursor.execute(query, ('%' + cedula + '%',))

        # Obtiene los resultados de la consulta
        data = cursor.fetchall()

        # Convierte los resultados en un formato JSON
        result = [{'inv_number': row.inv_number, 'd_asunto': row.d_asunto, 'd_number': row.d_number} for row in data]

        # Cierra la conexión a la base de datos
        cursor.close()
        connectionql.close()

        # Devuelve los datos en formato JSON
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
