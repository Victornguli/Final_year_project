odoo.define('widget_demo', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Widget = require('web.Widget');
var ajax = require('web.ajax');

var author = AbstractAction.extend({

    template: 'Author',

    cssLibs: [
        '/demo_on_21/static/src/css/style.css',
    ],

    jsLibs: [
        '/web/static/lib/nvd3/d3.v3.js',
        '/demo_on_21/static/src/js/libs/myd3.js',
        '/demo_on_21/static/src/js/libs/newd3.js',
    ],

    events: {
        'click #searchbtn': '_OnSearch',
    },

    willStart: function () {
        return $.when(ajax.loadLibs(this), this._super.apply(this, arguments));
    },

    _OnSearch: function(){
        this._rpc({
            route: '/authors/search',
            params: {
                'author': this.$el.find('input#searchtxt').val()
            },
        })
        .then(function (tasks) {
            $('svg').remove();

            for (var i=0; i<tasks.length; i++) {
                tasks[i].endDate = new Date(tasks[i].enddate)
                tasks[i].startDate = new Date(tasks[i].startdate)
            }

            var taskStatus = {
                "draft" : "bar-running",
                "inprogress" : "bar-succeeded",
                "cancelled" : "bar",
                "done" : "bar-killed"
            };

            var taskNames = ["Personal Activity", "Group Activity", "Fun", "Conference"];

            tasks.sort(function(a, b) {
                return Math.abs(a.endDate - b.endDate)
            });
            var maxDate = tasks[tasks.length - 1].endDate;

            tasks.sort(function(a, b) {
                return Math.abs(a.startDate - b.startDate);
            });
            var minDate = tasks[0].startDate;

            var format = "%H-%M";
            var gantt = d3.gantt().taskTypes(taskNames).taskStatus(taskStatus).tickFormat(format);
            gantt(tasks);
        });
    }

});

core.action_registry.add('widget_author', author);

});
