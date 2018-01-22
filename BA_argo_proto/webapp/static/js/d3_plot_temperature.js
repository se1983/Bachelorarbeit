// TODO Neue struktur

var margin = {top: 3, right: 2, bottom: 3, left: 5},
    width = 300 - margin.left - margin.right,
    height = 150 - margin.top - margin.bottom;

var parseDate = d3.time.format("%a, %d.%b %Y %H:%M:%S GMT").parse;
//
// var parseDate = d3.timeParse("%a, %d %b %Y %H:%M:%S GMT")

/* Achsendefinition */
// https://i.imgur.com/24Y31C2.png
var x = d3.time.scale().range([0, width]);
var y = d3.scale.linear().range([height, 0]);


// Einstellen der Achsenbeschriftungen
// TODO: Eigene Steuerung der Tick-Abstände - Feststellen der Y-Achse
var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);
var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(10);
// Define the line
var valueline = d3.svg.line()
    .interpolate("basis")
    .x(function (d) {
        return x(d.date);
    })
    .y(function (d) {
        return y(d.value);
    });

// Das SVG Canvas Element hinzufügen
var svg = d3.select(".animation")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function create_graph(identifier, data_type) {
    var URI = '/argo_float/' + identifier + '/' + data_type;
    console.log(URI);
    d3.json(URI, function (error, data) {

        data.forEach(function (d) {
        console.log(d);
        d.date = new Date(d.date);
        d.value = +d.value;
    });

    /* Anpassung der Achsen */
    // Werte werden so eingelesen dass sie in die Größe der Achsen passen
    x.domain(d3.extent(data, function (d) {
        return d.date;
    }));
    y.domain([0, d3.max(data, function (d) {
        return d.value;
    })]);

    // Zeichnen der Daten
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));

    // Zeichnen der X-Achse
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
    // Zeichnen der Y-Achse
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
    });
}


function update_graph(identidier, data_type) {


    data.forEach(function (d) {
        d.date = parseDate(d.date);
        d.value = +d.value;
    });
    // Scale the range of the data again
    x.domain(d3.extent(data, function (d) {
        return d.date;
    }));
    y.domain([0, d3.max(data, function (d) {
        return d.value;
    })]);
    // Select the section we want to apply our changes to
    var svg = d3.select("body").transition();
    // Make the changes
    svg.select(".line")   // change the line
        .duration(750)
        .attr("d", valueline(data));
    svg.select(".x.axis") // change the x axis
        .duration(750)
        .call(xAxis);
    svg.select(".y.axis") // change the y axis
        .duration(750)
        .call(yAxis);

}

function get_data(float_identifier, dataset){
    var URI = '/argo_float/' + float_identifier + '/' + dataset;
    console.log(URI);
    d3.json(URI,
    function (error, data) {
        console.log(error);
        console.log(data);
        return data;
    });

}
