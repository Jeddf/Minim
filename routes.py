from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    with sqlite3.connect("counts1.db") as conn:
        cursin = conn.cursor()
        sites=['VICE']
        logs={}
        for site in sites:
            cursin.execute("""SELECT word
                               FROM wordage
                               ORDER BY count DESC
                               LIMIT 10""")
            logs[site] = cursin.fetchall()
            cursin.execute("""SELECT count
                                FROM wordage
                                ORDER BY count DESC
                                LIMIT 10""")
            logs[site].extend(cursin.fetchall())
    
    return render_template('home.html', logs=logs, sites=sites)

if __name__ == '__main__':
    print "ip: 192.3.90.43"
    app.debug = True
    app.run(host='0.0.0.0')