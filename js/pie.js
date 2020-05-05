var chart = c3.generate({
    bindto: '#pie_chart',
    data: {
        // iris data from R
        columns: [
            ['Awareness', 870],
            ['Myth', 387],
            ['News', 627],
        ],
        type : 'pie',
        onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
    }
});