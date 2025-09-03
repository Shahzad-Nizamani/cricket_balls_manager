from flask import Flask, render_template, request, url_for, redirect
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def first():

    if request.method == "POST":
            return redirect(url_for("login"))
    try:
        with open("balls.json", 'r') as f:
            dic = json.load(f)
            names = list(dic.keys())
            temps = list(dic.values())
            balls = []
            times = []
            for temp in temps:
                balls.append(temp[0])
                times.append(temp[1])
            amounts = [int(ball)*180 for ball in balls]
        
        if len(names) == 0:
            return render_template("index.html")

        return render_template("index.html", names=names, balls=balls, times=times, amounts=amounts)
    
    except Exception as e:
        return f"Error: {e}"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("key") == "uzaircheater":
          return redirect(url_for("management"))
        else:
            wrong = "WRONG KEY!"
            return render_template("login.html", wrong=wrong)
        
    return render_template("login.html")

@app.route("/management", methods=["GET", "POST"])
def management():

    with open("balls.json", 'r') as f:
        dic = json.load(f)
        names = list(dic.keys())
        temps = list(dic.values())
        balls = []
        times = []
        for temp in temps:
            balls.append(temp[0])
            times.append(temp[1])
        amounts = [ball*180 for ball in balls]
    
    if len(names) == 0:
        return render_template("management.html")
    
    if request.method == "POST":
        new_name = request.form.get("new_name")
        new_balls = int(request.form.get("new_balls"))
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        dic[new_name] = [new_balls, current_time]

        with open("balls.json", 'w') as f:
           json.dump(dic, f, indent=4)
    names = list(dic.keys())
    temps = list(dic.values())
    balls = []
    times = []
    for temp in temps:
        balls.append(temp[0])
        times.append(temp[1])
    amounts = [int(ball) * 180 for ball in balls]
    return render_template("management.html", names=names, balls=balls, times=times, amounts=amounts)


if __name__ == "__main__":
    app.run(debug=True)