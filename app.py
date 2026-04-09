from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import date

app = Flask(__name__)
DATA_FILE = "data.json"

DEFAULT_DATA = {"car_name": "Meu Carro", "current_km": 52000, "items": [{"id": 1, "category": "Motor", "name": "Troca de oleo", "km": 5000, "last_km": 47000, "last_date": "2024-01-10"}, {"id": 2, "category": "Motor", "name": "Filtro de oleo", "km": 5000, "last_km": 47000, "last_date": "2024-01-10"}, {"id": 3, "category": "Motor", "name": "Filtro de ar", "km": 15000, "last_km": 40000, "last_date": "2023-06-01"}, {"id": 4, "category": "Freios", "name": "Pastilhas dianteiras", "km": 30000, "last_km": 25000, "last_date": "2022-09-15"}, {"id": 5, "category": "Freios", "name": "Pastilhas traseiras", "km": 40000, "last_km": 15000, "last_date": "2022-09-15"}, {"id": 6, "category": "Pneus", "name": "Rodizio de pneus", "km": 10000, "last_km": 44000, "last_date": "2023-11-20"}, {"id": 7, "category": "Pneus", "name": "Alinhamento", "km": 10000, "last_km": 44000, "last_date": "2023-11-20"}, {"id": 8, "category": "Fluidos", "name": "Fluido de freio", "km": 20000, "last_km": 35000, "last_date": "2023-03-05"}, {"id": 9, "category": "Fluidos", "name": "Liquido de arrefecimento", "km": 40000, "last_km": 15000, "last_date": "2021-07-12"}, {"id": 10, "category": "Eletrica", "name": "Bateria", "km": 60000, "last_km": 0, "last_date": "2021-01-08"}]}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    save_data(DEFAULT_DATA)
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(load_data())

@app.route("/api/km", methods=["POST"])
def update_km():
    data = load_data()
    data["current_km"] = request.json["km"]
    save_data(data)
    return jsonify({"ok": True})

@app.route("/api/car_name", methods=["POST"])
def update_car_name():
    data = load_data()
    data["car_name"] = request.json["name"]
    save_data(data)
    return jsonify({"ok": True})

@app.route("/api/item/done/<int:item_id>", methods=["POST"])
def mark_done(item_id):
    data = load_data()
    for item in data["items"]:
        if item["id"] == item_id:
            item["last_km"] = data["current_km"]
            item["last_date"] = str(date.today())
            break
    save_data(data)
    return jsonify({"ok": True})

@app.route("/api/item", methods=["POST"])
def add_item():
    data = load_data()
    body = request.json
    new_id = max((i["id"] for i in data["items"]), default=0) + 1
    data["items"].append({"id": new_id, "category": body["category"], "name": body["name"], "km": int(body["km"]), "last_km": data["current_km"], "last_date": str(date.today())})
    save_data(data)
    return jsonify({"ok": True})

@app.route("/api/item/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    data = load_data()
    data["items"] = [i for i in data["items"] if i["id"] != item_id]
    save_data(data)
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
