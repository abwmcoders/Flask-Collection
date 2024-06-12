from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods= ["GET", "POST"])
def welcome():
    name = ''
    food = ''
    if request.method == "POST" and 'username' in request.form:
        name = request.form.get('username')
        food = request.form.get('food')
        print(name)
    return render_template("index.html", name=name, food=food)

@app.route("/profile")
def profile():
    return "Welcome to the flask backend development profile page"

@app.route("/services")
def services():
    return "Welcome to the flask backend development services page"

@app.route("/method", methods=['GET', "POST"])
def method():
    if request.method == "Post":
        return "You are using the POST method of this website"
    else:
        return "You are using the GET method of this website"


app.run()