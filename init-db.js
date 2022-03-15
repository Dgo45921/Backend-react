db = db.getSiblingDB("users_db");
db.users_db.drop();

db.users_db.insertMany([
    {
        "username": "user prueba",
        "email": "aaaa@gmail.com",
        "password": "1234"
    }
]);


