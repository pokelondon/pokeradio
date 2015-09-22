var EXTENT = [new Date(2014, 0, 0), new Date(2016, 0, 0)];

$(document).ready(function() {
    (function() {
        if(!$('#playShare').length) {
            return;
        }
        var width = 160;
        var height = 160;
        var radius = Math.min(width, height) / 2;
        var donutWidth = 20;
        var r = Math.min(width, height) / 2;
        var labelr = r;

        var color = d3.scale.category20c();

        var svg = d3.select('#playShare')
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', 'translate(' + (width / 2) + ',' + (height / 2) + ')');

        var arc = d3.svg.arc()
            .innerRadius(radius - donutWidth)
            .outerRadius(radius);

        var pie = d3.layout.pie()
            .value(function(d) { return d.share })
            .sort(null);

        var g = svg.selectAll(".arc")
            .data(pie(user_play_share))
            .enter().append("g")
            .attr("class", "arc");

        g.append("path")
            .attr("d", arc)
            .style("fill", function(d) {
                if(d.data.label.length) {
                    return '#f84646'
                } else {
                    return color(d.data.share);
                }
            });

        g.append("text")
            .attr("transform", function(d) {
                var c = arc.centroid(d),
                    x = c[0],
                    y = c[1],
                    h = Math.sqrt(x*x + y*y);
                return "translate(" + (x/height * labelr) +  ',' + (y/height * labelr) +  ")";
            })
            .attr("dy", ".35em")
            .attr("text-anchor", function(d) {
                // are we past the center?
                return (d.endAngle + d.startAngle) / 2 > Math.PI ? "end" : "start";
            })
            .text(function(d) {
                return d.data.label;
            });
    }());

    // Metric
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
            h = th.height();

        // Setting the margins
        // You may set different margins for X/Y
        var xMargin = 30;
        var yMargin = 20;

        // Scale functions
        // Setting the range with the margin
        var y = d3.scale.linear()
            .domain([0, 10])
            .range([h - yMargin, yMargin]);

        var x = d3.time.scale()
            .domain(EXTENT)
            .range([xMargin, w - xMargin]);

        // Scale functions for creating the gradient fill/stroke
        // Calculating the color according to data in the range of colors
        // That user has passed with the data-range-[high-low]-color attributes
        var gradientY = d3.scale.linear()
            .domain([0,1,2,3,4,5,6,7,8,9,10]).range(['#e86e6b','#e86e6c','#fcd56b','#59d1ba','#59d1bb','#a5d36e']);

        // This is a different margin than the one for the chart
        // Setting the gradient stops from 0% to 100% will cause wrong color ranges
        // Because data points are positioned in the center of containing rect
        var percentageMargin = 100 / data.length;
        var percentageX = d3.scale.linear()
            .domain([0, data.length - 1])
            .range([percentageMargin, 100 - percentageMargin]);

        // Create S
        var container = d3.select(this).append("div");

        // Create SVG object and set dimensions
        var vis = container
            .append("svg:svg")
            .attr("width", w)
            .attr("height", h);


        // Create the group object and set styles for gradient definition
        // Which is about to add in a few lines
        var xAxis = vis.append("svg:g")
            .attr("class", "x-axis")
            .attr("transform", "translate(" + 0 + "," + (h-yMargin) + ")")
            .attr("stroke", "white")
            .call(
                d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .ticks(24)
                .tickSize(-h+(yMargin*2), 0, 0)
                .tickFormat(d3.time.format("%b"))
            );
        xAxis.selectAll("text")
            .style("text-anchor", "middle")
            .attr("transform", "translate(0,5)")
            .attr("fill", "white")
            .attr("stroke-width", "0");
        var yAxis = vis.append("svg:g")
            .attr("class", "y-axis")
            .attr("transform", "translate("+xMargin+"," + 0 + ")")
            .attr("stroke", "white")
            .call(d3.svg.axis()
                .scale(y)
                .orient("left")
                .ticks(8)
                .tickSize(-w+(xMargin*2), 0, 0)
                  .tickFormat(function(d, i){ return d })
            );
        yAxis.selectAll("line")
            .style("stroke-dasharray", ("3, 3"));
            yAxis.selectAll("text")
            .style("text-anchor", "start")
            .attr("transform", "translate(3,12)")
            .attr("fill", "white")
            .attr("stroke-width", "0");

        g = vis.append("svg:g")
                .attr("stroke", "url(#sparkline-gradient-" + sparklineId + ")")
                .attr("fill", "url(#sparkline-gradient-" + sparklineId + ")");


        var g = vis.append("svg:g")
            .attr("stroke", "url(#sparkline-gradient-" + sparklineId + ")")
            .attr("fill", "url(#sparkline-gradient-" + sparklineId + ")");


            // Create the line
            // Using cardinal interpolation because we need
            // The line to pass on every point
        var area = d3.svg.area()
            .interpolate("cardinal")
            .x(function(d,i) { return x(d.date); })
            .y0(h)
            .y1(function(d) { return y(d.value); });

        var line = d3.svg.line()
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
        for (i = 0; i < data.length; ++i) {
            var tooltip = container
                .append("div")
                .attr("class", "chart-tooltip")
                .attr("data-index", i).html(data[i].value + " play" + ((data[i].value > 1) ? 's' : ''));
            $tooltip = $(".chart-tooltip[data-index=" + i + "]");
            $tooltip.data({
                calcY: y,
                calcX: x
            });
            var tooltipLeft = $tooltip.data("calcX")(data[i].date) - ($tooltip.width() / 2);
            var tooltipTop = $tooltip.data("calcY")(data[i].value) - 30;

            // Position it again
            $tooltip.css({
                left: tooltipLeft + "px",
                top: tooltipTop + "px"
            });
        }


        // Creating invisible rectangles for a better hover interaction
        // Because otherwise user would need to hover to the line or point
        // Which is a terrible experience
        // Creating full height invisible bars and binding mouse events
        // To do some special stuff like showing data or adding classes to
        // The point in the targeted area

        var rect = g.selectAll(".bar-rect")
            .data(data)
            .enter().append("svg:rect")
            .attr("class", "bar-rect")
            .attr("x", function(d, i) { return x(d.date) - (w / data.length / 2) })
            .attr("y", 0)
            .attr("width", w / data.length)
            .attr("height", h)
            .on("mouseenter", function(d, i) {
                $('.chart-tooltip[data-index='+i+']').addClass('hover');
                // Add hover class to the targeted point
                var thisPoint = $(this).parent().parent().find('.point:eq(' + i + ')');
                    thisPoint.attr('class', (i===0||i===(data.length-1)) ? 'end point hover' : 'point hover');
            }).on("mouseleave", function(d, i) {
                $('.chart-tooltip').removeClass('hover');
                // Remove hover class from the targeted point
                var thisPoint = $(this).parent().parent().find('.point:eq(' + i + ')');
                    thisPoint.attr('class', (i===0||i===(data.length-1)) ? 'end point' : 'point');
            });

            // Helper function to calculate the HTML content of the tooltip
            // Tooltip may contain any HTML
            function formatTooltip(d, i) {
                return '<div class="title">' + d.value + '</div>'
            }



    // Bind calculator functions to tooltip


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
    areaFill = defs.append("svg:linearGradient");
    areaFill.attr("id", "area-fill");
    areaFill.attr("x1", "0%").attr("y1", "0%").attr("x2", "0%").attr("y2", "100%");
    areaFill.append("svg:stop").attr('offset', "0%").attr("style", 'stop-color:white;stop-opacity:0.1');
  	areaFill.append("svg:stop").attr('offset', "100%").attr("style", 'stop-color:white;stop-opacity:0');


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




    // Metric
    $('.js-report-sparkline-sm').each(function(sparklineId) {
        var th = $(this);

        // Instead of splitting with "," we are passing the data in JSON format
        // Because splitting may cause getting datas as string
        // And that breaks scale calculators
        // Also this chain clears the HTML content
        var data = window.playdata['track_' + th.data('id')];
        var parseDate = d3.time.format("%m-%Y");

        data.forEach(function(d) {
            d.date = parseDate.parse(d.date);
            d.value = +d.value;
        });

        // Get width and height of the container
        var w = th.width(),
            h = th.height();

        // Setting the margins
        // You may set different margins for X/Y
        var xMargin = 30;
        var yMargin = 20;

        // Scale functions
        // Setting the range with the margin
        y = d3.scale.linear()
                    .domain(EXTENT)
                    .range([yMargin, h - yMargin]),
        x = d3.scale.linear()
                    .domain([0, data.length - 1])
                    .range([xMargin, w - xMargin]),

        // Scale functions for creating the gradient fill/stroke
        // Calculating the color according to data in the range of colors
        // That user has passed with the data-range-[high-low]-color attributes
        gradientY = d3.scale.linear()
            .domain([0, 10])
            .range([th.data("range-low-color"), th.data("range-high-color")]),

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

        // Create the group object and set styles for gradient definition
        // Which is about to add in a few lines
        g = vis.append("svg:g")
                .attr("stroke", "url(#sparkline-gradient-" + sparklineId + ")")
                .attr("fill", "url(#sparkline-gradient-" + sparklineId + ")"),

        // Create the line
        // Using cardinal interpolation because we need
        // The line to pass on every point
        line = d3.svg.line()
            .interpolate("cardinal")
            .x(function(d, i) { return x(i); })
            .y(function(d) { return h - y(d.value); }),

        // Create points
        // We are only creating points for first and last data
          // Because that looks cooler :)
        points = g.selectAll(".point")
            .data(data)
            .enter().append("svg:circle")
            .attr("class", "point")
            .attr("cx", function(d, i) { return x(i) })
            .attr("cy", function(d, i) { return h - y(d.value) })
            .attr("r", function(d, i) { return (i === (data.length - 1) || i === 0) ? 5 : 0; });

    // Append the line to the group
    g.append("svg:path").attr("d", line(data));

    // Create the gradient effect
    // This is where the magic happens
    // We get datas and create gradient stops with calculated colors
    vis.append("svg:defs")
        .append("svg:linearGradient")
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
