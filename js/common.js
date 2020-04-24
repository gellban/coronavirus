//https://stackoverflow.com/questions/43574348/grouping-a-csv-file-in-d3
var d3groupby = function(csv_file_name, col_names_arr, callback){
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
    callback(valuesByKey);
  });

  // rollback(valuesByKey);
};//d3groupby


var groupByArrayJson = function(data, col_names_arr){
  var key_name = col_names_arr[0];
  var value_name = col_names_arr[1];
  // data.forEach(function(d){
  //   //group and organize your data as needed here
  //   valuesByKey = d3.nest()
  //   //set the decade as your key
  //   .key(function(d) {return d[key_name];})
  //   //rollup and sum your cat values by decade
  //   .rollup((function(d) {
  //     return {
  //         value: d3.sum(d, function(e) { return e[value_name]; }),
  //     };
  //   }))//.rollup
  //   .entries(data);
  // });//data.forEach
  // console.log('groupByArrayJson, data:', data);
  // return data;

  var result = [];
  array = data
  array.reduce(function(res, value) {
    key = value[key_name];
    value = parseInt(value[value_name]);
    // console.log('groupByArrayJson, key', key, ', value', value);
    if (!res[key]) {
      res[key] = { date: key, value: 0 };
      result.push(res[key])
      // console.log("#####!res[key]:", res[key]);
    }
    // console.log("#####res[key]:", res[key]);
    res[key].value += value;

    return res;
  }, {});
  // console.log('groupByArrayJson, result', result);
  return result;
};//groupByArrayJson()





function count_words(p_text, min_frequency, frequency_factor){
  var pattern = /\w+/g,
          // p_text = "I I am am am yes yes.",
      matchedWords = p_text.match( pattern );

  var counts = matchedWords.reduce(function(stats, word) {

    if (stats.hasOwnProperty(word)) {
      stats[word] = stats[word] + 1;
    } else {
      stats[word] = 1;
    }
    return stats;

  }, {});
  // console.log( counts );
    var json_arr = []
    // counts.forEach((item, i) => {
    //   json_arr.push({text: item, value:i})
    // });
    Object.keys(counts).forEach(function(key) {
      var i = counts[key];
      // console.table('Key : ' + key + ', Value : ' + i);
      if (i > min_frequency){
        json_arr.push({text: key, value:i*frequency_factor});
      }

    });
    console.log('json_arr', json_arr);
    return json_arr;

};//count_words(text)
