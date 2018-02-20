from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, TEXT
from bson import json_util, ObjectId
import json

app = Flask(__name__) 
mongo_object = MongoClient('localhost', 27017)
db = mongo_object['twitterdb']
collection = db['twitter_search']
 
@app.route('/', methods = ['GET'])
def pymongo_data_display():
    cursor = collection.find({})
    json_docs = []
    return render_template('test.html', result=cursor)

#Displaying search results
@app.route('/search_data', methods = ['POST'])
def search_data():
    form_text=request.form["text"]
    cursor = collection.find({'text':{'$regex':form_text}})
    return render_template('result.html', result = cursor)

#Method for action after applying filters
@app.route('/filter_count', methods =['POST'])
def filter_count():
    int_data = request.form["range_filter"].split("-")
    option_data = request.form.getlist("filters")
    int_data = [int(y) for y in int_data ]
    option_data = str(option_data[0])
    cursor = collection.find({option_data:{'$gt':int_data[0], '$lt':int_data[1]}})
    return render_template('favourites.html', result = cursor)

# Method for sorting the data
@app.route('/sorted_data', methods=['POST'])
def sorted_data():
    sort = request.form.getlist('sorted')
    sort = str(sort[0])
    cursor = collection.find().sort(sort)      
    return render_template('favourites.html', result = cursor)

if __name__ == '__main__': 
        app.run()