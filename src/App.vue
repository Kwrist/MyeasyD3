<template>
  <body id="app">
  <Top @givefilename="givename"></Top>
  <Search  :searchclear="searchtext2" @givesearch="getsearch"></Search>
  <Container :getfilename="middlefilename" :searchtext="searchtext" @searchclear="getsearch2"></Container>
  <Foot>foot</Foot>
  <div id="other"></div>
  </body>
</template>

<script>
import Top from './components/top'
import Container from './components/contatiner'
import Search from './components/search'
import Foot from './components/foot'
export default {
  name: 'app',
  components: {
    Search,
    Top,
    Container,
    Foot,
  },
  data(){
    return{
      screenWidth:document.body.clientWidth-17,
      searchtext:null,
      searchtext2:null,
      middlefilename:null,
    }
  },
  watch:{
    // screenWidth(val){
    //   if(!this.timer){
    //     this.screenWidth=val;
    //     this.timer=true;
    //     let that = this;
    //     setTimeout(function () {
    //       that.timer=false
    //     },400)
    //   }
    // }
  },
  mounted() {
    const that=this;
    window.onresize=()=>{
      return(()=>{
        window.screenWidth=document.body.clientWidth;
        that.screenWidth=window.screenWidth;
      })()
    }
  },
  methods:{
    getsearch:function (text) {
      this.searchtext=text;
    },
    getsearch2:function (text) {
      this.searchtext2=text;
    },
    givename:function (text) {
      this.middlefilename=text;
    }
  }
}
</script>

<style type="text/acss">

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;

}
.el-footer{
  height:60px;
  padding:0 20px;
  display:block;
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
}
#top-img{
  margin-bottom: -20px;
  height: 50px;
}
#line1 {
  stroke:blue;
  width: 60%;

}
.countries:hover{
  fill:red;
}
.el-divider{
  margin: 0;
}
.tick text{
  fill:#8e8883;
}
.tick line{
  stroke: #C0C0BB;
}
.el-drawer__body{
  overflow: scroll;
}
.line-path{
  fill:none;
  stroke: steelblue;
  stroke-linejoin: round;
}
.tooltip{
  position: absolute;
  width: 120px;
  height: auto;
  font-size: 14px;
  text-align: center;
  color: white;
  border: 2px solid black;
  background-color: black;
  border-radius: 5px;
}

.tooltip:after{
  content: '';
  position: absolute;
  bottom: 100%;
  left: 20%;
  margin-left: -8px;
  width: 0;
  height: 0;
  border-bottom: 12px solid black;
  border-right: 12px solid transparent;
  border-left: 12px solid transparent;
}
#other{
 font-size: 40px;
}
</style>
