from flask import Flask, render_template, request, url_for, redirect, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "yoursecretkey"
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
            desc = []
            for temp in temps:
                balls.append(temp[0])
                times.append(temp[1])
                desc.append(temp[2])

            amounts = [int(ball)*180 for ball in balls]
        
        if len(names) == 0:
            return render_template("index.html")

        return render_template("index.html", names=names, balls=balls, desc = desc, times=times, amounts=amounts)
    
    except Exception as e:
        return f"Error: {e}"

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        if request.form.get("key") == "Cheateruzair1133":
          session["auth"] = True
          return redirect(url_for("management"))
        else:
            wrong = "WRONG KEY!"
            return render_template("login.html", wrong=wrong)
        
    return render_template("login.html")

@app.route("/management", methods=["GET", "POST"])
def management():

    if not session.get("auth"):
        invalid = "You must enter key first."
        return redirect(url_for("first", invalid=invalid))

    with open("balls.json", 'r') as f:
        dic = json.load(f)
        names = list(dic.keys())
        temps = list(dic.values())
        balls = [t[0] for t in temps]
        times = [t[1] for t in temps]
        desc = [t[2] for t in temps]
        amounts = [ball*180 for ball in balls]
    
    if len(names) == 0:
        return render_template("management.html")
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "add":
            new_name = request.form.get("new_name")
            new_balls = int(request.form.get("new_balls"))
            new_desc = request.form.get("new_desc")
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
            dic[new_name] = [new_balls, current_time, new_desc]

        elif action == "update":
            name = request.form.get("name")
            ball = int(request.form.get("balls"))
            time = datetime.now().strftime("%d-%m-%Y %H:%M")
            desc = dic[name][2]
            dic[name] = [ball, time, desc]
        
        else:
            name = request.form.get("name")
            dic.pop(name)

        with open("balls.json", 'w') as f:
           json.dump(dic, f, indent=4)
        
        return redirect(url_for("first"))
           
    names = list(dic.keys())
    temps = list(dic.values())
    balls = [t[0] for t in temps]
    times = [t[1] for t in temps]
    desc = [t[2] for t in temps]
    amounts = [int(ball) * 180 for ball in balls]

    return render_template("management.html", names=names, balls=balls, desc=desc, times=times, amounts=amounts)


if __name__ == "__main__":
    app.run(debug=True)