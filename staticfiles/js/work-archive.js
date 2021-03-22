var workData = null;
var workArchiveChart = null;

$(function() {
    updateDeviceSelector(archive=true, nonarchive=true);

    // Set default date to now
    var month_element = document.querySelector('input[type="month"]');
    var cur_month = formatDate(new Date());
    month_element.value = cur_month;

    $('#on-chart-show').hide();
    
    // Load chart data 
    $('#load-btn').click(LoadWorkData);

    // Reload chart on parameters change
    $('#show-year-chart').click(UpdateChart);
    $('#date').change(function() { 
        $("#show-year-chart" ).prop("checked", false);
        UpdateChart();
    });
})

function UpdateChart() {
    if (!workData) {
        return
    }

    $('#on-chart-show').show();
        
    var date = document.getElementById('date').value;
    var year = parseInt(date.split('-')[0]);
    var month = parseInt(date.split('-')[1]);
    if (document.getElementById('show-year-chart').checked) { 
        ShowMonthChart(year);
    } else {
        ShowDayChart(year, month);
    }
}

function ShowDayChart(year, month) {    
    // Prepare chart data and labels
    labels = [...Array(getDaysInMonth(year, month)).keys()].map(function(val) {return ++val;}); // month days
    data = []
    if (!workData[year]) { 
        data = Array(labels.length).fill(0);
    } else {
        for (x of labels) { 
            value = workData[year][month][x];            
            if (!value) { 
                value = 0;
            }
            data.push(value);
        }
    }
    DrowWorkChart(data, labels);
}

function ShowMonthChart(year) {
    // Prepare chart data and labels
    labels = [...Array(12).keys()].map(function(val) {return ++val;}); // month numbers
    data = []
    if (!workData[year]) { 
        data = Array(12).fill(0);
    } else {
        for (month of labels) { 
            var sum = 0;
            for (day in workData[year][month]) { 
                value = workData[year][month][day];
                if (value) {
                    sum += value;
                }                
            }
            value = sum / getDaysInMonth(year, month); 
            data.push(value);
        }
    }
    DrowWorkChart(data, labels);
}

function DrowWorkChart(data, labels) {        
    chart_data = {
        labels: labels, 
        datasets: [
            {                            
                backgroundColor: 'white',                
                data: data,
            }           
        ]
    }

    var config = {
        type: 'bar',
        data: chart_data,
        options: {
            // responsive: true,            
            title: {
                display: true,
                text:    "Work Chart", 
                fontColor: 'white'
            },
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: '% of period worked',
                        fontColor: 'black' 
                    },
                    ticks: {                
                        fontColor: "white",        
                        beginAtZero: true                
                    }
                }], 
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'date',
                        fontColor: 'black' 
                    },
                    ticks: {                
                        fontColor: "white",        
                        beginAtZero: true                
                    }
                }]
            }
        },                
    };

    // Update chart if it's already drown
    if (workArchiveChart) {
        workArchiveChart.data = chart_data;
        workArchiveChart.update();
        return;
    }
    
    var ctx = document.getElementById("work-chart").getContext("2d");    
    workArchiveChart = new Chart(ctx, config);    
}

function LoadWorkData(e) {        
    e.preventDefault();
    
    // Load and check work archive
    deviceId = $('#device-selector').val();
    if (!deviceId || deviceId <= 0) { 
        printMessage('Incorrect device id');
        return;
    }
    
    loadWorkChartDataPromise(deviceId).then(function(data) {
        workData = data;
        UpdateChart();            
    })
    .catch(function(error) {
        console.error('Error loading work chart: ' + error);            
        printMessage('Can not load work chart');
    });
}

function loadWorkChartDataPromise(deviceId) {
    return new Promise(function (resolve, reject) { 
        loadWorkArchiveJsonPromise(deviceId).done(function(data, textStatus, jqXHR) {                         
            resolve(data);
        }).fail(function(jqxhr, textStatus, error) {
            console.error(`Error loading work archive for device ${deviceId}: ${error}`);
            reject();
        });
    })
}

function loadWorkArchiveJsonPromise(deviceId) {     
    return $.getJSON(`/work-archive/${deviceId}/work_archive.json`)
}

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;

    return [year, month].join('-');
}

var getDaysInMonth = function(year, month) {
   return new Date(year, month, 0).getDate();
  };