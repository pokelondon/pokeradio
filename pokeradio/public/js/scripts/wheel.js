
var fade = function(opacity) {
    return function(g, i) {
        svg.selectAll(".chord")
            .filter(function(d) {
                return d.source.index != i && d.target.index != i;
            })
        .transition()
            .style("opacity", opacity);
        var groups = [];
        svg.selectAll(".chord")
            .filter(function(d) {
                if (d.source.index == i) {
                    groups.push(d.target.index);
                }
                if (d.target.index == i) {
                    groups.push(d.source.index);
                }
            });
        groups.push(i);
        var length = groups.length;
        svg.selectAll('.group')
            .filter(function(d) {
                for (var i = 0; i < length; i++) {
                    if(groups[i] == d.index) return false;
                }
                return true;
            })
        .transition()
            .style("opacity", opacity);
    };
};
var outerRadius = 960 / 2,
    innerRadius = outerRadius - 130;

var fill = d3.scale.category20c();

    var chord = d3.layout.chord()
    .padding(.04)
.sortSubgroups(d3.descending)
    .sortChords(d3.descending);

    var arc = d3.svg.arc()
.innerRadius(innerRadius)
    .outerRadius(innerRadius + 20);

    var svg = d3.select("body").append("svg")
    .attr("width", outerRadius * 2)
    .attr("height", outerRadius * 2)
    .append("g")
    .attr("transform", "translate(" + outerRadius + "," + outerRadius + ")");

    d3.json(PRAD.json_endpoint, function(error, json) {

        chord.matrix(json.links);

        var g = svg.selectAll(".group")
        .data(chord.groups)
        .enter().append("g")
        .attr("class", "group");

    g.append("path")
        .style("fill", function(d) { return fill(d.index); })
        .style("stroke", function(d) { return fill(d.index); })
        .attr("d", arc)
        .on("mouseover", fade(0.1))
        .on("mouseout", fade(1));

    g.append("text")
        .each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })
        .attr("dy", ".35em")
        .attr("transform", function(d) {
            return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
            + "translate(" + (innerRadius + 26) + ")"
            + (d.angle > Math.PI ? "rotate(180)" : "");
        })
    .style("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
        .text(function(d) {
            return json.nodes[d.index];
        });

    svg.selectAll(".chord")
        .data(chord.chords)
        .enter().append("path")
        .attr("class", "chord")
        .style("stroke", function(d) { return d3.rgb(fill(d.source.index)).darker(); })
        .style("fill", function(d) { return fill(d.source.index); })
        .attr("d", d3.svg.chord().radius(innerRadius));

    });

d3.select(self.frameElement).style("height", outerRadius * 2 + "px");
