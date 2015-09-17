var EXTENT = [new Date(2014, 1, 1), new Date()];

$(document).ready(function() {
    $('.js-report-sparkline').each(function(sparklineId) {

        var th = $(this);

        // Instead of splitting with "," we are passing the data in JSON format
        // Because splitting may cause getting datas as string
        // And that breaks scale calculators
        // Also this chain clears the HTML content
        var parseDate = d3.time.format("%m-%Y");

        data.forEach(function(d) {
            d.date = parseDate.parse(d.date);
            d.value = +d.value;
        });


        // Get width and height of the container
        var w = th.width(),
            h = th.height(),

            // Setting the margins
            // You may set different margins for X/Y
            xMargin = 30,
            yMargin = 20,

            // Scale functions
            // Setting the range with the margin
            y = d3.scale.linear()
                .domain([0, 10])
                .range([h - yMargin, yMargin]),
            x = d3.time.scale()
                .domain(EXTENT)
                .range([xMargin, w - xMargin]),

            // Scale functions for creating the gradient fill/stroke
            // Calculating the color according to data in the range of colors
            // That user has passed with the data-range-[high-low]-color attributes
            gradientY = d3.scale.linear()
                .domain([0,1,2,3,4,5,6,7]) .range(['#e86e6b','#e86e6c','#fcd56b','#59d1ba','#59d1bb','#a5d36e']),

            // This is a different margin than the one for the chart
            // Setting the gradient stops from 0% to 100% will cause wrong color ranges
            // Because data points are positioned in the center of containing rect
            percentageMargin = 100 / data.length,
            percentageX = d3.scale.linear()
                .domain([0, data.length - 1])
                .range([percentageMargin, 100 - percentageMargin]),

            // Create S
            container = d3.select(this).append("div"),

            // Create SVG object and set dimensions
            vis = container
                .append("svg:svg")
                .attr("width", w)
                .attr("height", h)

                g = vis.append("svg:g")
                .attr("stroke", "url(#sparkline-gradient-" + sparklineId + ")")
                .attr("fill", "url(#sparkline-gradient-" + sparklineId + ")"),

            // Create the line
            // Using cardinal interpolation because we need
            // The line to pass on every point
            area = d3.svg.area()
                .interpolate("cardinal")
                .x(function(d,i) { return x(d.date); })
                .y0(h)
                .y1(function(d) { return y(d.value); }),
            line = d3.svg.line()
                .interpolate("cardinal")
                .x(function(d) { return x(d.date); })
                .y(function(d) { return y(d.value); });

    g.append("svg:path").attr("class","area").attr("d", area(data)).attr("style", "fill:url(#area-fill)");

    // Create points
    // We are only creating points for first and last data
    // Because that looks cooler :)
    var points = g.selectAll(".point")
        .data(data)
        .enter().append("svg:circle")
        .attr("class", function(d, i) { return (i === (data.length - 1) || i === 0) ? "point end" : "point"; })
        .attr("cx", function(d, i) { return x(d.date) })
        .attr("cy", function(d, i) { return y(d.value) })
        .attr("r",  function(d, i) { return (i === (data.length - 1) || i === 0) ? 5 : 3; });

    // Append the line to the group
    g.append("svg:path").attr("d", line(data));

    // Create the gradient effect
    // This is where the magic happens
    // We get datas and create gradient stops with calculated colors
    var defs = vis.append("svg:defs");
    defs.append("svg:linearGradient")
        .attr("id", "sparkline-gradient-" + sparklineId)
        .attr("x1", "0%").attr("y1", "0%").attr("x2", "100%").attr("y2", "0%")
        .attr("gradientUnits", "userSpaceOnUse")
        .selectAll(".gradient-stop")
        .data(data)
        .enter()
        .append("svg:stop").attr('offset', function(d, i) {
            return ((percentageX(i))) + "%";
        }).attr("style", function(d) {
            return "stop-color:" + gradientY(d.value) + ";stop-opacity:1";
        });

    });
});
