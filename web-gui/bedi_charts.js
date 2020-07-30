$( document ).ready(function() {
    var ctx = document.getElementById('BEDICharts').getContext('2d');

    $.ajaxSetup({
        async: false
    });

    var labels = [];
    var bedi_audi = [];
    var sentiment_audi = [];
    var likelihood_audi = [];
    $.getJSON('data/merged-data-audi.json', function(data) {
        results_audi = data;
        results_audi.sort(compare);
        results_audi.forEach(function(item){
            labels.push(item.date);
            bedi_audi.push(item.bedi);
            sentiment_audi.push(item.sentiment);
            likelihood_audi.push(item.likelihood);
        });
    });
    var bedi_vw = [];
    var sentiment_vw = [];
    var likelihood_vw = [];
    $.getJSON('data/merged-data-volkswagen.json', function(data2) {
        results_vw = data2;
        results_vw.sort(compare);
        results_vw.forEach(function(item2){
            bedi_vw.push(item2.bedi);
            sentiment_vw.push(item2.sentiment);
            likelihood_vw.push(item2.likelihood);
        });
    });
    var bedi_mercedes = [];
    var sentiment_mercedes = [];
    var likelihood_mercedes = [];
    $.getJSON('data/merged-data-mercedes.json', function(data3) {
        results_mercedes = data3;
        results_mercedes.sort(compare);
        results_mercedes.forEach(function(item3){
            bedi_mercedes.push(item3.bedi);
            sentiment_mercedes.push(item3.sentiment);
            likelihood_mercedes.push(item3.likelihood);
        });
    });
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            fill: false,
            datasets: [{
                label: 'BEDI Audi e-tron',
                data: bedi_audi,
                yAxisID: 'A',
                borderColor: '#00aaee',
                borderWidth: 4,
                fill: false,
            },
            {
                label: 'Sentiment Audi e-tron',
                data: sentiment_audi,
                yAxisID: 'B',
                borderColor: '#ff0000',
                borderWidth: 4,
                hidden: true,
                fill: false,
            },
            {
                label: 'Likelihood Audi e-tron',
                data: likelihood_audi,
                yAxisID: 'B',
                borderColor: '#00ee00',
                borderWidth: 4,
                hidden: true,
                fill: false,
            },
            {
                label: 'BEDI VW id.3',
                data: bedi_vw,
                yAxisID: 'A',
                borderColor: '#0066ee',
                borderWidth: 4,
                fill: false,
            },
            {
                label: 'Sentiment VW id.3',
                data: sentiment_vw,
                yAxisID: 'B',
                borderColor: '#bb2200',
                borderWidth: 4,
                hidden: true,
                fill: false,
            },
            {
                label: 'Likelihood VW id.3',
                data: likelihood_vw,
                yAxisID: 'B',
                borderColor: '#44cc44',
                borderWidth: 4,
                hidden: true,
                fill: false,
            },
            {
                label: 'BEDI Mercedes EQC',
                data: bedi_mercedes,
                yAxisID: 'A',
                borderColor: '#0022ee',
                borderWidth: 4,
                fill: false,
            },
            {
                label: 'Sentiment Mercedes EQC',
                data: sentiment_mercedes,
                yAxisID: 'B',
                borderColor: '#884400',
                borderWidth: 4,
                hidden: true,
                fill: false,
            },
            {
                label: 'Likelihood Mercedes EQC',
                data: likelihood_mercedes,
                yAxisID: 'B',
                borderColor: '#88aa88',
                borderWidth: 4,
                hidden: true,
                fill: false,
            },
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
                    ticks:{
                        min: -0.0015,
                        max: 0.0015
                    }
                  }, {
                    id: 'B',
                    type: 'linear',
                    position: 'right',
                    scaleLabel: {
                        display: true,
                        labelString: 'Sentiment & Likelihood',
                    },
                    ticks: {
                      max: 0.15,
                      min: -0.15
                    }
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
        myChart.update()
    })

    $('#audi').click(function(){
        myChart.data.datasets[0].hidden = false
        myChart.data.datasets[1].hidden = false
        myChart.data.datasets[2].hidden = false
        myChart.data.datasets[3].hidden = true
        myChart.data.datasets[4].hidden = true
        myChart.data.datasets[5].hidden = true
        myChart.data.datasets[6].hidden = true
        myChart.data.datasets[7].hidden = true
        myChart.data.datasets[8].hidden = true
        myChart.update()
    })

    $('#vw').click(function(){
        myChart.data.datasets[0].hidden = true
        myChart.data.datasets[1].hidden = true
        myChart.data.datasets[2].hidden = true
        myChart.data.datasets[3].hidden = false
        myChart.data.datasets[4].hidden = false
        myChart.data.datasets[5].hidden = false
        myChart.data.datasets[6].hidden = true
        myChart.data.datasets[7].hidden = true
        myChart.data.datasets[8].hidden = true
        myChart.update()
    })

    $('#mercedes').click(function(){
        myChart.data.datasets[0].hidden = true
        myChart.data.datasets[1].hidden = true
        myChart.data.datasets[2].hidden = true
        myChart.data.datasets[3].hidden = true
        myChart.data.datasets[4].hidden = true
        myChart.data.datasets[5].hidden = true
        myChart.data.datasets[6].hidden = false
        myChart.data.datasets[7].hidden = false
        myChart.data.datasets[8].hidden = false
        myChart.update()
    })

    $('#bedi').click(function(){
        myChart.data.datasets[0].hidden = false
        myChart.data.datasets[1].hidden = true
        myChart.data.datasets[2].hidden = true
        myChart.data.datasets[3].hidden = false
        myChart.data.datasets[4].hidden = true
        myChart.data.datasets[5].hidden = true
        myChart.data.datasets[6].hidden = false
        myChart.data.datasets[7].hidden = true
        myChart.data.datasets[8].hidden = true
        myChart.update()
    })

    $('#sentiment').click(function(){
        myChart.data.datasets[0].hidden = true
        myChart.data.datasets[1].hidden = false
        myChart.data.datasets[2].hidden = true
        myChart.data.datasets[3].hidden = true
        myChart.data.datasets[4].hidden = false
        myChart.data.datasets[5].hidden = true
        myChart.data.datasets[6].hidden = true
        myChart.data.datasets[7].hidden = false
        myChart.data.datasets[8].hidden = true
        myChart.update()
    })

    $('#likelihood').click(function(){
        myChart.data.datasets[0].hidden = true
        myChart.data.datasets[1].hidden = true
        myChart.data.datasets[2].hidden = false
        myChart.data.datasets[3].hidden = true
        myChart.data.datasets[4].hidden = true
        myChart.data.datasets[5].hidden = false
        myChart.data.datasets[6].hidden = true
        myChart.data.datasets[7].hidden = true
        myChart.data.datasets[8].hidden = false
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

