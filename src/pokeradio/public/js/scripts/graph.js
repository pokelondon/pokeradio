(function(window) {

    var width = 960,
        height = 700

    var svg = d3.select("#graph").append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force()
        .distance(500)
        .gravity(0.3)
        .charge(30)
        .size([width, height]);

    d3.json(PRAD.json_endpoint, function(error, json) {
        console.log(json);
        force
            .nodes(json.nodes)
            .links(json.links)
            .charge(function(d) {return d.value;})
            .start();
            //.charge(function(d) {return d.value;})

        var link = svg.selectAll(".link")
            .data(json.links)
            .enter()
            .append("line")
            .attr("class", "link")
            .attr("stroke-width", function(d) {
                if(d.value !== null) {
                    return d.value;
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
            .attr("x", -10)
            .attr("y", -10)
            .attr("width", 20)
            .attr("height", 20);

        node.append("text")
            .attr("dx", 12)
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
