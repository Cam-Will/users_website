from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
@app.route("/users")
def index():
    mysql = connectToMySQL('users_schema')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM users_schema.users;')  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("Read (All).html", users = users)
            

@app.route("/users/new", methods=["POST"]) 
def add_friend_to_db():
    mysql = connectToMySQL("users_schema")
    query = "INSERT INTO users_schema.users (first_name, last_name, email, created_at, updated_at) VALUES(%(fn)s, %(ln)s, %(email)s, NOW(), NOW());"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "email": request.form["email"]
    }
    mysql.query_db(query, data)
    return redirect("/users")

@app.route("/users/new")
def create_new():
    return render_template("Create.html")

@app.route("/users/<id>")
def read_one(id):
    mysql = connectToMySQL("users_schema")
    query = "SELECT * FROM users_schema.users WHERE id = %(user_id)s;"
    data = {"user_id": id}
    user = mysql.query_db(query, data)
    print(user)
    return render_template("Read (One).html", user = user[0])

@app.route("/users/<id>/edit", methods=["POST"])
def edit_one(id):
    mysql = connectToMySQL("users_schema")
    query = "UPDATE `users_schema`.`users` SET `first_name` = %(first)s, `last_name` = %(last)s, `email` = %(email)s, `updated_at` = NOW() WHERE (`id` = %(user_id)s);"
    data = {"first": request.form["fname"],
            "last" : request.form["lname"],
            "email": request.form["email"],
            "user_id": id
    }
    user = mysql.query_db(query, data)
    print(user)
    return redirect(f"/users/{id}")

@app.route("/users/<id>/edit")
def edit(id):
    mysql = connectToMySQL("users_schema")
    query = "SELECT * FROM users_schema.users WHERE id = %(user_id)s;"
    data = {"user_id": id}
    user = mysql.query_db(query, data)
    print(user)
    return render_template("Edit.html", user = user[0])

@app.route("/users/<id>/destroy")
def delete_user(id):
    mysql = connectToMySQL("users_schema")
    query = "DELETE FROM `users_schema`.`users` WHERE (`id` = %(user_id)s);"
    data = {"user_id": id}
    mysql.query_db(query, data)
    return redirect("/users") 

if __name__ == "__main__":
    app.run(debug = True)