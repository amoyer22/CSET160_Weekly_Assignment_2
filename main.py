from flask import Flask, render_template, request # render_template renders an html page
from sqlalchemy import create_engine, text

app = Flask(__name__)
# Connection string format: mysql://user:password@server/database
conn_str = "mysql://root:cset155@localhost/boatdb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/boats')
def boats():
    boats = conn.execute(text('SELECT * FROM boats')).all()
    return render_template('boats.html', boats = boats[:10])

@app.route('/create', methods = ['GET'])
def getBoat():
    return render_template('boat_create.html')

@app.route('/create', methods = ['POST'])
def createBoat():
    try:
        conn.execute(text('INSERT INTO boats VALUES(:id, :name, :type, :owner_id, :rental_price)'), request.form)
        return render_template('boat_create.html', error = None, success = "Successful")
    except:
        return render_template('boat_create.html', error = "Failed", success = None)
    
@app.route('/search', methods = ['GET', 'POST'])
def search():
    result = []
    if request.method == 'POST':
        boatID = request.form.get('id')
        if boatID:
            result = conn.execute(text("SELECT * FROM boats WHERE id=:id"), {'id': boatID}).all()
    return render_template('boats_search.html', result = result)


@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        boatID = request.form.get('id')
        name = request.form.get('name')
        boat_type = request.form.get('type')
        owner_id = request.form.get('owner_id')
        rental_price = request.form.get('')
        if boatID:
            result = conn.execute(text("""UPDATE boats SET name=:name, type=:type, owner_id=:owner_id, rental_price=:rental_price WHERE id=:id"""),{
                'id': boatID, 'name': name, 'type': boat_type, 'owner_id': owner_id, 'rental_price': rental_price})
            conn.commit()
            return render_template('boats_update.html', message="Boat updated." if result.rowcount > 0 else "Boat does not exist.")
    return render_template('boats_update.html')

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        boatID = request.form.get('id')
        if boatID:
            result = conn.execute(text("DELETE FROM boats WHERE id=:id"), {'id': boatID})
            conn.commit()
            return render_template('boats_delete.html', message="Boat has been deleted." if result.rowcount > 0 else "Boat does not exist.")
    return render_template('boats_delete.html')

if __name__ == '__main__':
    app.run(debug=True)
