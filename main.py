from flask import Flask, jsonify, request, render_template
import pyodbc

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_CONFIG = {
    'server': "191.239.122.127",  # Dirección IP del servidor SQL
    'database': "FNA",
    'username': "FNA",
    'password': "D0cUm3nT2024*.",
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

@app.route('/data/<cedula>')
def getByCedula(cedula):
    try:
        # Establece la conexión a la base de datos
        connectionql = connection()
        cursor = connectionql.cursor()

        # Ejecuta la consulta SQL para obtener los datos
        query = f"SELECT inv_number, d_asunto, d_number FROM inventoryview WHERE d_number LIKE '%{cedula}%'"
        cursor.execute(query)

        # Obtiene los resultados de la consulta
        data = cursor.fetchall()

        # Convierte los resultados en un formato JSON
        result = [{'inv_number': row.inv_number, 'd_asunto': row.d_asunto, 'd_number': row.d_number} for row in data]

        # Cierra la conexión a la base de datos
        cursor.close()
        connectionql.close()

        # Verifica el tipo de solicitud: JSON o texto plano
        if 'application/json' in request.headers.get('Accept', ''):
            return jsonify(result)
        else:
            # Si la solicitud no acepta JSON, devolver texto plano
            result_text = '\n'.join([f"Inv Number: {row['inv_number']}, Asunto: {row['d_asunto']}, D Number: {row['d_number']}" for row in result])
            return result_text

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)