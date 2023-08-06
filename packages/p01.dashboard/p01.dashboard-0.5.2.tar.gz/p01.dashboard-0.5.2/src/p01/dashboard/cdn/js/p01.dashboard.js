/* p01.dashboard.js */

// setup console
if(!window.console){
    window.console = {}
}
if(typeof window.console.log !== "function"){
    window.console.log = function(){}
}
if(typeof window.console.warn !== "function"){
    window.console.warn = function(){}
}

// Full screen
function doFullScreen() {
    var ele = $('body')[0];
    if (ele.requestFullscreen) {
        ele.requestFullscreen()
    }
    else if (ele.msRequestFullscreen) {
        ele.msRequestFullscreen()
    }
    else if (ele.mozRequestFullScreen) {
        ele.mozRequestFullScreen()
    }
    else if (ele.webkitRequestFullscreen) {
        ele.webkitRequestFullscreen()
    }else{
        console.log("Request full screen is not supported")
    }
}

function isEventSourceProvided() {
    if (window.EventSource === undefined) {
        $('#isEventSourceProvided').hide();
        $('#isEventSourceNotProvided').show();
    }
}


// Dashboard script
(function (window, document, undefined) {
    // Dashboard setup
    Dashboard = window.Dashboard || {};

    // fix transparency template matcher to data-bind attributes
    Transparency.matcher = function(element, key) {
        return element.el.getAttribute('data-bind') == key;
    };

    // shared helper methods
    var queryData = function(ele, attrName, _default) {
        // query value from element data
        if (typeof _default === "undefined") {
            _default = null;
        }
        var value = ele.data(attrName);
        if (value) {
            return value;
        }else{
            return _default;
        }
    }
    var applyToURL = function(url, attr, value, encodeURI) {
        if (typeof encodeURI === "undefined") {
            encodeURI = false;
        }
        if (encodeURI) {
            value = encodeURIComponent(value);
        }
        // apply to url if value is given
        if (value || value !== null || typeof _default !== "undefined") {
            return url += sep +attr+ '=' + value;
        }else{
            return url;
        }
    }
    var getZeroPrefix = function(i) {
        if (i < 10) {
            return "0" + i;
        } else {
            return i;
        }
    }
    // update widget data methods
    var bind = function(fn, me){
        // bind method to this. Use this method for bind this instead of using
        //  var self = this
        return function(){
            return fn.apply(me, arguments);
        };
    }
    var getUpdatedDirective = function(params) {
        // see transparency directive for more info at:
        // https://github.com/leonidas/transparency#directives
        var hours, minutes, timestamp, updated;
        if (this.updated) {
            timestamp = new Date(this.updated * 1000);
            hours = timestamp.getHours();
            minutes = ("0" + timestamp.getMinutes()).slice(-2);
            seconds = getZeroPrefix(timestamp.getSeconds());
            return 'Updated: ' + hours + ":" + minutes + ":" + seconds;
        }
    }

    /* server sent event controller */
    var GridController = Class({
        constructor: function() {
            this.grid = null;
            console.log('GridController constructed');
        },
        addWidget: function(widget) {
            // get element data
            var ele = $('#' + widget.id);
            var id = widget.id + '-widget';
            x = ele.data('x');
            y = ele.data('y');
            w = ele.data('width');
            h = ele.data('height');
            // remove data from element
            ele.removeData('x');
            ele.removeData('y');
            ele.removeData('width');
            ele.removeData('height');
            // wrap with grid item
            wrapper = '<div id="'+ id +'" class="grid-item" '
            wrapper += 'data-y="'+ y +'" ';
            wrapper += 'data-x="'+ x +'" ';
            wrapper += 'data-width="'+ w +'" ';
            wrapper += 'data-height="'+ h +'">';
            wrapper += '</div>';
            ele.wrap(wrapper);
            // add content class
            ele.addClass('grid-item-content');
        }
    });
    var grid = new GridController();

    /* server sent event controller */
    var SSEController = Class({
        constructor: function() {
            this.widgets = {};
            this.source = null;
            this.timeout = null;
            this.url = null;
            console.log('SSEController constructed');
        },
        addWidget: function(widget) {
            this.widgets[widget.id] = widget;
        },
        doMessage: function(msg) {
            // dispatch update data to metric items
            key = msg.id;
            var widget = this.widgets[key];
            if (!widget) {
                console.warn('Widget with id '+key+' not found');
            }else{
                try {
                    widget.doUpdate(msg);
                }catch(e) {
                    console.warn(e);
                }
            }
        },
        doReConnect: function() {
            console.log('Check connection');
            var self = this;
            // Handle IE and more capable browsers
            // Open new request as a HEAD to the root hostname with a random
            // param to bust the cache
            try {
                var xhr = new (window.ActiveXObject || XMLHttpRequest)("Microsoft.XMLHTTP");
                var url = ''
                url += '//' + window.location.hostname
                if (window.location.port) {
                    url += ':' + window.location.port;
                }
                url += "/?dashboard-connection-check=" + (new Date()).getTime();
                // Issue request and handle response
                console.log('Check connection with HEAD: ' + url);
                xhr.open('HEAD', url, false)
                xhr.send();
                if (xhr.status >= 200 && (xhr.status < 300 || xhr.status === 304)) {
                    console.log('connection check sucess, reload page');
                    window.location.reload();
                }
            } catch (error) {
                console.log('connection check failed, reschedule');
                setTimeout((function() {
                    self.doReConnect();
                }), self.timeout);
            }
        },
        setup: function(options) {
            // ensure options
            options = $.extend({
                view: 'events',
                // reload in 60 seconds after connection error
                timeout: 1 * 15 * 1000
            }, options);
            this.url = options.view
            this.timeout = options.timeout
            var self = this;
            // setup event source
            this.source = new EventSource(this.url);
            console.log('SSEController connect to ' + this.url)
            this.source.addEventListener('open', function(e) {
                return console.log("Connection opened", e);
            });
            // setup error handler
            this.source.addEventListener('error', function(e) {
                console.log("Connection error", e);
                try {
                    if (e.currentTarget.readyState === EventSource.CLOSED) {
                        console.log("Connection closed");
                        console.log('Reload dashboard scheduled');
                        return setTimeout((function() {
                            console.log('Reload dashboard');
                            return window.location.reload();
                        }), self.timeout);
                    }
                }catch(e) {
                    // conection not available
                    setTimeout((function() {
                        self.doReConnect();
                    }), self.timeout);
                }
            });
            // setup message handler
            this.source.addEventListener('message', function(e) {
                // console.log(e.data);
                data = JSON.parse(e.data);
                self.doMessage(data);
            });
        }
    });
    var controller = new SSEController();

    /* metric base class */
    var WidgetBase = Class({
        constructor: function() {
            this.id = null;
            // setup data converter
            this.directive = {
                updated: {
                    text: getUpdatedDirective
                }
            }
        },
        // setup widget methods
        doSetup: function(ele) {
            // setup properties
            this.id = ele.attr('id');
            this.title = queryData(ele, 'title');
            this.info = queryData(ele, 'info');
        },
        doRender: function(ele) {
            // render element
            ele.append('<p class="title">' + this.title + '</p>');
            ele.append('<p class="info">' + this.info + '</p>');
            return ele;
        },
        doRegister: function(ele) {
            // add widget to controller
            controller.addWidget(this);
        },
        // update widget data methods
        setUpdatedDate: function(data) {
            var hours, minutes, timestamp, updated;
            var node = $('#' + this.id + ' .updated');
            if (node && data.updated) {
                timestamp = new Date(data.updated * 1000);
                hours = timestamp.getHours();
                minutes = ("0" + timestamp.getMinutes()).slice(-2);
                seconds = getZeroPrefix(timestamp.getSeconds());
                node.html('Updated: ' + hours + ":" + minutes + ":" + seconds);
            }
        },
        setData: function(data) {
            // update data
            var ele = $('#' + this.id + ' .text');
            ele.html(data.text);
        },
        // update event message data
        doUpdate: function(data) {
            // update data and refresh This method get called from processor
            this.setData(data);
            // update timestamp
            this.setUpdatedDate(data);
        },
        init: function(ele) {
            // setup properties
            ele = this.doSetup(ele);
            // add widget to grid
            grid.addWidget(this);
            // render dom element
            ele = this.doRender(ele);
            // register widget
            this.doRegister(ele);
        }
    });

    /* Buildbot widget */
    var BuildbotWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            // setup data converter
            this.directive = {
                updated: {
                    text: getUpdatedDirective
                }
            }
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            return ele;
        },
        doRender: function(ele) {
            // render with transparency, just return
            return ele;
        },
        doUpdate: function(data) {
            // update data
            var ns = 'success warning failure skipped exception retry pending';
            var ctx = $('#' + this.id);
            if (data.items) {
                try {
                    ctx.render(data, this.directive);
                    // apply css classes
                    for (idx in data.items) {
                        var css = data.items[idx].css;
                        var li = $('li', ctx).eq(idx);
                        li.removeClass(ns);
                        li.addClass(css);
                    }
                }catch(e){
                    console.warn(e);
                }
            }
        }
    });

    /* Comment widget */
    var CommentWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            // setup data converter
            this.directive = {
                updated: {
                    text: getUpdatedDirective
                }
            }
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            return ele;
        },
        doRender: function(ele) {
            // render div element content
            return ele;
        },
        doUpdate: function(data) {
            // update data
            var ctx = $('#' + this.id);
            if (data.comment) {
                try {
                    ctx.render(data, this.directive);
                }catch(e){
                    console.warn(e);
                }
            }
        }
    });

    /* CLock widget */
    var ClockWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            this.info = null;
            this.location = null;
            this.setTime = bind(this.setTime, this);
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            this.title = queryData(ele, 'title');
            this.location = queryData(ele, 'location');
            this.info = queryData(ele, 'info');
            return ele;
        },
        doRender: function(ele) {
            // render div element content
            ele.append('<div class="block"></div>');
            block = ele.find('.block');
            block.append('<p class="date"></p>');
            block.append('<p class="time"></p>');
            if (this.location) {
                block.append('<p class="location">' + this.location + '</p>');
            }
            if (this.info) {
                block.append('<p class="info">' + this.info + '</p>');
            }
            return ele;
        },
        doRegister: function(ele) {
            // do not register widget for SSE updates, just let the clock tick
            this.setTime();
            this.doTick(ele);
        },
        setTime: function() {
            var h, m, s, today;
            today = new Date();
            h = today.getHours();
            m = today.getMinutes();
            s = today.getSeconds();
            m = getZeroPrefix(m);
            s = getZeroPrefix(s);
            var ctx = $('#' + this.id);
            $('.date', ctx).html(today.toDateString());
            $('.time', ctx).html(h + ":" + m + ":" + s);
        },
        doTick: function() {
            setInterval(this.setTime, 1000);
        }
    });

    /* Flot widget */
    var FlotWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            this.flot = null;
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            return ele;
        },
        doRender: function(ele) {
            // render div element content
            return ele;
        },
        doUpdate: function(data) {
            // render flot
            var ele = $('#' + this.id);
            // update data
            if (data.series) {
                var ele = $('#' + this.id);
                this.flot = $.plot(ele, data.series, data.options);
                var canvas = ele.find('canvas');
                canvas.width(ele.width() - 10);
                canvas.height(ele.height() - 10);
            }
        }
    });

    /* Gauge widget */
    var GaugeWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            this.gid = null;
            this.gauge = null;
            this.value = 0;
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            this.gid = this.id +'svg'
            this.title = queryData(ele, 'title');
            this.label = queryData(ele, 'label');
            this.value = queryData(ele, 'default', 0);
            this.min = queryData(ele, 'min', 0);
            this.max = queryData(ele, 'max', 100);
            return ele;
        },
        doRender: function(ele) {
            // render gauge in child div. Otherwise our data-width etc.
            // properties will get used as Gauge config options, argh
            var ctx = $('#' + this.id);
            ele.append('<div id="'+ this.gid+'"></div>');
            this.gauge = new JustGage({
                id: this.gid,
                value: this.value,
                min: this.min,
                max: this.max,
                relativeGaugeSize: true,
                title: this.title,
                label: this.label
            });
            return ele;
        },
        doUpdate: function(data) {
            // adjust gauge size
            var ctx = $('#' + this.id);
            var div = $('#' + this.gid, ctx);
            // kill div size
            div.css('height', 1);
            div.css('width', 1);
            // get real size
            var height = ctx.height() - 20;
            var width = ctx.width() - 20;
            div.css('width', width);
            div.css('height', height);
            // update data
            if (data.value) {
                try {
                    // refresh gauge value
                    this.gauge.refresh(data.value);
                    // render updated timestamp
                    // update timestamp
                    this.setUpdatedDate(data);
                }catch(e){
                    console.warn(e);
                }
            }
        }
    });

    /* Graph widget */
    var GraphWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            this.graph = null;
            this.renderer = null;
            this.color = null;
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            var ctx = $('#' + this.id);
            this.renderer = queryData(ctx, 'renderer', 'area');
            this.color = queryData(ele, 'color', '#ffffff');
            return ele;
        },
        doRender: function(ele) {
            // render with transparency, just return
            var ctx = $('#' + this.id);
            // get real size
            var height = ctx.outerHeight();
            var width = ctx.outerWidth();
            this.graph = new Rickshaw.Graph({
                element: ctx.get(0),
                width: width,
                height: height,
                renderer: this.renderer,
                series: [{
                    color: this.color,
                    data:  [
                        { x: 0, y: 0 }
                    ]
                }]
            });
            if (ctx.data('points')) {
                this.graph.series[0].data = ctx.data('points');
            }
            x_axis = new Rickshaw.Graph.Axis.Time({
                graph: this.graph
            });
            y_axis = new Rickshaw.Graph.Axis.Y({
                graph: this.graph,
                tickFormat: Rickshaw.Fixtures.Number.formatKMBT
            });
            this.graph.render();
            return ele;
        },
        doUpdate: function(data) {
            // update data
            var ctx = $('#' + this.id);
            var svg = $('svg', ctx);
            var height = ctx.outerHeight();
            var width = ctx.outerWidth();
            svg.attr('width', width);
            svg.attr('height', height);
            if (data.points) {
                try {
                    // update graph
                    if (this.graph) {
                        this.graph.series[0].data = data.points;
                        this.graph.render();
                        // update value
                        $('.value', ctx).html('' + data.value);
                        // update timestamp
                        this.setUpdatedDate(data);
                    }
                }catch(e){
                    console.log("Rickshaw render");
                    console.warn(e);
                }
            }
        }
    });

    /* HTML widget */
    var HTMLWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            // setup data converter
            this.directive = {
                content: {
                    html: function() {
                        return this.content;
                    }
                },
                updated: {
                    text: getUpdatedDirective
                }
            }
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            return ele;
        },
        doRender: function(ele) {
            // render with transparency, just return
            return ele;
        },
        doUpdate: function(data) {
            // update data
            var ctx = $('#' + this.id);
            if (data.content) {
                try {
                    ctx.render(data, this.directive);
                }catch(e){
                    console.warn(e);
                }
            }
        }
    });

    /* Knob widget */
    var KnobWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            this.dial = null;
            // setup data converter
            this.directive = {
                updated: {
                    text: getUpdatedDirective
                }
            }
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            this.dial = $('#' + this.id + ' input')
            this.dial.knob();
            return ele;
        },
        doRender: function(ele) {
            return ele;
        },
        doUpdate: function(data) {
            // update data
            if (data.value) {
                var ctx = $('#' + this.id);
                try {
                    // refresh gauge value
                    this.dial.val(data.value).trigger('change');
                    // render updated timestamp
                    ctx.render(data, this.directive);
                }catch(e){
                    console.warn(e);
                }
            }
        }
    });

    /* List widget */
    var ListWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            // setup data converter
            this.directive = {
                updated: {
                    text: getUpdatedDirective
                }
            }
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            return ele;
        },
        doRender: function(ele) {
            // render with transparency, just return
            return ele;
        },
        doUpdate: function(data) {
            // update data
            var ctx = $('#' + this.id);
            if (data.items) {
                try {
                    ctx.render(data, this.directive);
                }catch(e){
                    console.warn(e);
                }
            }
        }
    });

    /* Number widget */
    var NumberWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            // setup data converter
            this.directive = {
                updated: {
                    text: getUpdatedDirective
                }
            }
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            return ele;
        },
        doRender: function(ele) {
            // render with transparency, just return
            return ele;
        },
        doUpdate: function(data) {
            // update data
            var ctx = $('#' + this.id);
            if (data.number) {
                try {
                    ctx.render(data, this.directive);
                }catch(e){
                    console.warn(e);
                }
            }
        }
    });

    /* Text widget */
    var TextWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            // setup data converter
            this.directive = {
                updated: {
                    text: getUpdatedDirective
                }
            }
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            return ele;
        },
        doRender: function(ele) {
            // render with transparency, just return
            return ele;
        },
        doUpdate: function(data) {
            // update data
            var ctx = $('#' + this.id);
            if (data.text) {
                try {
                    ctx.render(data, this.directive);
                }catch(e){
                    console.warn(e);
                }
            }
        }
    });

    /* XError widget */
    var XErrorWidget = Class(WidgetBase, {
        constructor: function() {
            this.id = null;
            // setup data converter
            this.directive = {
                updated: {
                    text: getUpdatedDirective
                }
            }
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            return ele;
        },
        doRender: function(ele) {
            // render with transparency, just return
            return ele;
        },
        doUpdate: function(data) {
            // update data
            var ns = 'success warning failure skipped exception retry pending';
            var ctx = $('#' + this.id);
            if (data.items) {
                try {
                    ctx.render(data, this.directive);
                    // apply css classes
                    for (idx in data.items) {
                        var css = data.items[idx].css;
                        var li = $('li', ctx).eq(idx);
                        li.removeClass(ns);
                        li.addClass(css);
                    }
                }catch(e){
                    console.warn(e);
                }
            }
        }
    });

    /* ChartJS widget base class */
    var ChartJSWidget = Class(WidgetBase, {
        constructor: function() {
            this.type = 'bar';
            this.id = null;
            this.ctx = null;
            this.holder = null;
            this.area = null;
            this.chart = null;
        },
        doSetup: function(ele) {
            this.id = ele.attr('id');
            this.title = $('.title', ele).html();
            return ele;
        },
        doRender: function(ele) {
            // render div element content
            $(ele).append('<div class="canvas-holder"></div>');
            this.holder = ele.find('.canvas-holder');
            // canvas.append("<canvas width=\"" + width + "\" height=\"" + height + "\" class=\"chart-area\"><canvas>");
            this.holder.append("<canvas " + "\" class=\"chart-area\"><canvas>");
            this.area = this.holder.find('.chart-area');
            this.ctx = ele.find('.chart-area')[0].getContext('2d');
            return ele;
        },
        doUpdate: function(data) {
            var ele = $('#' + this.id);
            var parent = ele.parent();
            // kill area size
            this.area.css('height', 1);
            this.area.css('width', 1);
            // get real size
            // var height = parent.height() - 20;
            // var width = parent.width() - 20;
            var height = ele.height();
            var width = ele.width();
            // update data
            if (this.chart) {
                this.chart.destroy();
            }
            if (data.data) {
                options = $.extend({
                    responsive: true,
                    maintainAspectRatio: false
                }, data.options);
                this.chart = new Chart(this.ctx, {
                    type: this.type,
                    data: data.data,
                    options: options
                });
                this.chart.update();
                // set initial calculated size
                this.area.css('height', height);
                this.area.css('width', width);
            }
        }
    });

    /* BarChart widget */
    var BarChartWidget = Class(ChartJSWidget, {
        constructor: function() {
            this.type = 'bar';
            this.id = null;
            this.ctx = null;
            this.holder = null;
            this.area = null;
            this.chart = null;
        }
    });

    /* Doughnut widget */
    var DoughnutChartWidget = Class(ChartJSWidget, {
        constructor: function() {
            this.type = 'doughnut';
            this.id = null;
            this.ctx = null;
            this.holder = null;
            this.area = null;
            this.chart = null;
        }
    });

    /* LineChart widget */
    var LineChartWidget = Class(ChartJSWidget, {
        constructor: function() {
            this.type = 'line';
            this.id = null;
            this.ctx = null;
            this.holder = null;
            this.area = null;
            this.chart = null;
        }
    });

    /* PieChart widget */
    var PieChartWidget = Class(ChartJSWidget, {
        constructor: function() {
            this.type = 'pie';
            this.id = null;
            this.ctx = null;
            this.holder = null;
            this.area = null;
            this.chart = null;
        }
    });

    /* PolarAreaChart widget */
    var PolarAreaChartWidget = Class(ChartJSWidget, {
        constructor: function() {
            this.type = 'polarArea';
            this.id = null;
            this.ctx = null;
            this.holder = null;
            this.area = null;
            this.chart = null;
        }
    });

    /* RadarChart widget */
    var RadarChartWidget = Class(ChartJSWidget, {
        constructor: function() {
            this.type = 'radar';
            this.id = null;
            this.ctx = null;
            this.holder = null;
            this.area = null;
            this.chart = null;
        }
    });

    /* dom parser */
    var DashboardParser = Class({
        constructor: function() {
            this.factories = {};
        },
        addPlugin: function(key, factory) {
            this.factories[key] = factory;
        },
        doMatch: function(ele) {
            var ele = $(ele);
            var ready = ele.data('ready');
            if (ready !== true) {
                var key = ele.data('type');
                var factory = this.factories[key];
                if (factory) {
                    var obj = new factory();
                    obj.init(ele);
                    ele.data('ready', true);
                }
            }
        },
        doParse: function() {
            /* currently we only parse div tags */
            var divs = $('div');
            var self = this;
            $.each(divs, function(){
                self.doMatch(this);
            });
        }
    });
    var parser = new DashboardParser();

    // initialize parser
    (function() {
        if (Dashboard.ready) {
            return false;
        }
        // setup dasboard api methods
        window.Dashboard.addPlugin = function(key, factory){
            parser.addPlugin(key, factory)
        };
        window.Dashboard.setup = function(options){
            // setup EventSource controller
            controller.setup(options);
            // setup widgets and apply server sent event observer
            parser.doParse()
        };
        // setup default widgets
        Dashboard.addPlugin('Buildbot', BuildbotWidget);
        Dashboard.addPlugin('Clock', ClockWidget);
        Dashboard.addPlugin('Comment', CommentWidget);
        Dashboard.addPlugin('Flot', FlotWidget);
        Dashboard.addPlugin('Gauge', GaugeWidget);
        Dashboard.addPlugin('Graph', GraphWidget);
        Dashboard.addPlugin('HTML', HTMLWidget);
        Dashboard.addPlugin('Knob', KnobWidget);
        Dashboard.addPlugin('List', ListWidget);
        Dashboard.addPlugin('Number', NumberWidget);
        Dashboard.addPlugin('Text', TextWidget);
        Dashboard.addPlugin('XError', XErrorWidget);
        // chartjs widgets
        Dashboard.addPlugin('BarChart', BarChartWidget);
        Dashboard.addPlugin('DoughnutChart', DoughnutChartWidget);
        Dashboard.addPlugin('LineChart', LineChartWidget);
        Dashboard.addPlugin('PieChart', PieChartWidget);
        Dashboard.addPlugin('PolarAreaChart', PolarAreaChartWidget);
        Dashboard.addPlugin('RadarChart', RadarChartWidget);
        Dashboard.ready = true;
    })();

})(window, document);
