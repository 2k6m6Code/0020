function speed_meter()
{
    this.max='200';
    this.mix='0';
    this.max_color='150';
    this.mix_color='50';
    this.unit='bps/s';
    this.title='Speed';
    this.id='';
    this.time='1000';
    this.name='';
    this.total='';
}
speed_meter.prototype.set=(function(max,mix,max_color,mix_color,unit,title,id,time,name,total){
	var self=this;
        self.max=max;
        self.mix=mix;
        self.max_color=max_color;
    	self.mix_color=mix_color;
        self.unit=unit;
        self.title=title;
        self.id=id;
        self.time=time;
        self.name=name;
        self.total=total;
});

speed_meter.prototype.creat=(function(){
       var id = this.id;
       var name = this.name;
       var total = this.total;
        $("#"+id).highcharts({
            chart: {
                type: 'gauge',
                plotBackgroundColor: null,
                plotBackgroundImage: null,
                plotBorderWidth: 0,
                plotShadow: false
            },
            title: {
                text: this.title
            },
    	    pane: {
    	        startAngle: -150,
    	        endAngle: 150,
    	        background: [{
    	            backgroundColor: {
    	                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
    	                stops: [
    	                    [0, '#FFF'],
    	                    [1, '#333']
    	                ]
    	            },
    	            borderWidth: 0,
    	            outerRadius: '109%'
    	        },
    	        {
    	            backgroundColor: {
    	            	linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
    	            	stops: [
    	                    [0, '#333'],
    	                    [1, '#FFF']
    	            	]
    	            },
    	            borderWidth: 1,
    	            outerRadius: '107%'
    	        },
    	        {
    	        },
    	        {
    	            backgroundColor: '#DDD',
    	            borderWidth: 0,
    	            outerRadius: '105%',
    	            innerRadius: '103%'
    	        }]
    	    },
    	    yAxis: {
    	        min: 0,
    	        max: total,
    	        minorTickInterval: 'auto',
    	        minorTickWidth: 1,
    	        minorTickLength: 10,
    	        minorTickPosition: 'inside',
    	        minorTickColor: '#666',
    	        tickPixelInterval: 30,
    	        tickWidth: 2,
    	        tickPosition: 'inside',
    	        tickLength: 10,
    	        tickColor: '#666',
    	        labels: {
    	            step: 2,
    	            rotation: 'auto'
    	        },
    	        title: {
    	            text: this.unit
    	        },
    	        plotBands: [{
    	            from: 0,
    	            to: total/2,
    	            color: '#55BF3B' // green
    	        },
    	        {
    	            from:total/2,
    	            to:(total*3)/4,
    	            color: '#DDDF0D' // yellow
    	        },
    	        {
    	            from:(total*3)/4,
    	            to:total,
    	            color: '#DF5353' // red
    	        }]
    	    },
    	    series: [{
    	        enableMouseTracking: false,
    	        data: [0],
    	        dataLabels: {
    	            formatter: function () {
    	                var kmh = this.y;
    	                return kmh/1024;
    	            }
    	        }
    	    }]
    	},
        function (chart) {
                setInterval(function () {
                    if (chart.series)
                    {
                        var point = chart.series[0].points[0];
                    	$.get("speed_data.pl",{name:name,option:id},function(yy){
                   	    point.update(Math.round(yy*1024));
                   	});
                   } 
                },1000);
        });
    });
