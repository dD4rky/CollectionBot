import fastapi
import os 
from pydantic import BaseModel
import json

import logging

logger = logging.getLogger(__name__)
FORMAT = '[%(asctime)s]\t%(message)s'
logging.basicConfig(format=FORMAT)


class StatisticUnit(BaseModel):
    user_id : str
    data : str
    data_type : str
    length : int
    time : int
    

class Statistic():
    data : dict
    filepath : str

    def __init__(self, filepath : str = "message_history.json"):
        data_dir = os.environ["data_dir"]
        self.filepath = os.path.join(data_dir, filepath)
        
        if not os.path.isfile(self.filepath):
            with open(self.filepath, "w+") as f:
                json.dump({}, self.filepath, indent=4)
        self.load()

    def add(self, statistic_unit : StatisticUnit):
        if not statistic_unit["user_id"] in self.data.keys():
            self.data[statistic_unit["user_id"]] = {
                "messages": [],
                "count": 0 
            }
        self.data[statistic_unit["user_id"]]["messages"].append(statistic_unit)
        self.data[statistic_unit["user_id"]]["count"] = len(self.data[statistic_unit["user_id"]]["messages"])
        self.save()

    def load(self):
        with open(self.filepath, "r") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_filepath(self):
        return self.filepath


app = fastapi.FastAPI(debug=False)
statistic = Statistic()

@app.post("/message")
def message(statistic_unit : StatisticUnit):
    global statistic
    
    data = {
        "user_id" : statistic_unit.user_id,
        "data" : statistic_unit.data,
        "data_type" : statistic_unit.data_type,
        "length" : statistic_unit.length,
        "time" : statistic_unit.time
    } 

    statistic.add(data)

@app.get("/get_statistic_file")
def get_statistic_file():
    global statistic

    filepath = statistic.get_filepath()

    return fastapi.responses.FileResponse(path=filepath, 
                                          filename="statistic.json")