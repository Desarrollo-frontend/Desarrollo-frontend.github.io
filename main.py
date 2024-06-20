from flask import Flask, jsonify, request, render_template
import pyodbc
import os


def crear_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    DATABASE_CONFIG = {
        'server': os.getenv('DB_SERVER', '191.239.122.127'),  # Dirección IP del servidor SQL
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

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/data/', methods=['GET', 'POST'])
    def getByCedula():
        if request.method == 'GET':
            return jsonify({'message': 'Utilice el formulario para enviar una cedula'}), 400
        
        cedula = request.form.get('cedula', '')

        if not cedula:
            return jsonify({'error': 'Especifique un número de cedula'}), 400

        try:
            # Establece la conexión a la base de datos
            connectionql = connection()
            cursor = connectionql.cursor()

            # Ejecuta la consulta SQL para obtener los datos
            query = "SELECT inv_number, d_asunto, d_number FROM inventoryview WHERE d_number LIKE ?"
            cursor.execute(query, f'%{cedula}%')

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
    return app

if __name__ == "__main__":
    app.run(debug=True, port=5000)
