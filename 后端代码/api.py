#version: 1.0 
#9/2

from flask import Flask, render_template, request, make_response, jsonify
from flask_cors import CORS
import os
import json
from sql_class import sql_class
from handleNews import handleNews
app = Flask(__name__)
CORS(app, resources=r'/*')

sql = sql_class()

#获取原数据构建表格(类别-来源-柱状图-原始数据)
@app.route('/getSourceData_histogram/class_source', methods = ['GET', 'POST'])
def getSourceData_histogram_class_source():
    print("getSourceData_histogram_class_source")
    result_text = sql.getSourceData_histogram_class_source("source")
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#获取原数据构建表格(类别-来源-柱状图-模型)
@app.route('/getModelData_histogram/class_source',methods = ['GET', 'POST'])
def getModelData_histogram_class_source():
    print("getModelData_histogram_class_source")
    result_text = sql.getSourceData_histogram_class_source("classifier")
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#获取原数据构建表格(来源-类别-柱状图-原始数据)
@app.route('/getSourceData_histogram/source_class',methods = ['GET', 'POST'])
def getSourceData_histogram_source_class():
    print("getSourceData_histogram_source_class")
    result_text = sql.getSourceData_histogram_source_class("source")
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#获取原数据构建表格(来源-类别-柱状图-模型)
@app.route('/getModelData_histogram/source_class',methods = ['GET', 'POST'])
def getModelData_histogram_source_class():
    print("getModelData_histogram_source_class")
    result_text = sql.getSourceData_histogram_source_class("classifier")
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#获取原数据构建表格(类别-饼图-原始数据)
@app.route('/getSourceData_pie/class', methods = ['GET', 'POST'])
def getSourceData_pie_class():
    print("getSourceData_pie_class")
    result_text = sql.getSourceData_pie_class("source")
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#获取原数据构建表格(来源-饼图-原始数据)

@app.route('/getSourceData_pie/source', methods = ['GET', 'POST'])
def getSourceData_pie_source():
    print("getSourceData_pie_source")
    result_text = sql.getSourceData_pie_source()
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#获取原数据构建表格(类别-饼图-模型)
@app.route('/getModelData_pie/class', methods = ['GET', 'POST'])
def getModelData_pie_class():
    print("getModelData_pie_class")
    result_text = sql.getSourceData_pie_class("classifier")
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#获取原数据构建表格(来源-饼图-模型)
@app.route('/getModelData_pie/source', methods = ['GET', 'POST'])
def getModelData_pie_source():
    print("getModelData_pie_source")
    result_text = sql.getSourceData_pie_source()
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#***************8个图***********************#

#模型的关键词搜索,返回相关关键词的来源饼图
@app.route('/searchModelKeyWord/source',methods = ['GET', 'POST'])
def searchModelKeyWord_source():

    keyword = request.args.get("keyword")
    print("searchModelKeyWord_source:" + keyword)
    result_text = sql.searchSourceDataKeyWord_pie_source(keyword)
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#模型的关键词搜索,返回相关关键词的类别饼图
@app.route('/searchModelKeyWord/class',methods = ['GET', 'POST'])
def searchModelKeyWord_class():
    keyword = request.form.get("keyword")
    print("searchModelKeyWord_class:" + keyword)
    result_text = sql.searchSourceDataKeyWord_pie_class(keyword)
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#接收用户文件,处理后，返回文件列表(考虑文件重名?)
@app.route('/uploadFile', methods = ['GET', 'POST'])
def uploadFile():
    basePath = os.path.dirname(os.path.abspath(__file__))
    print("uploadFile")
    #上传文件列表
    upload_files = request.files.getlist('file')
    fileList = []
    for file in upload_files:
        filename = file.filename
        fileList.append(filename)
        savePath = os.path.join(basePath,'文件',filename)
        file.save(savePath)
    
    print(fileList)

    dic = {"name":fileList[0]}

    # #返回文件列表
    # print(fileList)
    # dic = {"name":"file","element":fileList}
    response = make_response(jsonify(dic))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#删除已上传的文件,返回成功OR失败
@app.route('/deleteFile', methods = ['GET', 'POST'])
def deleteFile():
    pass

#开始进行数据处理
@app.route('/startHandleNews',methods = ['GET', 'POST'])
def starthandleNews():
    print("start")
    #获取文件列表
    basePath = os.path.dirname(os.path.abspath(__file__))
    target_dir = basePath + '\\文件\\'
    filelist = []
    for filenames in os.listdir(target_dir):
        filelist.append(filenames)
        
    if len(filelist) == 0:
        return "succeed"
    #处理
    handle = handleNews(filelist)
    handle.start_handleNews()
    del handle
    return "succeed"

#获取用户上传文件的分类数据(类别-来源-柱状图)
@app.route('/getUploadData_histogram/class_source', methods = ['GET', 'POST'])
def getUploadData_histogram_class_source():
    pass

#获取用户上传文件的分类数据(来源-类别-柱状图)
@app.route('/getUploadData_histogram/source_class', methods = ['GET', 'POST'])
def getUploadData_histogram_source_class():
    pass

#获取用户上传文件的分类数据(来源饼图)
@app.route('/getUploadData_pie/source', methods = ['GET', 'POST'])
def getUploadData_pie_source():
    pass

#获取用户上传文件的分类数据(类别饼图)
@app.route('/getUploadData_pie/class', methods = ['GET', 'POST'])
def getUploadData_pie_class():
    print("getUploadData_pie_class")
    result_text = sql.getUploadData_pie_class()
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response


#获取用户上传文件的单个文件分类数据,返回str(新闻标签，新闻类别，新闻关键字，新闻内容)
@app.route('/getUploadData/classifierData', methods = ['GET', 'POST'])
def getClassifileData():
    filename = request.args.get("filename")
    print("getClassifierData:" + filename)
    result_text = sql.getContent(filename)
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#上传数据的关键词搜索,返回搜索结果的文件名列表
@app.route('/searchUploadKeyWord/fileList', methods = ['GET', 'POST'])
def searchUploadKeyWord_fileList():
    keyword = request.args.get("keyword")
    print("searchUploadKeyWord_fileList:" + keyword)
    result_text = sql.searchUploadKeyWord_fileList(keyword)
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#上传数据的关键词搜索,返回来源饼图
@app.route('/searchUploadKeyWord/source', methods = ['GET', 'POST'])
def searchUploadKeyWord_source():
    pass

#上传数据的关键词搜索，返回类别饼图
@app.route('/searchUploadKeyWord/class', methods = ['GET', 'POST'])
def searchUploadKeyWord_class():
    keyword = request.args.get("keyword")
    print("searchUploadKeyWord_class:" + keyword)
    result_text = sql.searchSourceDataKeyWord_pie_class(keyword)
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#词云
@app.route('/cloudWord',methods = ['GET', 'POST'])
def getCloudWords():
    keyword = request.args.get("keyword")
    print("getCloudWords:" + keyword)
    result_text = sql.wordCloud(keyword)
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

#错误处理，打印错误信息
@app.route('/sendError')
def sendError(errorStr):
    pass

#连接测试
@app.route('/connect_test', methods = ['GET', 'POST'])
def test():
    result_text = {"statusCode": 200,"message": "连接成功"}
    response = make_response(jsonify(result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000)