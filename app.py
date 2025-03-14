from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb+srv://ruslansyciov:S5EeQs83voUpylD7@cluster0.pxeux.mongodb.net/")
db = client['eventsDB']
events_collection = db['events']


@app.route('/')
def index():
    events = events_collection.find()
    events_list = []
    for event in events:
        event['_id'] = str(event['_id'])
        events_list.append(event)

    return render_template('index.html', events=events_list)


@app.route('/add_event', methods=['GET'])
def add_event():
    name = request.args.get('name')
    date_str = request.args.get('date')

    if name and date_str:
        event_date = datetime.strptime(date_str, "%m-%d")

        events_collection.insert_one({
            'name': name,
            'date': event_date
        })

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
