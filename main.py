from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId, MongoClient
from flask_cors import CORS

#cluster = "mongodb+srv://Diego:1234@cluster0.irkae.mongodb.net/users?retryWrites=true&w=majority"
#client = MongoClient(cluster)

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost/pythonreactdb"
# mongo = PyMongo(app)

CORS(app)

#db = client.users.users


def getBD():
    client = MongoClient(
    host="users_mongodb",
    port=27017,
    username="root",
    password="pass",
    authSource="admin"
    )
    db = client["users_db"]
    return db


@app.route("/")
def saludar():
    return "Estoy corriendo"


@app.route("/users", methods=["GET"])
def getUsers():
    db = getBD()
    users = []
    for doc in db.users_db.find():
        users.append({
            "_id": str(ObjectId(doc["_id"])),
            "username": doc["username"],
            "email": doc["email"],
            "password": doc["password"]
        })
    return jsonify(users)


@app.route("/users", methods=["POST"])
def crea_user():
    db = getBD()
    usuario_insertado = db.users_db.insert_one({
        "username": request.json["username"],
        "email": request.json["email"],
        "password": request.json["password"]
    })
    print(usuario_insertado.inserted_id)
    return jsonify({"id": str(usuario_insertado.inserted_id)})


@app.route("/user/<id>", methods=["GET"])
def getUser(id):
    db = getBD()
    user = db.users_db.find_one({"_id": ObjectId(id)})
    return jsonify({
        "_id": str(ObjectId(user["_id"])),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"]
    })


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    db = getBD()
    db.users_db.delete_one({"_id": ObjectId(id)})
    return jsonify({"mensaje": "usuario eliminado"})


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    db = getBD()
    print(id)
    print(request.json)
    db.users_db.update_one({"_id": ObjectId(id)}, {"$set": {
        "username": request.json["username"],
        "password": request.json["password"],
        "email": request.json["email"]
    }})
    return jsonify({"mensaje": "usuario actualizado"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
