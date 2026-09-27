from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Employee

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "codecraft-task2-secret-key"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Employee Management System - Task 2"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == "admin@example.com" and password == "admin123":
            return "Login successful!"

        return "Invalid email or password."

    return render_template("login.html")

@app.route("/employees")
def employees():
    employee_list = Employee.query.all()
    return render_template("employees.html", employees=employee_list)

@app.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        position = request.form["position"]

        new_employee = Employee(
            name=name,
            email=email,
            department=department,
            position=position
        )

        db.session.add(new_employee)
        db.session.commit()

        return redirect("/employees")

    return render_template("add_employee.html")

@app.route("/employees/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)

    if request.method == "POST":
        employee.name = request.form["name"]
        employee.email = request.form["email"]
        employee.department = request.form["department"]
        employee.position = request.form["position"]

        db.session.commit()

        return redirect("/employees")

    return render_template("edit_employee.html", employee=employee)

@app.route("/employees/delete/<int:id>")
def delete_employee(id):
    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    return redirect("/employees")

if __name__ == "__main__":
    app.run(debug=True)
