<template>
    <div id="app">
    <el-container>
        <el-header>
            <span id="mytitle" title="hppp" style="float: left; margin-left: 550px">基于D3引擎的算法可视化技术（新闻版）准确率82.99%</span>
            <el-button type="primary" icon="el-icon-share" @click="startdone">刷新</el-button>
            <el-button @click="drawer=true" type="primary">上传<i class="el-icon-u-pload el-icon--right"></i></el-button>
        </el-header>
    </el-container>
    <el-drawer
            title="文件上传列表"
            style="font-size: 20px;text-align: center;"
            :visible.sync="drawer"
            :direction="direction">
        <span>
            <el-upload
                class="upload-demo"
                action="http://localhost:5000/uploadFile"
                :on-preview="handlePreview"
                :on-remove="handleRemove"
                :on-progress="openFullScreen"
                :on-success="showFiles"
                :before-remove="beforeRemove"
                accept="txt"
                style="text-align: left;margin-left: 150px;"
                multiple>
            <div style="text-align: center">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传txt类型的文件{{fullscreenLoading}}</div>
                </div>
        </el-upload>
        </span>
    </el-drawer>
    </div>
</template>

<script>
    export default {
        name: "top.vue",
        data:function () {
            return{
                drawer:false,
                direction:'rtl',
                myfileList: [],
                fullscreenLoading: false
            }
        },
        methods: {
            handleRemove(file, fileList) {
                console.log("删除:"+file, fileList);
                // this.$axios.get("http://local:5000")
                //     .then(response=>{
                //         console.log(response);
                //     })
            },
            handlePreview(file) {
                console.log("点击文件"+file);
            },
            beforeRemove(file, fileList) {
                return this.$confirm(`确定移除 ${ file.name }？`);
            },
            showFiles(response,file,fileList){//上传一个文件成功时的操作
                console.log(response);
                this.$emit("givefilename",response);
                let myname=file.name;
                this.myfileList.push(myname.substr(0,myname.length-4));
            },
            openFullScreen() {

                const loading = this.$loading({
                    lock: true,
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(255,255,255,0)'
                });
                setTimeout(() => {
                    loading.close();
                }, 2000);
            },
            startdone(){//刷新按钮，点击之后后端才会开始处理数据
                const loading = this.$loading({
                    lock: true,
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(255,255,255,0)'
                });
                this.$axios.get("http://localhost:5000/startHandleNews")
                    .then(response=>{
                        console.log(response);
                        loading.close();
                    })
            }
        }
    }
</script>


<style type="text/scss" scoped>
    .el-header{
        background-color: #B3C0D1;
        color: #333;
        text-align: center;
        line-height: 60px;
        border-radius: 10px
    }

    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: center;
        line-height: 200px;
    }

    .el-main {
        background-color: #E9EEF3;
        color: #333;
        text-align: center;
        line-height: 160px;
    }
    .el-header{
        text-align: right;
    }
    .el-container{
        margin-bottom: 0;
        border-bottom: 4px solid #4e535da8;
        border-top: 4px solid #4e535da8;
    }
    #mytitle{
        float: left;
        font-size: 30px;
    }
</style>

