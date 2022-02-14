# Set up flask and python modules precariously, via this website: https://code.visualstudio.com/docs/python/tutorial-flask
# "You now have a self-contained environment ready for writing Flask code. VS Code activates the environment automatically when you use
# Terminal: Create New Terminal. If you open a separate command prompt or terminal, activate the environment by running source
# .venv\Scripts\Activate.ps1 (Windows). You know the environment is activated when the command prompt shows (.venv) at the beginning"

import json
import math
import sqlite3
from flask import Flask, render_template, request, redirect, g
from flask_session import Session
from helpers import usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
Session(app)

app.jinja_env.filters["usd"] = usd

con = sqlite3.connect('zoodatabase.db', check_same_thread=False)

cur = con.cursor() 

cur.execute('''DROP TABLE IF EXISTS phrase_table''')

cur.execute('''CREATE TABLE IF NOT EXISTS phrase_table
         (SYMB          TEXT     NOT NULL,
         SMALL          TEXT     NOT NULL,
         MEDIUM         TEXT     NOT NULL,
         LARGE          TEXT     NOT NULL
         );''')

content = [
        ("BTC", "a small phrase for BTC", "a medium phrase for BTC which is longer", "a large phrase for BTC which is even longer still"),
        ("BNB", "a small phrase for BNB", "a medium phrase for BNB which is longer", "a large phrase for BNB which is even longer still"),
        ("KCS", "a small phrase for KCS", "a medium phrase for KCS which is longer", "a large phrase for KCS which is even longer still"),
        ("FTT", "a small phrase for FTT", "a medium phrase for FTT which is longer", "a large phrase for FTT which is even longer still"),
        ("XRP", "a small phrase for XRP", "a medium phrase for XRP which is longer", "a large phrase for XRP which is even longer still"),
        ("HT", "a small phrase for HT", "a medium phrase for HT which is longer", "a large phrase for HT which is even longer still")
    ]

cur.executemany("INSERT INTO phrase_table (symb, small, medium, large) VALUES (?, ?, ?, ?)", content)
con.commit() 
for row in cur.execute("SELECT * FROM phrase_table"):
    print(row) # prints out all the rows in the phrase_table

apiKey = "XXXX---API-KEY-REMOVED-FOR-SECURITY---XXXX" #removed for security. Contact owner for their API key or get your own from cryptocompare

@app.route("/")
def index():
    return render_template("entrance.html", apiKey=apiKey)

@app.route("/payment-coins")
def private():
    return render_template("payment-coins.html", apiKey=apiKey)

@app.route("/public-coins")
def public():
    return render_template("public-coins.html", apiKey=apiKey)

@app.route("/extinct-coins")
def extinct():
    return render_template("extinct-coins.html", apiKey=apiKey)

@app.route("/governance-tokens")
def governance():
    return render_template("governance-tokens.html", apiKey=apiKey)

@app.route("/etfx-platform")
def etfx_platform():
    if request.args.get("bp"):
        bpString = request.args.get("bp")
        bpDict = json.loads(bpString)
        description = []
        sizes = ["SMALL", "MEDIUM", "LARGE"]
        print("...second print...")
        for key in bpDict:
            cur.execute('SELECT [%s] FROM phrase_table WHERE SYMB = ?' % (sizes[math.floor(bpDict[key] / 2)],), (key,))
            phrase = cur.fetchall()
            description.append(phrase)
        return render_template("etfx-platform.html", description=description, apiKey=apiKey)
    else:
        return render_template("etfx-platform.html", apiKey=apiKey)

@app.route("/privacy-coins")
def privacy():
    return render_template("privacy-coins.html", apiKey=apiKey)

@app.route("/security-tokens")
def security():
    return render_template("security-tokens.html", apiKey=apiKey)

@app.route("/stable-coins")
def stable():
    return render_template("stable-coins.html", apiKey=apiKey)

@app.route("/sustainable-coins")
def sustainable():
    return render_template("sustainable-coins.html", apiKey=apiKey)

@app.route("/utility-tokens")
def utility():
    return render_template("utility-tokens.html", apiKey=apiKey)