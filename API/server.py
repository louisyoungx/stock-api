from flask import Flask
import json
from Update.getData import getMonthData_tushare

app = Flask(__name__)

@app.route('/<stock_id>')
def getJsonData(stock_id):
    if stock_id is None:
        return 'ERROR'
    data = getMonthData_tushare(stock_id)
    # print(data)
    return json.dumps(data)
