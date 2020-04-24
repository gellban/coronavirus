
class BarChart{
// constructor(name) {
  constructor() {
    // invokes the setter
    this.dataset_file_name = "../data/cleaned.csv";//"bar-data.csv";
    this.country_name = "United States";//"Australia";
    this.y_axes_text = "Number of Confirmed Cases";
    console.log('this.dataset_file_name', this.dataset_file_name)
  }
  render(p_country_name){
    this.country_name = p_country_name || this.country_name;
    var dataset_file_name = this.dataset_file_name;//"../data/cleaned.csv";//"bar-data.csv";
    var country_name = this.country_name;//"China";//"Australia";
    var y_axes_text = this.y_axes_text;//"Number of Confirmed Cases";
    var div_name = "#svg_bar";
    var margin = {top: 20, right: 20, bottom: 70, left: 40},
        width = 400 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

    // Parse the date / time
    // var	parseDate = d3.time.format("m/d/y").parse;
    console.log('d3', d3)
    // var	parseDate = d3.time.format("%m/%d/%y").parse;
    // var timeFormat = d3.timeFormat('%H:%M:%S %L')
    var	parseDate = d3.timeParse("%m/%d/%y");

    // var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
    var x = d3.scaleBand([0, width], .05);

    var y = d3.scaleLinear([height, 0]);
    // var xScale = d3.scaleBand()
    //     .domain(d3.range(0, data.length))
    //     .range([0, width], .05)
    // var yScale = d3.scaleLinear()
    //     .domain([0, d3.max(data)])
    //     .range([height, 0])


    // var xAxis = d3.svg.axis()
    var xAxis = d3.axisBottom()
        .scale(x)
        // .orient("bottom")
        .tickFormat(d3.timeFormat("%m/%d"));// format the x axis

    var yAxis = d3.axisLeft()
        .scale(y)
        // .orient("left")
        .ticks(10);

    var svg_tag_name = "svg";
    var svg_id = d3.select(div_name).select(svg_tag_name);
    if (svg_id){//delete current chart
      svg_id.remove();
    }

    var svg = d3.select(div_name).append(svg_tag_name)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
    d3.csv(dataset_file_name, function(error, dataset) {
    		console.log('dataset', dataset);
    		var data = [];
    		dataset.forEach(function(d) {
    			// console.log("dataset, d:", d, ', d.updated:', d.updated);
    			if (d.country == country_name){
    				data.push({"date": d.updated, "value": d.confirmed});
    			}
    		});
    		data = groupByArrayJson(data, ["date",  "value"]);
    		console.log('before parsing data', data);
        data.forEach(function(d) {
            d.date = parseDate(d.date);
            d.value = +d.value;
        });
    		console.log('after parsing data', data);

      x.domain(data.map(function(d) { return d.date; }));
      // x.domain(data.map(function(d) { return d.value; }));
      y.domain([0, d3.max(data, function(d) { return d.value; })]);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(15," + height + ")")
          .call(xAxis)
        .selectAll("text")
          .style("text-anchor", "end")
          .attr("dx", "-.8em")
          .attr("dy", "-.55em")
          .attr("transform", "rotate(-90)" );

      svg.append("g")
          .attr("class", "y axis")
          // .attr("x",30+0 - (height / 1))
          .call(yAxis)
          .attr("transform", "translate(15,0)")
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - margin.left-10)
          .attr("x",0 - (height / 2))
          .attr("dy", ".71em")
          .style("text-anchor", "middle")
          .text(y_axes_text);

      svg.selectAll("bar")
          .data(data)
        .enter().append("rect")
          .style("fill", "steelblue")
          .attr("x", function(d) { return x(d.date); })
          // .attr("width", x.rangeBand())
          .attr("width", x())
          // .attr("y", function(d) { return y(0); })
          // .attr("height", function(d) { return height - y(0); })
          // .attr("transform", "translate(15,0)")
          // .transition()
          // .duration(2000)
          // .delay(function(d,i){console.log('^^^^^^^i', i) ; return(i*100)})
          ;

        // Animation
        // svg.selectAll("rect")
        //   .transition()
        //   .duration(800)
        //   .attr("y", function(d) { return y(d.value); })
        //   .attr("height", function(d) { return height - y(d.value); })
        //   .delay(function(d,i){console.log(i) ; return(i*100)})
        //
        // });

    });
  }
}//BarChart
window.addEventListener('load', function () {
  console.log("Hashim - It's loaded!")
  myBarChart = new BarChart("test");
  c = "China";
  myBarChart.render(c);
  // c = "United States"
  // myBarChart.render(c);
})
