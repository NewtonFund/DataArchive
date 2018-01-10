'use strict';

// Register `heatmapGenerator` component, along with its associated controller and template
angular.
module('heatmapGenerator').
component('heatmapGenerator', {
    templateUrl: 'heatmap-generator/heatmap-generator.template.html',
    controller: [
        function() {
            //        console.log("heatmapGenerator is loaded.");
            var self = this;

            self.drawHeatmap = function(inputValue, classname, xres, yres) {

                var power1 = parseFloat(inputValue.val1),
                    power2 = parseFloat(inputValue.val2);

                var w = window,
                    d = document,
                    e = d.documentElement,
                    g = d.getElementsByClassName(classname)[0];

                var margin = {
                    top: 20,
                    right: 40,
                    bottom: 20,
                    left: 20
                };

                var width = (w.innerWidth || e.clientWidth || g1.clientWidth) - margin.right - margin.left;

                var x_elements,
                    y_elements,
                    x_min,
                    y_min,
                    x_max,
                    y_max,
                    x_dimension,
                    y_dimension;

                var colorScale = d3.scale.threshold()
                    .domain([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0])
                    // -2.0 - -1.5: Red Wine #990012
                    // -1.5 - -1.0: Pinterest Red #C8232C
                    // -1.0 - -0.5: Bright Gold #FDD017
                    // -0.5 - 0.0: Shamrock Green #347C17
                    // 0.0 - 0.5: LJMU Green #C7D401
                    // 1.0 - 1.5: HMG Blue #266EBC
                    // 0.5 - 1.0: LJMU Blue #1A3278
                    // 1.5 - 2.0: Indigo #4B0082
                    // Outside -2.0 - 2.0: Charcoal #36454F
                    .range(["#36454F", "#990012", "#C8232C", "#FDD017", "#347C17", "#C7D401", "#266EBC", "#1A3278", "#4B0082", "#36454F"]);

                var data = [];
                populateData(xres, yres);

                x_elements = data.map(function(item) {
                    return parseInt(item.x, 10);
                });
                y_elements = data.map(function(item) {
                    return parseInt(item.y, 10);
                });

                x_min = Math.min.apply(Math, x_elements);
                x_max = Math.max.apply(Math, x_elements);
                y_min = Math.min.apply(Math, y_elements);
                y_max = Math.max.apply(Math, y_elements);

                y_dimension = y_max - y_min;
                x_dimension = x_max - x_min;

                var height = width / x_dimension * y_dimension;

                var itemSize = width / x_dimension,
                    //cellSize = itemSize - 1, // use this if grid lines are wanted
                    cellSize = itemSize; // use this if grid lines are not wanted

                var xScale = d3.scale.ordinal()
                    .domain(x_elements)
                    .rangeBands([0, x_dimension * itemSize]);

                var yScale = d3.scale.ordinal()
                    .domain(y_elements)
                    .rangeBands([0, y_dimension * itemSize]);

                var svg = d3.select('.' + classname)
                    .select("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .select("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                var cells = svg.selectAll('rect')
                    .data(data)
                    .enter()
                    .append('g')
                    .append('rect')
                    .attr('class', 'cell')
                    .attr('width', cellSize)
                    .attr('height', cellSize)
                    .attr('y', function(d) {
                        return yScale(d.y);
                    })
                    .attr('x', function(d) {
                        return xScale(d.x);
                    })

                d3.selectAll('rect')
                    .attr('fill', function(d) {
                        return colorScale(d.value);
                    })
                    .on("mouseover", function(d) {
                        d3.select(this).attr("fill", "#EEEEEE");
                    })
                    .on("mouseout", function(d) {
                        d3.select(this).attr("fill", function(d) {
                            return colorScale(d.value);
                        })
                    });

                d3.select(window).on('resize.updatesvg', updateWindow);

                // figure changes in size according to window side
                function updateWindow() {

                    width = (w.innerWidth || e.clientWidth || g.clientWidth) - margin.right - margin.left;
                    height = width / x_dimension * y_dimension;
                    itemSize = width / x_dimension;
                    //cellSize = itemSize - 1, // use this if grid lines are wanted
                    cellSize = itemSize; // use this if grid lines are not wanted

                    d3.select('svg')
                        .attr("width", width + margin.left + margin.right)
                        .attr("height", height + margin.top + margin.bottom);

                    xScale = d3.scale.ordinal()
                        .domain(x_elements)
                        .rangeBands([0, x_dimension * itemSize]);

                    yScale = d3.scale.ordinal()
                        .domain(y_elements)
                        .rangeBands([0, y_dimension * itemSize]);

                    d3.selectAll('rect')
                        .attr('width', cellSize)
                        .attr('height', cellSize)
                        .attr('y', function(d) {
                            return yScale(d.y);
                        })
                        .attr('x', function(d) {
                            return xScale(d.x);
                        });
                }

                function populateData(xres, yres) {
                    data = [];
                    xScaleFactor = Math.PI / 180. * (360./xres);
                    yScaleFactor = Math.PI / 180. * (180./yres);
                    for (var i = 0; i < xres; ++i) {
                        for (var j = 0; j < yres; ++j) {
                            var newItem = {};
                            newItem.x = i;
                            newItem.y = j;
                            newItem.value = Math.pow(Math.sin(i * xScaleFactor), power1) - Math.pow(1.2 * Math.cos(j * yScaleFactor), power2);
                            data.push(newItem);
                        }
                    };
                }

            }




        }
    ]
});
