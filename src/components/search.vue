<template>
    <div id="app">
        <el-container>
            <el-header >
                        <el-input v-model="searchText" placeholder="请输入待查询的信息" width="80%" maxlength="10" show-word-limit>{{searchText}}</el-input>
                        <el-button type="primary" icon="el-icon-search" @click="onSubmit">搜索</el-button>
            </el-header>
        </el-container>
    </div>
</template>

<script>

    export default {
        name: "search.vue",
        props:{
            searchclear:Number
        },
        data(){
            return{
                searchText:null,//只负责接受用户输入并传输到container组件中，并不会与后端进行交互
            }
        },
        methods: {
            onSubmit() {
               this.$emit('givesearch',this.searchText);
            }
        },
        watch:{
            searchclear:function () {
                this.searchText="";
              }
        }
    }
</script>


<style type="text/scss" scoped>
    #app{
        border-radius: 5px;
    }
    .el-header{
        background-color: #B3C0D1;
        color: #333;
        text-align: center;
        line-height: 60px;
        border-radius: 10px;
    }
    .el-header{
        text-align: left;
    }
    .el-input{
        width:65%;
        margin-right: 20px;
    }
    .el-button{
        vertical-align: middle;
    }
    .el-container{
        margin-top: -10px;
        float:right
    }

</style>

