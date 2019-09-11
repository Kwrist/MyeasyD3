<template>    <el-container style="height: 550px;">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
            <el-menu :default-openeds="['一']">
                <el-submenu index="一">
                    <template slot="title"><i class="el-icon-pie-chart"></i>可视化模型</template>
                    <div @click="openonlysvg">
                    <el-menu-item index="1-1" @click="changeCate(10)">分类图表-原始数据</el-menu-item>
                    <el-menu-item index="1-2" @click="changeCate(20)">分类图表-模型</el-menu-item>
                    <el-menu-item index="1-3" @click="changeCate(30)">类别词云</el-menu-item>
                    <el-menu-item index="1-4" :disabled="true">关系图</el-menu-item>
                    </div>
                </el-submenu>
            </el-menu>
            <el-menu>
                <el-submenu index="二">
                    <template slot="title"><i class="el-icon-more"></i>详细新闻</template>
                    <div @click="closesvgandsearch">
                        <el-menu-item v-for="(item,i) in newslist" :index="''+i" @click="getFormData(item.name)" >{{i+1}}:{{item.name}}</el-menu-item>
                    </div>
                </el-submenu>
            </el-menu>
            <el-menu>
                <el-menu-item @click="showsearchresult" index="三">
                    <template slot="title"><i class="el-icon-search"></i>搜索结果</template>
                </el-menu-item>
            </el-menu>
        </el-aside>
        <el-container class="child">
            <div>
                <el-row class="button001">
                    <el-button type="primary" @click="changesvg(1)" :disabled="!svgShow" plain>类别-来源</el-button>
                    <el-button type="info" @click="changesvg(2)" :disabled="!svgShow" plain>来源-类别</el-button>
                    <el-button type="warning" @click="changesvg(3)" :disabled="!svgShow" plain>来源占比图</el-button>
                    <el-button type="danger" @click="changesvg(4)"  :disabled="!(svgShow||searchSign)" plain>分类占比图</el-button>
                </el-row>
                <el-checkbox-group v-model="checkList" v-if="(datachange===3||datachange===4)&&checksign">
                    <el-checkbox v-for="(item,index) in acceptdata0" :label="index+1">{{item}}</el-checkbox>
                    <el-button @click="changecheck" style="margin-left: 20px">确认</el-button>
                </el-checkbox-group>
            </div>
<!--            <button id="haha" @click="accept2">123</button>-->
<!--            <div id="canvas"><svg :width="myWidth/1.2-50" :height="498/(1503/myWidth)-50"></svg></div>-->
            <div class="canvas" v-if="svgShow===true||searchSign===true">
                <el-row v-if="ciyunSign">
                    <el-button round @click="ciyuncate(1)">国际政治</el-button>
                    <el-button type="primary" round @click="ciyuncate(2)">国内政治</el-button>
                    <el-button type="success" round @click="ciyuncate(3)">互联网</el-button>
                    <el-button type="info" round @click="ciyuncate(4)">经济</el-button>
                    <el-button type="warning" round @click="ciyuncate(5)">军事</el-button>
                    <el-button type="danger" round @click="ciyuncate(6)">文化</el-button>
                </el-row>
                <span id="svgtitle" style="display: block"></span>
                <div class="searchtitle" v-show="searchSign===true&&searchhidden===false">{{searchshowtext}}</div>
                <svg width="1320" height="448"></svg>
            </div>
            <div class="newsdetail2" v-else-if="searchSign===false">
                <p>新闻标签：{{newsdetail.name}}</p>
                <p>新闻类别：{{newsdetail.category}}</p>
                <p>新闻关键字：{{newsdetail.key}}</p>
                <p>新闻相关关键字：{{newsdetail.otherkey}}</p>
                <p>新闻内容：</p>
                <textarea readonly>新闻内容：{{newsdetail.content}}</textarea>
            </div>
            <div v-else>
                <el-button>来源</el-button>
                <el-button>类比</el-button>
                <p>与当前关键字相关的新闻有xx条(具体结果已经在左边列表中筛选出来)</p>
            </div>

        </el-container>
    </el-container>
</template>

<script>
    import {histogram} from "@/components/d3/Histogram";
    import {piechart} from "@/components/d3/piechart";
    import * as d3 from "d3";
    import  {mycloud} from "@/components/d3/mycloud";
    import Vue from "vue";
    import $ from 'jquery';
    export default {
        name: "contatiner",
        props:{
            //myWidth:Number,//使屏幕自适应分辨率，因运算量较大，暂弃
            searchtext:String,//获得从Search中传来的搜索字符串
            getfilename:Object//获得从Top中传来的上传的文件名（one by one）
        },
        data() {
            return {
                searchshowtext:'还未输入搜索关键字，请输入关键字后再查看此页面。',//显示搜索后的结果，有两两种情况，未输入关键字点击搜索，输入关键字点击搜索
                searchhidden:true,//是否显示当前搜索结果
                searchnum:0,//获得与当前关键字相关的新闻条数
                checksign:true,
                ciyunSign:false,
                piechartcate:0,
                acceptdata0:null,
                acceptdata:null,
                rawJson:null,
                searchSign:false,//是否启用了搜索功能
                datachange:1,
                svgShow:true,
                try:null,
                cloudwordlist:[],
                data_cate:10,
                checkList: d3.range(1,20,1),
                newslist:null,//用来存储所有接受到的上传文件的文件列表，为数组
                newsdetail:{//存储一条新闻的详细信息
                    "name":null,
                    "category":null,
                    "key":null,
                    "otherkey":null,
                    "content":null}
            }
         },
        created(){//解决更新数据时v-for不同步更新的问题
          let old=Object.assign({},this.newslist);
          old={};
          this.newslist=old;
        },
        watch:{
            // svgShow:function () {
            //     console.log(this.datachange);
            //   if(this.svgShow===true){
            //       this.changesvg(this.datachange);
            //   }
            //
            // },
            searchtext:function () {//当接受到从top中传来的搜索字符串时，显示搜索结果
                const my=this;
                this.$axios.get('http://localhost:5000/searchUploadKeyWord/fileList',{//发送搜索关键字到后端
                    params:{
                        keyword:my.searchtext
                    }
                })
                    .then(function(response){

                        console.log('searchtext');
                        my.dataDestory();
                        my.checkList=d3.range(1,20,1);
                        my.ciyunSign=false;//关闭词云中的类别选项按钮
                        my.checksign=false;//关闭饼图中的选项按钮
                        my.searchhidden=false;//显示搜索结果
                        if(my.searchtext===""){
                            console.log("清空了");
                            my.svgShow=true;
                            my.searchSign=false;
                            my.newslist=response.data.children;
                            //my.myhistogram(11);//如果搜索为空，回到最初的状态
                        }else{
                            //这里处理搜索结果
                            my.svgShow=false;
                            my.searchSign=true;
                            my.searchnum=response.data.num;//获得结果数目
                            my.newslist=response.data.children;//获得结果文件列表
                            my.searchshowtext='共有'+my.searchnum+"条新闻与"+'"'+my.searchtext+'"相关。';
                            //获得的搜索结果
                        }
                    })
                    .catch(function (response) {
                        console.log(response);
                    })
            },
            getfilename:function () {
                this.newslist.push(this.getfilename);
            }
        },
        mounted() {
             let my=this;
            this.$nextTick(function () {//网站初始化时画一张柱状图
                this.$axios.get('http://localhost:5000/searchUploadKeyWord/fileList',{//发送搜索关键字到后端
                    params:{
                        keyword:"xx-xx"
                    }
                })
                    .then(function(response){
                        my.newslist=response.data.children;
                        my.myhistogram(11);
                    })
            });
         },
        methods:{
            changesvg:function(arg){
                //if(arg===this.datachange)return;
                this.dataDestory();
                this.searchhidden=true;
                this.datachange=arg;
                switch (arg) {
                    case 0:this.getWordCloud();break;
                    case 1:this.myhistogram(arg+this.data_cate);break;
                    case 2:this.myhistogram(arg+this.data_cate);break;
                    case 3:this.mypiechart(this.data_cate+arg);break;
                    case 4:this.mypiechart(this.data_cate+arg);break;
                    default:break;
                }
            },
            dataDestory:function () {
                d3.selectAll('g').remove();
                d3.selectAll('rect').remove();
                d3.selectAll('circle').remove();
                d3.selectAll('path').remove();
                d3.select('#other').select('div').remove();
                d3.select('#svgtitle').select('text').remove();
            },
             mypiechart:function (arg) {
                this.dataDestory();
                this.ciyunSign=false;
                 if(this.piechartcate!==arg)
                 this.checkList=d3.range(1,20,1);
                 let url;
                 this.checksign=true;
                 this.piechartcate=arg;
                 console.log(this.piechartcate);
                 this.checksign=true;
                 if(this.searchSign&&(arg===14||arg===24||arg===34)){//这里要获得的是搜索结果的分类图
                    url="http://localhost:5000/searchUploadKeyWord/class";
                 }
                 else if(arg===14){
                     url="http://localhost:5000/getSourceData_pie/class";
                 }
                 else if(arg===24){
                     url="http://localhost:5000/getModelData_pie/class";
                 }else{
                     url="http://localhost:5000/getSourceData_pie/source";
                 }
                 if(this.searchSign&&(arg===14||arg===24||arg===34)){
                     console.log(this.searchtext);
                     this.$axios.get(url,{
                         params:{
                             keyword:this.searchtext
                         }
                     }).then(response=>{
                         console.log(this.checkList);
                         this.rawJson=JSON.stringify(response.data);
                         this.acceptdata0=response.data.name;
                         piechart(this.rawJson,this.checkList);
                     });
                 }
                 else{
                    this.$axios.get(url).then(response=>{
                        console.log(this.checkList);
                         this.rawJson=JSON.stringify(response.data);
                         this.acceptdata0=response.data.name;
                         piechart(this.rawJson,this.checkList);
                    });
                 }
             },
             myhistogram:function (arg) {
                 this.checksign=false;
                 this.ciyunSign=false;
                 let url;
                 if(arg===11){//类别-来源-原始
                     url="http://localhost:5000/getSourceData_histogram/class_source";
                 }
                 else if(arg===12){//来源-类别-原始
                     url="http://localhost:5000/getSourceData_histogram/source_class";
                 }
                 else if(arg===21){//类别-来源-模型
                     url="http://localhost:5000/getModelData_histogram/class_source";
                 }
                 else{//来源-类别-模型
                     url="http://localhost:5000/getModelData_histogram/source_class";
                 }
                 this.$axios.get(url).then(response=>{
                     this.rawJson=JSON.stringify(response.data);
                     this.acceptdata=response.data;
                     histogram(this.rawJson);
                 });
             },
             getFormData:function (arg) {//显示一条新闻的详细信息
                 this.checksign=false;
                 this.ciyunSign=false;
                 let my=this;
                 this.$axios.get("http://localhost:5000/getUploadData/classifierData",{
                     params:{
                         filename:arg
                     }
                 })
                     .then(response=>{
                         console.log(response);
                         my.newsdetail=response.data;
                     })
             },
             changecheck:function(){
                this.mypiechart(this.piechartcate);
             },
             changeCate(arg){
                if(arg===10){
                    this.data_cate=10;
                    this.changesvg(1);
                }
                else if(arg===20){
                    this.data_cate=20;
                    this.changesvg(1);
                }
                else{
                    this.data_cate=30;
                    this.changesvg(0);
                }
             },
             closesvgandsearch(){
                 //this.$emit("searchclear",Math.random());
                 this.svgShow=false;
                 this.searchSign=false;
             },
             openonlysvg(){
                this.$emit("searchclear",Math.random());
                this.svgShow=true;
                this.searchSign=false;
             },
             showsearchresult(){//点击"搜索结果"按钮后显示搜索结果的函数
                console.log('showsearchresult');
                this.dataDestory();
                this.ciyunSign=false;
                this.searchhidden=false;
                this.searchSign=true;
                 this.checksign=false;
                if(this.searchtext===null){
                    this.searchshowtext="还未输入搜索关键字，请输入关键字后再查看此页面。"
                }
                else{
                    this.searchshowtext='共有'+this.searchnum+"条新闻与"+'"'+this.searchtext+'"相关。';
                }
             },
             getWordCloud:function(){
                //遗留一个未解决的bug，先点击详细新闻，再点击词云，词云没有马上生成，需要再点击一次
                this.datachange= 0;
                this.ciyunSign=true;
                this.searchSign=false;
                this.checksign=false;
                let wordOption={
                    'wordList':this.cloudwordlist,
                    'size':[1320,448],
                };
                mycloud(wordOption,this.getArticalList);
             },
             getArticalList:function (text) {//回调函数好像是一种很好的在js和vue文件之间传递数据的方式
                 this.searchtext=text;
             },
            ciyuncate:function (arg) {
                let giveword;
                switch (arg) {
                    case 1:giveword="国际政治";break;
                    case 2:giveword="国内政治";break;
                    case 3:giveword="互联网";break;
                    case 4:giveword="经济";break;
                    case 5:giveword="军事";break;
                    case 6:giveword="文化";break;
                }
                this.$axios.get("http://localhost:5000/cloudWord",{
                    params:{
                        keyword:giveword
                    }
                }).then(response=>{
                    console.log(response.data.cloudwordlist);
                    this.cloudwordlist=response.data.cloudwordlist;
                    this.changeCate(30);
                })
            }
         }
    }
</script>

<style scoped>
#canvas{
    border:none;
    margin: 0;
    padding: 0;
    z-index: 5000;
}
button{

}
.child{
    display: block;
}
.el-row{
    float: left;
    margin-left:20px;
    margin-right: -20px;
}
.el-checkbox{
    text-align: center;
    margin-top: 10px;
}
.el-container{
    border-left: 1px solid #eee;

}
.el-button{
    border-radius: 20px;
}

svg{
    margin-top: 0px;
    overflow: visible;
}
.tick text{
    fill:#8e8883;
}
.tick line{
    stroke: #C0C0BB;
}
text{
    text-shadow:
            -1px -1px 3px white,
            -1px  1px 3px white,
            1px -1px 3px white,
            1px  1px 3px white;
}
path{
    fill:none;
    stroke:#57bdc3;

}
.newsdetail2{
    display: block;
    font-size: 20px;
    text-align: left;
    margin-top: 20px;
    margin-left: 30px;
    line-height: 30px;
    float: left;
}
textarea{
    width: 760px;
    height: 142px;
    font-size: 15px;
    resize: none;
}
#svgtitle{
    margin-top: 20px;
    font-size: 15px;
}
    .button001{
        margin-top: -65px;
        margin-left: -170px;
    }
.searchtitle{
    margin-left: -20px;
}
</style>
