from flask import Flask, render_template, request # render_template renders an html page
from sqlalchemy import create_engine, text

app = Flask(__name__)
# Connection string format: mysql://user:password@server/database
conn_str = "mysql://root:cset155@localhost/boatdb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/boats')
def boats():
    boats = conn.execute(text('SELECT * FROM boats')).all()
    return render_template('boats.html', boats = boats[:10])

@app.route('/boatCreate', methods = ['GET'])
def getBoat():
    return render_template('boat_create.html')

@app.route('/boatCreate', methods = ['POST'])
def createBoat():
    try:
        conn.execute(text('INSERT INTO boats VALUES(:id, :name, :type, :owner_id, :rental_price)'), request.form)
        return render_template('boat_create.html', error = None, success = "Successful")
    except:
        return render_template('boat_create.html', error = "Failed", success = None)

@app.route('/<name>')
def greeting(name):
    return render_template('user.html', user = name) # var "user" is passed from user.html

if __name__ == '__main__':
    app.run(debug=True)
