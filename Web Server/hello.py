from flask import Flask
from io import BytesIO, StringIO

import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/data/<tablename>')
def get_csv(tablename):
    df_pd = pd.DataFrame({'aaa': [1,2,3],'aab':[4,5,6]})
    
    # Create buffer
    csv_buffer = StringIO()
    
    # Write dataframe to buffer
    df_pd.to_csv(csv_buffer, sep=";", index=False)
    
    return_string = csv_buffer.getvalue()
    
    return return_string

if __name__ == '__main__':
    app.run()