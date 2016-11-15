/**
 * Created by youzipi on 16/5/9.
 */

var data = [
    {
        'keywords': 'information',
        'year_citations': {
            2005: 12,
            2006: 13,
            2007: 9,
            2008: 11,
            2009: 14,
            2010: 8,
            2011: 11,
            2012: 10,
            2013: 16,
            2014: 27,
            2015: 15
        }
    }, {
        'keywords': 'performance',
        'year_citations': {
            2005: 13,
            2006: 11,
            2007: 8,
            2008: 4,
            2009: 6,
            2010: 7,
            2011: 7,
            2012: 9,
            2013: 13,
            2014: 8,
            2015: 10
        }
    }, {
        'keywords': 'network',
        'year_citations': {
            2005: 19,
            2006: 12,
            2007: 10,
            2008: 7,
            2009: 10,
            2010: 13,
            2011: 9,
            2012: 13,
            2013: 22,
            2014: 19,
            2015: 17
        }
    }, {
        'keywords': 'genetic algorithm',
        'year_citations': {
            2005: 5,
            2006: 7,
            2007: 2,
            2008: 5,
            2009: 8,
            2010: 6,
            2011: 10,
            2012: 10,
            2013: 13,
            2014: 4,
            2015: 7
        }
    }, {
        'keywords': 'design',
        'year_citations': {
            2005: 15,
            2006: 12,
            2007: 10,
            2008: 6,
            2009: 10,
            2010: 6,
            2011: 11,
            2012: 17,
            2013: 20,
            2014: 15,
            2015: 19
        }
    }, {
        'keywords': 'set',
        'year_citations': {
            2005: 5,
            2006: 1,
            2007: 1,
            2008: 2,
            2009: 4,
            2010: 3,
            2011: 4,
            2012: 11,
            2013: 6,
            2014: 13,
            2015: 6
        }
    }, {
        'keywords': 'selection',
        'year_citations': {
            2005: 2,
            2006: 2,
            2007: 4,
            2008: 6,
            2009: 2,
            2010: 2,
            2011: 12,
            2012: 5,
            2013: 7,
            2014: 15,
            2015: 9
        }
    },];
var option = {
    title: {
        text: '',
        x: "center"
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: [],
        y: "bottom"

    },
    toolbox: {
        show: true,
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    xAxis: [{
        type: 'category',
        data: []
    }],
    yAxis: [{
        type: 'value'
    }],
    series: []
};
var years = [];
for (var i = 2005; i < 2016; i++) {
    years.push(i);
}
option.xAxis[0]["data"] = years;//x轴数据
seriesData = [];
legends = [];
data.map(function (item) {
    var dis_item =
    {
        name: '',
        type: "line",
        data: [],
    };
    dis_item['name'] = item['keywords'];
    legends.push(item['keywords']);
    for (var i = 2005; i < 2016; i++) {
        dis_item['data'].push(item['year_citations'][i]);
    }
    seriesData.push(dis_item);
});
option.legend.data = legends;
console.log(legends);
console.log(years);


console.log(seriesData);
console.log(option);
