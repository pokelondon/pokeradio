(function(window) {

    var width = 960,
        height = 700

    var svg = d3.select("#graph").append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force()
        .gravity(0.9)
        .friction(0.8)
        .charge(-900)
        .linkDistance(400)
        .size([width, height]);

    d3.json(PRAD.json_endpoint, function(error, json) {
        force
            .links(json.links)
            .nodes(json.nodes)
            .charge(function(d) {
                var baseDistance = 600;
                var val = baseDistance / parseInt(d.value) * 10;
                return val;
            })
            .start();

        var link = svg.selectAll(".link")
            .data(json.links)
            .enter()
            .append("line")
            .attr("class", "link")
            .style("fill", function(d) {
                return '#e0c000';
            })
            .attr("stroke-width", function(d) {
                if(d.value !== null) {
                    return Math.sqrt(d.value);
                } else {
                    return 2;
                };
            });

        var node = svg.selectAll(".node")
            .data(json.nodes)
            .enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.append("image")
            .attr("xlink:href", function(d) { return "http://pokerad.io/profilepictures/" + d.id + ".jpg";})
            .attr("x", -15)
            .attr("y", -15)
            .attr("width", 30)
            .attr("height", 30);

        node.append("text")
            .attr("dx", 22)
            .attr("dy", ".35em")
            .text(function(d) { return d.name });

        force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

            node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
        });
    });


}(window));
