from flask import request, redirect, render_template, Blueprint, current_app, app, Flask
import requests, json
import pymongo

app = Flask(__name__, template_folder="templates")

mongo_url = "mongodb://54.234.20.210:27017"
client = pymongo.MongoClient(mongo_url)
db = client.tesla
collection = db.tesla_Models

tesla_models = [
    {"name": "Model S", "model": "Model_S", "image_url": "https://digitalassets.tesla.com/tesla-contents/image/upload/h_1800,w_1800,c_fit,f_auto,q_auto:best/Model-S-Exterior-Hero-Mobile-Global"},
    {"name": "Model X", "model": "Model_X", "image_url": "https://digitalassets.tesla.com/tesla-contents/image/upload/h_750,w_750,c_fit,f_auto,q_auto:best/Model-X-Exterior-Hero-Mobile-Global"},
    {"name": "Model 3", "model": "Model_3", "image_url": "https://www.tesla.com/ownersmanual/images/GUID-BEE67A59-6DD7-460C-9C49-0DD47E707A02-online-en-US.png"},
    {"name": "Model Y", "model": "Model_Y", "image_url": "https://digitalassets.tesla.com/tesla-contents/image/upload/h_600,w_1934,c_fit,f_auto,q_auto:best/Model-Y-Order-Hero-Desktop-Mobile-Global"},
    {"name": "Semi", "model": "Semi", "image_url": "https://digitalassets.tesla.com/tesla-contents/image/upload/h_750,w_1320,c_fit,f_auto,q_auto:best/Semi-Specs-Mobile-Global"}
]

@app.route("/")
def index():
    
    return render_template("index.html", data = None, tesla_models = tesla_models)

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

    carData = json.loads(requests.get(f"{request.host_url}getdata/{data['model']}").content)
    return render_template("index.html", data = carData, tesla_models = tesla_models)


#getdata route goes on middleware --> http:// ec2 instance/getdata

@app.route("/getdata/<model>")
def getdata(model):

    # Retrieve the model number from the query parameters
    model_number = model

    # Find the model in the tesla_models list
    model_info = next((m for m in tesla_models if m["model"].lower() == model_number.lower()), None)

    if model_info:
        # Include the image URL in the response
        data = {"test": "b", "data": f"Model Number: {model_number}", "image_url": model_info["image_url"]}

        return data
    
    else:
        return {"error": "Model not found"}

if __name__ == "__main__": 
        app.run(debug = True, port = 80, host = "0.0.0.0") 
