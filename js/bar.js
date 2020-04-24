// https://bl.ocks.org/d3noob/bdf28027e0ce70bd132edc64f1dd7ea4
// set the dimensions and margins of the graph
class BarChart{
// constructor(name) {
  constructor() {
    // invokes the setter
    // this.dataset_file_name = "../data/cleaned.csv";//"bar-data.csv";
    this.dataset_file_name = "data/cleaned.csv";//"bar-data.csv";
    this.country_name = "United States";//"Australia";
    this.y_axes_text = "Number of Confirmed Cases";
    console.log('this.dataset_file_name', this.dataset_file_name);
  }
  preprocess_data(dataset, country_name){
    console.log('dataset', dataset);
    var data = [];
    dataset.forEach(function(d) {
      // console.log("dataset, d:", d, ', d.updated:', d.updated);
      if (d.country == country_name){
        data.push({"updated": d.updated, "confirmed": d.confirmed});
      }
    });
    var	parseDate = d3.timeParse("%m/%d/%y");

    // data.forEach(function(d) {
    //   d.updated = parseDate(d.updated);
    //   d.confirmed = +d.confirmed;
    //   d.suspected = +d.suspected;
    //   d.recovered = +d.recovered;
    //   d.deaths = +d.deaths;
    //
    // });
    data = groupByArrayJson(data, ["updated",  "confirmed"]);
    data.forEach(function(d) {
      d.updated = parseDate(d.date);
      d.confirmed = +d.value;
      // d.suspected = +d.suspected;
      // d.recovered = +d.recovered;
      // d.deaths = +d.deaths;

    });
    console.log('before parsing data', data);
    // data.forEach(function(d) {
    //     d.date = parseDate(d.date);
    //     d.value = +d.value;
    // });


    console.log('###after parsing data', data);

    return data;
  }
  render(p_country_name){
    this.country_name = p_country_name || this.country_name;
    var dataset_file_name = this.dataset_file_name;//"../data/cleaned.csv";//"bar-data.csv";
    var country_name = this.country_name;//"China";//"Australia";
    var y_axes_text = this.y_axes_text;//"Number of Confirmed Cases";
    var div_name = "#svg_bar";
    var svg_tag_name = "svg";

    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 400 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom;

    // set the ranges
    var x = d3.scaleBand()
              .range([0, width])
              .padding(0.1);
    var y = d3.scaleLinear()
              .range([height, 0]);


    var xAxis = d3.axisBottom()
        .scale(x)
        // .orient("bottom")
        .tickFormat(d3.timeFormat("%m/%d"));// format the x axis


    var svg_id = d3.select(div_name).select(svg_tag_name);
    if (svg_id){//delete current chart
      svg_id.remove();
    }
    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select(div_name).append(svg_tag_name)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
    console.log('##svg created');
    var preprocess_data = this.preprocess_data;
    // get the data
    // d3.csv("../data/cleaned.csv", function(error, data) {
    d3.csv("data/cleaned.csv", function(error, data) {
        if (error) throw error;
      data = preprocess_data(data, country_name);
      // format the data, to be integers instead of strings

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
          // .attr("y", function(d) { return y(d.confirmed); })
          // .attr("height", function(d) { return height - y(d.confirmed); });
          .attr("y", function(d) { return y(0); })
          .attr("height", function(d) { return height - y(0); });

          // Animation
          svg.selectAll("rect")
            .transition()
            .duration(800)
            .attr("y", function(d) { return y(d.confirmed); })
            .attr("height", function(d) { return height - y(d.confirmed); })
            .delay(function(d,i){console.log(i) ; return(i*100)});

      // add the x Axis
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          //.call(d3.axisBottom(x));
          .call(xAxis);

      // add the y Axis
      svg.append("g")
          .call(d3.axisLeft(y));

    });
  };
};

console.log("Hashim - It's loaded!")
myBarChart = new BarChart();
c = "China";
myBarChart.render(c);

c = "United States"
myBarChart.render(c);
