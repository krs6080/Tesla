from flask import request, redirect, render_template, Blueprint, current_app, app, Flask
import requests, json
import pymongo

app = Flask(__name__, template_folder="templates")

mongo_url = "mongodb://34.224.93.45:27017"
client = pymongo.MongoClient(mongo_url)
db = client.tesla
collection = db.tesla_Models

tesla_models = [
    {"model": "Model S", "image_url": "https://digitalassets.tesla.com/tesla-contents/image/upload/h_1800,w_1800,c_fit,f_auto,q_auto:best/Model-S-Exterior-Hero-Mobile-Global"},
    {"model": "Model X", "image_url": "https://digitalassets.tesla.com/tesla-contents/image/upload/h_750,w_750,c_fit,f_auto,q_auto:best/Model-X-Exterior-Hero-Mobile-Global"},
    {"model": "Model 3", "image_url": "https://www.tesla.com/ownersmanual/images/GUID-BEE67A59-6DD7-460C-9C49-0DD47E707A02-online-en-US.png"},
    {"model": "Model Y", "image_url": "https://digitalassets.tesla.com/tesla-contents/image/upload/h_600,w_1934,c_fit,f_auto,q_auto:best/Model-Y-Order-Hero-Desktop-Mobile-Global"},
    {"model": "Semi", "image_url": "https://digitalassets.tesla.com/tesla-contents/image/upload/h_750,w_1320,c_fit,f_auto,q_auto:best/Semi-Specs-Mobile-Global"}
]

@app.route("/")
def index():
    data = requests.get("http://107.23.165.101/getdata").json()
    return render_template("index.html", data = data)

@app.route("/submit", methods= ["POST"])
def submit():
    data = None
    if request.form:
        data = request.form
    elif request.data:
        data = request.data

    try:
        data = json.loads(data)
    except: pass

    print(data)

    model_number = data.get("model")

    result = collection.insert_one({"model": model_number})
    print(f"Inserted document with ID: {result.inserted_id}")

    # Redirect to /getdata with the model number as a query parameter
    return redirect(f"/getdata?model={model_number}")

#getdata route goes on middleware --> http:// ec2 instance/getdata

@app.route("/getdata")
def getdata():
      #data = " bhu"
      #return {"test":"b", "data": data}

    # Retrieve the model number from the query parameters
    model_number = request.args.get("model", "")

    # Find the model in the tesla_models list
    model_info = next((m for m in tesla_models if m["model"].lower() == model_number.lower()), None)

    if model_info:
        # Include the image URL in the response
        data = {"test": "b", "data": f"Model Number: {model_number}", "image_url": model_info["image_url"]}

        # Check if the request wants JSON response
        if request.headers.get('Accept') == 'application/json':
            return jsonify(data)
        else:
            return render_template("index.html", data=data)
    else:
        return {"error": "Model not found"}

if __name__ == "__main__": 
        app.run(debug = True, port = 80, host = "0.0.0.0") 
