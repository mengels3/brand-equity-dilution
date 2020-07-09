$( document ).ready(function() {
    var ctx = document.getElementById('BEDICharts').getContext('2d');

    $.ajaxSetup({
        async: false
    });

    var labels = [];
    var bedi_audi = [];
    var visibility_audi = [];
    var sentiment_audi = [];
    var likelihood_audi = [];
    $.getJSON('data/merged-data-audi.json', function(data) {
        results_audi = data;
        results_audi.sort(compare);
        results_audi.forEach(function(item){
            labels.push(item.date);
            bedi_audi.push(item.bedi);
            visibility_audi.push(item.visibility);
            sentiment_audi.push(item.sentiment);
            likelihood_audi.push(item.likelihood);
        });
    });
    var bedi_vw = [];
    var visibility_vw = [];
    var sentiment_vw = [];
    var likelihood_vw = [];
    $.getJSON('data/merged-data-volkswagen.json', function(data2) {
        results_vw = data2;
        results_vw.forEach(function(item2){
            bedi_vw.push(item2.bedi);
            visibility_vw.push(item2.visibility);
            sentiment_vw.push(item2.sentiment);
            likelihood_vw.push(item2.likelihood);
        });
    });
    var bedi_mercedes = [];
    var visibility_mercedes = [];
    var sentiment_mercedes = [];
    var likelihood_mercedes = [];
    $.getJSON('data/merged-data-mercedes.json', function(data3) {
        results_mercedes = data3;
        results_mercedes.forEach(function(item3){
            bedi_mercedes.push(item3.bedi);
            visibility_mercedes.push(item3.visibility);
            sentiment_mercedes.push(item3.sentiment);
            likelihood_mercedes.push(item3.likelihood);
        });
    });
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'BEDI Audi e-tron',
                data: bedi_audi,
                yAxisID: 'A',
                borderColor: '#00aaee',
                borderWidth: 4
            },
            {
                label: 'Sentiment Audi e-tron',
                data: sentiment_audi,
                yAxisID: 'B',
                borderColor: '#ff0000',
                borderWidth: 4,
                hidden: true,
            },
            {
                label: 'Likelihood Audi e-tron',
                data: likelihood_audi,
                yAxisID: 'B',
                borderColor: '#00ee00',
                borderWidth: 4,
                hidden: true
            },
            {
                label: 'Visibility Audi e-tron',
                data: visibility_audi,
                yAxisID: 'B',
                borderColor: '#ffdd00',
                borderWidth: 4,
                hidden: true
            },
            {
                label: 'BEDI VW id.3',
                data: bedi_vw,
                yAxisID: 'A',
                borderColor: '#0066ee',
                borderWidth: 4
            },
            {
                label: 'Sentiment VW id.3',
                data: sentiment_vw,
                yAxisID: 'B',
                borderColor: '#bb2200',
                borderWidth: 4,
                hidden: true
            },
            {
                label: 'Likelihood VW id.3',
                data: likelihood_vw,
                yAxisID: 'B',
                borderColor: '#44cc44',
                borderWidth: 4,
                hidden: true
            },
            {
                label: 'Visibility VW id.3',
                data: visibility_vw,
                yAxisID: 'B',
                borderColor: '#ffbb00',
                borderWidth: 4,
                hidden: true
            },
            {
                label: 'BEDI Mercedes EQC',
                data: bedi_mercedes,
                yAxisID: 'A',
                borderColor: '#0022ee',
                borderWidth: 4,
            },
            {
                label: 'Sentiment Mercedes EQC',
                data: sentiment_mercedes,
                yAxisID: 'B',
                borderColor: '#884400',
                borderWidth: 4,
                hidden: true
            },
            {
                label: 'Likelihood Mercedes EQC',
                data: likelihood_mercedes,
                yAxisID: 'B',
                borderColor: '#88aa88',
                borderWidth: 4,
                hidden: true
            },
            {
                label: 'Visibility Mercedes EQC',
                data: visibility_mercedes,
                yAxisID: 'B',
                borderColor: '#ff8800',
                borderWidth: 4,
                hidden: true
            }
            ]
        },
        options: {
            scales: {
                 yAxes: [{
                    id: 'A',
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        display: true,
                        labelString: 'BEDI',
                    },
                    // ticks:{
                    //     min: -0.005,
                    //     max: 0.005
                    // }
                  }, {
                    id: 'B',
                    type: 'linear',
                    position: 'right',
                    scaleLabel: {
                        display: true,
                        labelString: 'Sentiment, Likelihood, Visibility',
                    },
                    // ticks: {
                    //   max: 0.2,
                    //   min: -0.2
                    // }
                  }]
            },
            responsive: true,
            legend: {
                position: 'left',
                align: 'middle'

            }
        }
    });

    $('#all').click(function(){
        myChart.data.datasets[0].hidden = false
        myChart.data.datasets[1].hidden = false
        myChart.data.datasets[2].hidden = false
        myChart.data.datasets[3].hidden = false
        myChart.data.datasets[4].hidden = false
        myChart.data.datasets[5].hidden = false
        myChart.data.datasets[6].hidden = false
        myChart.data.datasets[7].hidden = false
        myChart.data.datasets[8].hidden = false
        myChart.data.datasets[9].hidden = false
        myChart.data.datasets[10].hidden = false
        myChart.data.datasets[11].hidden = false
        myChart.update()
    })

    $('#audi').click(function(){
        myChart.data.datasets[0].hidden = false
        myChart.data.datasets[1].hidden = false
        myChart.data.datasets[2].hidden = false
        myChart.data.datasets[3].hidden = false
        myChart.data.datasets[4].hidden = true
        myChart.data.datasets[5].hidden = true
        myChart.data.datasets[6].hidden = true
        myChart.data.datasets[7].hidden = true
        myChart.data.datasets[8].hidden = true
        myChart.data.datasets[9].hidden = true
        myChart.data.datasets[10].hidden = true
        myChart.data.datasets[11].hidden = true
        myChart.update()
    })

    $('#vw').click(function(){
        myChart.data.datasets[0].hidden = true
        myChart.data.datasets[1].hidden = true
        myChart.data.datasets[2].hidden = true
        myChart.data.datasets[3].hidden = true
        myChart.data.datasets[4].hidden = false
        myChart.data.datasets[5].hidden = false
        myChart.data.datasets[6].hidden = false
        myChart.data.datasets[7].hidden = false
        myChart.data.datasets[8].hidden = true
        myChart.data.datasets[9].hidden = true
        myChart.data.datasets[10].hidden = true
        myChart.data.datasets[11].hidden = true
        myChart.update()
    })

    $('#mercedes').click(function(){
        myChart.data.datasets[0].hidden = true
        myChart.data.datasets[1].hidden = true
        myChart.data.datasets[2].hidden = true
        myChart.data.datasets[3].hidden = true
        myChart.data.datasets[4].hidden = true
        myChart.data.datasets[5].hidden = true
        myChart.data.datasets[6].hidden = true
        myChart.data.datasets[7].hidden = true
        myChart.data.datasets[8].hidden = false
        myChart.data.datasets[9].hidden = false
        myChart.data.datasets[10].hidden = false
        myChart.data.datasets[11].hidden = false
        myChart.update()
    })

    $('#bedi').click(function(){
        myChart.data.datasets[0].hidden = false
        myChart.data.datasets[1].hidden = true
        myChart.data.datasets[2].hidden = true
        myChart.data.datasets[3].hidden = true
        myChart.data.datasets[4].hidden = false
        myChart.data.datasets[5].hidden = true
        myChart.data.datasets[6].hidden = true
        myChart.data.datasets[7].hidden = true
        myChart.data.datasets[8].hidden = false
        myChart.data.datasets[9].hidden = true
        myChart.data.datasets[10].hidden = true
        myChart.data.datasets[11].hidden = true
        myChart.update()
    })

    $('#sentiment').click(function(){
        myChart.data.datasets[0].hidden = true
        myChart.data.datasets[1].hidden = false
        myChart.data.datasets[2].hidden = true
        myChart.data.datasets[3].hidden = true
        myChart.data.datasets[4].hidden = true
        myChart.data.datasets[5].hidden = false
        myChart.data.datasets[6].hidden = true
        myChart.data.datasets[7].hidden = true
        myChart.data.datasets[8].hidden = true
        myChart.data.datasets[9].hidden = false
        myChart.data.datasets[10].hidden = true
        myChart.data.datasets[11].hidden = true
        myChart.update()
    })

    $('#likelihood').click(function(){
        myChart.data.datasets[0].hidden = true
        myChart.data.datasets[1].hidden = true
        myChart.data.datasets[2].hidden = false
        myChart.data.datasets[3].hidden = true
        myChart.data.datasets[4].hidden = true
        myChart.data.datasets[5].hidden = true
        myChart.data.datasets[6].hidden = false
        myChart.data.datasets[7].hidden = true
        myChart.data.datasets[8].hidden = true
        myChart.data.datasets[9].hidden = true
        myChart.data.datasets[10].hidden = false
        myChart.data.datasets[11].hidden = true
        myChart.update()
    })

    $('#visibility').click(function(){
        myChart.data.datasets[0].hidden = true
        myChart.data.datasets[1].hidden = true
        myChart.data.datasets[2].hidden = true
        myChart.data.datasets[3].hidden = false
        myChart.data.datasets[4].hidden = true
        myChart.data.datasets[5].hidden = true
        myChart.data.datasets[6].hidden = true
        myChart.data.datasets[7].hidden = false
        myChart.data.datasets[8].hidden = true
        myChart.data.datasets[9].hidden = true
        myChart.data.datasets[10].hidden = true
        myChart.data.datasets[11].hidden = false
        myChart.update()
    })
    
    function compare( a, b ) {
        if ( a.date < b.date ){
            return -1;
        }
        if ( a.date > b.date ){
            return 1;
        }
        return 0;
    };

});

