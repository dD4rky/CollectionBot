import os 
import fastapi
from pydantic import BaseModel
import json

import logging

logger = logging.getLogger(__name__)
FORMAT = '[%(asctime)s]\t%(message)s'
logging.basicConfig(filename='log.log', format=FORMAT)

class Statistic():
    data : dict
    filepath : str

    def __init__(self, filepath : str = "data.json"):
        data_dir = os.environ["data_dir"]
        self.filepath = os.path.join(data_dir, filepath)
        
        if not os.path.isfile(self.filepath):
            with open(self.filepath, "w+") as f:
                json.dump({}, f, indent=4)
        self.load()

    def __call__(self, user_id, msg):
        if user_id in self.data.keys():
            self.data[user_id]["messages"].append(msg)
            self.data[user_id]["count"] = len(self.data[user_id]["messages"])
        else:
            self.data[user_id] = {
                "messages": [msg],
                "count": 1 
            }
        self.save()

    def load(self):
        with open(self.filepath, "r") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

class PostMessage(BaseModel):
    user_id : str
    msg : str

app = fastapi.FastAPI(debug=False)
statistic = Statistic()

@app.post("/message")
def message(request : PostMessage):
    global statistic
    
    statistic(request.user_id, request.msg)