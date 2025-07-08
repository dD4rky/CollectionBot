import fastapi
import os 
from pydantic import BaseModel

import logging

import pandas as pd

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
    df : pd.DataFrame
    filepath : str

    def __init__(self, filepath : str = "message_history.csv"):
        data_dir = os.environ["data_dir"]
        self.filepath = os.path.join(data_dir, filepath)
        
        if not os.path.isfile(self.filepath):
            df = pd.DataFrame(data={"user_id" : [], 
                "data": [],
                "data_type" : [],
                "length" : [],
                "time" : []},
                columns=["user_id", "data", "data_type", "length", "time"])
            df.to_csv(self.filepath, index=False)

        self.load()

    def add(self, statistic_unit : StatisticUnit):
        new_row = pd.DataFrame(data=statistic_unit,
            columns=["user_id", "data", "data_type", "length", "time"])
        
        self.df = pd.concat([self.df, new_row])
        self.save()

    def load(self):
        self.df = pd.read_csv(self.filepath)

    def save(self):
        self.df.to_csv(self.filepath, index=False)

    def get_filepath(self):
        return self.filepath

    def get_last_registration(self):
        return self.df.tail(1).to_dict(orient='list')

app = fastapi.FastAPI(debug=False)
statistic = Statistic()

@app.post("/message")
def message(statistic_unit : StatisticUnit):
    global statistic
    
    data = {
        "user_id" : [statistic_unit.user_id],
        "data" : [statistic_unit.data],
        "data_type" : [statistic_unit.data_type],
        "length" : [statistic_unit.length],
        "time" : [statistic_unit.time]
    } 

    statistic.add(data)

@app.get("/get_statistic_file")
def get_statistic_file():
    global statistic

    filepath = statistic.get_filepath()

    return fastapi.responses.FileResponse(path=filepath, 
                                          filename="statistic.csv")

@app.get("/get_last_statistic_registration") # for regression test
def get_last_statistic_registration():
    global statistic
    
    return statistic.get_last_registration()
