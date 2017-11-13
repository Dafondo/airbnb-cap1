$.getJSON('/stats', function (data) {
    Highcharts.chart('graph1', {
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: '30 Day Availability vs Average Review Score',
        },
        xAxis: {
            title: {
                text: 'Days Available in One Month'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true,
            allowDecimals: false
        },
        yAxis: {
            title: {
                text: 'Average Review Score (out of 100)'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{point.x} days available</b><br>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">Average review score:</td>' +
                    '<td style="padding:0">${point.y:.2f}</td></tr>'
                }
            }
        },
        series: [{
            name: 'Availability vs Score',
            data: data[0]
        }]
    });
    cat1 = new Array();
    series1 = new Array();
    for (var item in data[1]) {
        cat1.push(data[1][item][0]);
        series1.push(data[1][item][1]);
    }
    Highcharts.chart('graph2', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Average Price Per Day for Each Neighborhood'
        },
        xAxis: {
            categories: cat1,
            crosshair: true,
            title: {
                text: 'Neighborhood'
            }
        },
        yAxis: {
            title: {
                text: 'Average Price'
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px"><b>{point.key}</b></span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">Price per night:</td>' +
                '<td style="padding:0">${point.y:.2f}</td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'series1',
            data: series1
        }]
    });
    cat2 = new Array();
    series2 = new Array();
    for (var item in data[2]) {
        cat2.push(data[2][item][0]);
        series2.push(data[2][item][1]);
    }
    Highcharts.chart('graph3', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Host Response Time vs Average Communication Rating'
        },
        xAxis: {
            categories: cat2,
            crosshair: true,
            title: {
                text: 'Host Response Time'
            }
        },
        yAxis: {
            title: {
                text: 'Average Communication Rating (out of 10)'
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px"><b>{point.key}</b></span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">Rating: </td>' +
                '<td style="padding:0">{point.y:.2f}</td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'series2',
            data: series2
        }]
    });
});