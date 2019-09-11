# -*- coding: gb2312 -*- 

#sql_class类包含对数据库的操作
#version: 1.1
#9/3
import os
import pymssql 
import json
import math

class sql_class:
    
    server = "127.0.0.1"  #连接服务器地址
    user = "sa"      #连接帐号
    password = "123456"  #连接密码
    
    
    #类的构造函数
    def __init__(self):
        self.conn = pymssql.connect(self.server, self.user, self.password, "news_classifier")  #获取连接
    
    def connect_close(self):
        self.conn.close()
    
    #从数据库中取相关的表格(类别-来源-柱状图-原始数据和分类数据)    source/classifier
    def getSourceData_histogram_class_source(self,mark):
        cursor = self.conn.cursor() #获取光标
        
        #news_source = ['BBC中文网','德国之声','东亚日报','俄罗斯卫星网','路透社','美国之音','纽约时报中文网','日本新闻网','日经中文网','台湾旺报','新加坡联合早报','星岛环球网','英国《金融时报》']
        
        news_source = []
        cursor.execute('SELECT DISTINCT news_source FROM source_data')
        row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])
        news_label = ['国际政治', '国内政治', '互联网', '经济', '军事', '文化']

        guoji_list = []
        guonei_list = []
        internet_list = []
        economy_list = []
        army_list = []
        culture_list = []
        
        guoji_dic = {"name":'国际政治'}
        guonei_dic = {"name":'国内政治'}
        internet_dic = {"name":'互联网'}
        economy_dic = {"name": '经济'}
        army_dic = {"name": '军事'}
        culture_dic = {"name": '文化'}
        
        for label in news_label:
            for source in news_source:
                try:
                    if mark=="source":
                        cursor.execute('select count(*) from source_data where news_source=%s and news_label=%s',(source,label))
                    elif mark=="classifier":
                        cursor.execute('select count(*) from source_data where news_source=%s and classifier_label=%s',(source,label))
                    row = cursor.fetchone()
                    num = row[0]
                    dic = {"name":source,"value":num}
                    if label=='国际政治':
                        guoji_list.append(dic)
                    elif label == '国内政治':
                        guonei_list.append(dic)
                    elif label == '互联网':
                        internet_list.append(dic)
                    elif label == '经济':
                        economy_list.append(dic)
                    elif label == '军事':
                        army_list.append(dic)
                    elif label == '文化':
                        culture_list.append(dic)
                except:
                    print("error")
        #再将每个list合并入一个类别的字典

        guoji_dic['children'] = guoji_list
        guonei_dic['children'] = guonei_list
        internet_dic['children'] = internet_list
        economy_dic['children'] = economy_list
        army_dic['children'] = army_list
        culture_dic['children'] = culture_list
        
        #并入总字典
        result = {"name":"sourceData"}
        result['children'] = [guoji_dic,guonei_dic,internet_dic,economy_dic,army_dic,culture_dic]
        #cursor.execute('select news_label from source_data group by news_label')
        #row = cursor.fetchall()
        cursor.close()
        return result

    #从数据库中取相关的表格(来源-类别-柱状图-原始数据和分类数据)
    def getSourceData_histogram_source_class(self,mark):
        cursor = self.conn.cursor() #获取光标
        
        news_source = []
        cursor.execute('SELECT DISTINCT news_source FROM source_data')
        row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])
        news_label = ['国际政治', '国内政治', '互联网', '经济', '军事', '文化']
            
        result_list = []
        for source in news_source:
            source_list = []
            for label in news_label:
                try:
                    if mark=="source":
                        cursor.execute('select count(*) from source_data where news_source=%s and news_label=%s',(source,label))
                    elif mark=="classifier":
                        cursor.execute('select count(*) from source_data where news_source=%s and classifier_label=%s',(source,label))
                    row = cursor.fetchone()
                    num = row[0]
                    dic = {"name":label,"value":num}
                    source_list.append(dic)
                except:
                    print("error")
            source_dic = {"name":source,"children":source_list}
            result_list.append(source_dic)
        
        #并入总字典
        result = {"name":"sourceData"}
        result['children'] = result_list
        cursor.close()
        return result

    #从数据库中取原始数据相关的表格(类别饼图)
    def getSourceData_pie_class(self,mark):
        cursor = self.conn.cursor() #获取光标
        news_label = ['国际政治', '国内政治', '互联网', '经济', '军事', '文化']

        pie_list = []

        for label in news_label:
            try:
                if mark == "source":
                    cursor.execute('select count(*) from source_data where news_label=%s',label)
                elif mark == "classifier":
                    cursor.execute('select count(*) from source_data where classifier_label=%s',label)
                row = cursor.fetchone()
                num = row[0]
                dic = {"name":label,"value":num}
                pie_list.append(dic)

            except:
                print("error")

        result = {"name":news_label}
        result["element"] = pie_list
        return result

    #从数据库中取原始数据相关的表格(来源饼图)
    def getSourceData_pie_source(self):
        cursor = self.conn.cursor() #获取光标

        news_source = []    #新闻来源
        cursor.execute('SELECT DISTINCT news_source FROM source_data')
        row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])

        pie_list = []

        for source in news_source:
            try:              
                cursor.execute('select count(*) from source_data where news_source=%s',source)
                row = cursor.fetchone()
                num = row[0]
                dic = {"name":source,"value":num}
                pie_list.append(dic)

            except:
                print("error")

        result = {"name":news_source}
        result["element"] = pie_list
        return result

    #从数据库中搜索原始数据的关键词，返回统计结果(类别饼图)
    def searchSourceDataKeyWord_pie_class(self,keyWord):
        cursor = self.conn.cursor() #获取光标
        #先搜索关键词，把内容拉出来
        cursor.execute('select upload_data.news_id,news_keyWord FROM upload_data,upload_keyWord WHERE upload_data.news_id=upload_keyWord.news_id')
        row = cursor.fetchall()
        contentList = []
        for word in row:
            contentList.append((word[0],word[1]))

        #关键词匹配
        content_id = []
        for index in range(len(contentList)):
            if keyWord in contentList[index][1]:
                content_id.append(contentList[index][0])

        #查数据，构造饼图
        news_label = ['国际政治', '国内政治', '互联网', '经济', '军事', '文化']

        pie_list = []

        guoji_count = 0
        guonei_count = 0
        internet_count = 0
        economy_count = 0
        army_count = 0
        culture_count = 0

        for news_id in content_id:
            try:
                cursor.execute('select classifier_label from upload_data where news_id=%s',news_id)
                row = cursor.fetchone()
                label = row[0]
                if label=='国际政治':
                    guoji_count += 1
                elif label == '国内政治':
                    guonei_count += 1
                elif label == '互联网':
                    internet_count += 1
                elif label == '经济':
                    economy_count += 1
                elif label == '军事':
                    army_count += 1
                elif label == '文化':
                    culture_count += 1
            except:
                print("error")

        pie_list.append({"name":"国际政治","value":guoji_count})
        pie_list.append({"name":"国内政治","value":guonei_count})
        pie_list.append({"name":"互联网","value":internet_count})
        pie_list.append({"name":"经济","value":economy_count})
        pie_list.append({"name":"军事","value":army_count})
        pie_list.append({"name":"文化","value":culture_count})

        result = {"name":news_label}
        result["element"] = pie_list
        return result
       
    #从数据库中搜索原始数据的关键词，返回统计结果(来源饼图)
    def searchSourceDataKeyWord_pie_source(self,keyWord):
        cursor = self.conn.cursor() #获取光标
        #先搜索关键词，把内容拉出来
        cursor.execute('select news_source,news_keyWord FROM source_data,source_keyWord WHERE source_data.news_id=source_keyWord.news_id')
        row = cursor.fetchall()
        contentList = []
        for word in row:
            contentList.append((word[0],word[1]))

        #关键词匹配
        content_source = []
        for index in range(len(contentList)):
            if keyWord in contentList[index][1]:
                content_source.append(contentList[index][0])

        #查数据，构造饼图
        news_source = []    #新闻来源
        cursor.execute('SELECT DISTINCT news_source FROM source_data')
        row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])

        #构造字典
        result = {"name":news_source}
        res_list = []
        for s in news_source:
            dic = {"name":s}
            dic['value'] = content_source.count(s)
            res_list.append(dic)
        result['element'] = res_list
        return result
        
    #从数据库中取用户上传的数据的分类结果的表格数据（类别-来源-柱状图）              待修改
    def getUploadData_histogram_class_source(self,identify = "all"):
        cursor = self.conn.cursor() #获取光标
        
        #获取新闻来源集
        news_source = []
        if identify=="all":
            cursor.execute('SELECT DISTINCT news_source FROM upload_data')
            row = cursor.fetchall()
        else:
            cursor.execute('SELECT DISTINCT news_source FROM upload_data WHERE identify=%s',identify)
            row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])
        news_label = ['国际政治', '国内政治', '互联网', '经济', '军事', '文化']
        
        guoji_list = []
        guonei_list = []
        internet_list = []
        economy_list = []
        army_list = []
        culture_list = []
        
        guoji_dic = {"name":'国际政治'}
        guonei_dic = {"name":'国内政治'}
        internet_dic = {"name":'互联网'}
        economy_dic = {"name": '经济'}
        army_dic = {"name": '军事'}
        culture_dic = {"name": '文化'}
        
        for label in news_label:
            for source in news_source:
                try:
                    if identify=="all":
                        cursor.execute('select count(*) from upload_data where news_source=%s and classifier_label=%s',(source,label))
                        row = cursor.fetchone()
                    else:
                        cursor.execute('select count(*) from upload_data where news_source=%s and classifier_label=%s and identify=%s',(source,label,identify))
                        row = cursor.fetchone()
                    num = row[0]
                    dic = {"name":source,"value":num}
                    if label=='国际政治':
                        guoji_list.append(dic)
                    elif label == '国内政治':
                        guonei_list.append(dic)
                    elif label == '互联网':
                        internet_list.append(dic)
                    elif label == '经济':
                        economy_list.append(dic)
                    elif label == '军事':
                        army_list.append(dic)
                    elif label == '文化':
                        culture_list.append(dic)
                except:
                    print("error")
        #再将每个list合并入一个类别的字典

        guoji_dic['children'] = guoji_list
        guonei_dic['children'] = guonei_list
        internet_dic['children'] = internet_list
        economy_dic['children'] = economy_list
        army_dic['children'] = army_list
        culture_dic['children'] = culture_list
        
        #并入总字典
        result = {"name":"uploadData"}
        result['children'] = [guoji_dic,guonei_dic,internet_dic,economy_dic,army_dic,culture_dic]
        #cursor.execute('select news_label from source_data group by news_label')
        #row = cursor.fetchall()
        cursor.close()
        return result
  
    #从数据库中取用户上传的数据的分类结果的表格数据（来源-类别-柱状图）              待修改
    def getUploadData_histogram_source_class(self,identify = "all"):
        cursor = self.conn.cursor() #获取光标
        
        news_source = []
        cursor.execute('SELECT DISTINCT news_source FROM upload_data')
        row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])
        news_label = ['国际政治', '国内政治', '互联网', '经济', '军事', '文化']
            
        result_list = []
        for source in news_source:
            source_list = []
            for label in news_label:
                try:
                    cursor.execute('select count(*) from upload_data where news_source=%s and classifier_label=%s',(source,label))
                    row = cursor.fetchone()
                    num = row[0]
                    dic = {"name":label,"value":num}
                    source_list.append(dic)
                except:
                    print("error")
            source_dic = {"name":source,"children":source_list}
            result_list.append(source_dic)
        
        #并入总字典
        result = {"name":"sourceData"}
        result['children'] = result_list
        cursor.close()
        return result
    #从数据库中取用户上传的数据的分类结果的表格数据（类别饼图） 
    def getUploadData_pie_class(self,identify = "all"):
        cursor = self.conn.cursor() #获取光标
        news_label = ['国际政治', '国内政治', '互联网', '经济', '军事', '文化']

        pie_list = []

        for label in news_label:
            try:
                if identify=="all":
                    cursor.execute('select count(*) from upload_data where classifier_label=%s',label)
                    row = cursor.fetchone()
                else:
                    cursor.execute('select count(*) from upload_data where classifier_label=%s and identify=%s',(label,identify))
                    row = cursor.fetchone()
                num = row[0]
                dic = {"name":label,"value":num}
                pie_list.append(dic)

            except:
                print("error")

        result = {"name":news_label}
        result["element"] = pie_list
        return result
    
    #搜索用户上传数据的关键词，返回文件列表
    def searchUploadKeyWord_fileList(self,keyWord,identify = "all"):
        cursor = self.conn.cursor() #获取光标
        #先搜索关键词，把内容拉出来
        if keyWord == "xx-xx":
            cursor.execute('SELECT news_source FROM upload_data')
            row = cursor.fetchall()
            fileList = []
            for word in row:
                dic = {"name":word[0]}
                fileList.append(dic)
                
            result = {"num":len(fileList),"name":"fileList"}
            result['children'] = fileList
            return result

        else:
            cursor.execute('select upload_data.news_id,news_keyWord FROM upload_data,upload_keyWord WHERE upload_data.news_id=upload_keyWord.news_id')
        row = cursor.fetchall()
        contentList = []
        for word in row:
            contentList.append((word[0],word[1]))
        
        #关键词匹配
        content_id = []
        for index in range(len(contentList)):
            if keyWord in contentList[index][1]:
                content_id.append(contentList[index][0])

        #查数据,返回文件列表
        fileList = []
        for index in content_id:
            cursor.execute('select news_source FROM upload_data WHERE news_id=%s',index)
            row = cursor.fetchall()
            dic = {"name":row[0][0]}
            fileList.append(dic)

        result = {"num":len(fileList),"name":"fileList"} 
        result['children'] = fileList
        return result  
        
    #根据上传文件的文件名返回内容/分类结果(新闻标签，新闻类别，新闻关键字，新闻内容)
    def getContent(self,filename,identify = "all"):
        cursor = self.conn.cursor() #获取光标
        cursor.execute('selectKeyWord @keyWord = %s',filename)
        row = cursor.fetchone()
        keylist = row[3].split(" ") 
        keyword = []
        otherkey = []
        for index in range(len(keylist)):
            if index < 4:
                keyword.append(keylist[index])
            else:
                otherkey.append(keylist[index])
            if index >=10:
                break
        dic = {
            "name":row[0],
            "category" :row[1],
            "key":' '.join(keyword),
            "otherkey":' '.join(otherkey),
            "content":row[2] 
        }
        return dic

    #存储用户上传的文件(upload_data),dataFrame包含文件名，内容，分词表,关键字，预期分类（可能为空），分类结果，上传时间，文件集标识
    def savaUploadData(self,dataFrame,time,identify = "all"):
        cursor = self.conn.cursor() #获取光标
        datalist = dataFrame.values.tolist()
        for data in datalist:
            cursor.execute('insert into upload_data(news_source,classifier_label,upload_time,identify) values (%s,%s,%s,%s)',(data[0],data[5],time,identify))
            self.conn.commit()
            cursor.execute('insert into upload_keyWord(news_content,news_keyWord) values (%s,%s)',(data[1],data[4]))
            self.conn.commit()
        print("写入数据库成功")

    #词云
    def wordCloud(self,classifier):
        cursor = self.conn.cursor() #获取光标
        wordList = []
        cursor.execute('EXEC getSourceCloudWord @classifier=%s',classifier)
        row = cursor.fetchall()
        for w in row:
            word = w[0].split("   ")
            #print(word)
            for line in word:
                wordList.append(line)
        
        cursor.execute('EXEC getUploadCloudWord @classifier=%s',classifier)
        row = cursor.fetchall()
        for w in row:
            word = w[0].split(" ")
            for line in word:
                wordList.append(line)

        #print(wordList)
        #计数
        count = {}
        for words in wordList:
            if wordList.count(words)>1:
                count[words] = wordList.count(words)

        list_sort = sorted(count.items(),reverse = True,key=lambda x:x[1])
        #print(list_sort)
        #做映射，比例尺：（120 - 10）/数据最大值-数据最小值
        #计算：比例尺 * （数据值 - 数据最小值） = 字号 - 10
        wordList.clear()
        data_max = int(list_sort[0][1])
        data_min = 2
        ratio = 110 / (data_max - data_min)
        
        for i in range(len(list_sort)):
            if i > 50:
                break
            data_num = int(list_sort[i][1])
            wordSize = math.ceil(ratio * (data_num - data_min) + 10)
            dic = {"text":list_sort[i][0],"size":wordSize}
            wordList.append(dic)
        
        result = {"cloudwordlist":wordList}
        return result

# test = sql_class()
# result = test.wordCloud("军事")
# print(json.dumps(result,ensure_ascii=False))
# test.connect_close()
