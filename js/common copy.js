//https://stackoverflow.com/questions/43574348/grouping-a-csv-file-in-d3
var d3groupby = function(csv_file_name, col_names_arr, rollback){
  // var col_names_arr = ["country", "confirmed", "recovered", "deaths"];
  console.log('csv_file_name:', csv_file_name, 'col_names_arr:', col_names_arr);
  var data;// = d3.csv.parse(d3.select('#data_csv').text());
  d3.csv(csv_file_name, function(err, data_temp) {
    if (err) {console.log('Error reading csv file');}
    console.log('Read csv file successfully');
    data = data_temp;
    console.log('data[0]', data[0]);
    var valuesByKey;
    var key_name = col_names_arr[0];
    var col1_name = col_names_arr[1];
    var col2_name = col_names_arr[2];
    var col3_name = col_names_arr[3];

    console.log('data.forEach');
    data.forEach(function(d){
    	//group and organize your data as needed here
      valuesByKey = d3.nest()
      //set the decade as your key
      .key(function(d) {return d[key_name];})
      //rollup and sum your cat values by decade
      .rollup((function(d) {
        return {
            col1: d3.sum(d, function(e) { return e[col1_name]; }),
            col2: d3.sum(d, function(e) { return e[col2_name]; }),
            col3: d3.sum(d, function(e) { return e[col3_name]; }),
        };
      }))
      .entries(data);
    });
    // console.log('valuesByKey', valuesByKey);
    rollback(valuesByKey);
  });

  // rollback(valuesByKey);
}
