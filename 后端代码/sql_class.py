# -*- coding: gb2312 -*- 

#sql_class����������ݿ�Ĳ���
#version: 1.1
#9/3
import os
import pymssql 
import json
import math

class sql_class:
    
    server = "127.0.0.1"  #���ӷ�������ַ
    user = "sa"      #�����ʺ�
    password = "123456"  #��������
    
    
    #��Ĺ��캯��
    def __init__(self):
        self.conn = pymssql.connect(self.server, self.user, self.password, "news_classifier")  #��ȡ����
    
    def connect_close(self):
        self.conn.close()
    
    #�����ݿ���ȡ��صı��(���-��Դ-��״ͼ-ԭʼ���ݺͷ�������)    source/classifier
    def getSourceData_histogram_class_source(self,mark):
        cursor = self.conn.cursor() #��ȡ���
        
        #news_source = ['BBC������','�¹�֮��','�����ձ�','����˹������','·͸��','����֮��','ŦԼʱ��������','�ձ�������','�վ�������','̨������','�¼��������籨','�ǵ�������','Ӣ��������ʱ����']
        
        news_source = []
        cursor.execute('SELECT DISTINCT news_source FROM source_data')
        row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])
        news_label = ['��������', '��������', '������', '����', '����', '�Ļ�']

        guoji_list = []
        guonei_list = []
        internet_list = []
        economy_list = []
        army_list = []
        culture_list = []
        
        guoji_dic = {"name":'��������'}
        guonei_dic = {"name":'��������'}
        internet_dic = {"name":'������'}
        economy_dic = {"name": '����'}
        army_dic = {"name": '����'}
        culture_dic = {"name": '�Ļ�'}
        
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
                    if label=='��������':
                        guoji_list.append(dic)
                    elif label == '��������':
                        guonei_list.append(dic)
                    elif label == '������':
                        internet_list.append(dic)
                    elif label == '����':
                        economy_list.append(dic)
                    elif label == '����':
                        army_list.append(dic)
                    elif label == '�Ļ�':
                        culture_list.append(dic)
                except:
                    print("error")
        #�ٽ�ÿ��list�ϲ���һ�������ֵ�

        guoji_dic['children'] = guoji_list
        guonei_dic['children'] = guonei_list
        internet_dic['children'] = internet_list
        economy_dic['children'] = economy_list
        army_dic['children'] = army_list
        culture_dic['children'] = culture_list
        
        #�������ֵ�
        result = {"name":"sourceData"}
        result['children'] = [guoji_dic,guonei_dic,internet_dic,economy_dic,army_dic,culture_dic]
        #cursor.execute('select news_label from source_data group by news_label')
        #row = cursor.fetchall()
        cursor.close()
        return result

    #�����ݿ���ȡ��صı��(��Դ-���-��״ͼ-ԭʼ���ݺͷ�������)
    def getSourceData_histogram_source_class(self,mark):
        cursor = self.conn.cursor() #��ȡ���
        
        news_source = []
        cursor.execute('SELECT DISTINCT news_source FROM source_data')
        row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])
        news_label = ['��������', '��������', '������', '����', '����', '�Ļ�']
            
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
        
        #�������ֵ�
        result = {"name":"sourceData"}
        result['children'] = result_list
        cursor.close()
        return result

    #�����ݿ���ȡԭʼ������صı��(����ͼ)
    def getSourceData_pie_class(self,mark):
        cursor = self.conn.cursor() #��ȡ���
        news_label = ['��������', '��������', '������', '����', '����', '�Ļ�']

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

    #�����ݿ���ȡԭʼ������صı��(��Դ��ͼ)
    def getSourceData_pie_source(self):
        cursor = self.conn.cursor() #��ȡ���

        news_source = []    #������Դ
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

    #�����ݿ�������ԭʼ���ݵĹؼ��ʣ�����ͳ�ƽ��(����ͼ)
    def searchSourceDataKeyWord_pie_class(self,keyWord):
        cursor = self.conn.cursor() #��ȡ���
        #�������ؼ��ʣ�������������
        cursor.execute('select upload_data.news_id,news_keyWord FROM upload_data,upload_keyWord WHERE upload_data.news_id=upload_keyWord.news_id')
        row = cursor.fetchall()
        contentList = []
        for word in row:
            contentList.append((word[0],word[1]))

        #�ؼ���ƥ��
        content_id = []
        for index in range(len(contentList)):
            if keyWord in contentList[index][1]:
                content_id.append(contentList[index][0])

        #�����ݣ������ͼ
        news_label = ['��������', '��������', '������', '����', '����', '�Ļ�']

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
                if label=='��������':
                    guoji_count += 1
                elif label == '��������':
                    guonei_count += 1
                elif label == '������':
                    internet_count += 1
                elif label == '����':
                    economy_count += 1
                elif label == '����':
                    army_count += 1
                elif label == '�Ļ�':
                    culture_count += 1
            except:
                print("error")

        pie_list.append({"name":"��������","value":guoji_count})
        pie_list.append({"name":"��������","value":guonei_count})
        pie_list.append({"name":"������","value":internet_count})
        pie_list.append({"name":"����","value":economy_count})
        pie_list.append({"name":"����","value":army_count})
        pie_list.append({"name":"�Ļ�","value":culture_count})

        result = {"name":news_label}
        result["element"] = pie_list
        return result
       
    #�����ݿ�������ԭʼ���ݵĹؼ��ʣ�����ͳ�ƽ��(��Դ��ͼ)
    def searchSourceDataKeyWord_pie_source(self,keyWord):
        cursor = self.conn.cursor() #��ȡ���
        #�������ؼ��ʣ�������������
        cursor.execute('select news_source,news_keyWord FROM source_data,source_keyWord WHERE source_data.news_id=source_keyWord.news_id')
        row = cursor.fetchall()
        contentList = []
        for word in row:
            contentList.append((word[0],word[1]))

        #�ؼ���ƥ��
        content_source = []
        for index in range(len(contentList)):
            if keyWord in contentList[index][1]:
                content_source.append(contentList[index][0])

        #�����ݣ������ͼ
        news_source = []    #������Դ
        cursor.execute('SELECT DISTINCT news_source FROM source_data')
        row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])

        #�����ֵ�
        result = {"name":news_source}
        res_list = []
        for s in news_source:
            dic = {"name":s}
            dic['value'] = content_source.count(s)
            res_list.append(dic)
        result['element'] = res_list
        return result
        
    #�����ݿ���ȡ�û��ϴ������ݵķ������ı�����ݣ����-��Դ-��״ͼ��              ���޸�
    def getUploadData_histogram_class_source(self,identify = "all"):
        cursor = self.conn.cursor() #��ȡ���
        
        #��ȡ������Դ��
        news_source = []
        if identify=="all":
            cursor.execute('SELECT DISTINCT news_source FROM upload_data')
            row = cursor.fetchall()
        else:
            cursor.execute('SELECT DISTINCT news_source FROM upload_data WHERE identify=%s',identify)
            row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])
        news_label = ['��������', '��������', '������', '����', '����', '�Ļ�']
        
        guoji_list = []
        guonei_list = []
        internet_list = []
        economy_list = []
        army_list = []
        culture_list = []
        
        guoji_dic = {"name":'��������'}
        guonei_dic = {"name":'��������'}
        internet_dic = {"name":'������'}
        economy_dic = {"name": '����'}
        army_dic = {"name": '����'}
        culture_dic = {"name": '�Ļ�'}
        
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
                    if label=='��������':
                        guoji_list.append(dic)
                    elif label == '��������':
                        guonei_list.append(dic)
                    elif label == '������':
                        internet_list.append(dic)
                    elif label == '����':
                        economy_list.append(dic)
                    elif label == '����':
                        army_list.append(dic)
                    elif label == '�Ļ�':
                        culture_list.append(dic)
                except:
                    print("error")
        #�ٽ�ÿ��list�ϲ���һ�������ֵ�

        guoji_dic['children'] = guoji_list
        guonei_dic['children'] = guonei_list
        internet_dic['children'] = internet_list
        economy_dic['children'] = economy_list
        army_dic['children'] = army_list
        culture_dic['children'] = culture_list
        
        #�������ֵ�
        result = {"name":"uploadData"}
        result['children'] = [guoji_dic,guonei_dic,internet_dic,economy_dic,army_dic,culture_dic]
        #cursor.execute('select news_label from source_data group by news_label')
        #row = cursor.fetchall()
        cursor.close()
        return result
  
    #�����ݿ���ȡ�û��ϴ������ݵķ������ı�����ݣ���Դ-���-��״ͼ��              ���޸�
    def getUploadData_histogram_source_class(self,identify = "all"):
        cursor = self.conn.cursor() #��ȡ���
        
        news_source = []
        cursor.execute('SELECT DISTINCT news_source FROM upload_data')
        row = cursor.fetchall()
        for source in row:
            news_source.append(source[0])
        news_label = ['��������', '��������', '������', '����', '����', '�Ļ�']
            
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
        
        #�������ֵ�
        result = {"name":"sourceData"}
        result['children'] = result_list
        cursor.close()
        return result
    #�����ݿ���ȡ�û��ϴ������ݵķ������ı�����ݣ�����ͼ�� 
    def getUploadData_pie_class(self,identify = "all"):
        cursor = self.conn.cursor() #��ȡ���
        news_label = ['��������', '��������', '������', '����', '����', '�Ļ�']

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
    
    #�����û��ϴ����ݵĹؼ��ʣ������ļ��б�
    def searchUploadKeyWord_fileList(self,keyWord,identify = "all"):
        cursor = self.conn.cursor() #��ȡ���
        #�������ؼ��ʣ�������������
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
        
        #�ؼ���ƥ��
        content_id = []
        for index in range(len(contentList)):
            if keyWord in contentList[index][1]:
                content_id.append(contentList[index][0])

        #������,�����ļ��б�
        fileList = []
        for index in content_id:
            cursor.execute('select news_source FROM upload_data WHERE news_id=%s',index)
            row = cursor.fetchall()
            dic = {"name":row[0][0]}
            fileList.append(dic)

        result = {"num":len(fileList),"name":"fileList"} 
        result['children'] = fileList
        return result  
        
    #�����ϴ��ļ����ļ�����������/������(���ű�ǩ������������Źؼ��֣���������)
    def getContent(self,filename,identify = "all"):
        cursor = self.conn.cursor() #��ȡ���
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

    #�洢�û��ϴ����ļ�(upload_data),dataFrame�����ļ��������ݣ��ִʱ�,�ؼ��֣�Ԥ�ڷ��ࣨ����Ϊ�գ������������ϴ�ʱ�䣬�ļ�����ʶ
    def savaUploadData(self,dataFrame,time,identify = "all"):
        cursor = self.conn.cursor() #��ȡ���
        datalist = dataFrame.values.tolist()
        for data in datalist:
            cursor.execute('insert into upload_data(news_source,classifier_label,upload_time,identify) values (%s,%s,%s,%s)',(data[0],data[5],time,identify))
            self.conn.commit()
            cursor.execute('insert into upload_keyWord(news_content,news_keyWord) values (%s,%s)',(data[1],data[4]))
            self.conn.commit()
        print("д�����ݿ�ɹ�")

    #����
    def wordCloud(self,classifier):
        cursor = self.conn.cursor() #��ȡ���
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
        #����
        count = {}
        for words in wordList:
            if wordList.count(words)>1:
                count[words] = wordList.count(words)

        list_sort = sorted(count.items(),reverse = True,key=lambda x:x[1])
        #print(list_sort)
        #��ӳ�䣬�����ߣ���120 - 10��/�������ֵ-������Сֵ
        #���㣺������ * ������ֵ - ������Сֵ�� = �ֺ� - 10
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
# result = test.wordCloud("����")
# print(json.dumps(result,ensure_ascii=False))
# test.connect_close()
