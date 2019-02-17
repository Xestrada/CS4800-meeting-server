from flask import Flask, jsonify, request, Response
from flask_restful import Api
from flask_cors import CORS
from sqlite3 import connect

app = Flask(__name__)
CORS(app)
app.debug = True
api = Api(app)

# Enumerate Columns to JSON
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        j = row[idx]
        # If string is in JSON Object or Array format convert
        if type(j) is str and ("{" in j or '[' in j):
            j = eval(j)
        d[col[0]] = j
    return d

def get():
    db = connect('Meetings.db')
    db.row_factory = dict_factory
    cursor = db.cursor()
    cursor.execute('SELECT * from meetings')
    all = cursor.fetchall()
    json = {'meetings': all}
    db.close()
    return jsonify(json)

def post():
    db = connect('Meetings.db')
    cursor = db.cursor()
    data = request.get_json()
    meeting= (str(data['date']),
              str(data['meeting_time']),
              str(data['attended']),
              str(data['topics']),
              str(data['todo']),
              str(data['completed']))
    sql = "INSERT INTO meetings (date, meeting_time, attended, topics, todo, completed) values(?,?,?,?,?,?)"

    cursor.execute(sql, meeting)
    db.commit()
    db.close()
    return Response(
        status=201
    )

def put(id):
    db = connect('Meetings.db')
    cursor = db.cursor()
    data = request.get_json()
    meeting= (str(data['date']),
              str(data['meeting_time']),
              str(data['attended']),
              str(data['topics']),
              str(data['todo']),
              str(data['completed']),
              id)
    sql = "UPDATE meetings SET date=?, meeting_time=?, attended=?, topics=?, todo=?, completed=? WHERE id=?"
    cursor.execute(sql, meeting)
    db.commit()
    return Response(
        status=201
    )

def delete(id):
    db = connect('Meetings.db')
    cursor = db.cursor()
    cursor.execute('DELETE FROM meetings WHERE id=?', id)
    db.commit()
    return Response(
        status=201
    )

@app.route('/meetings', methods=["GET", "POST"])
def meetings():
    if request.method == 'GET':
        return get()
    elif request.method == 'POST':
        return post()

@app.route('/meetings/<id>', methods=['PUT', 'DELETE'])
def updateMeetings(id):
    if request.method == 'PUT':
        return put(id)
    elif request.method == 'DELETE':
        return delete(id)


if __name__ == '__main__':
     app.run(port='5002')