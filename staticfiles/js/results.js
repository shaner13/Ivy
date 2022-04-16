//prediction data
const yearly_vals = JSON.parse(document.getElementById('yearly_json').textContent);
console.log(yearly_vals)

const monthly_vals = JSON.parse(document.getElementById('monthly_json').textContent);
console.log(monthly_vals)

data = createData(yearly_vals, monthly_vals)
yearly_KwH = data[0]
yearly_Savings = data[1]
KwH_drilldown_data = data[2]
Savings_drilldown_data = data[3]

// Create the chart
Highcharts.chart('kwh_chart', {
    chart: {
        type: 'line'
    },
    title: {
        text: 'KwH Generated'
    },
    subtitle: {
        text: 'Click each point to inspect per month.'
    },
    accessibility: {
        announceNewData: {
            enabled: true
        }
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        title: {
            text: 'KwH'
        },
        min: 0,
        // max: yearly_KwH[0]['y'] * 2
    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y:.1f}'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f} KwH</b><br/>'
    },

    series: [
        {
            name: "KwH Generated",
            colorByPoint: true,
            data: yearly_KwH
           
        }
    ],
    drilldown: {
        breadcrumbs: {
            position: {
                align: 'right'
            }
        },
        series: KwH_drilldown_data
    },
    exporting: {
        buttons: {
            contextButton: {
                menuItems: [
                    'printChart',
                    'separator',
                    'downloadPNG',
                    'downloadJPEG',
                    'downloadPDF',
                    'separator',
                    'downloadCSV'
                ]
            }
        }
    }
});

// Create the chart
Highcharts.chart('savings_chart', {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Savings Per Year'
    },
    subtitle: {
        text: 'Click each point to inspect per month.'
    },
    accessibility: {
        announceNewData: {
            enabled: true
        }
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        title: {
            text: 'Euro'
        },
        min: 0
    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y:.1f}'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>€{point.y:.2f}</b><br/>'
    },

    series: [
        {
            name: "Savings Per Year",
            colorByPoint: true,
            data: yearly_Savings
           
        }
    ],
    drilldown: {
        breadcrumbs: {
            position: {
                align: 'right'
            }
        },
        series: Savings_drilldown_data
    },
    exporting: {
        buttons: {
            contextButton: {
                menuItems: [
                    'printChart',
                    'separator',
                    'downloadPNG',
                    'downloadJPEG',
                    'downloadPDF',
                    'separator',
                    'downloadCSV'
                ]
            }
        }
    }
});


function createData(yearly_values, monthly_values){
    labels = yearly_values['yearly_labels']
    KwH = yearly_values['yearly_KwH']
    Savings = yearly_values['yearly_savings']

    let KwH_data = []
    KwH.forEach(function (item, index) {
        KwH_data.push({name: labels[index], y: item, drilldown: labels[index]})
    })

    let savings_data = []
    Savings.forEach(function (item, index) {
        savings_data.push({name: labels[index], y: item, drilldown: labels[index]})
    })

    let KwH_drilldown_data = []
    monthly_values2 = Object.keys(monthly_vals)
    monthly_values2.forEach(function (key, index) {
        KwH_drilldown_data.push({name: key, id: key,
        data: monthly_values[key]['monthly_labels'].map((item,index) => [item, monthly_values[key]['monthly_KwH'][index]])
        })
    })
    console.log(KwH_drilldown_data)

    let Savings_drilldown_data = []
    monthly_values2.forEach(function (key, index) {
        Savings_drilldown_data.push({name: key, id: key,
        data: monthly_values[key]['monthly_labels'].map((item,index) => [item, monthly_values[key]['monthly_savings'][index]])
        })
    })

    let data = [KwH_data, savings_data, KwH_drilldown_data, Savings_drilldown_data]
    return data
}
