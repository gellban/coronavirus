// var text = `
// In some communities, "e-text" is used much more narrowly, to refer to electronic documents that are, so to speak, "plain vanilla ASCII". By this is meant not only that the document is a plain text file, but that it has no information beyond "the text itself"—no representation of bold or italics, paragraph, page, chapter, or footnote boundaries, etc. Michael S. Hart,[2] for example, argued that this "is the only text mode that is easy on both the eyes and the computer". Hart made the correct[according to whom?] point that proprietary word-processor formats made texts grossly inaccessible; but that is irrelevant to standard, open data formats. The narrow sense of "e-text" is now uncommon, because the notion of "just vanilla ASCII" (attractive at first glance), has turned out to have serious difficulties:
//
// First, this narrow type of "e-text" is limited to the English letters. Not even Spanish ñ or the accented vowels used in many European languages cannot be represented (unless awkwardly and ambiguously as "~n" "a'"). Asian, Slavic, Greek, and other writing systems are impossible.
//
// Second, diagrams and pictures cannot be accommodated, and many books have at least some such material; often it is essential to the book.
//
// Third, "e-texts" in this narrow sense have no reliable way to distinguish "the text" from other things that occur in a work. For example, page numbers, page headers, and footnotes might be omitted, or might simply appear as additional lines of text, perhaps with blank lines before and after (or not). An ornate separator line might be represented instead by a line of asterisks (or not). Chapter and sections titles, likewise, are just additional lines of text: they might be detectable by capitalization if they were all caps in the original (or not). Even to discover what conventions (if any) were used, makes each book a new research or reverse-engineering project.
//
// In consequence of this, such texts cannot be reliably re-formatted. A program cannot reliably tell where footnotes, headers or footers are, or perhaps even paragraphs, so it cannot re-arrange the text, for example to fit a narrower screen, or read it aloud for the visually impaired. Programs might apply heuristics to guess at the structure, but this can easily fail.
//
// Fourth, and a perhaps surprisingly[according to whom?] important issue, a "plain-text" e-text affords no way to represent information about the work. For example, is it the first or the tenth edition? Who prepared it, and what rights do they reserve or grant to others? Is this the raw version straight off a scanner, or has it been proofread and corrected? Metadata relating to the text is sometimes included with an e-text, but there is by this definition no way to say whether or where it is preset. At best, the text of the title page might be included (or not), perhaps with centering imitated by indentation.
//
// Fifth, texts with more complicated information cannot really be handled at all. A bilingual edition, or a critical edition with footnotes, commentary, critical apparatus, cross-references, or even the simplest tables. This leads to endless practical problems: for example, if the computer cannot reliably distinguish footnotes, it cannot find a phrase that a footnote interrupts.
//
// Even raw scanner OCR output usually produces more information than this, such as the use of bold and italic. If this information is not kept, it is expensive and time-consuming to reconstruct it; more sophisticated information such as what edition you have, may not be recoverable at all.
//
// If actuality, even "plain text" uses some kind of "markup"—usually control characters, spaces, tabs, and the like: Spaces between words; two returns and 5 spaces for paragraph. The main difference from more formal markup is that "plain texts" use implicit, usually undocumented conventions, which are therefore inconsistent and difficult to recognize.[3]
//
// The narrow sense of e-text as "plain vanilla ASCII" has fallen out of favor.[according to whom?] Nevertheless, many such texts are freely available on the Web, perhaps as much because they are easily produced as because of any purported portability advantage. For many years Project Gutenberg strongly favored this model of text, but with time, has begun to develop and distribute more capable forms such as HTML.
// `;

var sort_json_arr_by_key = function(array, key)
{
 return array.sort(function(a, b)
 {
  var x = a[key]; var y = b[key];
  return ((x < y) ? -1 : ((x > y) ? 1 : 0));
 });
};//sort_json_arr_by_key()

class WordCloudChart{
// constructor(name) {
  constructor() {
    // invokes the setter
    // this.dataset_file_name = "../data/cleaned.csv";//"bar-data.csv";
    // this.country_name = "United States";//"Australia";
    // this.y_axes_text = "Number of Confirmed Cases";
    // console.log('this.dataset_file_name', this.dataset_file_name);
  }
  render(country_name){
    var min_frequency = 1,
        frequency_factor = 200;
    var preprocess_data = this.preprocess_data;
    var render_sub = this.render_sub;
    // this.render_sub(text, min_frequency, frequency_factor);
    // var filename = '../data/tweet_stem_world_all.csv';//"../data/corona_stem_class_website_csv.csv"
    var filename = 'data/tweet_stem_world_all.csv';//"../data/corona_stem_class_website_csv.csv"
    d3.csv(filename, function(error, dataset) {
      if (error) throw error;
      console.log('##dataset - tweets:', dataset);
      var tweet_stems = preprocess_data(dataset, country_name);
      console.log('##dataset - tweets:', tweet_stems);
      render_sub(tweet_stems, min_frequency, frequency_factor);
      // format the data, to be integers instead of strings
    });
  }//render()
  //preprocess dataset
  preprocess_data(dataset, country_name){
    console.log('dataset', dataset);
    var data = [];
    var tweet_stems = '';
    dataset.forEach(function(d) {
      // tweet_stems += d.stem.replace(/[0-9]/g, '');//remove numbers
      tweet_stems += d.stem;
      // console.log("dataset, d:", d, ', d.updated:', d.updated);
      // if (d.country == country_name){
      //   data.push({"updated": d.updated, "confirmed": d.confirmed});
      // }
    });
    console.log('#####tweet_stems:', tweet_stems);
    // alert('finish concactenating tweets');
    return tweet_stems;
  }//preprocess_data()

  render_sub(text, min_frequency, frequency_factor){
    var data_word_cloud = count_words(text, min_frequency, frequency_factor);
    //get last 100 elements

    // alert('finish count_words for tweets');
    data_word_cloud = sort_json_arr_by_key(data_word_cloud, 'value');
    data_word_cloud = data_word_cloud.slice(Math.max(data_word_cloud.length - 1000, 0));
    console.log('data_word_cloud:', data_word_cloud);
    var data = data_word_cloud;
    // var myWords = ["Hello", "Everybody", "How", "Are", "You", "Today", "It", "Is", "A", "Lovely", "Day", "I", "Love", "Coding", "In", "My", "Van", "Mate"]

    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 10, bottom: 10, left: 10},
        width = 450 - margin.left - margin.right,
        height = 450 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var word_cloud_div = "#word_cloud_div";
    var svg = d3.select(word_cloud_div).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");



    var layout = d3.layout.cloud()
        .size([400, 300])
        .words(data)
        .on("end", draw2);

    function draw2(words) {
        var max_freq = 1;
        var my_fill = d3.scaleOrdinal(d3.schemeCategory20);
                  // d3.scaleLinear()
                  // .range([0, max_freq]);
        d3.select("#svg_word_cloud")
            .append("g")
            .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter()
            .append("text")
            .text((d) => d.text)
            .style("font-size", (d) => d.size + "px")
            .style("font-family", (d) => d.font)
            .style("fill", (d, i) => my_fill(i))
            .attr("text-anchor", "middle")
            .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")");
    }





    layout.start();
  }//render_sub()



}//class







// // function count_word(string){
// var string = string = "I I am am am yes yes.";//'I am Hashim Hashim one';
//
//   var pattern = /\w+/g,
//       matchedWords = string.match( pattern );
//
//   var counts = matchedWords.reduce(function ( stats, word ) {
//       console.log('stats', stats);
//       if ( stats.hasOwnProperty( word ) ) {
//           stats[ word ] = stats[ word ] + 1;
//       } else {
//           stats[ word ] = 1;
//       }
//       return json_arr;
//   }, {} );
//
//   var json_arr = []
//   counts.forEach((item, i) => {
//     json_arr.push({text: item, value:i})
//   });
//
//   /* Now that `counts` has our object, we can log it. */
//   console.log('#####????########counts',counts );
// // };//count_word(string)
// // var string = string = "I I am am am yes yes.";//'I am Hashim Hashim one';
// // count_word(string)







console.log("Hashim - It's loaded!");
var myWordCloudChart = new WordCloudChart(); //global variable
myWordCloudChart.render('All');
