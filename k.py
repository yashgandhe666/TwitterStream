from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, TEXT
from bson import json_util, ObjectId
import json
import pandas as pd
from math import ceil

app = Flask(__name__) 
mongo_object = MongoClient('localhost', 27017)
db = mongo_object['twitterdb']
collection = db['twitter_search']
 
@app.route('/', methods = ['GET'])
def pymongo_data_display():

    offset = int(request.args.get('offset', default=0))
    limit = int(request.args.get('limit', default=10))
    starting_id = collection.find().sort('_id', 1)
    last_id = starting_id[offset]['_id']
    # page = request.args.get(get_page_parameter(), type = int, default = 1)
    cursor = collection.find({'_id': {'$gte': last_id}}).sort('_id', 1).limit(limit)    
    result = []
    for i in cursor:
        result.append(i)
    next_url = '/?limit=' + str(limit) +'&offset=' + str(offset+limit)
    previous_url = '/?limit=' + str(limit) +'&offset=' + str(offset-limit)

    total = ceil(collection.find().count()/10)*10
    print(collection.find().count())
    print(total)
    if (offset+limit) >= total:
        flag1 = 0
    else:
        flag1 = 1

    if offset == 0:
        flag2 = 0
    else:
        flag2 = 1

    # pagination = Pagination(page=page, total=cursor.count(), record_name = 'result')
    # print(pagination.page)
    # print(q)
    return render_template('test.html', result=result, next_url = next_url, previous_url= previous_url, flag1= flag1, flag2 = flag2)

#Displaying search results
@app.route('/search_data', methods = ['POST'])
def search_data():
    form_text=request.form["text"]
    cursor = collection.find({"$or": [{'text':{'$regex':form_text}}, {'username': {'$regex':form_text}},{'name': {'$regex':form_text}}]})
    result = []
    for i in cursor:
        result.append(i)
    return render_template('result.html', result = result)

#Method for action after applying int filters
@app.route('/filter_count', methods =['POST'])
def filter_count():    
    int_data = request.form["range_filter"].split("-")
    option_data = request.form.getlist("filters")
    int_data = [int(y) for y in int_data ]
    option_data = str(option_data[0])
    cursor = collection.find({option_data:{'$gt':int_data[0], '$lt':int_data[1]}})   
    return render_template('result.html', result = cursor)

#Method for action after applying date filter
@app.route('/date_filter', methods =['POST'])
def date_filter():
    int_data = request.form['date_filter'].split('=')
    cursor = collection.find({created_at:{'$gt':int_data[0], '$lt':int_data[1]}})
    result = []
    for i in cursor:
        result.append(i)
    return render_template('result.html', result = cursor)

# Method for sorting the data
@app.route('/sorted_data', methods=['POST'])
def sorted_data():
    sort = request.form.getlist('sorted')
    sort = str(sort[0])
    cursor = collection.find().sort(sort)      
    return render_template('result.html', result = cursor)

if __name__ == '__main__': 
        app.run()