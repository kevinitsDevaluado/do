/*
    ===================================
        Yearly Visitors | Options
    ===================================
*/
var yearly = {
    chart: {
        height: 230,
        type: 'bar',
        toolbar: {
            show: false,
        },
        dropShadow: {
            enabled: true,
            top: 1,
            left: 1,
            blur: 1,
            color: '#515365',
            opacity: 0.3,
        }
    },
    colors: ['#fc8edf', '#c20d5a'],
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded'
        },
    },
    dataLabels: {
        enabled: false
    },
    legend: {
        position: 'bottom',
        horizontalAlign: 'center',
        fontSize: '14px',
        markers: {
            width: 10,
            height: 10,
        },
        itemMargin: {
            horizontal: 0,
            vertical: 8
        }
    },
    grid: {
        borderColor: '#f7f7f7',
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    series: [{
        name: 'Directo',
        data: [58, 44, 55, 57, 56, 61, 58, 63, 60, 66, 56, 63]
    }, {
        name: 'Orgánico',
        data: [91, 76, 85, 101, 98, 87, 105, 91, 114, 94, 66, 70]
    }],
    xaxis: {
        categories: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dec'],
    },
    fill: {
        type: 'gradient',
        gradient: {
            shade: 'dark',
            type: 'vertical',
            shadeIntensity: 0.3,
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 0.8,
            stops: [0, 100]
        }
    },
    tooltip: {
        theme: 'dark',
        y: {
            formatter: function(val) {
                return val
            }
        }
    }
}



/*
    ===================================
        Monthly Visitors | Options
    ===================================
*/
var monthly = {
    chart: {
        height: 230,
        type: 'bar',
        toolbar: {
            show: false,
        },
        dropShadow: {
            enabled: true,
            top: 1,
            left: 1,
            blur: 1,
            color: '#515365',
            opacity: 0.3,
        }
    },
    colors: ['#fc8edf', '#c20d5a'],
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded'
        },
    },
    dataLabels: {
        enabled: false
    },
    legend: {
        position: 'bottom',
        horizontalAlign: 'center',
        fontSize: '14px',
        markers: {
            width: 10,
            height: 10,
        },
        itemMargin: {
            horizontal: 0,
            vertical: 8
        }
    },
    grid: {
        borderColor: '#f7f7f7',
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    series: [{
        name: 'Directo',
        data: [58, 44, 55, 57, 56, 61, 58, 63, 60, 66, 56, 63, 58, 44, 55, 57, 56, 61, 58, 63, 60, 66, 56, 63, 61, 58, 63, 60, 66, 56, 63]
    }, {
        name: 'Organico',
        data: [91, 76, 85, 101, 98, 87, 105, 91, 114, 94, 66, 70, 91, 76, 85, 101, 98, 87, 105, 91, 114, 94, 66, 70, 87, 105, 91, 114, 94, 66, 70, ]
    }],
    xaxis: {
        categories: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'],
    },
    fill: {
        type: 'gradient',
        gradient: {
            shade: 'dark',
            type: 'vertical',
            shadeIntensity: 0.3,
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 0.8,
            stops: [0, 100]
        }
    },
    tooltip: {
        theme: 'dark',
        y: {
            formatter: function(val) {
                return val
            }
        }
    }
}


/*
    ===================================
        Weekly Visitors | Options
    ===================================
*/
var weekly = {
    chart: {
        height: 230,
        type: 'bar',
        toolbar: {
            show: false,
        },
        dropShadow: {
            enabled: true,
            top: 1,
            left: 1,
            blur: 1,
            color: '#515365',
            opacity: 0.3,
        }
    },
    colors: ['#fc8edf', '#c20d5a'],
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded'
        },
    },
    dataLabels: {
        enabled: false
    },
    legend: {
        position: 'bottom',
        horizontalAlign: 'center',
        fontSize: '14px',
        markers: {
            width: 10,
            height: 10,
        },
        itemMargin: {
            horizontal: 0,
            vertical: 8
        }
    },
    grid: {
        borderColor: '#f7f7f7',
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    series: [{
        name: 'Directo',
        data: [58, 44, 55, 57, 56, 61, 58]
    }, {
        name: 'Organico',
        data: [91, 76, 85, 101, 98, 87, 105]
    }],
    xaxis: {
        categories: ['Lun', 'Mar', 'Mier', 'Jue', 'Vie', 'Sab', 'Sub'],
    },
    fill: {
        type: 'gradient',
        gradient: {
            shade: 'dark',
            type: 'vertical',
            shadeIntensity: 0.3,
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 0.8,
            stops: [0, 100]
        }
    },
    tooltip: {
        theme: 'dark',
        y: {
            formatter: function(val) {
                return val
            }
        }
    }
}



/*
    ==============================
    |    @Render Charts Script    |
    ==============================
*/


/*
    ===================================
        Yearly Visitors | Script
    ===================================
*/


var d_1C_3 = new ApexCharts(
    document.querySelector("#yearly"),
    yearly
);
d_1C_3.render();

/*
    ===================================
        Monthly Visitors | Script
    ===================================
*/
var d_1C_3 = new ApexCharts(
    document.querySelector("#monthly"),
    monthly
);
d_1C_3.render();

/*
    ===================================
        Weekly Visitors | Script
    ===================================
*/
var d_1C_3 = new ApexCharts(
    document.querySelector("#weekly"),
    weekly
);
d_1C_3.render();

/*////////PASTEL///////////////////////////////////////////////////////////////////////////////////////////////////////////////////// */

/*
    ==================================
        Traffic | Options
    ==================================
*/





                        

// Followers


var d_1options3 = {
    chart: {
        id: 'sparkline1',
        type: 'area',
        height: 50,
        sparkline: {
            enabled: true
        },
    },
    stroke: {
        curve: 'smooth',
        width: 2,
    },
    series: [{
        name: 'Ventas',
        data: [38, 60, 38, 52, 36, 40, 28]
    }],
    labels: ['1', '2', '3', '4', '5', '6', '7'],
    yaxis: {
        min: 0
    },
    colors: ['#4361ee'],
    tooltip: {
        x: {
            show: false,
        }
    },
    fill: {
        type: "gradient",
        gradient: {
            type: "vertical",
            shadeIntensity: 1,
            inverseColors: !1,
            opacityFrom: .60,
            opacityTo: .05,
            stops: [100, 100]
        }
    }
}


// Followers


var d_1C_5 = new ApexCharts(document.querySelector("#hybrid_followers"), d_1options3);
d_1C_5.render()


// Referral


var d_1options4 = {
    chart: {
        id: 'sparkline1',
        type: 'area',
        height: 50,
        sparkline: {
            enabled: true
        },
    },
    stroke: {
        curve: 'smooth',
        width: 0,
    },
    series: [{
        name: 'Paginas vistas',
        data: [60, 28, 52, 38, 40, 36, 38]
    }],
    labels: ['1', '2', '3', '4', '5', '6', '7'],
    yaxis: {
        min: 0
    },
    colors: ['#fff'],
    tooltip: {
        x: {
            show: false,
        }
    },
    fill: {
        type: "gradient",
        gradient: {
            type: "vertical",
            shadeIntensity: 1,
            inverseColors: !1,
            opacityFrom: .60,
            opacityTo: .05,
            stops: [100, 100]
        }
    }
}

// Referral


var d_1C_6 = new ApexCharts(document.querySelector("#hybrid_followers1"), d_1options4);
d_1C_6.render()


// Engagement Rate


var d_1options5 = {
    chart: {
        id: 'sparkline1',
        type: 'area',
        height: 50,
        sparkline: {
            enabled: true
        },
    },
    stroke: {
        curve: 'smooth',
        width: 2,
    },
    fill: {
        opacity: 1,
    },
    series: [{
        name: 'Porcentaje de rebote',
        data: [28, 50, 36, 60, 38, 52, 38]
    }],
    labels: ['1', '2', '3', '4', '5', '6', '7'],
    yaxis: {
        min: 0
    },
    colors: ['#1abc9c'],
    tooltip: {
        x: {
            show: false,
        }
    },
    fill: {
        type: "gradient",
        gradient: {
            type: "vertical",
            shadeIntensity: 1,
            inverseColors: !1,
            opacityFrom: .50,
            opacityTo: .05,
            stops: [100, 100]
        }
    }
}


// Engagement Rate


var d_1C_7 = new ApexCharts(document.querySelector("#hybrid_followers2"), d_1options5);
d_1C_7.render()



// Revinue Rate


var d_1options6 = {
    chart: {
        id: 'sparkline1',
        type: 'area',
        height: 50,
        sparkline: {
            enabled: true
        },
    },
    stroke: {
        curve: 'smooth',
        width: 2,
    },
    fill: {
        opacity: 1,
    },
    series: [{
        name: 'Revinue Status',
        data: [28, 50, 36, 60, 38, 52, 38]
    }],
    labels: ['1', '2', '3', '4', '5', '6', '7'],
    yaxis: {
        min: 0
    },
    colors: ['#af4190'],
    tooltip: {
        x: {
            show: false,
        }
    },
    fill: {
        type: "gradient",
        gradient: {
            type: "vertical",
            shadeIntensity: 1,
            inverseColors: !1,
            opacityFrom: .30,
            opacityTo: .05,
            stops: [100, 100]
        }
    }
}




/*
    ==============================
    |    @Render Charts Script    |
    ==============================
*/


// Engagement Rate


var d_1C_7 = new ApexCharts(document.querySelector("#rv_status_chart4"), d_1options6);
d_1C_7.render()
                   