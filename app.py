from hashlib import sha3_256
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# === Определение варианта ===
study_group = "БИ211"  # поменяй при необходимости
fullname = "Ялтонская Екатерина Максимовна"
suffix = "ИТКС. Лабораторная работа 1"
string_for_hash = f"{study_group} {fullname} {suffix}"
var_total = 3
variant = int(sha3_256(string_for_hash.encode("utf-8")).hexdigest(), 16) % var_total + 1
print("Variant:", variant)

# === Подключение к БД (берём из переменной окружения) ===
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    # На проде лучше падать с ошибкой. Для отладки допустим fallback, но в compose мы зададим DATABASE_URL.
    db_url = "sqlite:///dev.sqlite3"
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# === Модель ===
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# === Базовые маршруты ===
@app.route("/")
def index():
    return "Service is up. Variant: {}".format(variant)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

# === CRUD: начнём с 2-х endpoints (остальные добавишь по шагам) ===
@app.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "done": t.done} for t in tasks])

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True, silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify(error="title is required"), 400
    task = Task(title=title, done=bool(data.get("done", False)))
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "done": task.done}), 201

#new

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        # 404, если id не существует
        return jsonify(error="task not found"), 404

    data = request.get_json(silent=True) or {}
    # Обновляем только разрешённые поля
    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            return jsonify(error="title must be a non-empty string"), 400
        task.title = title.strip()

    if "done" in data:
        # принимаем true/false
        if not isinstance(data["done"], bool):
            return jsonify(error="done must be boolean"), 400
        task.done = data["done"]

    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "done": task.done}), 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(error="task not found"), 404
    db.session.delete(task)
    db.session.commit()
    # Тело не нужно, 204 говорит «успешно, но без содержимого»
    return ("", 204)

if __name__ == "__main__":
    # 0.0.0.0 важно для работы в контейнере
    app.run(host="0.0.0.0", port=5000)
