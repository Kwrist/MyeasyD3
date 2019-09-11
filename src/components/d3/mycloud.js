const d3 = require("d3"),
    cloud = require("./d3.layout.cloud");

let mycloud=function (option, callback) {


    let theSize=option.size,
        theWordList=option.wordList;

    let layout = cloud()
        .size(theSize)
        .words(theWordList)
        .padding(5)
        .rotate(function () {
            return ~~(Math.random() * 3) * 90;
        })
        .font("Impact")
        .fontSize(function (d) {
            return d.size;
        })
        .on("end", draw);

    layout.start();

    function draw(words) {

        let color=d3.scaleOrdinal(d3.schemeCategory10);

        d3.select('svg')
            .append("g")
            .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function (d) {
                return d.size + "px";
            })
            .style("font-family", "Impact")
            .style('cursor','pointer')
            .style('fill',function (d,i) {
                return color(i);
            })
            .attr("text-anchor", "middle")
            .attr("transform", function (d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function (d) {
                return d.text;
            })
            .on('click',function (d) {
                callback(d.text);
            });
    }
};

export {mycloud};
