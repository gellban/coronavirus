
console.log('##Start map')
// function delayedHello(callback) {
//
//     console.log("Hello!");
//     d3groupby(csv_file_name, col_names_arr, function(dataset) {
//       console.log('dataset', dataset);
//       dataset.forEach(function(d){
//         // console.log('dataset.forEach, d:', d);
//         data.set(d.key, +d.value.col1);
//       });
//       console.log('data', data);
//       console.log('data.get("Mainland China")', data.get("Mainland China"));
//       return data;
//     });//read data
//     callback(null);
//
// }
// var q = d3.queue();
// q.defer(delayedHello);
// q.defer(delayedHello);
// q.await(function(error) {
//   if (error) throw error;
//   console.log("Goodbye!");
// });


var svg_map = "#svg_map_div";
// The svg:  select svg div, and get width and height attributes. Similar to jQuery
// var svg = d3.select(svg_map);
console.log('2');
var svg = d3.select(svg_map).append("svg")
        .attr("width", 800)
        .attr("height", 500)
;
console.log('###svg', svg);
console.log('3');

var    width = +svg.attr("width"),
    height = +svg.attr("height");

// Append Div for tooltip to SVG
var tooltip = d3.select("body")
		    .append("div")
    		.attr("class", "tooltip")
    		.style("opacity", 0);
// Map and projection
var path = d3.geoPath();
var projection = d3.geoNaturalEarth()
.scale(width / 2 / Math.PI)
.translate([width / 2, height / 2])
// var projection = d3.geoAiry().rotate(rotate).clipAngle(90);
var path = d3.geoPath()
    .projection(projection);

// Data and color scale
var data = d3.map();
var country_codes = d3.map();
// var data_temp = d3.map();
var colorScheme = d3.schemeReds[6];//number of different red fill color
// var colorScheme = d3.schemeBlues[6];//number of different red fill color
colorScheme.unshift("#eee")
var colorScale = d3.scaleThreshold()
    // .domain([1, 6, 11, 26, 101, 1001])
    .domain([1, 6, 11, 16, 21, 101])
    // .domain([10, 60, 110, 260, 101000000, 10010000000])
    .range(colorScheme);


// Legend
var g = svg.append("g")
    .attr("class", "legendThreshold")
    .attr("transform", "translate(20,20)");
g.append("text")
    .attr("class", "caption")
    .attr("x", 0)
    .attr("y", -6)
    .text("#Confirmed Cases");
var labels = ['0', '1-5', '6-10', '11-15', '16-20', '21-100', '> 100'];
var legend = d3.legendColor()
    .labels(function (d) { return labels[d.i]; })
    .shapePadding(4)
    .scale(colorScale);
svg.select(".legendThreshold")
    .call(legend);
var col_names_arr = ["country", "confirmed", "recovered", "deaths"];
// var csv_file_name = "../data/cleaned.csv"
var csv_file_name = "data/cleaned.csv"





// var key_name = col_names_arr[0];
// var col_names_arr = col_names[1:];
// Load external data and boot
// d3.queue()
//     // .defer(d3.json, "geomap/world_geo.geojson")//geo svg map json dataset
//     // .defer(d3.csv, "data/mooc-countries.csv", function(d) { data.set(d.code, +d.total); })//read data
//     // .defer(d3.csv, "data/mooc-countries.csv", function(d) { data_temp.set(d.id, +d.total); })//read data
//     // .defer(d3groupby,csv_file_name, col_names_arr, function(dataset) {
//     //   console.log('dataset', dataset);
//     //   dataset.forEach(function(d){
//     //     // console.log('dataset.forEach, d:', d);
//     //     data.set(d.key, +d.value.col1);
//     //   });
//     //   console.log('data', data);
//     //   console.log('data.get("Mainland China")', data.get("Mainland China"));
//     //   // return data;
//     // })//read data
//     // .defer(delayedHello)
//     .await(test);
//     // .await(render_map);

d3groupby(csv_file_name, col_names_arr, function(dataset) {
  console.log('dataset', dataset);
  dataset.forEach(function(d){
    // console.log('dataset.forEach, d:', d);
    data.set(d.key, +d.value.col1);
  });
  console.log('data', data);
  console.log('data.get("Mainland China")', data.get("Mainland China"));

  d3.queue()
      .defer(d3.json, "geomap/world_geo.geojson")//geo svg map json dataset
      .defer(d3.csv, "data/country_codes.csv", (d) => {country_codes.set(d.alpha_3, d.name);})//save country 3-alpha abbrev
      // .await(test);
      .await(render_map);
  // return data;
});//read data

function test() {
  console.log('start test123().');
}
function render_map(error, topo) {
    console.log('start ready().');
    if (error) throw error;
    // console.log('start ready(), topo:', topo);
    // console.log('country_codes', country_codes);



    // Draw the map
    svg.append("g")
        .attr("class", "countries")
        .selectAll("path")
        .data(topo.features)
        .enter().append("path")
            .attr("fill", function (d){
                // Pull data for this country
                var key = d.properties.name;
                var ckey = country_codes.get(d.id);//get country name
                // console.log('geo data, country apprevd.id,d:',d, 'key', key, 'data.get(key)', data.get(key), ' ckey', ckey, 'd.id', d.id, 'data.get(ckey)', data.get(ckey));
                // d.total = data.get(d.id) || 0;
                d.value = data.get(ckey) || 0;
                // Set the color
                return colorScale(d.value);
            })
            .attr("d", path)
            .on("mouseover", function(d, i){
              // console.log("hover, d", d);
              var currentState = this;
              d3.select(this)
              .style('stroke', '#ccc')
              ;

              tooltip.transition()
                    	   .duration(200)
                         .style("opacity", .9);
               tooltip.text(d.properties.name + "(" + d.id + "):" + d.value)
               .style("left", (d3.event.pageX) + "px")
               .style("top", (d3.event.pageY - 28) + "px")
               .style("opacity", 1)
               ;
            })
            .on('mouseout', function(d, i) {
                // console.log("mouseout, d", d);
                d3.select(this).style('stroke', '#fff');

                tooltip.transition()
                          .duration(500)
                          .style("opacity", 0);
                // d3.selectAll('path')
                //         .style({
                //             'fill':"steelblue"
                //         });
            })
            .on("click", function(d) {
              var country_name = country_codes.get(d.id);//get country name
              console.log('on click, d:', d, '#key:', d.id, '#value:', d.value, 'country_name', country_name);
              myBarChart.render(country_name);
            })
            ;
}
