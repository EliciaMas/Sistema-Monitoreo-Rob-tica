from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Conexión obligatoria con MongoDB para persistencia [cite: 13, 24]
client = MongoClient('mongodb://db_mongo:27017/')
db = client.robotica_db
logs = db.eventos

@app.route('/api/log', methods=['POST'])
def log_event():
    data = request.json
    # Registrar cada evento con información relevante [cite: 22]
    evento = {
        "tipo_accion": data.get("accion"),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "datos_asociados": data.get("detalles", "Sin detalles adicionales")
    }
    
    # Guardar en la base de datos MongoDB [cite: 24, 29]
    logs.insert_one(evento)
    return jsonify({"status": "Evento registrado exitosamente"}), 201

@app.route('/api/logs', methods=['GET'])
def get_logs():
    # El frontend consumirá estos datos para el dashboard [cite: 34]
    lista_eventos = list(logs.find({}, {'_id': 0}).sort("timestamp", -1))
    return jsonify(lista_eventos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)