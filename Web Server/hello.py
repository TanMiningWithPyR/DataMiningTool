from flask import Flask, request
from io import BytesIO, StringIO

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import base64
import os

app = Flask(__name__)
# app.debug = True

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/get_image/<plotname>')
def get_image(plotname):
    df_data_pd = pd.DataFrame(
            {'aaa': [1,2,3],
             'aab':[4,5,6]}
            )
    plt.plot(df_data_pd)   
    # 写入内存，py3 BytesIO()
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    # img转义base64编码
    # img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
    return img_buffer.getvalue()

@app.route('/send_image/<plotname>', methods=["POST"])
def send_image(plotname):
	# print(os.getcwd())
	if request.method=='POST':
		# print("Posted image: {}".format(request.files['image']))
		# image = request.files['image']
		# images = {'image': image.read()}
		# r = requests.post("http://127.0.0.1:8000/upload/", files=images)

		# if r.ok:
		# 	return "File uploaded!"
		# else:
		# 	return "Error uploading file!"

		# img_buffer = BytesIO(request.files['image'])		
		# with open(os.path.join(os.getcwd(),'test.png'), 'wb') as f:
		# 	f.write(img_buffer.getvalue())

		# img转义base64编码
		# img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
		# print(type(request.files['image']))
		request.files['image'].save(os.path.join(os.getcwd(),'test.png'))
		return "Server received image!"

@app.route('/get_data/<tablename>')
def get_csv(tablename):
    df_tablename_pd = pd.DataFrame(
            {'表名':['dict_aaaa_aaaa'],
             '数据来源':['test'],
             '原始表名':['test'],
             '表结构创建人':['谭夫有'],
             '创建时间':['2019/5/14'],
             '主键字段':['aaa'],
             '第一索引字段':[np.nan],
             '第二索引字段':[np.nan],
             '第三索引字段':[np.nan],
             '表内容描述':['test'],
             '表的层级':['0'],
             '中文释义':['测试'],
             '英文释义':['test'],
             '选中':[0],
             '已创建':[0],
             '已导入':[0]}
            ) 
    df_tablestructure_pd = pd.DataFrame(
            {'字段ID':['dict_aaaa_aaaa.aaa','dict_aaaa_aaaa.aab'],
             '字段名':['aaa','aab'],
             '字段类型':['CHAR','INT'],
             '字段宽度':['1',np.nan],
             '精度':[np.nan,np.nan],
             '索引顺序':[np.nan,np.nan],
             '索引类型':[np.nan,np.nan],
             '英文释义':['column1','column2'],
             '中文释义':['第一列','第二列'],
             '字段来源':[np.nan,np.nan],
             '备注':[np.nan,np.nan],
             '表名':['dict_aaaa_aaaa','dict_aaaa_aaaa']}
            )
    df_data_pd = pd.DataFrame(
            {'aaa': [1,2,3],
             'aab':[4,5,6]}
            )
    
    # Create buffer
    csv_tablename_buffer = StringIO()
    csv_tablestructure_buffer = StringIO()
    csv_data_buffer = StringIO()
    
    # Write dataframe to buffer
    df_tablename_pd.to_csv(csv_tablename_buffer, sep=";", index=False)
    df_tablestructure_pd.to_csv(csv_tablestructure_buffer, sep=";", index=False)
    df_data_pd.to_csv(csv_data_buffer, sep=";", index=False)
    
    return_string = "##".join([csv_tablename_buffer.getvalue(),
    	csv_tablestructure_buffer.getvalue(),
    	csv_data_buffer.getvalue()])
    
    return return_string

@app.route('/send_data/<tablename>',methods=["POST"])
def post_csv(tablename):
	if request.method=='POST':
		send_string = request.form['text'] 
		send_string_list = send_string.split('##')
		# Create buffer
		csv_tablename_buffer = StringIO(send_string_list[0])
		csv_tablestructure_buffer = StringIO(send_string_list[1])
		csv_data_buffer = StringIO(send_string_list[2])

		df_tablename_pd = pd.read_csv(csv_tablename_buffer, sep = ';')
		df_tablestructure_pd = pd.read_csv(csv_tablestructure_buffer, sep = ';')
		df_data_pd = pd.read_csv(csv_data_buffer, sep = ';')
		#print(df_tablename_pd)   
		#print(df_tablestructure_pd)
		print(df_data_pd)    
		return "Server received data!"

if __name__ == '__main__':
    app.run()