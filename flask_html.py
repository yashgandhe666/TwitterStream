from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, TEXT
import json
import csv
from math import ceil

app = Flask(__name__) 
mongo_object = MongoClient('localhost', 27017)
db = mongo_object['twitterdb']
collection = db['twitter_search']

#Logic of the Pagination Function
def paginate(offset, limit, total):
    if (offset+limit) >= total:
        flag1 = 0
    else:
        flag1 = 1

    if offset == 0:
        flag2 = 0
    else:
        flag2 = 1
    
    return [flag1, flag2]

@app.route('/', methods = ['GET'])
def pymongo_data_display():
    #Paginate the main page as well as display all the relevant filter categories
    offset = int(request.args.get('offset', default=0))
    limit = int(request.args.get('limit', default=10))
    starting_id = collection.find().sort('_id', 1)
    last_id = starting_id[offset]['_id']
    cursor = collection.find({'_id': {'$gte': last_id}}).sort('_id', 1).limit(limit)    
    result = []
    for i in cursor:
        result.append(i)
    #generating the next and previous urls
    next_url = '/?limit=' + str(limit) +'&offset=' + str(offset+limit)
    previous_url = '/?limit=' + str(limit) +'&offset=' + str(offset-limit)

    total = ceil(collection.find().count()/10)*10
    [flag1, flag2] = paginate(offset, limit,total)

    return render_template('test.html', result=result, next_url = next_url, previous_url= previous_url, flag1= flag1, flag2 = flag2)

#Displaying search results
@app.route('/search_data', methods = ['POST'])
def search_data():
    form_text=str(request.form["text"])
    select_list = request.form.getlist("search_filter")
    select_list = str(select_list[0])
    print (select_list)
    # cursor = collection.find({"$or": [{'text':{'$regex':form_text}}, {'username': {'$regex':form_text}},{'name': {'$regex':form_text}},{'language': {'$regex':form_text}}]})
    cursor = collection.find({select_list: {'$regex': form_text}})
    return render_template('result.html', result = cursor)

#Method for action after applying int filters
@app.route('/filter_count', methods =['POST'])
def filter_count():    
    int_data = request.form["range_filter"].split("-")
    option_data = request.form.getlist("filters")
    int_data = [int(y) for y in int_data ]
    option_data = str(option_data[0])
    cursor = collection.find({option_data:{'$gte':int_data[0], '$lte':int_data[1]}})
    result = []
    for i in cursor:
        result.append(i)
    
    #exporting to csv (API 3)
    for tweet in result:
        try:
            saveFile = open('export.csv', 'a')
            t = tweet['text']
            t_mod = t.replace('\"', '\"\"')
            saveFile.write(
                "\"" + t_mod + "\"" + ',' +
                tweet['created_at'] + ',' + str(tweet['username']) + ',' + str(tweet['tweet_id']) + ',' + str(tweet['retweets']) + ',' +
                str(tweet['favourites']) + ',' + str(tweet['followers'])
            )
            saveFile.write("\n")
            saveFile.close()
        except:
            saveFile = open('export.csv', 'a')
            saveFile.write("Data in incorrect format")
            saveFile.write('\n')
            saveFile.close()


    return render_template('result.html', result = result)

# Method for sorting the data
@app.route('/sorted_data', methods=['POST'])
def sorted_data():
    sort = request.form.getlist('sorted')
    sort = str(sort[0])
    cursor = collection.find().sort(sort)      
    return render_template('result.html', result = cursor)

@app.route('/exact', methods=['POST'])
def exact():
    sort1 = str(request.form.getlist('exact_choice')[0])
    sort2 = str(request.form.getlist('parameter')[0])
    text_field = str(request.form['field'])

    if sort1 == 'start':
        cursor = collection.find({sort2:{'$regex':'^'+ text_field}})
    elif sort1 == 'end':
        cursor = collection.find({sort2:{'$regex': text_field+'$'}})
    elif sort1 == 'exact':
        cursor = collection.find({sort2:{'$regex':'^' + text_field + '$'}})
    return render_template('result.html', result = cursor)


if __name__ == '__main__': 
        app.run()