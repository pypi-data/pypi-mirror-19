"use strict";
var STONEGRIDS = {};
(function($){
    $.fn.extend({
        /**
         * Creates a grid.
         *
         * @param      {<dict>}  config  The configuration
         */
        createGrid: function(config){
            config = getDefaultConfigGrid(config)
            if ('footer' in config){
                if(config['footer']){
                    var footer = createFooter(config['columns'])
                    $(this).append(footer)
                }
            }
            STONEGRIDS[this[0].id] = {};
            STONEGRIDS[this[0].id]['config'] = config;
            STONEGRIDS[this[0].id]['gridmethods'] = this.DataTable(config);
        },
        /**
         * Update data of grid
         *
         * @param      {<list of lists>}  datas   The new rows
         */
        updateData: function(datas, footer){
            STONEGRIDS[this[0].id]['datas'] = datas
            STONEGRIDS[this[0].id]['footer'] = footer
            STONEGRIDS[this[0].id]['gridmethods'].clear()
            STONEGRIDS[this[0].id]['gridmethods'].rows.add(datas)
            STONEGRIDS[this[0].id]['gridmethods'].draw()
            if(typeof(footer) != 'undefined'){
                this.updateFooter(footer)
            }
            $('.DTFC_RightWrapper').hide()
        },

        setTitleFileExport: function(title){
            STONEGRIDS[this[0].id]['gridmethods'].destroy()
            var config = STONEGRIDS[this[0].id]['config']
            var new_buttons = []
            $.each(config['buttons'], function(index, value){
                value['title'] = title
                new_buttons.push(value)
            })
            config['buttons'] = new_buttons
            STONEGRIDS[this[0].id]['gridmethods'] = this.DataTable(config);
            this.updateData(STONEGRIDS[this[0].id]['datas'], STONEGRIDS[this[0].id]['footer'])
            this.hideColumns(STONEGRIDS[this[0].id]['hideColumns'])
        },
        /**
         * Resize teh grid
         */
        resizeColumns: function(){
          STONEGRIDS[this[0].id]['gridmethods'].columns.adjust();
          STONEGRIDS[this[0].id]['gridmethods'].draw(true)
        },
        /**
         * Hides the columns.
         *
         * @param      {<list of number of columns>}  hideColumns  The hide columns
         */
        hideColumns: function(hideColumns){
            STONEGRIDS[this[0].id]['hideColumns'] = hideColumns
            STONEGRIDS[this[0].id]['gridmethods'].columns().visible(true)
            STONEGRIDS[this[0].id]['gridmethods'].columns(hideColumns).visible(false)
            STONEGRIDS[this[0].id]['gridmethods'].draw()
        },
        /**
         * Update footer data
         *
         * @param      {<dict>}  data    The data
         */
        updateFooter: function(data){
            var id_grid = this[0].id
            var columns_count = STONEGRIDS[id_grid]['gridmethods'].columns()[0].length
            $.each(data, function(key, value){
                var footers = STONEGRIDS[id_grid]['gridmethods'].columns(':contains(' + key + ')').footer()
                var footer;
                if (footers.length > 1){
                    $.each(footers, function(index, value2){
                        var id_value = value2.id.replace('_footer', '')
                        if(id_value==key){
                            footer= value2
                        }
                    })
                }
                else{
                    footer = footers[0]
                }
                 $(footer).html(value)
            });
        }
    });
    
    var createFooter = function(columns){
        var html_footer = ''
        for(var i = 0 ; i< columns.length; i++){html_footer+="<td id='" + columns[i]['data'] + "_footer'></td>"}
        html_footer = '<tfoot><tr>' + html_footer + '</tfoot></tr>'
        return html_footer;
    }
    /**
     * Gets the default configuration grid.
     *
     * @param      {<dict>}    config  The configuration
     * @return     {<dict>}    The default configuration grid.
     */
    var getDefaultConfigGrid = function(config){
        var dataSet = [
            {
                "Tipo":       "Tiger Nixon",
                "Tarj":   "System Architect",
                "Traf":     "$3,120",
                "Benef": "2011/04/25",
                "office":     "Edinburgh",
                "extn":       "5421"
            },
            {
                "Tipo":       "Garrett Winters",
                "Tarj":   "Director",
                "Traf":     "$5,300",
                "Benef": "2011/07/25",
                "office":     "Edinburgh",
                "extn":       "8422"
            }
        ];
        var default_config = {
            data: dataSet,
            searching: false,
            paging: true,
            scrollY: 100,
            deferRender:    true,
            scroller:       true,
            scrollX: true,
            footer: false,
            // fixedColumns:   {
            //     leftColumns: 1,
            // },
            // dom: 'Bfrtip',
            // buttons: [
            //     {
            //         extend: 'excelHtml5',
            //         exportOptions: {
            //             columns: ':visible'
            //         }
            //     }, 
            //     {
            //         extend: 'pdfHtml5',
            //         exportOptions: {
            //             columns: ':visible'
            //         }
            //     }, 
            //     {
            //         extend: 'csvHtml5',
            //         exportOptions: {
            //             columns: ':visible'
            //         }
            //     }, 
            // ],
            columns: [
                { title: "Tipo" , data: "Tipo" },
                { title: "Tarj", data: "Tarj", render: $.fn.dataTable.render.number( '.', ',', 0) }, // thousand separator, decimal separator, floating point precision, prefix string (op), postfirx string (op)
                { title: "Traf", data: "Traf", render: $.fn.dataTable.render.number( '.', ',', 2) },
                { title: "Benef", data: "Benef", render: $.fn.dataTable.render.number( '.', ',', 2) },
            ],
        }
        var result = extendJqueryExtend(default_config, config)
        result = normalizerConfig(result)
        return result;
    }

    /**
     * { function_description }
     *
     * @param      {<type>}  config  The configuration
     */
    var normalizerConfig = function(config){
        config = searchBoolean(config)
        config['columns'] = normalizeColumns(config['columns'])
        return config
    }

    var normalizeColumns = function(columnConfig){
        var new_columns = []
        $.each(columnConfig, function(index, value){
            if(Object.keys(value).includes('render')){
                if(typeof(value['render'].includes)=='undefined'){
                    value['render'] = fillRender(value['render'])
                }
            }
            new_columns.push(value)
        })
        return new_columns
    }

    var fillRender = function(render){
        render = renderNumber(render['thousands'], render['decimal'], render['round'], render['prefix'], render['postfix'], render['mod'], render['number'])
        return render
    }

    var renderNumber = function(thousands, decimal, precision, prefix, postfix, operator, num){
        return {
                display: function ( d ) {
                    if (operator != ''){
                        if (operator == 'mul'){
                            d = d * num
                        }
                    }
                    // dataTable.render.number function is called in order to avoid using __htmlEscapeEntities
                    return $.fn.dataTable.render.number(thousands, decimal, precision, prefix, postfix).display(d);
                }
            };
    }

})(jQuery)