/**
 *
 * @name:  表格增强插件-独立版本
 * @author: yelog
 * @link: https://github.com/yelog/layui-soul-table
 * @license: MIT
 * @version: v1.5.21
 */
layui.define(["table"], function (exports) {
    var $ = layui.$, table = layui.table, HIDE = "layui-hide", tables = {}, originCols = {}, defaultConfig = {
        fixTotal: !1,
        drag: !0,
        rowDrag: !1,
        autoColumnWidth: !0,
        contextmenu: !1,
        fixResize: !0,
        overflow: !1,
        fixFixedScroll: !0,
        filter: !1
    }, _BODY = $("body"), _DOC = $(document), mod = {
        render: function (e) {
            tables[e.id] = e;
            var t = $.extend({}, defaultConfig, e);
            if (t.filter && t.filter.cache) {
                var i = location.pathname + location.hash + e.id, l = this.deepStringify(e.cols);
                if (!originCols[e.id]) {
                    originCols[e.id] = this.deepClone(e.cols);
                    var a = localStorage.getItem(i);
                    a && l === localStorage.getItem("origin" + i) ? this.updateCols(e, this.deepParse(a)) : (localStorage.setItem("origin" + i, l), localStorage.removeItem(i))
                }
            } else this.clearCache(e);
            this.suspendConfig[e.id] = {
                drag: !1,
                rowDrag: !1
            }, t.fixTotal && this.fixTotal(e), t.drag && this.drag(e, t.drag), t.rowDrag && this.rowDrag(e, t.rowDrag), t.autoColumnWidth && this.autoColumnWidth(e, t.autoColumnWidth), this.contextmenu(e, t.contextmenu), t.fixResize && this.fixResizeRightFixed(e), t.overflow && this.overflow(e, t.overflow), t.fixFixedScroll && this.fixFixedScroll(e)
        }, config: function (e) {
            "object" == typeof e && $.extend(!0, defaultConfig, e)
        }, updateCols: function (a, n) {
            var o, r, d, e = {}, t = [], i = [], l = $(a.elem).next().children(".layui-table-box"),
                s = l.children(".layui-table-fixed").children(".layui-table-header").children("table"),
                c = $.merge(l.children(".layui-table-header").children("table"), s),
                h = l.children(".layui-table-header").children("table"),
                f = l.children(".layui-table-fixed").children(".layui-table-body").children("table"),
                u = l.children(".layui-table-body").children("table"),
                p = $.merge(l.children(".layui-table-body").children("table"), f);
            for (o = 0; o < a.cols.length; o++) for (r = 0; r < a.cols[o].length; r++) a.cols[o][r].oldPos = o + "-" + r, e[a.cols[o][r].key] = a.cols[o][r];
            for (o = 0; o < n.length; o++) {
                for (i = [], r = 0; r < n[o].length; r++) {
                    if (d = a.index + "-" + n[o][r].key, n[o][r].width && e[n[o][r].key] !== n[o][r].width && this.getCssRule(a, d, function (e) {
                        e.style.width = (n[o][r].width ? n[o][r].width : 0) + "px"
                    }), e[n[o][r].key].hide !== n[o][r].hide && (c.find('th[data-key="' + d + '"]')[n[o][r].hide ? "addClass" : "removeClass"]("layui-hide"), p.find('td[data-key="' + d + '"]')[n[o][r].hide ? "addClass" : "removeClass"]("layui-hide")), (e[n[o][r].key].oldPos !== o + "-" + r || e[n[o][r].key].fixed !== n[o][r].fixed) && n[o][r].fixed !== e[n[o][r].key].fixed) return a.cols = n, void table.reload(a.id);
                    e[n[o][r].key].fixed = n[o][r].fixed, e[n[o][r].key].width = n[o][r].width, e[n[o][r].key].hide = n[o][r].hide, i.push(e[n[o][r].key])
                }
                t.push(i)
            }

            function y(e, t) {
                for (o = 0; o < n.length; o++) for (r = 0; r < n[o].length; r++) {
                    d = a.index + "-" + n[o][r].key;
                    var i = $(e).children(t + ":eq(" + r + ")").attr("data-key");
                    if (i !== d && ($(e).children(t + ":eq(" + r + ")").before($(e).children(t + '[data-key="' + d + '"]')), n[o][r].fixed)) {
                        var l = ("th" === t ? s : f).children().children("th" === t ? "tr" : 'tr[data-index="' + $(e).attr("data-index") + '"]');
                        l.children(t + '[data-key="' + i + '"]').before(l.children(t + '[data-key="' + d + '"]'))
                    }
                }
            }

            h.children().children("tr").each(function () {
                y(this, "th")
            }), u.children().children("tr").each(function () {
                y(this, "td")
            }), a.cols = t, table.resize(a.id)
        }, getCssRule: function (e, i, l) {
            var t = e.elem.next().find("style")[0], a = t.sheet || t.styleSheet || {}, n = a.cssRules || a.rules;
            layui.each(n, function (e, t) {
                if (t.selectorText === ".laytable-cell-" + i) return l(t), !0
            })
        }, autoColumnWidth: function (e, n) {
            var t = this;

            function i(h, l) {
                var e = $(l.elem),
                    t = e.next().children(".layui-table-box").children(".layui-table-header").children("table").children("thead").children("tr").children("th"),
                    i = e.next().children(".layui-table-box").children(".layui-table-fixed").children(".layui-table-header").children("table").children("thead").children("tr").children("th"),
                    f = e.next().children(".layui-table-box").children(".layui-table-body").children("table").children("tbody").children("tr"),
                    u = e.next().children(".layui-table-total").find("tr");

                function a(e, t, i) {
                    var l = t.data("key"), a = l.split("-"), n = 3 === a.length ? a[1] + "-" + a[2] : "";
                    if (!(1 < t.attr("colspan") || t.data("unresize")) && i) {
                        var o = t.text().width(t.css("font")) + 21, r = t.css("font");
                        if (f.children('td[data-key="' + l + '"]').each(function (e, t) {
                            var i = 0;
                            $(this).children().children() && 0 < $(this).children().children().length ? i += $(this).children().html().width(r) : i = $(this).text().width(r), o < i && (o = i)
                        }), 0 < u.length) {
                            var d = u.children('td[data-key="' + l + '"]').text().width(r);
                            o < d && (o = d)
                        }
                        o += 32, h.getCssRule(e, l, function (e) {
                            e.style.width = o + "px"
                        });
                        for (var s = 0; s < e.cols.length; s++) for (var c = 0; c < e.cols[s].length; c++) if (e.cols[s][c].key === n) {
                            e.cols[s][c].width = o;
                            break
                        }
                    }
                }

                String.prototype.width = function (e) {
                    var t = e || _BODY.css("font"), i = $("<div>" + this + "</div>").css({
                        position: "absolute",
                        float: "left",
                        "white-space": "nowrap",
                        visibility: "hidden",
                        font: t
                    }).appendTo(_BODY), l = i.width();
                    return i.remove(), l
                }, void 0 !== n && void 0 !== n.dblclick && !n.dblclick || t.add(i).on("dblclick", function (e) {
                    var t = $(this), i = e.clientX - t.offset().left;
                    a(l, t, 0 < t.parents(".layui-table-fixed-r").length ? i <= 10 : t.width() - i <= 10)
                }), n && n.init && t.add(i).each(function (e) {
                    var t = $(this).attr("data-key").split("-");
                    !1 === l.cols[t[1]][t[2]].autoWidth || Array.isArray(n.init) && -1 === n.init.indexOf($(this).attr("data-field")) || a(l, $(this), !0)
                })
            }

            "object" == typeof e ? i(t, e) : "string" == typeof e ? i(t, tables[e]) : void 0 === e && layui.each(tables, function () {
                i(t, this)
            })
        }, drag: function (I, e) {
            if (!(1 < I.cols.length)) {
                var D = this, t = $(I.elem), _ = t.next().children(".layui-table-box"),
                    s = $.merge(_.children(".layui-table-header").children("table"), _.children(".layui-table-fixed").children(".layui-table-header").children("table")),
                    O = _.children(".layui-table-fixed").children(".layui-table-body").children("table"),
                    c = _.children(".layui-table-body").children("table"),
                    W = $.merge(_.children(".layui-table-body").children("table"), O),
                    F = t.next().children(".layui-table-total").children("table"),
                    T = t.next().children(".layui-table-total").children("table.layui-table-total-fixed"),
                    h = t.next().children(".layui-table-total").children("table:eq(0)"), z = I.id,
                    X = "simple" === e || e && "simple" === e.type, E = e && e.toolbar, Y = !1, B = !1;
                if (!s.attr("drag")) {
                    if (s.attr("drag", !0), E) {
                        _.append('<div class="soul-drag-bar"><div data-type="left">左固定</div><div data-type="none">不固定</div><div data-type="right">右固定</div></div>');
                        var N = _.children(".soul-drag-bar");
                        N.children("div").on("mouseenter", function () {
                            $(this).addClass("active")
                        }).on("mouseleave", function () {
                            $(this).removeClass("active")
                        })
                    }
                    s.find("th").each(function () {
                        var k = $(this), C = k.data("field"), w = k.data("key");
                        if (w) {
                            var e = w.split("-"), d = I.cols[e[1]][e[2]], S = e[1] + "-" + e[2],
                                R = 0 < k.parents(".layui-table-fixed").length;
                            $(this).find("span:first,.laytable-cell-checkbox").css("cursor", "move").on("mousedown", function (e) {
                                if (!D.suspendConfig[z].drag && 0 === e.button) {
                                    e.preventDefault();
                                    var y = k.clone().css("visibility", "hidden"), t = k.position().left,
                                        b = k.offset().top, v = e.clientX - t,
                                        x = k.parents("tr:eq(0)").css("background-color"), m = k.width(), r = $(this),
                                        g = d.fixed;
                                    B = !0, _DOC.bind("selectstart", function () {
                                        return !1
                                    }), _BODY.on("mousemove", function (e) {
                                        if (B && y) {
                                            _.removeClass("no-left-border"), Y || (E && (N.attr("data-type", g || "none"), N.addClass("active")), k.after(y), k.addClass("isDrag").css({
                                                position: "absolute",
                                                "z-index": 1,
                                                "border-left": "1px solid #e6e6e6",
                                                "background-color": x,
                                                width: m + 1
                                            }), X || ((R ? O : W).find('td[data-key="' + w + '"]').each(function () {
                                                $(this).after($(this).clone().css("visibility", "hidden").attr("data-clone", "")), $(this).addClass("isDrag").css({
                                                    position: "absolute",
                                                    "z-index": 1,
                                                    "border-left": "1px solid #e6e6e6",
                                                    "background-color": $(this).css("background-color"),
                                                    width: m + 1
                                                })
                                            }), 0 < F.length && (R ? T : F).find('td[data-key="' + w + '"]').each(function () {
                                                $(this).after($(this).clone().css("visibility", "hidden").attr("data-clone", "")), $(this).addClass("isDrag").css({
                                                    position: "absolute",
                                                    "z-index": 1,
                                                    "background-color": $(this).parents("tr:eq(0)").css("background-color"),
                                                    width: m + 1
                                                })
                                            }))), Y = !0;
                                            var t, i, l, a, n, o = e.clientX - v, r = y.prev().prev(), d = 0 < r.length,
                                                s = d ? r.data("key").split("-") : [],
                                                c = y.next().hasClass("layui-table-patch") ? [] : y.next(),
                                                h = 0 < c.length, f = h ? c.data("key").split("-") : [],
                                                u = d && y.position().left - o > r.width() / 2,
                                                p = h && o - y.position().left > c.width() / 2;
                                            if (Math.abs(y.position().left - o), 0 < y.position().left - o ? !d || !!g != !!I.cols[s[1]][s[2]].fixed : !h || !!g != !!I.cols[f[1]][f[2]].fixed) return k.css("left", y.position().left), W.find('td[data-key="' + w + '"][data-clone]').each(function (e) {
                                                $(this).prev().css("left", y.position().left)
                                            }), 0 < F.length && F.find('td[data-key="' + w + '"][data-clone]').each(function (e) {
                                                $(this).prev().css("left", y.position().left)
                                            }), void _.addClass("no-left-border");
                                            if (k.css("left", o), u) {
                                                for (y.after(r), $("#soul-columns" + z + '>li[data-value="' + C + '"]').after($("#soul-columns" + z + '>li[data-value="' + C + '"]').prev()), l = 0; l < I.cols.length; l++) {
                                                    for (a = 0; a < I.cols[l].length; a++) if (I.cols[l][a].key === S) {
                                                        t = l, i = a;
                                                        break
                                                    }
                                                    if (void 0 !== t && void 0 !== i) break
                                                }
                                                n = I.cols[t][i - 1], I.cols[t][i - 1] = I.cols[t][i], I.cols[t][i] = n, D.fixTableRemember(I)
                                            } else if (p) {
                                                for (y.prev().before(c), $("#soul-columns" + z + '>li[data-value="' + C + '"]').before($("#soul-columns" + z + '>li[data-value="' + C + '"]').next()), l = 0; l < I.cols.length; l++) {
                                                    for (a = 0; a < I.cols[l].length; a++) if (I.cols[l][a].key === S) {
                                                        t = l, i = a;
                                                        break
                                                    }
                                                    if (void 0 !== t && void 0 !== i) break
                                                }
                                                n = I.cols[t][i + 1], I.cols[t][i + 1] = I.cols[t][i], I.cols[t][i] = n, D.fixTableRemember(I)
                                            }
                                            W.find('td[data-key="' + w + '"][data-clone]').each(function () {
                                                $(this).prev().css("left", o), u ? 0 !== $(this).prev().prev().length && $(this).after($(this).prev().prev()) : p && 0 !== $(this).next().length && $(this).prev().before($(this).next())
                                            }), 0 < F.length && F.find('td[data-key="' + w + '"][data-clone]').each(function () {
                                                $(this).prev().css("left", o), u ? 0 !== $(this).prev().prev().length && $(this).after($(this).prev().prev()) : p && 0 !== $(this).next().length && $(this).prev().before($(this).next())
                                            }), e.clientY - b < -15 ? (0 === $("#column-remove").length && _BODY.append('<i id="column-remove" class="layui-red layui-icon layui-icon-delete"></i>'), $("#column-remove").css({
                                                top: e.clientY - $("#column-remove").height() / 2,
                                                left: e.clientX - $("#column-remove").width() / 2,
                                                "font-size": b - e.clientY + "px"
                                            }), $("#column-remove").show()) : $("#column-remove").hide()
                                        }
                                    }).on("mouseup", function () {
                                        if (_DOC.unbind("selectstart"), _BODY.off("mousemove").off("mouseup"), B && y) {
                                            if (B = !1, Y) {
                                                "checkbox" !== d.type && r.on("click", function (e) {
                                                    e.stopPropagation()
                                                }), Y = !1, _.removeClass("no-left-border"), k.removeClass("isDrag").css({
                                                    position: "relative",
                                                    "z-index": "inherit",
                                                    left: "inherit",
                                                    "border-left": "inherit",
                                                    width: "inherit",
                                                    "background-color": "inherit"
                                                }), k.next().remove();
                                                var t = k.prev().data("key");
                                                if (g) {
                                                    var e = _.children(".layui-table-header").children("table").find('th[data-key="' + w + '"]');
                                                    t ? e.parent().children('th[data-key="' + t + '"]').after(e) : "right" === g ? 0 < k.siblings().length && _.children(".layui-table-header").children("table").find('th[data-key="' + k.next().data("key") + '"]').prev().after(e) : (e.parent().prepend('<th class="layui-hide"></th>'), e.parent().children("th:first").after(e), e.parent().children("th:first").remove())
                                                }
                                                if (X ? (W.find('td[data-key="' + w + '"]').each(function () {
                                                    if (t) $(this).parent().children('td[data-key="' + t + '"]').after($(this)); else if ("right" === g) {
                                                        if (0 < k.siblings().length) {
                                                            var e = $(this).parent().children('td[data-key="' + k.next().data("key") + '"]').prev();
                                                            0 < e.length ? e.after($(this)) : ($(this).parent().prepend('<td class="layui-hide"></td>'), $(this).parent().children("td:first").after($(this)), $(this).parent().children("td:first").remove())
                                                        }
                                                    } else $(this).parent().prepend('<td class="layui-hide"></td>'), $(this).parent().children("td:first").after($(this)), $(this).parent().children("td:first").remove()
                                                }), 0 < F.length && F.find('td[data-key="' + w + '"]').each(function () {
                                                    if (t) $(this).parent().children('td[data-key="' + t + '"]').after($(this)); else if ("right" === g) {
                                                        var e = $(this).parent().children('td[data-key="' + k.next().data("key") + '"]').prev();
                                                        0 < e.length ? e.after($(this)) : ($(this).parent().prepend('<td class="layui-hide"></td>'), $(this).parent().children("td:first").after($(this)), $(this).parent().children("td:first").remove())
                                                    } else $(this).parent().prepend('<td class="layui-hide"></td>'), $(this).parent().children("td:first").after($(this)), $(this).parent().children("td:first").remove()
                                                })) : R ? (c.find('td[data-key="' + w + '"]').each(function () {
                                                    if (t) $(this).parent().children('td[data-key="' + t + '"]').after($(this)); else if ("right" === g) {
                                                        if (0 < k.siblings().length) {
                                                            var e = $(this).parent().children('td[data-key="' + k.next().data("key") + '"]').prev();
                                                            0 < e.length ? e.after($(this)) : ($(this).parent().prepend('<td class="layui-hide"></td>'), $(this).parent().children("td:first").after($(this)), $(this).parent().children("td:first").remove())
                                                        }
                                                    } else $(this).parent().prepend('<td class="layui-hide"></td>'), $(this).parent().children("td:first").after($(this)), $(this).parent().children("td:first").remove()
                                                }), O.find('td[data-key="' + w + '"][data-clone]').each(function () {
                                                    $(this).prev().removeClass("isDrag").css({
                                                        position: "relative",
                                                        "z-index": "inherit",
                                                        left: "inherit",
                                                        "border-left": "inherit",
                                                        width: "inherit",
                                                        "background-color": "inherit"
                                                    }), $(this).remove()
                                                }), 0 < F.length && (h.find('td[data-key="' + w + '"]').each(function () {
                                                    if (t) $(this).parent().children('td[data-key="' + t + '"]').after($(this)); else if ("right" === g) {
                                                        var e = $(this).parent().children('td[data-key="' + k.next().data("key") + '"]').prev();
                                                        0 < e.length ? e.after($(this)) : ($(this).parent().prepend('<td class="layui-hide"></td>'), $(this).parent().children("td:first").after($(this)), $(this).parent().children("td:first").remove())
                                                    } else $(this).parent().prepend('<td class="layui-hide"></td>'), $(this).parent().children("td:first").after($(this)), $(this).parent().children("td:first").remove()
                                                }), T.find('td[data-key="' + w + '"][data-clone]').each(function () {
                                                    $(this).prev().removeClass("isDrag").css({
                                                        position: "relative",
                                                        "z-index": "inherit",
                                                        left: "inherit",
                                                        width: "inherit",
                                                        "background-color": "inherit"
                                                    }), $(this).remove()
                                                }))) : (W.find('td[data-key="' + w + '"][data-clone]').each(function () {
                                                    $(this).prev().removeClass("isDrag").css({
                                                        position: "relative",
                                                        "z-index": "inherit",
                                                        left: "inherit",
                                                        width: "inherit",
                                                        "background-color": "inherit"
                                                    }), $(this).remove()
                                                }), 0 < F.length && F.find('td[data-key="' + w + '"][data-clone]').each(function () {
                                                    $(this).prev().removeClass("isDrag").css({
                                                        position: "relative",
                                                        "z-index": "inherit",
                                                        left: "inherit",
                                                        width: "inherit",
                                                        "background-color": "inherit"
                                                    }), $(this).remove()
                                                })), y = null, E) {
                                                    if (0 < N.children(".active").length && N.children(".active").attr("data-type") !== N.attr("data-type")) {
                                                        var i, l, a, n, o = N.children(".active").attr("data-type");
                                                        for (i = 0; i < I.cols.length; i++) for (l = 0; l < I.cols[i].length; l++) "right" === o || "none" === o && "right" === N.attr("data-type") ? void 0 === n && ("right" === I.cols[i][l].fixed ? n = {
                                                            x: i,
                                                            y: l
                                                        } : l === I.cols[i].length - 1 && (n = {
                                                            x: i,
                                                            y: l + 1
                                                        })) : void 0 !== n || I.cols[i][l].fixed && "right" !== I.cols[i][l].fixed || (n = {
                                                            x: i,
                                                            y: l
                                                        }), I.cols[i][l].key === S && (a = {x: i, y: l});
                                                        d.fixed = "none" !== o && o, a.y !== n.y && (I.cols[a.x].splice(a.y, 1), a.y < n.y && --n.y, I.cols[n.x].splice(n.y, 0, d), D.fixTableRemember(I)), table.reload(z)
                                                    }
                                                    N.removeClass("active")
                                                }
                                            } else r.unbind("click");
                                            $("#column-remove").is(":visible") && (s.find("thead>tr>th[data-key=" + w + "]").addClass(HIDE), W.find('tbody>tr>td[data-key="' + w + '"]').addClass(HIDE), F.find('tbody>tr>td[data-key="' + w + '"]').addClass(HIDE), d.hide = !0, D.fixTableRemember(I), $("#soul-columns" + z).find('li[data-value="' + C + '"]>input').prop("checked", !1)), $("#column-remove").hide()
                                        }
                                    })
                                }
                            })
                        }
                    })
                }
            }
        }, rowDrag: function (h, v) {
            var x, e, m = this, g = $(h.elem), k = g.next().children(".layui-table-box"),
                C = k.children(".layui-table-fixed").children(".layui-table-body").children("table"),
                w = k.children(".layui-table-body").children("table"),
                t = $.merge(k.children(".layui-table-body").children("table"), C), S = h.id, R = !1,
                i = v.trigger || "row", I = !1 !== v.numbers, D = null, _ = 0,
                l = "row" === i ? t.children("tbody").children("tr") : t.find(i);
            for ("row" !== i && t.find(i).css("cursor", "move"), x = 0; x < h.cols.length; x++) for (e = 0; e < h.cols[x].length; e++) if ("numbers" === h.cols[x][e].type) {
                D = h.index + "-" + x + "-" + e, _ = parseInt(w.find('td[data-key="' + D + '"]:first').text());
                break
            }
            l.on("mousedown", function (e) {
                if (!m.suspendConfig[S].rowDrag && 0 === e.button) {
                    var s = "row" === i ? $(this) : $(this).parents("tr:eq(0)"), c = parseInt(s.data("index")),
                        f = w.children("tbody").children("tr[data-index=" + c + "]"),
                        u = f.clone().css("visibility", "hidden"),
                        p = C.children("tbody").children("tr[data-index=" + c + "]"),
                        y = k.children(".layui-table-body").scrollTop(), t = s.position().top, b = e.clientY - t;
                    _BODY.on("mousemove", function (e) {
                        if (!R) {
                            R = !0;
                            var t = g.next().find("style")[0], i = t.sheet || t.styleSheet || {};
                            m.addCSSRule(i, ".layui-table-view .layui-table td", "cursor: move"), m.addCSSRule(i, ".layui-table tr", "transition: none"), k.addClass("noselect"), f.after(u), f.css({
                                position: "absolute",
                                "z-index": 1
                            }), p.each(function () {
                                $(this).after($(this).clone().css("visibility", "hidden")), $(this).css({
                                    position: "absolute",
                                    "z-index": 102
                                })
                            })
                        }
                        var l = e.clientY - b + (k.children(".layui-table-body").scrollTop() - y), a = u.position().top,
                            n = f.prev(), o = 0 < n.length, r = u.next(), d = 0 < r.length,
                            s = o && a - l > n.height() / 2, c = d && l - a > r.height() / 2;
                        if (0 < a - l ? !o : !d) return f.css("top", a), void p.each(function () {
                            $(this).css("top", a)
                        });

                        function h(e, t) {
                            var i = parseInt(e.data("index")) + t;
                            return e.data("index", i), e.attr("data-index", i), e
                        }

                        f.css("top", l), p.each(function () {
                            $(this).css("top", l)
                        }), s ? (h(f, -1), u.after(h(n, 1)), p.each(function () {
                            h($(this), -1), $(this).next().after(h($(this).prev(), 1))
                        })) : c && (h(f, 1).before(h(r, -1)), p.each(function () {
                            h($(this), 1), $(this).before(h($(this).next().next(), -1))
                        }))
                    }).on("mouseup", function (e) {
                        if (_BODY.off("mousemove").off("mouseup"), R) {
                            R = !1, k.removeClass("noselect"), f.css({
                                position: "inherit",
                                "z-index": "inherit"
                            }), f.next().remove(), p.each(function () {
                                $(this).css({position: "inherit", "z-index": "inherit"}), $(this).next().remove()
                            });
                            var t = g.next().find("style")[0], i = t.sheet || t.styleSheet || {},
                                l = i.cssRules || i.rules;
                            layui.each(l, function (e, t) {
                                ".layui-table-view .layui-table td" === t.selectorText && (t.style.cursor = "default")
                            });
                            var a = s.index();
                            if (a !== c) {
                                var n = table.cache[S], o = n.splice(c, 1)[0];
                                if (n.splice(a, 0, o), D && I) {
                                    var r = [a, c].sort();
                                    for (x = r[0]; x <= r[1]; x++) {
                                        var d = _ + x;
                                        C.find('td[data-key="' + D + '"]:eq(' + x + ")").children().html(d), w.find('td[data-key="' + D + '"]:eq(' + x + ")").children().html(d), n[x][table.config.indexName] = d - 1
                                    }
                                }
                                "function" == typeof v.done && v.done.call(h, {
                                    row: o,
                                    newIndex: a,
                                    oldIndex: c,
                                    cache: n
                                })
                            }
                        }
                    })
                }
            })
        }, fixTableRemember: function (e, t) {
            if (void 0 === e.filter ? defaultConfig.filter && defaultConfig.filter.cache : e.filter.cache) {
                if (t && t.rule) for (var i = t.rule.selectorText.split("-")[3] + "-" + t.rule.selectorText.split("-")[4], l = 0; l < e.cols.length; l++) for (var a = 0; a < e.cols[l].length; a++) if (e.cols[l][a].key === i) {
                    e.cols[l][a].width = t.rule.style.width.replace("px", "");
                    break
                }
                var n = location.pathname + location.hash + e.id;
                localStorage.setItem(n, this.deepStringify(e.cols))
            }
        }, clearCache: function (e) {
            var t;
            e && (t = "object" == typeof e ? void 0 !== e.config ? e.config.id : e.id : e, localStorage.removeItem(location.pathname + location.hash + t), originCols[t] && this.updateCols(tables[t], this.deepClone(originCols[t])))
        }, overflow: function (e, t) {
            var i = {};
            if ("string" == typeof t) i = {type: t}; else {
                if ("object" != typeof t) return;
                i = t
            }
            var n, o, l = $(e.elem), a = l.next().find(".layui-table-header"), r = l.next().find(".layui-table-body"),
                d = l.next().find(".layui-table-total"), s = i.hoverTime || 0, c = i.color || "white",
                h = i.bgColor || "black", f = i.minWidth || 300, u = i.maxWidth || 300;
            if ("tips" === i.type) {
                function p(e) {
                    clearTimeout(o);
                    var t = $(this), i = t.children(".layui-table-cell"), l = i.outerWidth(),
                        a = l < f ? f : u < l ? u : l;
                    t.data("off") || (e ? layer.close(n) : i.prop("scrollWidth") > l && (n = layer.tips('<span style="color: ' + c + '">' + $(this).text() + "</span>", this, {
                        tips: [1, h],
                        maxWidth: a,
                        time: 0
                    })))
                }

                r.off("mouseenter", "td").off("mouseleave", "td").on("mouseenter", "td", function () {
                    var e = this;
                    o = setTimeout(function () {
                        p.call(e)
                    }, s)
                }).on("mouseleave", "td", function () {
                    p.call(this, "hide")
                }), i.header && a.off("mouseenter", "th").off("mouseleave", "th").on("mouseenter", "th", function () {
                    var e = this;
                    o = setTimeout(function () {
                        p.call(e)
                    }, s)
                }).on("mouseleave", "th", function () {
                    p.call(this, "hide")
                }), i.total && d.off("mouseenter", "td").off("mouseleave", "td").on("mouseenter", "td", function () {
                    var e = this;
                    o = setTimeout(function () {
                        p.call(e)
                    }, s)
                }).on("mouseleave", "td", function () {
                    p.call(this, "hide")
                })
            } else "title" === i.type && (r.off("mouseenter", "td").on("mouseenter", "td", function () {
                var e = $(this), t = e.children(".layui-table-cell");
                e.data("off") || t.prop("scrollWidth") > t.outerWidth() && t.attr("title", $(this).text())
            }), i.header && a.off("mouseenter", "th").on("mouseenter", "th", function () {
                var e = $(this), t = e.children(".layui-table-cell");
                e.data("off") || t.prop("scrollWidth") > t.outerWidth() && t.attr("title", $(this).text())
            }), i.total && d.off("mouseenter", "td").on("mouseenter", "td", function () {
                var e = $(this), t = e.children(".layui-table-cell");
                e.data("off") || t.prop("scrollWidth") > t.outerWidth() && t.attr("title", $(this).text())
            }))
        }, contextmenu: function (h, e) {
            for (var t = $(h.elem), i = t.next().children(".layui-table-box"), l = $.merge(i.children(".layui-table-header").children("table"), i.children(".layui-table-fixed").children(".layui-table-header").children("table")), a = i.children(".layui-table-fixed").children(".layui-table-body").children("table"), n = $.merge(i.children(".layui-table-body").children("table"), a), o = t.next().children(".layui-table-total").children("table"), f = h.id, r = {
                header: {
                    box: l,
                    tag: "th",
                    opts: e ? e.header : "",
                    cols: {}
                },
                body: {box: n, tag: "td", opts: e ? e.body : "", cols: {}, isBody: !0},
                total: {box: o, tag: "td", opts: e ? e.total : "", cols: {}}
            }, d = !1, s = 0; s < h.cols.length; s++) for (var c = 0; c < h.cols[s].length; c++) h.cols[s][c].contextmenu && (d = !0, r.header.cols[h.cols[s][c].key] = h.cols[s][c].contextmenu.header, r.body.cols[h.cols[s][c].key] = h.cols[s][c].contextmenu.body, r.total.cols[h.cols[s][c].key] = h.cols[s][c].contextmenu.total);
            if (e || d) {
                for (var u in r) !function (i) {
                    r[i].box.find(r[i].tag).on("contextmenu", function (e) {
                        $("#soul-table-contextmenu-wrapper").remove(), _BODY.append('<div id="soul-table-contextmenu-wrapper"></div>'), $("#soul-table-contextmenu-wrapper").on("click", function (e) {
                            e.stopPropagation()
                        });
                        var t = r[i].cols[$(this).data("key").substr($(this).data("key").indexOf("-") + 1)];
                        return !1 !== t && (t && 0 < t.length ? (p($("#soul-table-contextmenu-wrapper"), e.pageX, e.pageY, t, $(this), r[i].box, r[i].tag, r[i].isBody), !1) : !1 !== r[i].opts && (r[i].opts && 0 < r[i].opts.length ? (p($("#soul-table-contextmenu-wrapper"), e.pageX, e.pageY, r[i].opts, $(this), r[i].box, r[i].tag, r[i].isBody), !1) : void 0))
                    })
                }(u);
                _BODY.on("click", function () {
                    $("#soul-table-contextmenu-wrapper").remove()
                })
            }

            function p(e, t, i, l, o, r, d, s) {
                var a, n = [];
                for (n.push('<ul class="soul-table-contextmenu">'), a = 0; a < l.length; a++) n.push('<li data-index="' + a + '" class="' + (l[a].children && 0 < l[a].children.length ? "contextmenu-children" : "") + '">'), l[a].icon ? n.push('<i class="prefixIcon ' + l[a].icon + '" />') : n.push('<i class="prefixIcon" />'), n.push(l[a].name), l[a].children && 0 < l[a].children.length && n.push('<i class="endIcon layui-icon layui-icon-right" />'), n.push("</li>");
                n.push("</ul>"), e.append(n.join(""));
                var c = e.children().last();
                for (i + c.outerHeight() > _BODY.prop("scrollHeight") && (i -= c.outerHeight()) < 0 && (i = 0), "left" === e.parent().data("direction") && 0 < e.offset().left - c.outerWidth() ? (t = -c.outerWidth(), c.data("direction", "left")) : t + c.outerWidth() + e.offset().left > _BODY.prop("scrollWidth") && ((t = t - c.outerWidth() - e.outerWidth()) + e.offset().left < 0 && (t = -e.offset().left), c.data("direction", "left")), c.css({
                    top: i + "px",
                    left: t + "px"
                }), a = 0; a < l.length; a++) "function" == typeof l[a].click && function (t) {
                    e.children(".soul-table-contextmenu:last").children('li[data-index="' + t + '"]').on("click", function () {
                        var e = o.parents("tr:eq(0)").data("index"), a = r.find('tr[data-index="' + e + '"]'),
                            n = layui.table.cache[f][e];
                        l[t].click.call(h, {
                            cell: o,
                            elem: "th" === d ? o : s ? r.children("tbody").children('tr[data-index="' + e + '"]').children('[data-key="' + o.data("key") + '"]') : r.find('[data-key="' + o.data("key") + '"]'),
                            trElem: r.children("tbody").children('tr[data-index="' + e + '"]'),
                            text: o.text(),
                            field: o.data("field"),
                            del: s ? function () {
                                table.cache[f][e] = [], a.remove(), table.resize(f)
                            } : "",
                            update: s ? function (e) {
                                e = e || {}, layui.each(e, function (i, e) {
                                    if (i in n) {
                                        var l, t = a.children('td[data-field="' + i + '"]');
                                        n[i] = e, table.eachCols(f, function (e, t) {
                                            t.field == i && t.templet && (l = t.templet)
                                        }), t.children(".layui-table-cell").html(l ? "function" == typeof l ? l(n) : layui.laytpl($(l).html() || e).render(n) : e), t.data("content", e)
                                    }
                                })
                            } : "",
                            row: s ? n : {}
                        }), $("#soul-table-contextmenu-wrapper").remove()
                    })
                }(a);
                e.children(".soul-table-contextmenu:last").children("li").on("mouseenter", function (e) {
                    e.stopPropagation(), $(this).siblings(".contextmenu-children").children("ul").remove(), $(this).hasClass("contextmenu-children") && p($(this), $(this).outerWidth(), $(this).position().top, l[$(this).data("index")].children, o, r, d, s)
                })
            }
        }, fixTotal: function (e) {
            var t = $(e.elem), i = t.next().children(".layui-table-total"), l = t.next().find("style")[0],
                a = l.sheet || l.styleSheet || {};
            if (0 < i.length) {
                var n = t.next().children(".layui-table-box"),
                    o = n.children(".layui-table-fixed-l").children(".layui-table-body").children("table").children("tbody").children("tr:eq(0)").children("td"),
                    r = n.children(".layui-table-fixed-r").children(".layui-table-body").children("table").children("tbody").children("tr:eq(0)").children("td"),
                    d = [];
                i.children(".layui-table-total-fixed").remove(), 0 < o.length && (this.addCSSRule(a, ".layui-table-total-fixed-l .layui-table-patch", "display: none"), t.next().css("position", "relative"), d.push('<table style="position: absolute;background-color: #fff;left: 0;top: ' + (i.position().top + 1) + 'px" cellspacing="0" cellpadding="0" border="0" class="layui-table layui-table-total-fixed layui-table-total-fixed-l"><tbody><tr>'), o.each(function () {
                    $(this).data("key") && d.push(i.children("table:eq(0)").find('[data-key="' + $(this).data("key") + '"]').prop("outerHTML"))
                }), d.push("</tr></tbody></table>"), i.append(d.join(""))), 0 < r.length && (this.addCSSRule(a, ".layui-table-total-fixed-r td:first-child", "border-left:1px solid #e6e6e6"), this.addCSSRule(a, ".layui-table-total-fixed-r td:last-child", "border-left: none"), t.next().css("position", "relative"), (d = []).push('<table style="position: absolute;background-color: #fff;right: 0;top: ' + (i.position().top + 1) + 'px" cellspacing="0" cellpadding="0" border="0" class="layui-table layui-table-total-fixed layui-table-total-fixed-r"><tbody><tr>'), r.each(function () {
                    d.push(i.children("table:eq(0)").find('[data-key="' + $(this).data("key") + '"]').prop("outerHTML"))
                }), d.push("</tr></tbody></table>"), i.append(d.join("")))
            }
        }, fixResizeRightFixed: function (l) {
            var i, a = this,
                e = $(l.elem).next().children(".layui-table-box").children(".layui-table-fixed-r").children(".layui-table-header").children("table"),
                n = {}, o = "layui-table-sort", r = "layui-table-sort-invalid";
            0 < e.length && (e.find("th").off("mousemove").on("mousemove", function (e) {
                var t = $(this), i = t.offset().left, l = e.clientX - i;
                t.data("unresize") || n.resizeStart || (t.width() - l <= 10 && _BODY.css("cursor", "initial"), n.allowResize = l <= 10, _BODY.css("cursor", n.allowResize ? "col-resize" : ""))
            }).off("mousedown").on("mousedown", function (e) {
                var i = $(this);
                if (n.allowResize) {
                    i.find("." + o).removeClass(o).addClass(r);
                    var t = i.data("key");
                    e.preventDefault(), n.resizeStart = !0, n.offset = [e.clientX, e.clientY], a.getCssRule(l, t, function (e) {
                        var t = e.style.width || i.outerWidth();
                        n.rule = e, n.ruleWidth = parseFloat(t), n.othis = i, n.minWidth = i.data("minwidth") || l.cellMinWidth
                    })
                }
            }), _DOC.on("mousemove", function (e) {
                if (n.resizeStart) {
                    if (layui.soulTable.fixTableRemember(l, n), e.preventDefault(), n.rule) {
                        var t = n.ruleWidth - e.clientX + n.offset[0];
                        t < n.minWidth && (t = n.minWidth), n.rule.style.width = t + "px"
                    }
                    i = 1
                }
            }).on("mouseup", function (e) {
                n.resizeStart && setTimeout(function () {
                    n.othis.find("." + r).removeClass(r).addClass(o), _BODY.css("cursor", ""), n = {}, a.scrollPatch(l)
                }, 30), 2 === i && (i = null)
            }))
        }, fixFixedScroll: function (e) {
            var t = $(e.elem), i = t.next().children(".layui-table-box").children(".layui-table-fixed"),
                l = t.next().children(".layui-table-box").children(".layui-table-main");
            i.on("mouseenter", function () {
                $(this).children(".layui-table-body").addClass("soul-fixed-scroll").on("scroll", function () {
                    var e = $(this).scrollTop();
                    l.scrollTop(e)
                })
            }).on("mouseleave", function () {
                $(this).children(".layui-table-body").removeClass("soul-fixed-scroll").off("scroll")
            })
        }, scrollPatch: function (e) {
            function t(e) {
                if (s && c) {
                    if (!(e = e.eq(0)).find(".layui-table-patch")[0]) {
                        var t = $('<th class="layui-table-patch"><div class="layui-table-cell"></div></th>');
                        t.find("div").css({width: s}), e.find("tr").append(t)
                    }
                } else e.find(".layui-table-patch").remove()
            }

            var i = $(e.elem), l = i.next().children(".layui-table-box").children(".layui-table-header"),
                a = i.next().children(".layui-table-total"),
                n = i.next().children(".layui-table-box").children(".layui-table-main"),
                o = i.next().children(".layui-table-box").children(".layui-table-fixed"),
                r = i.next().children(".layui-table-box").children(".layui-table-fixed-r"), d = n.children("table"),
                s = n.width() - n.prop("clientWidth"), c = n.height() - n.prop("clientHeight"),
                h = d.outerWidth() - n.width();
            t(l), t(a);
            var f = n.height() - c;
            o.find(".layui-table-body").css("height", d.height() >= f ? f : "auto"), r[0 < h ? "removeClass" : "addClass"](HIDE), r.css("right", s - 1)
        }, copy: function (e) {
            var t;
            e ? ((t = document.createElement("div")).id = "tempTarget", t.style.opacity = "0", t.innerText = e, document.body.appendChild(t)) : t = document.querySelector("#" + id);
            try {
                var i = document.createRange();
                i.selectNode(t), window.getSelection().removeAllRanges(), window.getSelection().addRange(i), document.execCommand("copy"), window.getSelection().removeAllRanges()
            } catch (e) {
                console.log("复制失败")
            }
            e && t.parentElement.removeChild(t)
        }, addCSSRule: function (e, t, i, l) {
            "insertRule" in e ? e.insertRule(t + "{" + i + "}", l) : "addRule" in e && e.addRule(t, i, l)
        }, deepStringify: function (e) {
            var i = "[[JSON_FUN_PREFIX_", l = "_JSON_FUN_SUFFIX]]";
            return JSON.stringify(e, function (e, t) {
                return "function" == typeof t ? i + t.toString() + l : t
            })
        }, deepParse: function (str) {
            var JSON_SERIALIZE_FIX = {PREFIX: "[[JSON_FUN_PREFIX_", SUFFIX: "_JSON_FUN_SUFFIX]]"};
            return JSON.parse(str, function (key, value) {
                return "string" == typeof value && 0 < value.indexOf(JSON_SERIALIZE_FIX.SUFFIX) && 0 === value.indexOf(JSON_SERIALIZE_FIX.PREFIX) ? eval("(" + value.replace(JSON_SERIALIZE_FIX.PREFIX, "").replace(JSON_SERIALIZE_FIX.SUFFIX, "") + ")") : value
            }) || {}
        }, deepClone: function (e) {
            var t = Array.isArray(e) ? [] : {};
            if (e && "object" == typeof e) for (var i in e) e.hasOwnProperty(i) && (t[i] = e && "object" == typeof e[i] ? this.deepClone(e[i]) : e[i]);
            return t
        }, clearOriginCols: function (e) {
            e ? delete originCols[e] : originCols = {}
        }, suspendConfig: {}, suspend: function (e, t, i) {
            this.suspendConfig[e][t] = i
        }
    };
    exports("soulTable", mod)
});