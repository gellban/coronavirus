// https://bl.ocks.org/d3noob/bdf28027e0ce70bd132edc64f1dd7ea4
// set the dimensions and margins of the graph
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// set the ranges
var x = d3.scaleBand()
          .range([0, width])
          .padding(0.1);
var y = d3.scaleLinear()
          .range([height, 0]);

var	parseDate = d3.timeParse("%m/%d/%y");

// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("#svg_bar").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
console.log('##svg created');
// get the data
d3.csv("../data/cleaned.csv", function(error, data) {
  if (error) throw error;

  // format the data, to be integers instead of strings
  data.forEach(function(d) {
    d.updated = parseDate(d.updated);
    d.confirmed = +d.confirmed;
    d.suspected = +d.suspected;
    d.recovered = +d.recovered;
    d.deaths = +d.deaths;

  });
  console.log('##data:', data);
  // Scale the range of the data in the domains
  x.domain(data.map(function(d) { return d.updated; }));
  y.domain([0, d3.max(data, function(d) { return d.confirmed; })]);

  // append the rectangles for the bar chart
  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.updated); })
      .attr("width", x.bandwidth())
      .attr("y", function(d) { return y(d.confirmed); })
      .attr("height", function(d) { return height - y(d.confirmed); });

  // add the x Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  // add the y Axis
  svg.append("g")
      .call(d3.axisLeft(y));

});
