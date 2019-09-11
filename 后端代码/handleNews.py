

#handleNews类包含对上传文件的分词、数据库存储以及模型拟合操作
#version :1.0
#9/2

import os
import pandas
import numpy
import jieba
import jieba.analyse
from sklearn.model_selection import  train_test_split
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
import datetime

from sql_class import sql_class

class handleNews:
    fileList = []
    dataFrame = pandas.DataFrame()
    
    #初始化，获取文件列表,加载模型文件
    def __init__(self,filenameList,identify = "all"):
        self.fileList = filenameList
        self.root_dir = os.path.dirname(os.path.abspath(__file__)) #c:\Users\Asam\Desktop\项目准备\code
        self.identify = identify
    
    def checkDataFrame(self):

        return self.dataFrame

    #开始对文件列表进行一系列操作
    def start_handleNews(self):
        self.read_File()
        path = self.root_dir + '\\text1.csv'
        self.dataFrame.to_csv(path,encoding='utf-8',index=False,header=False)
        self.cutWord()
        path = self.root_dir + '\\text2.csv'
        self.dataFrame.to_csv(path,encoding='utf-8',index=False,header=False)
        self.rm_stopWord()
        path = self.root_dir + '\\text3.csv'
        self.dataFrame.to_csv(path,encoding='utf-8',index=False,header=False)
        self.get_keyWord()
        path = self.root_dir + '\\text4.csv'
        self.dataFrame.to_csv(path,encoding='utf-8',index=False,header=False)
        self.run_model()
        #获取当前时间
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        #写入数据库
        self.inputData(time,self.identify)
        
        #删除文件
        for filename in self.fileList:
            filepath = self.root_dir + '\\文件\\' + filename
            os.remove(filepath)
        #return self.checkDataFrame()
    
    #读取文件,建立数据表
    def read_File(self):
        self.dataFrame['news_source'] = pandas.Series(self.fileList)

        all_content = []
        for filename in self.fileList:
            filePath = self.root_dir + '\\文件\\' + filename
            text = open(filePath,encoding='utf-8-sig').read()
            all_content.append(text)
        self.dataFrame['content'] = pandas.Series(all_content)

    #jieba库分词
    def cutWord(self):
        content_S = []
        content = self.dataFrame.content.values.tolist()

        for line in content:
            current_segment = jieba.lcut(str(line))
            if len(current_segment) > 1 and current_segment!='\r\n':
                content_S.append(current_segment)

        #添加到数据表中
        self.dataFrame['content_S'] = pandas.Series(content_S)

    #引入停用词
    def rm_stopWord(self):
        open_dir = self.root_dir + '\\StopWords.txt'
        stopWords = open(open_dir,encoding='utf-8-sig').read()
        stopword=[]
        #转成list
        for word in stopWords:
            stopword.append(word)

        #去除停用词
        def rm_stopWord(contents,stopwords):
            contents_clean = []
            for line in contents:
                line_clean = []
                for word in line:
                    if word in stopwords:
                        continue
                    line_clean.append(word)
                contents_clean.append(str(line_clean))
            return contents_clean
        
        contents = self.dataFrame['content_S'].values.tolist()
        content_clean = rm_stopWord(contents,stopword)

        #加入数据表
        self.dataFrame['content_clean'] = content_clean

    #提取关键词
    def get_keyWord(self):
        topicWords = []
        content_clean = self.dataFrame['content_clean'].values.tolist()
        for line in content_clean:
            content_str = ''.join(line)
            result = ' '.join(jieba.analyse.extract_tags(content_str,topK=20,withWeight=False))
            topicWords.append(result)
        #加入数据表
        self.dataFrame['keyWord'] = pandas.Series(topicWords)
    
    #构建模型数据集，跑模型
    def run_model(self):
        #构造模型数据集
        contents_clean = self.dataFrame['content_clean'].values

        words = []
        for line_index in range(len(contents_clean)):
            words.append(''.join(contents_clean[line_index]))

        print(words[0])
        vec_dir = self.root_dir + '\\模型\\words.m'
        clf_dir = self.root_dir + '\\模型\\model.m'
        vec = joblib.load(vec_dir)
        clf = joblib.load(clf_dir)
        predict_result = clf.predict(vec.transform(words))
        #print(predict_result)
        self.dataFrame['classifier_label'] = pandas.Series(predict_result)
        self.replace_label()

    #标签去向量化
    def replace_label(self):
        label_mapping = {1 : "国内政治", 2 : "国际政治", 3 : "互联网",4 : "经济",5 : "军事",6 : "文化"}
        self.dataFrame['classifier_label'] = self.dataFrame['classifier_label'].map(label_mapping)
    
    #写入数据库
    def inputData(self,time,identify = "all"):
        sql = sql_class()
        sql.savaUploadData(dataFrame = self.dataFrame,time = time,identify = identify)
        sql.connect_close()

    
# target_dir='C:\\Users\\Asam\\Desktop\\code\\文件'
# search_file = []
# for filenames in os.listdir(target_dir):
#     search_file.append(filenames)
# test = handleNews(search_file)
# test.start_handleNews()