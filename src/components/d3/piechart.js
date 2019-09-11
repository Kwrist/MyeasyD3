// create 2 data_set
import * as d3 from "d3";

//missdata代表要删除的信息
const render=function(dataset,color){


    const svg=d3.select("svg");
    svg.attr('transform','translate(0,10)');
    const width=+svg.attr("width");
    const height=+svg.attr("height");

    //转换数据
    const pie = d3.pie() //创建饼状图
        .value(function (d) {
            return d.value;
        });//值访问器

    //dataset为转换前的数据 piedata为转换后的数据
    const piedata = pie(dataset);

    //绘制
    const outerRadius = 200;
    const innerRadius = 0;//内半径和外半径

    //创建弧生成器
    const arc = d3.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius);


    //添加对应数目的弧组
    const arcs = svg.selectAll("g")
        .data(piedata)
        .enter()
        .append("g")
        .attr("transform", "translate(" + (width / 2) + "," + (height / 2) + ")");

    //添加弧的路径元素
    arcs.append("path")
        .attr("fill", function (d, i) {
            return color(i);
        })
        .attr("d", function (d) {
            return arc(d);
        });

    //添加弧内的文字
    arcs.append("text")
        .attr("transform", function (d) {
            var x = arc.centroid(d)[0] * 1.4;//文字的x坐标
            var y = arc.centroid(d)[1] * 1.4;
            return "translate(" + x + "," + y + ")";
        })
        .attr("text-anchor", "middle")
        .text(function (d) {
            let percent = Number(d.value) / d3.sum(dataset, function (d) {
                return d.value;
            }) * 100;
            if(percent<3)return "";
            else return percent.toFixed(1) + "%";
        });

    const mypadding=2.2;
    const zzy=0;
    //添加连接弧外文字的直线元素
    arcs.append("line")
        .attr("stroke", "black")
        .attr("x1", function (d) {
            if(d.endAngle-d.startAngle<0.2)return 0;
            else
            return arc.centroid(d)[0] * 2;
        })
        .attr("y1", function (d) {
            if(d.endAngle-d.startAngle<0.2)return 0;
            return arc.centroid(d)[1] * 2;
        })
        .attr("x2", function (d) {
            if(d.endAngle-d.startAngle<0.2)return 0;
            return arc.centroid(d)[0] * mypadding+zzy;
        })
        .attr("y2", function (d) {
            if(d.endAngle-d.startAngle<0.2)return 0;
            return arc.centroid(d)[1] * mypadding+zzy;
        });

    const fontsize = 10;
    arcs.append("line")
        .style("stroke", "black")
        .each(function (d) {
            d.textLine = {x1: 0, y1: 0, x2: 0, y2: 0};
        })
        .attr("x1", function (d) {
            if(d.endAngle-d.startAngle<0.2)return 0;
            d.textLine.x1 = arc.centroid(d)[0] * mypadding+zzy;
            return d.textLine.x1;
        })
        .attr("y1", function (d) {
            if(d.endAngle-d.startAngle<0.2)return 0;
            d.textLine.y1 = arc.centroid(d)[1] * mypadding+zzy;
            return d.textLine.y1;
        })
        .attr("x2", function (d) {
            if(d.endAngle-d.startAngle<0.2)return 0;
            var strLen = getPixelLength(d.data.name, fontsize) * 1.5;
            var bx = arc.centroid(d)[0] * mypadding+zzy;
            d.textLine.x2 = bx >= 0 ? bx + strLen : bx - strLen;
            return d.textLine.x2;
        })
        .attr("y2", function (d) {
            if(d.endAngle-d.startAngle<0.2)return 0;
            d.textLine.y2 = arc.centroid(d)[1] * mypadding+zzy;
            return d.textLine.y2;
        });

    arcs.append("text")
        .attr("transform", function (d) {
            let x = 0;
            let y = 0;
            x = (d.textLine.x1 + d.textLine.x2) / 2;
            y = d.textLine.y1;
            y = y > 0 ? y + fontsize * 1.1 : y - fontsize * 0.4;
            return "translate(" + x + "," + y + ")";
        })
        .style("text-anchor", "middle")
        .style("font-size", fontsize)
        .text(function (d) {
            if(d.endAngle-d.startAngle<0.2)return "";
            return d.data.name;
        });

//添加一个提示框
    let tooltip = d3.select("#other")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0.0);

    arcs.on("mouseover", function (d, i) {
        tooltip.html(d.data.name + "的数量为" + "<br />" + d.data.value + "件")
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY + 20) + "px")
            .style("opacity", 1.0);
        tooltip.style("box-shadow", "10px 0px 0px" + color(i));//在提示框后添加阴影
    })
        .on("mousemove", function (d) {
            tooltip.style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY + 20) + "px");
        })
        .on("mouseout", function (d) {
            //鼠标移除 透明度设为0
            tooltip.style("opacity", 0.0);
        });

    function getPixelLength(str, fontsize) {
        let curLen = 0;
        for (var i = 0; i < str.length; i++) {
            var code = str.charCodeAt(i);
            var pixelLen = code > 255 ? fontsize : fontsize / 2;
            curLen += pixelLen;
        }
        return curLen;
    }
};

// http://localhost:8081/data/piechart.json
//http://127.0.0.1:5000/connect_test
let color;
let count=1;
const piechart=function (rawJson,missdata) {
// A function that create / update the plot for a given variable:
        let data=JSON.parse(rawJson);
        let my = [];
        let i=1;
        for (let prop in data.element) {
            if (missdata.indexOf(i) > -1) {
                my[i-1] = data.element[i-1];
            }
            i++;
        }
        let mycolor=[];
        let step=0.15;
        for(let i=0;i<20;i++){
            mycolor.push(d3.interpolateRainbow(step*i) );
        }
        if(count>-1){
            color = d3.scaleOrdinal()
                .domain(data.element)
                .range(mycolor);
            count-=2;
        }

        my=trimSpace(my);
        render(my, color);
};

function trimSpace(array){
    for(var i = 0 ;i<array.length;i++)
    {
        if(array[i] === " " || array[i] == null || typeof(array[i]) == "undefined")
        {
            array.splice(i,1);
            i= i-1;

        }
    }
    return array;
}

// Initialize the plot with the first dataset
export {piechart};

