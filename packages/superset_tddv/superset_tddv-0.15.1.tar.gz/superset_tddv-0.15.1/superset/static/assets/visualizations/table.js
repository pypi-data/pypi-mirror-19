import d3 from 'd3';
import { fixDataTableBodyHeight } from '../javascripts/modules/utils';
import { timeFormatFactory, formatDate } from '../javascripts/modules/dates';

require('./table.css');
const $ = require('jquery');
require('jquery-ui');

require('datatables-bootstrap3-plugin/media/css/datatables-bootstrap3.css');
import 'datatables.net';
import dt from 'datatables.net-bs';
dt(window, $);

function tableVis(slice) {
  let count = 0;
  const fC = d3.format('0,000');
  let timestampFormatter;
  const container = $(slice.selector);

  function refresh() {
    function onError(xhr) {
      slice.error(xhr.responseText, xhr);
      return;
    }


    function GetQueryString(url, name, result) {
      let search = url;
      const resultCopy = result.concat();
      const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
      const r = search.substring(search.indexOf('?')).substr(1).match(reg);
      if (r) {
        const target = unescape(r[2]);
        if (r !== null && target !== null && target !== '') {
          search = search.replace('&' + name + '=' + target, '');
          resultCopy.push(target);
          return GetQueryString(search, name, resultCopy);
        } else {
          return resultCopy;
        }
      } else {
        return resultCopy;
      }
    }

    // get slice by sliceId
    function sliceUrl(sliceId) {
      const navigateSlice = $.ajax({
        url: '/superset/rest/api/sliceUrl',
        async: false,
        data: { sliceId: sliceId },
        dataType: 'json',
      });
      return navigateSlice.responseText;
    }


    let left = 10;
    let startHeight;
    const isIE = (document.all) ? true : false;
    const Extend = function (destination, source) {
      for (const property in source) {
        destination[property] = source[property];
      }
    };
    const Bind = function (object, fun, args) {
      return function () {
        return fun.apply(object, args || []);
      };
    };
    const BindAsEventListener = function (object, fun) {
      const args = Array.prototype.slice.call(arguments).slice(2);
      return function (event) {
        return fun.apply(object, [event || window.event].concat(args));
      };
    };
    const CurrentStyle = function (element) {
      return element.currentStyle || document.defaultView.getComputedStyle(element, null);
    };
    function create(elm, parent, fn) {
      const element = document.createElement(elm);
      fn && fn(element);
      parent && parent.appendChild(element);
      return element;
    }
    function addListener(element, e, fn) {
      element.addEventListener ?
      element.addEventListener(e, fn, false) :
      element.attachEvent('on' + e, fn);
    }
    function removeListener(element, e, fn) {
      element.removeEventListener ?
      element.removeEventListener(e, fn, false) :
      element.detachEvent('on' + e, fn);
    }
    const Class = function (properties) {
      const eleClass = function () {
        return (arguments[0] !== null && this.init && typeof(this.init) === 'function') ?
        this.init.apply(this, arguments) : this;
      };
      eleClass.prototype = properties;
      return eleClass;
    };

    const Dialog = new Class({
      options: {
        Width: 300,
        Height: 300,
        Left: 100,
        Top: 100,
        Titleheight: 26,
        Minwidth: 200,
        Minheight: 200,
        CancelIco: true,
        ResizeIco: false,
        Info: '',
        Content: '',
        Zindex: 10,
      },
      init: function (options) {
        this.optDragobj = null;
        this.optResize = null;
        this.optCancel = null;
        this.optBody = null;
        this.optX = 0;
        this.optY = 0;
        this.optFM = BindAsEventListener(this, this.Move);
        this.optFS = Bind(this, this.Stop);
        this.optIsdrag = null;
        this.optCss = null;
        this.Width = this.options.Width;
        this.Height = this.options.Height;
        this.Left = this.options.Left;
        this.Top = this.options.Top;
        this.CancelIco = this.options.CancelIco;
        this.Info = this.options.Info;
        this.Content = this.options.Content;
        this.Minwidth = this.options.Minwidth;
        this.Minheight = this.options.Minheight;
        this.Titleheight = this.options.Titleheight;
        this.Zindex = this.options.Zindex;
        Extend(this, options);
        Dialog.Zindex = this.Zindex;
  // 构造dialog
        const obj = ['dialogcontainter', 'dialogtitle', 'dialogtitleinfo', 'dialogtitleico',
        'dialogbody', 'dialogbottom'];
        for (let i = 0; i < obj.length; i++) {
          obj[i] = create('div', null, function (e) {
            const elm = e;
            elm.className = obj[i];
            return elm;
          });
        }
        obj[2].innerHTML = this.Info;
        obj[4].innerHTML = this.Content;
        obj[1].appendChild(obj[2]);
        obj[1].appendChild(obj[3]);
        obj[0].appendChild(obj[1]);
        obj[0].appendChild(obj[4]);
        obj[0].appendChild(obj[5]);
        document.body.appendChild(obj[0]);
        this.optDragobj = obj[0];
        this.optResize = obj[5];
        this.optCancel = obj[3];
        this.optBody = obj[4];
    // o,x1,x2
    // 设置Dialog的长 宽 ,left ,Top
    // with(this._dragobj.style){
    //      height = this.Height + "px";top = this.Top + "px";width = this.Width +"px";
    //      left = this.Left + "px";zIndex = this.Zindex;
    // }
        this.optDragobj.style.height = this.Height + 'px';
        this.optDragobj.style.top = this.Top + 'px';
        this.optDragobj.style.width = this.Width + 'px';
        this.optDragobj.style.left = this.Left + 'px';
        this.optDragobj.style.zIndex = this.Zindex;
        this.optBody.style.height = this.Height
        - this.Titleheight - parseInt(CurrentStyle(this.optBody).paddingLeft) * 2 + 'px';
        // 添加事件
        addListener(this.optDragobj, 'mousedown', BindAsEventListener(this, this.Start, true));
        addListener(this.optCancel, 'mouseover', Bind(this, this.Changebg,
        [this.optCancel, '0px 0px', '-21px 0px']));
        addListener(this.optCancel, 'mouseout', Bind(this, this.Changebg,
        [this.optCancel, '0px 0px', '-21px 0px']));
        addListener(this.optCancel, 'mousedown', BindAsEventListener(this, this.Disappear));
        addListener(this.optBody, 'mousedown', BindAsEventListener(this, this.Cancelbubble));
        addListener(this.optResize, 'mousedown', BindAsEventListener(this, this.Start, false));
      },
      Disappear: function (e) {
        this.Cancelbubble(e);
        document.body.removeChild(this.optDragobj);
      },
      Cancelbubble: function (e) {
        this.optDragobj.style.zIndex = ++Dialog.Zindex;
        document.all ? (e.cancelBubble = true) : (e.stopPropagation());
      },
      Changebg: function (o, x1, x2) {
        o.style.backgroundPosition = (o.style.backgroundPosition === x1) ? x2 : x1;
      },
      Start: function (e, isdrag) {
        startHeight = this.optBody.style.height;
        if (!isdrag) {
          this.Cancelbubble(e);
        }
        this.optCss = isdrag ? { x: 'left', y: 'top' } : { x: 'width', y: 'height' };
        this.optDragobj.style.zIndex = ++Dialog.Zindex;
        this.optIsdrag = isdrag;
        this.optX = isdrag ? (e.clientX - this.optDragobj.offsetLeft || 0) :
        (this.optDragobj.offsetLeft || 0);
        this.optY = isdrag ? (e.clientY - this.optDragobj.offsetTop || 0) :
        (this.optDragobj.offsetTop || 0);
        if (isIE) {
          addListener(this.optDragobj, 'losecapture', this.optFS);
          this.optDragobj.setCapture();
        } else {
          e.preventDefault();
          addListener(window, 'blur', this.optFS);
        }
        addListener(document, 'mousemove', this.optFM);
        addListener(document, 'mouseup', this.optFS);
      },
      Move: function (e) {
        window.getSelection ? window.getSelection().removeAllRanges() :
        document.selection.empty();
        const iX = e.clientX - this.optX;
        const iY = e.clientY - this.optY;
        this.optDragobj.style[this.optCss.x] = (this.optIsdrag ? Math.max(iX, 0) :
        Math.max(iX, this.Minwidth)) + 'px';
        this.optDragobj.style[this.optCss.y] = (this.optIsdrag ? Math.max(iY, 0) :
        Math.max(iY, this.Minheight)) + 'px';
        if (!this.optIsdrag) {
          this.optBody.style.height = Math.max(iY - this.Titleheight,
          this.Minheight - this.Titleheight) -
          2 * parseInt(CurrentStyle(this.optBody).paddingLeft) + 'px';
        }
      },
      Stop: function () {
        removeListener(document, 'mousemove', this.optFM);
        removeListener(document, 'mouseup', this.optFS);
        if (startHeight !== this.optBody.style.height) {
          const frame = this.optBody.childNodes[0];
          let newUrl = frame.getAttribute('src');
          const navHeight = GetQueryString(newUrl, 'navHeight', []);
          if (navHeight.length !== 0) {
            newUrl = newUrl.replace('navHeight=' + navHeight,
            'navHeight=' + this.optBody.style.height);
          } else {
            newUrl += '&navHeight=' + this.optBody.style.height;
          }
          frame.setAttribute('src', newUrl);
        }
        if (isIE) {
          removeListener(this.optDragobj, 'losecapture', this.optFS);
          this.optDragobj.releaseCapture();
        } else {
          removeListener(window, 'blur', this.optFS);
        }
      },
    });
    function createModal(title, url, height, width) {
      let modals;
      if ($('#modals').attr('id') !== undefined) {
        modals = $('#modals');
      } else {
        modals = document.createElement('div');
        $(modals).attr('id', 'modals');
        document.body.append(modals);
      }
      const modalCount = $('#modals').children().length;
      const navHeight = height - 26 - 20 + 'px';
      let newUrl = url;
      newUrl += '&navHeight=' + navHeight;
      const content = '<iframe id = "newSlice_' + modalCount +
      '" width = "100%" height = "100%" scrolling = "no" frameBorder = "0" src = "' +
      newUrl + '"> </iframe>';
      new Dialog({
        Url: newUrl,
        Height: height,
        Width: width,
        Info: title,
        Left: 300 + left,
        Content: content,
        Zindex: (++Dialog.Zindex),
      });
      left += 10;
    }

    // add listener to get navigate message
    $(document).ready(function () {
      window.onmessage = function (e) {
        if (e.data.type === 'newWindow') {
          window.open(e.data.url, null, null);
        } else {
           // make modal can be add only once
          if ($('#newSlice_' + count).attr('id') === undefined) {
            // showModal(e.data.title, e.data.url);
            createModal(e.data.title, e.data.url, e.data.navHeight, e.data.navWidth);
            count++;
          }
        }
      };
    });

    // add filter by change url
    function addFilter(url, colArr) {
      let newUrl = url;
      for (let i = 0; i < colArr.length; i++) {
        const flt = newUrl.match(/flt_col/g);
        let nextFltIndex = 0;
        if (flt === null || flt === '') {
          nextFltIndex = 1;
        } else {
          nextFltIndex = flt.length + 1;
        }
        const col = colArr[i].col;
        const val = (colArr[i].title === '') ? colArr[i].val : colArr[i].title;
        const nextFlt = '&flt_col_' + nextFltIndex + '=' + col + '&flt_op_' + nextFltIndex +
            '=in&flt_eq_' + nextFltIndex + '=' + val;
        newUrl += nextFlt;
      }
      return newUrl;
    }


    function onSuccess(json) {
      const data = json.data;
      const fd = json.form_data;
      // console.log("form_data:");
      // console.log(fd);
      // Removing metrics (aggregates) that are strings
      const realMetrics = [];
      for (const k in data.records[0]) {
        if (fd.metrics.indexOf(k) > -1 && !isNaN(data.records[0][k])) {
          realMetrics.push(k);
        }
      }
      const metrics = realMetrics;

      function col(c) {
        const arr = [];
        for (let i = 0; i < data.records.length; i++) {
          arr.push(data.records[i][c]);
        }
        return arr;
      }
      const maxes = {};
      for (let i = 0; i < metrics.length; i++) {
        maxes[metrics[i]] = d3.max(col(metrics[i]));
      }

      if (fd.table_timestamp_format === 'smart_date') {
        timestampFormatter = formatDate;
      } else if (fd.table_timestamp_format !== undefined) {
        timestampFormatter = timeFormatFactory(fd.table_timestamp_format);
      }

      const div = d3.select(slice.selector);
      div.html('');
      const table = div.append('table')
        .classed(
          'dataframe dataframe table table-striped table-bordered ' +
          'table-condensed table-hover dataTable no-footer', true)
        .attr('width', '100%');

      // add header style
      const headerStyle = fd.headerValue;
      table.append('thead').append('tr')
        .selectAll('th')
        .data(data.columns)
        .enter()
        .append('th')
        .attr('style', headerStyle)
        .text(function (d) {
          return d;
        });

      // get compare info from form_data
      const compareMetricLefts = [];
      const compareMetricRights = [];
      const compareExprs = [];
      const compareValues = [];
      for (let i = 1; i < 10; i++) {
        if (fd['compare_expr_' + i] !== '') {
          compareMetricLefts.push(col(fd['compare_metricLeft_' + i]));
          compareMetricRights.push(col(fd['compare_metricRight_' + i]));
          compareExprs.push(fd['compare_expr_' + i]);
          compareValues.push(fd['compare_value_' + i]);
        }
      }

      table.append('tbody')
        .selectAll('tr')
        .data(data.records)
        .enter()
        .append('tr')
        .selectAll('td')
        .data((row) => data.columns.map((c) => {
          let val = row[c];
          if (c === 'timestamp') {
            val = timestampFormatter(val);
          }
          return {
            col: c,
            val,
            isMetric: metrics.indexOf(c) >= 0,
          };
        }))
        .enter()
        .append('td')
        /* .style('background-image', function (d) {
          if (d.isMetric) {
            const perc = Math.round((d.val / maxes[d.col]) * 100);
            return (
              `linear-gradient(to right, lightgrey, lightgrey ${perc}%, ` +
              `rgba(100,100,100,100) ${perc}%`
            );
          }
          return null;
        }) */
        .attr('style', function (d) {
          // add body style
          let bodyStyle = fd.bodyValue;

          // add column style
          for (let i = 1; i < 10; i++) {
            if (fd['colStyle_value_' + i] !== '') {
              if (d.col === fd['colStyle_metric_' + i]) {
                bodyStyle += fd['colStyle_value_' + i] + ';';
                break;
              }
            } else {
              break;
            }
          }

          // add condition style
          for (let i = 1; i < 10; i++) {
            if (fd['style_expr_' + i] !== '') {
              if (d.isMetric && d.col === fd['style_metric_' + i]) {
                let expr = fd['style_expr_' + i].replace(/x/g, d.val);
                // make '=' to '=='
                expr = expr.replace(/=/g, '==').replace(/>==/g, '>=').replace(/<==/g, '<=');
                // console.log(expr);
                if ((expr.indexOf('$.inArray') === -1 && eval(expr))
                  || (expr.indexOf('$.inArray') !== -1 && eval(expr) !== -1)) {
                  // console.log(fd['style_value_' + i]);
                  bodyStyle += fd['style_value_' + i] + ';';
                }
              }
            } else {
              break;
            }
          }

          // add two colums compare style
          for (let i = 0; i < compareExprs.length; i++) {
            if (d.isMetric && d.col === fd['compare_metricLeft_' + (i + 1)]) {
              const expr = compareExprs[i].replace('x', compareMetricLefts[i][0])
                         .replace('y', compareMetricRights[i][0]).replace(/=/g, '==')
                         .replace(/>==/g, '>=').replace(/<==/g, '<=');
              // console.log(expr);
              if (d.val === compareMetricLefts[i][0] && eval(expr)) {
                bodyStyle += compareValues[i];
              }
              // delete the first element
              compareMetricLefts[i].splice(0, 1);
              compareMetricRights[i].splice(0, 1);
              break;
            }
          }
          return bodyStyle;
        })
        .attr('title', (d) => {
          if (!isNaN(d.val)) {
            return fC(d.val);
          }
          return null;
        })
        .attr('data-sort', function (d) {
          return (d.isMetric) ? d.val : null;
        })
        // .on('click', function (d) {
        //   if (!d.isMetric && fd.table_filter) {
        //     const td = d3.select(this);
        //     if (td.classed('filtered')) {
        //       slice.removeFilter(d.col, [d.val]);
        //       d3.select(this).classed('filtered', false);
        //     } else {
        //       d3.select(this).classed('filtered', true);
        //       slice.addFilter(d.col, [d.val]);
        //     }
        //   }
        // })
        // .style('cursor', function (d) {
        //   return (!d.isMetric) ? 'pointer' : '';
        // })
        .on('click', function (d) {
          for (let i = 1; i <= 10; i++) {
            if (fd['navigate_expr_' + i] !== '') {
              if (d.isMetric && d.col === fd['navigate_metric_' + i]) {
                let expr = fd['navigate_expr_' + i].replace(/x/g, d.val);
                // make '=' to '=='
                expr = expr.replace(/=/g, '==').replace(/>==/g, '>=').replace(/<==/g, '<=');
                if (((expr.indexOf('$.inArray') === -1 && eval(expr))
                || (expr.indexOf('$.inArray') !== -1 && eval(expr) !== -1))) {
                  const type = fd['navigate_open_' + i];
                  const navHeight = (fd['navigate_height_' + i] === '') ? 300 :
                  fd['navigate_height_' + i];
                  const navWidth = (fd['navigate_width_' + i] === '') ? 300 :
                  fd['navigate_width_' + i];
                  const slc = JSON.parse(sliceUrl(fd['navigate_slice_' + i]));
                  let url = slc.url;
                  const title = slc.title;
                  if (url != null) {
                    const standalone = GetQueryString(url, 'standalone', []);
                    const navGroupby = GetQueryString(url, 'groupby', []);
                    if (standalone.length === 0) {
                      if (url.indexOf('standalone') !== -1) {
                        url = url.replace(/standalone=/, 'standalone=true');
                      } else {
                        url += '&standalone=true';
                      }
                    }
                    const sourceGroupby = fd.groupby;
                    const colArr = [];
                    if (navGroupby.length > 0) {
                      for (let j = 0; j < sourceGroupby.length; j++) {
                        const ele = this.parentNode.childNodes[j];
                        for (let k = 0; k < navGroupby.length; k++) {
                          // make navigate groupby val equals source groupby
                          if (sourceGroupby[j] === navGroupby[k]) {
                            colArr.push({
                              val: ele.textContent,
                              col: navGroupby[k],
                              title: ele.title,
                            });
                          }
                        }
                      }
                    }
                    url = addFilter(url, colArr);
                    const postData = {
                      url: url,
                      title: title,
                      type: type,
                      navHeight: navHeight,
                      navWidth: navWidth,
                    };
                    window.parent.postMessage(postData, '*');  // send message to navigate
                  }
                }
              }
            }
          }
        })
        .style('cursor', function (d) {
          return (d.isMetric) ? 'pointer' : '';
        })
        .html((d) => {
          let html = '';
          let icon = '';
          let color = 'black';
          if (d.isMetric) {
            html = slice.d3format(d.col, d.val);
          } else {
            html = d.val;
          }
          for (let i = 1; i < 10; i++) {
            if (fd['style_expr_' + i] !== '') {
              if (d.isMetric && d.col === fd['style_metric_' + i]) {
                let expr = fd['style_expr_' + i].replace(/x/g, d.val);
                // make '=' to '=='
                expr = expr.replace(/=/g, '==').replace(/>==/g, '>=').replace(/<==/g, '<=');
                if ((expr.indexOf('$.inArray') === -1 && eval(expr))
                  || (expr.indexOf('$.inArray') !== -1 && eval(expr) !== -1)) {
                  icon = fd['style_icon_' + i];
                }
              }
            } else {
              break;
            }
          }
          // set icon color
          if (icon === 'fa fa-arrow-up' || icon === 'fa fa-angle-double-up') {
            color = 'green;';
          } else if (icon === 'fa fa-arrow-down' || icon === 'fa fa-angle-double-down') {
            color = 'red;';
          }

          // set link style
          for (let i = 1; i < 10; i++) {
            if (fd['navigate_expr_' + i] !== '') {
              if (d.isMetric && d.col === fd['navigate_metric_' + i]) {
                let expr = fd['navigate_expr_' + i].replace(/x/g, d.val);
                // make '=' to '=='
                expr = expr.replace(/=/g, '==').replace(/>==/g, '>=').replace(/<==/g, '<=');
                if ((expr.indexOf('$.inArray') === -1 && eval(expr))
                  || (expr.indexOf('$.inArray') !== -1 && eval(expr) !== -1)) {
                  html = '<a href="#">' + html + '</a>';
                  break;
                }
              }
            } else {
              break;
            }
          }

          return html + '<i style="margin-left:20px;color:'
                      + color + '" class="' + icon + '" aria-hidden="true"></i>';
        });
      const height = slice.height();
      let paging = false;
      let pageLength;
      if (fd.page_length && fd.page_length > 0) {
        paging = true;
        pageLength = parseInt(fd.page_length, 10);
      }
      const datatable = container.find('.dataTable').DataTable({
        paging,
        pageLength,
        aaSorting: [],
        searching: fd.include_search,
        bInfo: false,
        scrollY: height + 'px',
        scrollCollapse: true,
        scrollX: true,
      });
      fixDataTableBodyHeight(
          container.find('.dataTables_wrapper'), height);
      // Sorting table by main column
      if (fd.metrics.length > 0) {
        const mainMetric = fd.metrics[0];
        datatable.column(data.columns.indexOf(mainMetric)).order('desc').draw();
      }
      slice.done(json);
      container.parents('.widget').find('.tooltip').remove();
    }
    $.getJSON(slice.jsonEndpoint(), onSuccess).fail(onError);
  }

  return {
    render: refresh,
    resize() {},
  };
}

module.exports = tableVis;
