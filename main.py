from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/pythonreactdb"
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users


@app.route("/users", methods=["GET"])
def getUsers():
    users = []

    for doc in db.find():
        users.append({
            "_id": str(ObjectId(doc["_id"])),
            "username": doc["username"],
            "email": doc["email"],
            "password": doc["password"]
        })
    return jsonify(users)


@app.route("/users", methods=["POST"])
def crea_user():
    #print(request.json)
    usuario_insertado = db.insert_one({
        "username": request.json["username"],
        "email": request.json["email"],
        "password": request.json["password"]
    })
    print(usuario_insertado.inserted_id)
    return jsonify({"id": str(usuario_insertado.inserted_id)})


@app.route("/user/<id>", methods=["GET"])
def getUser(id):
    user = db.find_one({"_id": ObjectId(id)})
    return jsonify({
        "_id": str(ObjectId(user["_id"])),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"]
    })


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    db.delete_one({"_id": ObjectId(id)})
    return jsonify({"mensaje":"usuario eliminado"})


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    print(id)
    print(request.json)
    db.update_one({"_id": ObjectId(id)}, {"$set": {
        "username": request.json["username"],
        "password": request.json["password"],
        "email": request.json["email"]
    }})
    return jsonify({"mensaje":"usuario actualizado"})


if __name__ == "__main__":
    app.run(debug=True)
