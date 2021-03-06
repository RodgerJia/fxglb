/**
 *
 * @name:  表格筛选扩展
 * @author: yelog
 * @link: https://github.com/yelog/layui-soul-table
 * @license: MIT
 * @version: v1.5.21
 */
layui.define(["table", "form", "laydate", "util", "excel", "laytpl"], function (e) {
    var J, A, H, l, a, V = layui.jquery, $ = layui.table, _ = layui.form, p = layui.laydate, K = layui.laytpl,
        y = layui.util, Q = layui.excel, z = {}, U = "SOUL_ROW_INDEX", Z = {}, E = "layui-hide", i = 1,
        ee = [void 0, "", null], ie = {}, te = {}, le = {}, Y = {
            eq: "等于",
            ne: "≠ 不等于",
            gt: "> 大于",
            ge: "≥ 大于等于",
            lt: "< 小于",
            le: "≤ 小于等于",
            contain: "包含",
            notContain: "不包含",
            start: "以...开头",
            end: "以...结尾",
            null: "为空",
            notNull: "不为空"
        }, b = {all: "全部", yesterday: "昨天", thisWeek: "本周", lastWeek: "上周", thisMonth: "本月", thisYear: "今年"},
        M = ["column", "data", "condition", "editCondition", "excel"], m = {
            column: "soul-column",
            data: "soul-dropList",
            condition: "soul-condition",
            editCondition: "soul-edit-condition",
            excel: "soul-export",
            clearCache: "soul-clear-cache"
        }, h = {in: "data", condition: "condition", date: "condition"},
        v = {data: {mode: "condition", type: "eq", value: ""}, condition: {mode: "in", values: []}};
    e("tableFilter", {
        destroy: function (e) {
            if (e) if (Array.isArray(e)) for (var i = 0; i < e.length; i++) t(e[i]); else t(e);

            function t(e) {
                if (e) {
                    var i = e.config.id;
                    V("#soul-filter-list" + i).remove(), V("#soulCondition" + i).remove(), V("#soulDropList" + i).remove(), delete z[i], delete ie[i], delete le[i]
                }
            }
        }, clearFilter: function (e) {
            "string" == typeof e && (e = le[e]), ie[e.id] && ie[e.id].filterSos && "[]" !== ie[e.id].filterSos && (ie[e.id].filterSos = "[]", this.soulReload(e, !0), le[e.id].where && le[e.id].where.filterSos && "[]" !== le[e.id].where.filterSos && (le[e.id].where.filterSos = "[]"))
        }, render: function (g) {
            var x, u, k = this, t = V(g.elem), e = t.next().children(".layui-table-box").children(".layui-table-main"),
                i = t.next().children(".layui-table-box").children(".layui-table-header").children("table"),
                l = t.next().children(".layui-table-box").children(".layui-table-fixed-l").children(".layui-table-header").children("table"),
                a = t.next().children(".layui-table-box").children(".layui-table-fixed-r").children(".layui-table-header").children("table"),
                C = g.id, w = k.getCompleteCols(g.cols), o = g.filter && g.filter.items || M, d = !1, n = !1,
                s = void 0 === g.excel || !(!g.excel || void 0 !== g.excel.on && !g.excel.on) && g.excel;
            for (x = 0; x < w.length; x++) w[x].field && w[x].filter && (d = !0, 0 === i.find('th[data-field="' + w[x].field + '"]').children().children(".soul-table-filter").length && (n = !0, 0 < i.find('th[data-field="' + w[x].field + '"]').children().children(".layui-table-sort").length ? (i.find('th[data-field="' + w[x].field + '"]').children().children(".layui-table-sort").hide(), i.find('th[data-field="' + w[x].field + '"]').children().append('<span class="layui-table-sort soul-table-filter layui-inline" data-items="' + (w[x].filter.items ? w[x].filter.items.join(",") : "") + '" data-column="' + w[x].field + '" lay-sort="' + i.find('th[data-field="' + w[x].field + '"]').children().children(".layui-table-sort").attr("lay-sort") + '" ' + (void 0 === w[x].filter.split ? "" : 'data-split="' + w[x].filter.split + '"') + '><i class="soul-icon soul-icon-filter"></i><i class="soul-icon soul-icon-filter-asc"></i><i class="soul-icon soul-icon-filter-desc"></i></span>')) : i.find('th[data-field="' + w[x].field + '"]').children().append('<span class="soul-table-filter layui-inline" data-items="' + (w[x].filter.items ? w[x].filter.items.join(",") : "") + '" data-column="' + w[x].field + '" ' + (void 0 === w[x].filter.split ? "" : 'data-split="' + w[x].filter.split + '"') + '><i class="soul-icon soul-icon-filter"></i><i class="soul-icon soul-icon-filter-asc"></i><i class="soul-icon soul-icon-filter-desc"></i></span>'), 0 < l.find('th[data-field="' + w[x].field + '"]').children().children(".layui-table-sort").length ? (l.find('th[data-field="' + w[x].field + '"]').children().children(".layui-table-sort").hide(), l.find('th[data-field="' + w[x].field + '"]').children().append('<span class="layui-table-sort soul-table-filter layui-inline" data-items="' + (w[x].filter.items ? w[x].filter.items.join(",") : "") + '" data-column="' + w[x].field + '" lay-sort="' + l.find('th[data-field="' + w[x].field + '"]').children().children(".layui-table-sort").attr("lay-sort") + '" ' + (void 0 === w[x].filter.split ? "" : 'data-split="' + w[x].filter.split + '"') + '><i class="soul-icon soul-icon-filter"></i><i class="soul-icon soul-icon-filter-asc"></i><i class="soul-icon soul-icon-filter-desc"></i></span>')) : l.find('th[data-field="' + w[x].field + '"]').children().append('<span class="soul-table-filter layui-inline" data-items="' + (w[x].filter.items ? w[x].filter.items.join(",") : "") + '" data-column="' + w[x].field + '" ' + (void 0 === w[x].filter.split ? "" : 'data-split="' + w[x].filter.split + '"') + '><i class="soul-icon soul-icon-filter"></i><i class="soul-icon soul-icon-filter-asc"></i><i class="soul-icon soul-icon-filter-desc"></i></span>'), 0 < a.find('th[data-field="' + w[x].field + '"]').children().children(".layui-table-sort").length ? (a.find('th[data-field="' + w[x].field + '"]').children().children(".layui-table-sort").hide(), a.find('th[data-field="' + w[x].field + '"]').children().append('<span class="layui-table-sort soul-table-filter layui-inline" data-items="' + (w[x].filter.items ? w[x].filter.items.join(",") : "") + '" data-column="' + w[x].field + '" lay-sort="' + a.find('th[data-field="' + w[x].field + '"]').children().children(".layui-table-sort").attr("lay-sort") + '" ' + (void 0 === w[x].filter.split ? "" : 'data-split="' + w[x].filter.split + '"') + '><i class="soul-icon soul-icon-filter"></i><i class="soul-icon soul-icon-filter-asc"></i><i class="soul-icon soul-icon-filter-desc"></i></span>')) : a.find('th[data-field="' + w[x].field + '"]').children().append('<span class="soul-table-filter layui-inline" data-items="' + (w[x].filter.items ? w[x].filter.items.join(",") : "") + '" data-column="' + w[x].field + '" ' + (void 0 === w[x].filter.split ? "" : 'data-split="' + w[x].filter.split + '"') + '><i class="soul-icon soul-icon-filter"></i><i class="soul-icon soul-icon-filter-asc"></i><i class="soul-icon soul-icon-filter-desc"></i></span>')));
            if (le[g.id] = g, te[g.id] = d) {
                if ((!g.filter || void 0 === g.filter.bottom || g.filter.bottom) && 0 === t.next().children(".soul-bottom-contion").length) {
                    t.next().children(".layui-table-box").after('<div class="soul-bottom-contion"><div class="condition-items"></div><div class="editCondtion"><a class="layui-btn layui-btn-primary">编辑筛选条件</a></div></div>');
                    var r = t.next().children(".layui-table-box").children(".layui-table-body").outerHeight() - t.next().children(".soul-bottom-contion").outerHeight();
                    g.page && t.next().children(".layui-table-page").hasClass("layui-hide") && (r += t.next().children(".layui-table-page").outerHeight()), t.next().children(".layui-table-box").children(".layui-table-body").css("height", r);
                    var c = r - k.getScrollWidth(e[0]), h = e.children("table").height();
                    t.next().children(".layui-table-box").children(".layui-table-fixed").children(".layui-table-body").css("height", c <= h ? c : "auto"), t.next().children(".soul-bottom-contion").children(".condition-items").css("width", t.next().children(".soul-bottom-contion").width() - t.next().children(".soul-bottom-contion").children(".editCondtion").width() + "px"), t.next().children(".soul-bottom-contion").children(".editCondtion").children("a").on("click", function () {
                        k.showConditionBoard(g)
                    })
                }
                if (!n || z[g.id] || g.isSoulFrontFilter) return z[g.id] = !1, g.isSoulFrontFilter = !1, !g.url && g.page && g.data && g.data.forEach(function (e) {
                    Z[g.id][e[U]] = e
                }), void this.bindFilterClick(g);
                if (!g.url && g.page && g.data && g.data.length > g.limit && layui.each(g.data, function (e, i) {
                    i[g.indexName] = e
                }), g.url && !g.page ? Z[g.id] = layui.table.cache[g.id] : Z[g.id] = g.data || layui.table.cache[g.id], Z[g.id].forEach(function (e, i) {
                    e[U] = i
                }), g.filter && g.filter.clearFilter) {
                    if (g.where && g.where.filterSos && 0 < JSON.parse(g.where.filterSos).length) return g.where.filterSos = "[]", ie[g.id] = g.where || {}, void k.soulReload(g, !1);
                    ie[g.id] = g.where || {}
                } else {
                    if ((void 0 === g.url || !g.page || void 0 === g.where.filterSos) && ie[g.id] && 0 < JSON.parse(ie[g.id].filterSos || "[]").length) return g.where.filterSos = ie[g.id].filterSos, ie[g.id] = g.where, void k.soulReload(g, !1);
                    ie[g.id] = g.where || {}
                }
                if (0 === V("#soul-filter-list" + C).length) {
                    void 0 !== g.soulSort && !g.soulSort || (void 0 === t.attr("lay-filter") && t.attr("lay-filter", C), $.on("sort(" + t.attr("lay-filter") + ")", function (e) {
                        g.limit = le[g.id].limit, g.url && g.page ? (ie[g.id].field = e.field, ie[g.id].order = e.type, z[g.id] = !0, $.render(V.extend(g, {
                            initSort: e,
                            where: ie[g.id],
                            page: {curr: 1}
                        }))) : !g.url && g.page && ("asc" === e.type ? Z[g.id] = layui.sort(Z[g.id], e.field) : "desc" === e.type ? Z[g.id] = layui.sort(Z[g.id], e.field, !0) : Z[g.id] = layui.sort(Z[g.id], g.indexName), g.initSort = e, g.page = {curr: 1}, k.soulReload(g, !1))
                    }));
                    var f = [], p = {
                        column: '<li class="soul-column"><i class="layui-icon layui-icon-table"></i> 表格列 <i class="layui-icon layui-icon-right" style="float: right"></i></li>',
                        data: '<li class="soul-dropList"><i class="soul-icon soul-icon-drop-list"></i> 筛选数据 <i class="layui-icon layui-icon-right" style="float: right"></i></li>',
                        condition: '<li class="soul-condition"><i class="soul-icon soul-icon-query"></i> 筛选条件 <i class="layui-icon layui-icon-right" style="float: right"></i></li>',
                        editCondition: '<li class="soul-edit-condition"><i class="layui-icon layui-icon-edit"></i> 编辑筛选条件 </li>',
                        excel: '<li class="soul-export"><i class="soul-icon soul-icon-download"></i> 导出excel </li>',
                        clearCache: '<li class="soul-clear-cache"><i class="layui-icon layui-icon-delete"></i> 清除缓存 </li>'
                    };
                    for (f.push('<div id="soul-filter-list' + C + '"><form action="" class="layui-form" lay-filter="orm"><ul id="main-list' + C + '" style="display: none">'), f.push('<li class="soul-sort" data-value="asc" ><i class="soul-icon soul-icon-asc"></i> 升序排列 </li>'), f.push('<li class="soul-sort" data-value="desc"  style="border-bottom: 1px solid #e6e6e6"><i class="soul-icon soul-icon-desc"></i> 降序排列 </li>'), x = 0; x < M.length; x++) "excel" === M[x] && !s || f.push(p[M[x]]);
                    f.push('</ul><ul id="soul-columns' + C + '" style="display: none;">');
                    var y = {};
                    for (x = 0; x < w.length; x++) "checkbox" !== w[x].type && w[x].field ? (f.push('<li data-value="' + w[x].field + '" data-key="' + x + '"><input type="checkbox" value="' + g.index + "-" + w[x].key + '" title="' + w[x].title + '" data-fixed="' + (w[x].fixed || "") + '" lay-skin="primary" lay-filter="changeColumns' + C + '" ' + (w[x].hide ? "" : "checked") + "></li>"), w[x].filter && w[x].filter.type && (w[x].filter.field ? y[w[x].filter.field] = w[x].filter.type : y[w[x].field] = w[x].filter.type)) : f.push('<li class="layui-hide"><input type="checkbox" title="' + w[x].title + '" /></li>');
                    2 !== JSON.stringify(y).length && (g.where.tableFilterType = JSON.stringify(y)), f.push('</ul><div id="soul-dropList' + C + '" style="display: none"><div class="filter-search"><input type="text" placeholder="关键字搜索" class="layui-input"></div><div class="check"><div class="multiOption" data-type="all"><i class="soul-icon">&#xe623;</i> 全选</div><div class="multiOption" data-type="none"><i class="soul-icon">&#xe63e;</i> 清空</div><div class="multiOption" data-type="reverse"><i class="soul-icon">&#xe614;</i>反选</div></div><ul></ul></div>'), f.push('<ul id="soul-condition' + C + '" style="display: none;"></ul></form></div>'), V("body").append(f.join(""));
                    var m = !0;
                    _.on("checkbox(changeColumns" + C + ")", function (e) {
                        m = !1;
                        var i = e.value;
                        for (e.elem.checked ? t.next().find("[data-key=" + i + "]").removeClass(E) : t.next().find("[data-key=" + i + "]").addClass(E), x = 0; x < g.cols.length; x++) for (u = 0; u < g.cols[x].length; u++) g.index + "-" + g.cols[x][u].key === i && (g.cols[x][u].hide = !e.elem.checked);
                        layui.soulTable && layui.soulTable.fixTableRemember(g), t.next().children(".layui-table-box").children(".layui-table-body").children("table").children("tbody").children("tr.childTr").children("td").attr("colspan", t.next().children(".layui-table-box").children(".layui-table-header").find("thead>tr>th:visible").length), $.resize(C)
                    }), V("#soul-columns" + C + ">li[data-value]").on("click", function () {
                        V(this).find(":checkbox").is(":disabled") || (m && V(this).find("div.layui-form-checkbox").trigger("click"), m = !0)
                    }), V("#soul-dropList" + C + " .check [data-type]").on("click", function () {
                        switch (V(this).data("type")) {
                            case"all":
                                V(this).parents("#soul-dropList" + C).find("input[type=checkbox]:not(:checked)").prop("checked", !0);
                                break;
                            case"reverse":
                                V(this).parents("#soul-dropList" + C).find("input[type=checkbox]").each(function () {
                                    V(this).prop("checked", !V(this).prop("checked"))
                                });
                                break;
                            case"none":
                                V(this).parents("#soul-dropList" + C).find("input[type=checkbox]:checked").prop("checked", !1)
                        }
                        return _.render("checkbox", "orm"), k.updateDropList(g, V("#main-list" + C).data("field")), !1
                    }), V("#soul-dropList" + C + " .filter-search input").on("input", function () {
                        var e = V(this).val();
                        "" === e ? V("#soul-dropList" + C + ">ul>li").show() : (V("#soul-dropList" + C + ">ul>li").hide(), V("#soul-dropList" + C + '>ul>li[data-value*="' + e.toLowerCase() + '"]').show())
                    }), V("#main-list" + C + " .soul-column").on("mouseover", function (e) {
                        for (k.hideDropList(g), k.hideCondition(g), e.stopPropagation(), J && clearTimeout(J), w = k.getCompleteCols(g.cols), x = 0; x < w.length; x++) V("#soul-columns" + C).find('li[data-value="' + w[x].field + '"]>input').prop("checked", !w[x].hide);
                        var i, t;
                        _.render("checkbox", "orm"), V("#soul-columns" + C).show(), t = V(this).parent().offset().left + V(this).parent().width() + V("#soul-columns" + C).width() < document.body.clientWidth ? (i = V(this).parent().offset().left + V(this).parent().width(), "fadeInLeft") : (i = V(this).parent().offset().left - V("#soul-columns" + C).width(), "fadeInRight"), V("#soul-columns" + C).css({
                            top: V(this).offset().top,
                            left: i
                        }).removeClass().addClass(t + " animated")
                    }), V("#main-list" + C + " .soul-dropList").on("mouseover", function (e) {
                        if (V("#soul-dropList" + C).is(":visible") && !V("#soul-dropList" + C).hasClass("fadeOutLeft")) return !1;
                        k.hideColumns(g), k.hideCondition(g), e.stopPropagation(), A && clearTimeout(A), V("#soul-dropList" + C + ">.filter-search>input").val(""), V("#soul-dropList" + C).show();
                        var i, t, l = V("#main-list" + C).data("field");
                        t = V("#main-list" + C).offset().left + V("#soul-dropList" + C).width() + V("#soul-dropList" + C).width() < document.body.clientWidth ? (i = V("#main-list" + C).offset().left + V("#main-list" + C).width(), "fadeInLeft") : (i = V("#main-list" + C).offset().left - V("#soul-dropList" + C).width(), "fadeInRight"), V("#soulDropList" + C).find("." + l + "DropList li input[type=checkbox]:checked").prop("checked", !1);
                        var a = ie[g.id] || {}, o = JSON.parse(a.filterSos ? a.filterSos : null), d = "", n = "";
                        if (o) for (x = 0; x < o.length; x++) if (o[x].head && "in" === o[x].mode && o[x].field === l) {
                            for (d = o[x].id, n = o[x].prefix, u = 0; u < o[x].values.length; u++) V("#soulDropList" + C).find("." + l + 'DropList li input[type=checkbox][value="' + o[x].values[u] + '"]').prop("checked", !0);
                            break
                        }
                        V("#soul-dropList" + C + ">ul").data({
                            head: !0,
                            id: d,
                            prefix: n,
                            refresh: !0,
                            split: V("#main-list" + C).data("split")
                        }).html(V("#soulDropList" + C).find("." + l + "DropList li").clone()), V("#soul-dropList" + C).css({
                            top: V(this).offset().top,
                            left: i
                        }).show().removeClass().addClass(t + " animated"), setTimeout(function () {
                            V("#soul-dropList" + C + ">.filter-search>input").focus(), _.render("checkbox", "orm")
                        }, 1);
                        var s = !0;
                        _.on("checkbox(soulDropList" + C + ")", function (e) {
                            s = !1, k.updateDropList(g, l)
                        }), V("#soul-dropList" + C + ">ul>li[data-value]").on("click", function () {
                            s && V(this).find("div.layui-form-checkbox").trigger("click"), s = !0
                        })
                    }), V("#main-list" + C + " .soul-condition").on("mouseover", function (e) {
                        if (V("#soul-condition" + C).is(":visible") && !V("#soul-condition" + C).hasClass("fadeOutLeft")) return !1;
                        k.hideColumns(g), k.hideDropList(g), e.stopPropagation(), H && clearTimeout(H);
                        var i = document.body.clientWidth;
                        V("#soul-condition" + C).show();
                        var t, l, n = V(this).parent().data("field");
                        l = V(this).parent().offset().left + V(this).parent().width() + V("#soul-condition" + C).width() < i ? (t = V(this).parent().offset().left + V(this).parent().width(), "fadeInLeft") : (t = V(this).parent().offset().left - V("#soul-condition" + C).width(), "fadeInRight");
                        var s, a = [], o = ie[g.id] || {}, d = JSON.parse(o.filterSos ? o.filterSos : null);
                        if (d) for (x = 0; x < d.length; x++) if (d[x].head && d[x].field === n && ("date" === d[x].mode || "group" === d[x].mode)) {
                            s = d[x];
                            break
                        }
                        var r = V(this).parent().data("type");
                        if (k.startsWith(r, "date")) k.showDate(g, n, s, l, V(this).offset().top, V(this).parent().offset().left + V(this).parent().width(), "down", !0); else {
                            var u = {};
                            for (x = 0; x < w.length; x++) w[x].field && (u[w[x].field] = w[x]);
                            var c = "<select lay-filter='conditionChange'>";
                            for (var h in Y) c += '<option value="' + h + '">' + Y[h] + "</option>";
                            if (c += "</select>", a.push('<table class="condition-table"><tbody>'), s && s.children && 0 < s.children.length) for (x = 0; x < s.children.length; x++) {
                                var f = s.children[x].id, p = s.children[x].prefix, y = s.children[x].type,
                                    m = s.children[x].value;
                                for (var h in a.push('<tr data-id="' + f + '">'), 0 === x ? a.push('<td class="soul-condition-title">' + u[n].title + "</td>") : a.push('<td>   <div>      <input type="checkbox" name="switch" lay-filter="soul-coondition-switch" lay-skin="switch" lay-text="与|或" ' + (p && "and" !== p ? "" : "checked") + ">    </div></td>"), a.push('<td style="width: 110px;"><div class="layui-block" ><select lay-filter="conditionChange">'), Y) a.push('<option value="' + h + '" ' + (h === y ? "selected" : "") + ">" + Y[h] + "</option>");
                                a.push("</select></div></td>"), a.push('<td style="width: 110px;"><div class="layui-block" ><input class="layui-input value" value="' + (m || "") + '" placeholder="值" /></div></td>'), a.push('<td><i class="layui-icon layui-icon-delete del" style="font-size: 23px; color: #FF5722; cursor: pointer"></i></td>'), a.push("</tr>")
                            } else a.push('<tr data-id="" data-type="eq" data-value=""><td class="soul-condition-title">' + u[n].title + '</td><td style="width: 110px;"><div class="layui-block" >' + c + '</div></td><td style="width: 110px;"><div class="layui-block" ><input class="layui-input value" placeholder="值" /></div></td><td><i class="layui-icon layui-icon-delete del" style="font-size: 23px; color: #FF5722; cursor: pointer"></i></td></tr>');

                            function v(e) {
                                var i = e.data("id"), t = V("#soul-condition" + C).data("id"),
                                    l = e.find('input[lay-filter="soul-coondition-switch"]:checked').prop("checked") ? "and" : "or",
                                    a = e.find("select").val(), o = e.find(".value").val(),
                                    d = V("#soul-condition" + C).data("head");
                                s = t ? {
                                    id: i,
                                    prefix: l,
                                    mode: "condition",
                                    field: n,
                                    type: a,
                                    value: o,
                                    groupId: t
                                } : {
                                    head: d,
                                    prefix: "and",
                                    mode: "group",
                                    field: n,
                                    children: [{
                                        id: k.getDifId(),
                                        prefix: l,
                                        mode: "condition",
                                        field: n,
                                        type: a,
                                        value: o,
                                        groupId: t
                                    }]
                                }, k.updateWhere(g, s), t ? i || e.data("id", s.id) : (V("#soul-condition" + C).data("id", s.id), e.data("id", s.children[0].id))
                            }

                            function b(e) {
                                var i;
                                1 === V(e).parents("table:eq(0)").find("tr").length ? (i = V("#soul-condition" + C).data("id"), V("#soul-condition" + C).data("id", ""), V(e).parents("tr:eq(0)").find("select").val("eq"), V(e).parents("tr:eq(0)").find(".value").val("").show(), _.render("select", "orm")) : (i = V(e).parents("tr:eq(0)").data("id"), 0 === V(e).parents("tr:eq(0)").index() && V(e).parents("table:eq(0)").find("tr:eq(1)>td:eq(0)").html(u[n].title).addClass("soul-condition-title"), V(e).parents("tr:eq(0)").remove()), i && k.updateWhere(g, {
                                    id: i,
                                    delete: !0
                                })
                            }

                            a.push('</tbody></table><div style="text-align: center; padding-top: 5px"><button class="layui-btn layui-btn-sm" data-type="add"><i class="layui-icon">&#xe654;</i>添加</button><span style="display: inline-block;width: 50px"></span><button class="layui-btn layui-btn-sm" data-type="search"><i class="layui-icon">&#xe615;</i>查询</button></div>'), V("#soul-condition" + C).data({
                                head: !0,
                                id: s && s.id || ""
                            }).html(a.join("")).css({
                                top: V(this).offset().top,
                                left: t
                            }).show().removeClass().addClass(l + " animated"), V(".condition-table").on("click", function () {
                                return !1
                            }), V("#soul-condition" + C + " button[data-type]").on("click", function () {
                                if ("add" === V(this).data("type")) {
                                    var e, i = V("#soul-condition" + C).data("id"),
                                        t = V("#soul-condition" + C).data("head"),
                                        l = V("#soul-condition" + C).find("tr:eq(0)");
                                    e = i ? {
                                        head: t,
                                        prefix: "and",
                                        field: n,
                                        mode: "condition",
                                        type: "eq",
                                        value: "",
                                        groupId: i
                                    } : {
                                        head: t,
                                        prefix: "and",
                                        mode: "group",
                                        field: n,
                                        children: [{
                                            id: k.getDifId(),
                                            prefix: "and",
                                            field: n,
                                            mode: "condition",
                                            type: l.find("select").val(),
                                            value: l.find(".value").val()
                                        }, {
                                            id: k.getDifId(),
                                            prefix: "and",
                                            field: n,
                                            mode: "condition",
                                            type: "eq",
                                            value: ""
                                        }]
                                    }, k.updateWhere(g, e), i || (V("#soul-condition" + C).data("id", e.id), l.data("id", e.children[0].id));
                                    var a = '<tr data-id="' + (i ? e.id : e.children[1].id) + '"><td>   <div>      <input type="checkbox" name="switch" lay-filter="soul-coondition-switch" lay-skin="switch" lay-text="与|或" checked>   </div></td><td style="width: 110px;"><div class="layui-block">' + c + '</div></td><td style="width: 110px;"><div class="layui-block"><input class="layui-input value" placeholder="值" /></div></td><td><i class="layui-icon layui-icon-delete del" style="font-size: 23px; color: #FF5722; cursor: pointer"></i></td></tr>';
                                    V("#soul-condition" + C + ">table>tbody").append(a), V("#soul-condition" + C).find(".del:last").on("click", function () {
                                        b(this)
                                    }), V("#soul-condition" + C + " input.value:last").on("input", function () {
                                        v(V(this).parents("tr:eq(0)"))
                                    })
                                } else "search" === V(this).data("type") && k.soulReload(g);
                                return _.render("select", "orm"), _.render("checkbox", "orm"), !1
                            }), V("#soul-condition" + C + " input.value").on("input", function () {
                                v(V(this).parents("tr:eq(0)"))
                            }), _.on("select(conditionChange)", function (e) {
                                "null" === e.value || "notNull" === e.value ? V(this).parents("tr").find("input.value").hide() : V(this).parents("tr").find("input.value").show(), v(V(e.elem).parents("tr:eq(0)"))
                            }), _.on("switch(soul-coondition-switch)", function (e) {
                                v(V(this).parents("tr:eq(0)"))
                            }), V("#soul-condition" + C + " .del").on("click", function () {
                                b(this)
                            })
                        }
                        _.render("select", "orm"), _.render("checkbox", "orm")
                    }), V("#soul-columns" + C + ", #soul-dropList" + C).on("mouseover", function (e) {
                        e.stopPropagation()
                    }), V("#main-list" + C + " .soul-edit-condition").on("mouseover", function (e) {
                        k.hideColumns(g), k.hideDropList(g), k.hideCondition(g), e.stopPropagation()
                    }).on("click", function () {
                        V("#main-list" + C).hide(), k.showConditionBoard(g)
                    }), V("#main-list" + C + " .soul-export").on("mouseover", function (e) {
                        k.hideColumns(g), k.hideDropList(g), k.hideCondition(g), e.stopPropagation()
                    }).on("click", function () {
                        V("#main-list" + C).hide(), k.export(le[g.id])
                    }), V("#main-list" + C + " .soul-clear-cache").on("mouseover", function (e) {
                        k.hideColumns(g), k.hideDropList(g), k.hideCondition(g), e.stopPropagation()
                    }).on("click", function () {
                        V("#main-list" + C).hide(), layui.soulTable && layui.soulTable.clearCache(g), layer.msg("已还原！", {
                            icon: 1,
                            time: 1e3
                        })
                    }), V("#main-list" + C).on("mouseover", function (e) {
                        var i = e.pageX, t = e.pageY, l = V(this), a = l.offset().top, o = a + l.height(),
                            d = l.offset().left, n = d + l.width();
                        i <= d || n <= i || t <= a || o <= t || (k.hideColumns(g), k.hideDropList(g), k.hideCondition(g))
                    })
                } else {
                    for (y = {}, x = 0; x < w.length; x++) "checkbox" !== w[x].type && w[x].field && w[x].filter && w[x].filter.type && (w[x].filter.field ? y[w[x].filter.field] = w[x].filter.type : y[w[x].field] = w[x].filter.type);
                    2 !== JSON.stringify(y).length && (g.where.tableFilterType = JSON.stringify(y))
                }
                if (0 === V("#soulDropList" + C).length && V("body").append('<div id="soulDropList' + C + '" style="display: none"></div>'), 0 < i.find(".soul-table-filter").length) {
                    var v = [], b = -1 !== o.indexOf("data");
                    if (i.find(".soul-table-filter").each(function (e, i) {
                        V(this).data("column") && (b && !V(this).data("items") || -1 !== V(this).data("items").split(",").indexOf("data")) && v.push(V(this).data("column"))
                    }), 0 < v.length) if (void 0 !== g.url && g.page) {
                        var L = JSON.parse(JSON.stringify(g.where)), S = g.url;
                        L.columns = JSON.stringify(v), V.ajax({
                            url: S,
                            data: L,
                            dataType: "json",
                            method: "post",
                            headers: g.headers || {},
                            contentType: g.contentType,
                            success: function (e) {
                                var i = [];
                                for (var t in e) {
                                    var l = e[t];
                                    if (1 === l.length && "" === l[0] || 0 === l.length) i.push("<ul class='" + t + "DropList' data-value='" + t + "'><li style='color: gray;line-height: 25px;padding-left: 20px;'>(无数据)</li></ul>"); else {
                                        var a = [];
                                        a.push("<ul class='" + t + "DropList' data-value='" + t + "'>");
                                        var o = w;
                                        for (u = 0; u < o.length; u++) if (o[u].field === t) {
                                            if (o[u].filter.split) {
                                                var d = [];
                                                for (x = 0; x < l.length; x++) for (var n = l[x].split(o[u].filter.split), s = 0; s < n.length; s++) -1 === d.indexOf(n[s]) && d.push(n[s]);
                                                l = d
                                            }
                                            for (l.sort(function (e, i) {
                                                return isNaN(e) || isNaN(i) ? String(e) >= String(i) : Number(e) - Number(i)
                                            }), x = 0; x < l.length; x++) if (-1 === ee.indexOf(l[x])) {
                                                var r = {};
                                                r[t] = l[x], a.push('<li data-value="' + String(l[x]).toLowerCase() + '"><input type="checkbox" value="' + l[x] + '" title="' + k.parseTempData(o[u], l[x], r, !0).replace(/\"|\'/g, "'") + '" lay-skin="primary" lay-filter="soulDropList' + C + '"></li>')
                                            }
                                            break
                                        }
                                        a.push("</ul>"), i.push(a.join(""))
                                    }
                                }
                                V("#soulDropList" + C).html(i.join(""))
                            },
                            error: function () {
                            }
                        })
                    } else {
                        var D = Z[g.id], N = {};
                        for (x = 0; x < D.length; x++) for (u = 0; u < v.length; u++) {
                            var O = void 0 === D[x][v[u]] ? "" : D[x][v[u]];
                            N[v[u]] ? -1 === N[v[u]].indexOf(O) && N[v[u]].push(O) : N[v[u]] = [O]
                        }
                        var T = w, F = [];
                        for (u = 0; u < T.length; u++) {
                            var I = T[u].field, W = N[I];
                            if (!W || 1 === W.length && "" === W[0]) F.push("<ul class='" + I + "DropList' data-value='" + I + "'><li style='color: gray;line-height: 25px;padding-left: 20px;'>(无数据)</li></ul>"); else {
                                if (T[u].filter && T[u].filter.split) {
                                    var P = [];
                                    for (x = 0; x < W.length; x++) for (var R = String(W[x]).split(T[u].filter.split), B = 0; B < R.length; B++) -1 === P.indexOf(R[B]) && P.push(R[B]);
                                    W = P
                                }
                                W.sort(function (e, i) {
                                    return isNaN(e) || isNaN(i) ? String(e) >= String(i) : Number(e) - Number(i)
                                });
                                var q = [];
                                for (q.push("<ul class='" + I + "DropList' data-value='" + I + "'>"), x = 0; x < W.length; x++) if (-1 === ee.indexOf(W[x])) {
                                    var j = {};
                                    j[I] = W[x], q.push('<li data-value="' + String(W[x]).toLowerCase() + '"><input type="checkbox" value="' + W[x] + '" title="' + k.parseTempData(T[u], W[x], j, !0).replace(/\"|\'/g, "'") + '" lay-skin="primary" lay-filter="soulDropList' + C + '"></li>')
                                }
                                q.push("</ul>"), F.push(q.join(""))
                            }
                        }
                        V("#soulDropList" + C).html(F.join(""))
                    } else k.bindFilterClick(g)
                }
                this.bindFilterClick(g)
            } else g.url && !g.page ? Z[g.id] = layui.table.cache[g.id] : Z[g.id] = g.data || layui.table.cache[g.id]
        }, showConditionBoard: function (p) {
            var a, e, y, m = this, v = p.id, i = ie[p.id] || {},
                o = i.tableFilterType ? JSON.parse(i.tableFilterType) : {},
                t = i.filterSos ? JSON.parse(i.filterSos) : [], d = [], n = {}, l = p.filter && p.filter.items || M,
                s = m.getCompleteCols(p.cols);
            for (y = 0; y < s.length; y++) s[y].field && s[y].filter && (a = a || s[y], e = s[y].filter.items || l, n[s[y].field] = {
                title: s[y].title,
                items: e
            });
            for (d.push('<div class="soul-edit-out">'), d.push('<div class="layui-form" lay-filter="soul-edit-out">'), d.push('<div><a class="layui-btn layui-btn-sm" data-type="addOne"><i class="layui-icon layui-icon-add-1"></i> 添加条件</a><a class="layui-btn layui-btn-sm" data-type="addGroup"><i class="layui-icon layui-icon-add-circle" ></i> 添加分组</a><a class="layui-btn layui-btn-sm" data-type="search" style="float: right"><i class="layui-icon layui-icon-search"></i> 查询</a><span style="float: right"><input type="checkbox" lay-filter="out_auto" class="out_auto" title="实时更新"></span></div>'), d.push("<hr>"), d.push("<ul>"), y = 0; y < t.length; y++) c(t[y], d, n, 0, y === t.length - 1);

            function c(e, i, t, l, a) {
                var o = e.id, d = e.field, n = e.mode, s = e.type, r = "or" === e.prefix;
                switch (i.push('<li data-id="' + o + '" data-field="' + d + '" ' + (a ? 'class="last"' : "") + ' data-mode="' + n + '" data-type="' + s + '" data-value="' + (void 0 === e.value ? "" : e.value) + '" >'), i.push('<div><table><tbody><tr><td data-type="top"></td></tr><tr><td data-type="bottom"></td></tr></tbody></table></div>'), i.push('<div><input type="checkbox" name="switch" lay-filter="soul-edit-switch" lay-skin="switch" lay-text="与|或" ' + (r ? "" : "checked") + "></div>"), n) {
                    case"in":
                        i.push('<div class="layui-firebrick item-field">' + t[d].title + "</div>"), i.push('<div class="layui-deeppink item-type" >筛选数据</div>'), i.push('<div class="layui-blueviolet item-value">共' + (e.values ? e.values.length : 0) + "条数据</div>"), i.push('<div class="layui-red delete-item"><i class="layui-icon layui-icon-close-fill"></i></div>');
                        break;
                    case"date":
                        i.push('<div class="layui-firebrick item-field">' + t[d].title + "</div>"), i.push('<div class="layui-deeppink item-type">选择日期</div>'), i.push('<div class="layui-blueviolet item-value">' + ("specific" === e.type ? e.value || "请选择" : b[e.type]) + "</div>"), i.push('<div class="layui-red delete-item"><i class="layui-icon layui-icon-close-fill"></i></div>');
                        break;
                    case"condition":
                        i.push('<div class="layui-firebrick item-field">' + t[d].title + "</div>"), i.push('<div class="layui-deeppink item-type">' + Y[e.type] + "</div>"), "null" !== s && "notNull" !== s && i.push('<div class="layui-blueviolet item-value">' + (void 0 === e.value || "" === e.value ? "请输入..." : e.value) + "</div>"), i.push('<div class="layui-red delete-item"><i class="layui-icon layui-icon-close-fill"></i></div>');
                        break;
                    case"group":
                        if (i.push('<div class="layui-firebrick">分组</div>'), i.push('<div><a class="layui-btn layui-btn-xs" data-type="addOne"><i class="layui-icon layui-icon-add-1"></i> 添加条件</a><a class="layui-btn layui-btn-xs" data-type="addGroup"><i class="layui-icon layui-icon-add-circle"></i> 添加分组</a></div>'), i.push('<div class="layui-red delete-item"><i class="layui-icon layui-icon-close-fill"></i></div>'), i.push('<ul class="group ' + (a ? "" : "line") + '">'), e.children) for (var u = 0; u < e.children.length; u++) c(e.children[u], i, t, 0, u === e.children.length - 1);
                        i.push("</ul>")
                }
                i.push("</li>")
            }

            function r(e) {
                m.hideDropList(p), m.hideCondition(p), m.hideColumns(p), m.hideBfPrefix(p), m.hideBfType(p);
                var i = V(e).offset().top + V(e).outerHeight(), t = V(e).offset().left;
                V("#soul-bf-column" + v).find("li.soul-bf-selected").removeClass("soul-bf-selected"), V("#soul-bf-column" + v).data("field", V(e).parent().data("field")).data("id", V(e).parent().data("id")).data("mode", V(e).parent().data("mode")).data("group", V(e).parents("li:eq(2)").data("id") || "").data("refresh", V(".soul-edit-out .out_auto").prop("checked")).show().css({
                    top: i,
                    left: t
                }).removeClass().addClass("fadeInUp animated").find('li[data-field="' + V(e).parent().data("field") + '"]').addClass("soul-bf-selected")
            }

            function u(e) {
                m.hideDropList(p), m.hideCondition(p), m.hideColumns(p), m.hideBfColumn(p), m.hideBfPrefix(p);
                var i = V(e).offset().top + V(e).outerHeight(), t = V(e).offset().left, l = V(e).parent().data("field");
                switch (V("#soul-bf-type" + v + " li").hide(), o[l] && 0 === o[l].indexOf("date") && V("#soul-bf-type" + v + " li[data-mode=date]").show(), -1 !== n[l].items.indexOf("data") && V("#soul-bf-type" + v + " li[data-mode=in]").show(), -1 !== n[l].items.indexOf("condition") && V("#soul-bf-type" + v + " li[data-mode=condition]").show(), V("#soul-bf-type" + v).find("li.soul-bf-selected").removeClass("soul-bf-selected"), V(e).parent().data("mode")) {
                    case"in":
                        V("#soul-bf-type" + v).find('li[data-mode="in"]').addClass("soul-bf-selected");
                        break;
                    case"date":
                        V("#soul-bf-type" + v).find('li[data-mode="date"]').addClass("soul-bf-selected");
                    case"condition":
                        V("#soul-bf-type" + v).find('li[data-value="' + V(e).parent().data("type") + '"]').addClass("soul-bf-selected")
                }
                V("#soul-bf-type" + v).data("type", V(e).parent().data("type")).data("mode", V(e).parent().data("mode")).data("id", V(e).parent().data("id")).data("group", V(e).parents("li:eq(2)").data("id") || "").data("refresh", V(".soul-edit-out .out_auto").prop("checked")).show().css({
                    top: i,
                    left: t
                }).removeClass().addClass("fadeInUp animated")
            }

            function h(i) {
                m.hideColumns(p), m.hideBfType(p), m.hideBfPrefix(p), m.hideBfColumn(p);
                var e = V(i).offset().left, t = V(i).parent().data("mode"), l = V(i).parent().data("field"),
                    a = V(i).parent().data("id"), o = V(i).parent().data("head"), d = V(i).parent().data("prefix"),
                    n = V(i).parent().data("value"), s = V(".soul-edit-out .out_auto").prop("checked"),
                    r = ie[p.id] || {}, u = r.filterSos ? JSON.parse(r.filterSos) : [];
                switch (t) {
                    case"in":
                        if (m.hideCondition(p), A && clearTimeout(A), V("#soul-dropList" + v + ">.filter-search>input").val(""), V("#soul-dropList" + v).show(), V("#soulDropList" + v).find("." + l + "DropList li input[type=checkbox]:checked").prop("checked", !1), (h = m.getFilterSoById(u, a)).values) for (y = 0; y < h.values.length; y++) V("#soulDropList" + v).find("." + l + 'DropList li input[type=checkbox][value="' + h.values[y] + '"]').prop("checked", !0);
                        V("#soul-dropList" + v + ">ul").data("id", a).data("head", o).data("refresh", s).data("prefix", d).html(V("#soulDropList" + v).find("." + l + "DropList li").clone()), _.render("checkbox", "orm"), f = V(i).offset().top + V(i).outerHeight(), V("#soul-dropList" + v).css({
                            top: f,
                            left: e
                        }).show().removeClass().addClass("fadeInUp animated"), setTimeout(function () {
                            V("#soul-dropList" + v + ">.filter-search>input").focus()
                        }, 1);
                        var c = !0;
                        _.on("checkbox(soulDropList" + v + ")", function (e) {
                            c = !1, m.updateDropList(p, l)
                        }), V("#soul-dropList" + v + ">ul>li[data-value]").on("click", function () {
                            c && V(this).find("div.layui-form-checkbox").trigger("click"), c = !0
                        });
                        break;
                    case"date":
                        m.hideDropList(p), H && clearTimeout(H);
                        var h = m.getFilterSoById(u, a), f = V(i).offset().top + V(i).height();
                        m.showDate(p, l, h, "fadeInUp", f, e, "down", s);
                        break;
                    case"condition":
                        V(i).hide(), V(i).after('<div><input class="layui-input tempValue" value="" /></div>'), V(i).next().children().val(n).select().on("keydown", function (e) {
                            13 === e.keyCode && V(this).blur()
                        }).on("blur", function () {
                            var e = V(this).val();
                            V(i).html(void 0 === e || "" === e ? "请输入..." : e), V(i).show(), V(this).parent().remove(), e !== n && (V(i).parent().data("value", e), m.updateWhere(p, {
                                id: a,
                                value: e
                            }), s && m.soulReload(p))
                        })
                }
            }

            d.push("</ul>"), d.push("</div>"), d.push("</div>"), layer.open({
                title: "编辑条件",
                type: 1,
                offset: "auto",
                area: ["480px", "480px"],
                content: d.join("")
            }), _.render(null, "soul-edit-out"), _.on("checkbox(out_auto)", function (e) {
                e.elem.checked && m.soulReload(p)
            }), _.on("switch(soul-edit-switch)", function (e) {
                var i, t, l, a;
                t = (i = e).elem.checked ? "and" : "or", l = V(i.elem).parents("li:eq(0)").data("id"), a = V(".soul-edit-out .out_auto").prop("checked"), V(i.elem).parents("li:eq(0)").data("prefix", t), m.updateWhere(p, {
                    id: l,
                    prefix: t
                }), a && m.soulReload(p)
            }), V(".soul-edit-out .item-field").on("click", function (e) {
                e.stopPropagation(), r(this)
            }), V(".soul-edit-out .item-type").on("click", function (e) {
                e.stopPropagation(), u(this)
            }), V(".soul-edit-out .item-value").on("click", function (e) {
                e.stopPropagation(), h(this)
            }), V(".soul-edit-out .delete-item").on("click", function () {
                var e = V(this).parent().data("id"), i = V(".soul-edit-out .out_auto").prop("checked");
                V(this).parent().remove(), m.updateWhere(p, {id: e, delete: !0}), i && m.soulReload(p)
            }), V(".soul-edit-out a[data-type]").on("click", function () {
                "search" === V(this).data("type") ? m.soulReload(p) : function e(i) {
                    var t = V(".soul-edit-out .out_auto").prop("checked");
                    d = [];
                    switch (V(i).data("type")) {
                        case"addOne":
                            var l = {prefix: "and", field: a.field, mode: "condition", type: "eq", value: ""};
                            V(i).parent().parent().data("id") && V.extend(l, {groupId: V(i).parent().parent().data("id")}), m.updateWhere(p, l), d.push('<li data-id="' + l.id + '" data-field="' + l.field + '" data-mode="' + l.mode + '" data-type="' + l.type + '" data-value="' + l.value + '" data-prefix="' + l.prefix + '" class="last">'), d.push('<div><table><tbody><tr><td data-type="top"></td></tr><tr><td data-type="bottom"></td></tr></tbody></table></div>'), d.push('<div><input type="checkbox" name="switch" lay-filter="soul-edit-switch" lay-skin="switch" lay-text="与|或" checked></div>'), d.push('<div class="layui-firebrick item-field">' + n[l.field].title + "</div>"), d.push('<div class="layui-deeppink item-type">等于</div>'), d.push('<div class="layui-blueviolet item-value">请输入...</div>'), d.push('<div class="layui-red delete-item"><i class="layui-icon layui-icon-close-fill"></i></div>'), d.push("</li>");
                            break;
                        case"addGroup":
                            var l = {prefix: "and", mode: "group", children: []};
                            V(i).parent().parent().data("id") && V.extend(l, {groupId: V(i).parent().parent().data("id")}), m.updateWhere(p, l), d.push('<li data-id="' + l.id + '" class="last">'), d.push('<div><table><tbody><tr><td data-type="top"></td></tr><tr><td data-type="bottom"></td></tr></tbody></table></div>'), d.push('<div><input type="checkbox" name="switch" lay-filter="soul-edit-switch" lay-skin="switch" lay-text="与|或" checked></div>'), d.push('<div class="layui-firebrick">分组</div>'), d.push('<div><a class="layui-btn layui-btn-xs" data-type="addOne"><i class="layui-icon layui-icon-add-1"></i> 添加条件</a><a class="layui-btn layui-btn-xs" data-type="addGroup"><i class="layui-icon layui-icon-add-circle"></i> 添加分组</a></div>'), d.push('<div class="layui-red delete-item"><i class="layui-icon layui-icon-close-fill"></i></div>'), d.push('<ul class="group">'), d.push("</ul>"), d.push("</li>")
                    }
                    t && m.soulReload(p);
                    0 < V(i).parent().parent().children("ul").children("li").length && (V(i).parent().parent().children("ul").children("li:last").removeClass("last"), 0 < V(i).parent().parent().children("ul").children("li:last").children("ul.group").length && V(i).parent().parent().children("ul").children("li:last").children("ul.group").addClass("line"));
                    V(i).parent().parent().children("ul").append(d.join(""));
                    _.render("checkbox", "soul-edit-out");
                    "addGroup" === V(i).data("type") ? V(i).parent().parent().children("ul").children("li:last").find("a[data-type]").on("click", function () {
                        e(this)
                    }) : (V(i).parent().parent().children("ul").children("li:last").find(".item-field").on("click", function (e) {
                        e.stopPropagation(), r(this)
                    }), V(i).parent().parent().children("ul").children("li:last").find(".item-type").on("click", function (e) {
                        e.stopPropagation(), u(this)
                    }), V(i).parent().parent().children("ul").children("li:last").find(".item-value").on("click", function (e) {
                        e.stopPropagation(), h(this)
                    }));
                    V(i).parent().parent().children("ul").children("li:last").children(".delete-item").on("click", function () {
                        var e = V(this).parent().data("id"), i = V(".soul-edit-out .out_auto").prop("checked");
                        V(this).parent().remove(), m.updateWhere(p, {id: e, delete: !0}), i && m.soulReload(p)
                    })
                }(this)
            })
        }, hideColumns: function (e, i) {
            var t = e.id;
            V("#soul-columns" + t).removeClass().addClass("fadeOutLeft animated"), J && clearTimeout(J), void 0 === i || i ? J = setTimeout(function (e) {
                V("#soul-columns" + t).hide()
            }, 500) : V("[id^=soul-columns]").hide()
        }, hideDropList: function (e, i) {
            var t = e.id;
            V("#soul-dropList" + t).removeClass().addClass("fadeOutLeft animated"), A && clearTimeout(A), void 0 === i || i ? A = setTimeout(function (e) {
                V("#soul-dropList" + t).hide()
            }, 500) : V("[id^=soul-dropList]").hide()
        }, hideCondition: function (e, i) {
            var t = e.id;
            V("#soul-condition" + t).removeClass().addClass("fadeOutLeft animated"), H && clearTimeout(H), void 0 === i || i ? H = setTimeout(function (e) {
                V("#soul-condition" + t).hide()
            }, 500) : V("[id^=soul-condition]").hide()
        }, hideBfPrefix: function (e, i) {
            var t = e.id;
            V("#soul-bf-prefix" + t).removeClass().addClass("fadeOutDown animated"), l && clearTimeout(l), void 0 === i || i ? l = setTimeout(function () {
                V("#soul-bf-prefix" + t).hide()
            }, 500) : V("[id=soul-bf-prefix" + t + "]").hide()
        }, hideBfColumn: function (e, i) {
            var t = e.id;
            V("#soul-bf-column" + t).removeClass().addClass("fadeOutDown animated"), l && clearTimeout(l), void 0 === i || i ? l = setTimeout(function () {
                V("#soul-bf-column" + t).hide()
            }, 500) : V("[id=soul-bf-column" + t + "]").hide()
        }, hideBfType: function (e, i) {
            var t = e.id;
            V("#soul-bf-type" + t).removeClass().addClass("fadeOutDown animated"), a && clearTimeout(a), void 0 === i || i ? a = setTimeout(function () {
                V("#soul-bf-type" + t).hide()
            }, 500) : V("[id=soul-bf-type" + t + "]").hide()
        }, bindFilterClick: function (o) {
            var d, n = this, e = V(o.elem),
                i = e.next().children(".layui-table-box").children(".layui-table-header").children("table"),
                t = e.next().children(".layui-table-box").children(".layui-table-fixed-l").children(".layui-table-header").children("table"),
                l = e.next().children(".layui-table-box").children(".layui-table-fixed-r").children(".layui-table-header").children("table"),
                s = o.id, r = o.filter && o.filter.items || M;

            function a(i) {
                var e, t, l = i.data("items") ? i.data("items").split(",") : r;
                n.hideColumns(o, !1), n.hideDropList(o, !1), n.hideCondition(o, !1), V("[id^=main-list]").hide(), V("#main-list" + s).data({
                    field: i.data("column"),
                    split: i.data("split")
                }), V("#soul-columns" + s + " [type=checkbox]").attr("disabled", !1), V("#soul-columns" + s + " li[data-key=" + i.parents("th").data("key").split("-")[2] + "] [type=checkbox]").attr("disabled", !0), V("#main-list" + s + " > li").hide(), i.hasClass("layui-table-sort") && V("#main-list" + s + " .soul-sort").show();
                for (var a = 0; a < l.length; a++) V("#main-list" + s + " ." + m[l[a]]).show(), V("#main-list" + s + " ." + m[l[a]]).index() !== a + 2 && V("#main-list" + s + '>li:eq("' + (a + 2) + '")').before(V("#main-list" + s + " ." + m[l[a]]));
                d && clearTimeout(d), t = i.offset().left + V("#main-list" + s).outerWidth() < document.body.clientWidth ? (e = i.offset().left + 10, "fadeInLeft") : (e = i.offset().left - V("#main-list" + s).outerWidth(), "fadeInRight"), V("#main-list" + s).data("type", o.where.tableFilterType && JSON.parse(o.where.tableFilterType)[i.data("column")] || "").hide().css({
                    top: i.offset().top + 10,
                    left: e
                }).show().removeClass().addClass(t + " animated"), V("#main-list" + s + " .soul-sort").on("click", function (e) {
                    i.siblings(".layui-table-sort").find(".layui-table-sort-" + V(this).data("value")).trigger("click"), V("#main-list" + s).hide()
                }), _.render("checkbox", "orm")
            }

            i.find(".soul-table-filter").off("click").on("click", function (e) {
                e.stopPropagation(), a(V(this))
            }), t.find(".soul-table-filter").off("click").on("click", function (e) {
                e.stopPropagation(), a(V(this))
            }), l.find(".soul-table-filter").off("click").on("click", function (e) {
                e.stopPropagation(), a(V(this))
            }), V(document).on("click", function (e) {
                V("#main-list" + s).hide(), n.hideColumns(o, !1), n.hideDropList(o, !1), n.hideCondition(o, !1), n.hideBfPrefix(o, !1), n.hideBfColumn(o, !1), n.hideBfType(o, !1)
            }), V("#main-list" + s + ",#soul-columns" + s + ",#soul-dropList" + s + ",#soul-condition" + s).on("click", function (e) {
                V(this).find(".layui-form-selected").removeClass("layui-form-selected"), e.stopPropagation()
            }), n.renderBottomCondition(o);
            for (var u = ie[o.id] || {}, c = JSON.parse(u.filterSos ? u.filterSos : "[]"), h = 0; h < c.length; h++) if (c[h].head) {
                var f = !1;
                switch (c[h].mode) {
                    case"in":
                        c[h].values && 0 < c[h].values.length && (f = !0);
                        break;
                    case"date":
                        "all" !== c[h].type && void 0 !== c[h].value && "" !== c[h].value && (f = !0);
                        break;
                    case"group":
                        c[h].children && 0 < c[h].children.length && (f = !0)
                }
                i.find('thead>tr>th[data-field="' + c[h].field + '"] .soul-table-filter').attr("soul-filter", "" + f), t.find('thead>tr>th[data-field="' + c[h].field + '"] .soul-table-filter').attr("soul-filter", "" + f), l.find('thead>tr>th[data-field="' + c[h].field + '"] .soul-table-filter').attr("soul-filter", "" + f)
            }
        }, resize: function (e) {
            var i = V(e.elem), t = i.next().children(".layui-table-box"), l = t.children(".layui-table-main");
            if (0 < i.next().children(".soul-bottom-contion").length) {
                i.next().children(".soul-bottom-contion").children(".condition-items").css("width", i.next().children(".soul-bottom-contion").width() - i.next().children(".soul-bottom-contion").children(".editCondtion").outerWidth());
                var a = i.next().height() - i.next().children(".soul-bottom-contion").outerHeight();
                0 < i.next().children(".layui-table-tool").length && (a -= i.next().children(".layui-table-tool").outerHeight()), 0 < i.next().children(".layui-table-total").length && (a -= i.next().children(".layui-table-total").outerHeight()), 0 < i.next().children(".layui-table-page").length && (a -= i.next().children(".layui-table-page").outerHeight()), a -= i.next().children(".layui-table-box").children(".layui-table-header").outerHeight(), i.next().children(".layui-table-box").children(".layui-table-body").height(a);
                var o = a - this.getScrollWidth(l[0]), d = l.children("table").height();
                i.next().children(".layui-table-box").children(".layui-table-fixed").children(".layui-table-body").height(o <= d ? o : "auto");
                var n = l.width() - l.prop("clientWidth");
                t.children(".layui-table-fixed-r").css("right", n - 1)
            }
        }, updateDropList: function (e, i) {
            V(e.elem);
            var t = e.id, l = V("#soul-dropList" + t + ">ul").data("id"),
                a = V("#soul-dropList" + t + ">ul input[type=checkbox]:checked"), o = [],
                d = V("#soul-dropList" + t + ">ul").data("head"), n = V("#soul-dropList" + t + ">ul").data("prefix"),
                s = V("#soul-dropList" + t + ">ul").data("refresh"), r = V("#soul-dropList" + t + ">ul").data("split");
            0 < a.length && a.each(function () {
                o.push(V(this).val())
            });
            var u = {id: l, head: d, prefix: n || "and", mode: "in", field: i, split: r, values: o};
            this.updateWhere(e, u), l || V("#soul-dropList" + t + ">ul").data("id", u.id), 0 < V(".soul-edit-out").length && V('.soul-edit-out li[data-id="' + u.id + '"]>.item-value').html("共" + (u.values ? u.values.length : 0) + "条数据"), s && this.soulReload(e)
        }, getFilterSoById: function (e, i) {
            for (var t = 0; t < e.length; t++) {
                if (e[t].id === i) return e[t];
                if ("group" === e[t].mode) for (var l = 0; l < e[t].children.length; l++) {
                    var a = this.getFilterSoById(e[t].children, i);
                    if (a) return a
                }
            }
            return null
        }, updateWhere: function (e, i) {
            var a = this, t = ie[e.id] || {}, l = JSON.parse(t.filterSos ? t.filterSos : "[]");
            if (i.id || i.groupId) for (var o = 0; o < l.length; o++) {
                if (i.delete && l[o].id === i.id) {
                    l.splice(o, 1);
                    break
                }
                if (d(l[o], i)) break
            } else ("in" !== i.mode || i.values && 0 < i.values.length) && l.push(V.extend(i, {id: a.getDifId()}));

            function d(e, i) {
                var t = !1;
                if (e.id === i.id && (V.extend(e, i), t = !0), i.id || e.id !== i.groupId) {
                    if ("group" === e.mode) for (var l = 0; l < e.children.length; l++) {
                        if (i.delete && e.children[l].id === i.id) return e.children.splice(l, 1), 1;
                        if (d(e.children[l], i)) return 1
                    }
                } else e.children.push(V.extend(i, {id: a.getDifId()}));
                return t
            }

            t.filterSos = JSON.stringify(l), e.where = t, ie[e.id] = t
        }, soulReload: function (e, i) {
            var a = this, t = V(e.elem),
                l = t.next().children(".layui-table-box").children(".layui-table-main").scrollLeft();
            if (z[e.id] = void 0 === i || i, void 0 !== e.url && e.page) t.data("scrollLeft", l), $.reload(e.id, {
                where: ie[e.id] || {},
                page: {curr: 1}
            }); else {
                var o = ie[e.id] || {}, d = JSON.parse(o.filterSos ? o.filterSos : "[]"),
                    n = o.tableFilterType ? JSON.parse(o.tableFilterType) : {}, s = layer.load(2);
                if (e.page || (e.limit = 1e8), 0 < d.length) {
                    var r = [];
                    if (layui.each(Z[e.id], function (e, i) {
                        for (var t = !0, l = 0; l < d.length; l++) t = a.handleFilterSo(d[l], i, n, t, 0 === l);
                        t && r.push(i)
                    }), e.page) $.reload(e.id, {
                        data: r,
                        initSort: e.initSort,
                        isSoulFrontFilter: !0,
                        page: {curr: 1}
                    }); else {
                        var u = e.url;
                        t.next().off("click"), $.reload(e.id, {
                            url: "",
                            initSort: e.initSort,
                            isSoulFrontFilter: !0,
                            data: r
                        }).config.url = u
                    }
                    e.data = r
                } else e.page ? $.reload(e.id, {
                    data: Z[e.id],
                    initSort: e.initSort,
                    isSoulFrontFilter: !0,
                    page: {curr: 1}
                }) : $.reload(e.id, {data: Z[e.id], initSort: e.initSort, isSoulFrontFilter: !0}), e.data = Z[e.id];
                t.next().children(".layui-table-box").children(".layui-table-main").scrollLeft(l), layer.close(s)
            }
        }, handleFilterSo: function (e, i, t, l, a) {
            var o, d, n, s = !a && "or" === e.prefix, r = e.field, u = e.value, c = !0;
            if (e.children && 0 < e.children.length) {
                for (var h = 0; h < e.children.length; h++) c = this.handleFilterSo(e.children[h], i, t, c, 0 === h);
                return s ? l || c : l && c
            }
            switch (e.mode) {
                case"in":
                    if (!(e.values && 0 < e.values.length)) return l;
                    if (e.split) {
                        var f = (i[r] + "").split(e.split), p = !1;
                        for (h = 0; h < f.length; h++) -1 !== e.values.indexOf(f[h]) && (p = !0);
                        c = p
                    } else c = -1 !== e.values.indexOf(i[r] + "");
                    break;
                case"condition":
                    if ("null" !== e.type && "notNull" !== e.type && (void 0 === u || "" === u)) return l;
                    switch (e.type) {
                        case"eq":
                            c = isNaN(i[r]) || isNaN(u) ? i[r] === u : Number(i[r]) === Number(u);
                            break;
                        case"ne":
                            c = isNaN(i[r]) || isNaN(u) ? i[r] !== u : Number(i[r]) !== Number(u);
                            break;
                        case"gt":
                            c = isNaN(i[r]) || isNaN(u) ? i[r] > u : Number(i[r]) > Number(u);
                            break;
                        case"ge":
                            c = isNaN(i[r]) || isNaN(u) ? i[r] >= u : Number(i[r]) >= Number(u);
                            break;
                        case"lt":
                            c = isNaN(i[r]) || isNaN(u) ? i[r] < u : Number(i[r]) < Number(u);
                            break;
                        case"le":
                            c = isNaN(i[r]) || isNaN(u) ? i[r] <= u : Number(i[r]) <= Number(u);
                            break;
                        case"contain":
                            c = -1 !== (i[r] + "").indexOf(u);
                            break;
                        case"notContain":
                            c = -1 === (i[r] + "").indexOf(u);
                            break;
                        case"start":
                            c = 0 === (i[r] + "").indexOf(u);
                            break;
                        case"end":
                            var y = (i[r] + "").length - (u + "").length;
                            c = 0 <= y && (i[r] + "").lastIndexOf(u) === y;
                            break;
                        case"null":
                            c = void 0 === i[r] || "" === i[r] || null === i[r];
                            break;
                        case"notNull":
                            c = void 0 !== i[r] && "" !== i[r] && null !== i[r]
                    }
                    break;
                case"date":
                    var m = new Date(Date.parse(i[r].replace(/-/g, "/")));
                    switch (e.type) {
                        case"all":
                            c = !0;
                            break;
                        case"yesterday":
                            c = i[r] && x(m, b() - 86400, b() - 1);
                            break;
                        case"thisWeek":
                            c = i[r] && x(m, g(), g() + 604800 - 1);
                            break;
                        case"lastWeek":
                            c = i[r] && x(m, g() - 604800, g() - 1);
                            break;
                        case"thisMonth":
                            c = i[r] && x(m, new Date((new Date).setDate(1)).setHours(0, 0, 0, 0) / 1e3, (o = new Date, d = o.getMonth(), n = ++d, new Date(o.getFullYear(), n, 1) / 1e3 - 1));
                            break;
                        case"thisYear":
                            c = i[r] && x(m, new Date((new Date).getFullYear(), 1, 1) / 1e3, new Date((new Date).getFullYear() + 1, 1, 1) / 1e3 - 1);
                            break;
                        case"specific":
                            var v = m.getFullYear();
                            v += "-" + k(m.getMonth() + 1), v += "-" + k(m.getDate()), c = i[r] && v === u
                    }
            }

            function b() {
                return (new Date).setHours(0, 0, 0, 0) / 1e3
            }

            function g() {
                var e = new Date, i = e.getDay() || 7;
                return new Date(e.setDate(e.getDate() - i + 1)).setHours(0, 0, 0, 0) / 1e3
            }

            function x(e, i, t) {
                return e.getTime() / 1e3 >= i && e.getTime() / 1e3 <= t
            }

            function k(e) {
                return (e += "").length <= 1 && (e = "0" + e), e
            }

            return s ? l || c : l && c
        }, getDifId: function () {
            return i++
        }, showDate: function (a, o, e, i, t, l, d, n) {
            var s = this, r = a.id, u = [], c = document.body.clientWidth;
            for (var h in u.push('<div class="' + o + 'Condition" data-value="' + o + '" style="padding: 5px;" >'), u.push('<div class="layui-row">'), b) u.push('<div class="layui-col-sm4"><input type="radio" name="datetime' + r + o + '" lay-filter="datetime' + r + '" value="' + h + '" title="' + b[h] + '"></div>');
            u.push("</div>"), u.push('<div><input type="radio" name="datetime' + r + o + '" lay-filter="datetime' + r + '"  value="specific" title="过滤具体日期"> <input type="hidden" class="specific_value"><div class="staticDate"></div></div></div>'), V("#soul-condition" + r).html(u.join(""));
            var f = y.toDateString(new Date, "yyyy-MM-dd");
            e ? (V("#soul-condition" + r).data({
                id: e.id,
                head: !0
            }), V("#soul-condition" + r + ">." + o + 'Condition [name^=datetime][value="' + e.type + '"]').prop("checked", !0), "specific" === e.type && (f = e.value)) : (V("#soul-condition" + r).data({
                id: "",
                head: !0
            }), V("#soul-condition" + r + ">." + o + 'Condition [name^=datetime][value="all"]').prop("checked", !0)), V("#soul-condition" + r + " .specific_value").val(f), p.render({
                elem: "#soul-condition" + r + " .staticDate",
                position: "static",
                calendar: !0,
                btns: ["now"],
                value: f,
                done: function (e) {
                    var i = V("#soul-condition" + r).data("id"), t = V("#soul-condition" + r).data("head");
                    V("#soul-condition" + r + " .specific_value").val(e), V("#soul-condition" + r + " [name^=datetime]:checked").prop("checked", !1), V("#soul-condition" + r + " [name^=datetime][value=specific]").prop("checked", !0);
                    var l = {id: i, head: t, prefix: "and", mode: "date", field: o, type: "specific", value: e};
                    s.updateWhere(a, l), i || V("#soul-condition" + r).data("id", l.id), 0 < V(".soul-edit-out").length && V('.soul-edit-out li[data-id="' + l.id + '"]').children(".item-value").html(l.value), n && s.soulReload(a), _.render("radio", "orm")
                }
            }), _.on("radio(datetime" + r + ")", function (e) {
                var i = V("#soul-condition" + r).data("id"), t = {
                    id: i,
                    head: V("#soul-condition" + r).data("head"),
                    prefix: "and",
                    mode: "date",
                    field: o,
                    type: e.value,
                    value: V("#soul-condition" + r + " .specific_value").val()
                };
                s.updateWhere(a, t), i || V("#soul-condition" + r).data("id", t.id), 0 < V(".soul-edit-out").length && V('.soul-edit-out li[data-id="' + t.id + '"]').children(".item-value").html(b[t.type] || t.value), n && s.soulReload(a)
            }), _.render("radio", "orm"), "down" === d ? i = l + V("#soul-condition" + r).width() < c ? "fadeInLeft" : (l = l - V("#main-list" + r).width() - V("#soul-condition" + r).width(), "fadeInRight") : t = t - V("#soul-condition" + r).outerHeight() - 10, V("#soul-condition" + r).css({
                top: t,
                left: l
            }).show().removeClass().addClass(i + " animated")
        }, bottomConditionHtml: function (e, i, t, l) {
            var a = "or" === i.prefix, o = i.field;
            if ("group" !== i.mode) {
                switch (e.push('<div class="condition-item" data-field="' + o + '" data-id="' + i.id + '" data-mode="' + i.mode + '" data-type="' + i.type + '" data-value="' + (void 0 === i.value ? "" : i.value) + '" data-prefix="' + (i.prefix || "and") + '">'), l || e.push('<div class="item-prefix layui-red">' + (a ? "或" : "与") + "</div> "), e.push('<div class="item-field layui-firebrick">' + t[o].title + "</div> "), e.push('<div class="item-type layui-deeppink">'), i.mode) {
                    case"in":
                        e.push("筛选数据");
                        break;
                    case"condition":
                        e.push(Y[i.type]);
                        break;
                    case"date":
                        e.push("选择日期");
                        break;
                    default:
                        e.push("未知")
                }
                if (e.push("</div> "), "null" !== i.type && "notNull" !== i.type) {
                    switch (e.push('<div class="item-value layui-blueviolet ' + ("date" === i.mode && "specific" !== i.type) + '">'), i.mode) {
                        case"in":
                            e.push("共" + (i.values ? i.values.length : 0) + "条数据");
                            break;
                        case"date":
                            e.push("specific" === i.type ? i.value || "请选择" : b[i.type]);
                            break;
                        case"condition":
                        default:
                            e.push(void 0 === i.value || "" === i.value ? "请输入..." : i.value)
                    }
                    e.push("</div>")
                }
                e.push('<i class="condition-item-close soul-icon soul-icon-unfold" ></i>'), e.push("</div>")
            } else if (i.children && 0 < i.children.length) {
                e.push('<div class="condition-item" data-id="' + i.id + '" data-prefix="' + (i.prefix || "and") + '">'), l || e.push('<div class="item-prefix layui-red">' + (a ? "或" : "与") + "</div> ");
                for (var d = 0; d < i.children.length; d++) this.bottomConditionHtml(e, i.children[d], t, 0 === d);
                e.push('<i class="condition-item-close soul-icon soul-icon-unfold" ></i>'), e.push("</div>")
            }
        }, renderBottomCondition: function (f) {
            for (var e, p = this, i = ie[f.id] || {}, y = i.filterSos ? JSON.parse(i.filterSos) : [], d = i.tableFilterType ? JSON.parse(i.tableFilterType) : {}, t = V(f.elem), m = f.id, l = t.next().children(".soul-bottom-contion"), n = {}, a = [], o = f.filter && f.filter.items || M, s = p.getCompleteCols(f.cols), r = 0; r < s.length; r++) s[r].field && s[r].filter && (-1 === (e = s[r].filter.items || o).indexOf("data") && -1 === e.indexOf("condition") || (n[s[r].field] = {
                title: s[r].title,
                items: e
            }));
            for (r = 0; r < y.length; r++) p.bottomConditionHtml(a, y[r], n, 0 === r);
            if (l.children(".condition-items").html(a.join("")), a = [], 0 === V("#soul-bf-prefix" + m).length && (a.push('<div id="soul-bf-prefix' + m + '" style="display: none;"><ul>'), a.push('<li data-value="and">与</li>'), a.push('<li data-value="or">或</li>'), a.push("</ul></div>")), 0 === V("#soul-bf-column" + m).length) {
                for (var u in a.push('<div id="soul-bf-column' + m + '" style="display: none;"><ul>'), n) a.push('<li data-field="' + u + '">' + n[u].title + "</li>");
                a.push("</ul></div>")
            }
            if (0 === V("#soul-bf-type" + m).length) {
                for (var c in a.push('<div id="soul-bf-type' + m + '" style="display: none;"><ul>'), a.push('<li data-value="in" data-mode="in">筛选数据</li>'), a.push('<li data-value="all" data-mode="date">选择日期</li>'), Y) a.push('<li data-value="' + c + '" data-mode="condition">' + Y[c] + "</li>");
                a.push("</ul></div>")
            }
            0 === V("#soul-bf-cond2-dropList" + m).length && a.push('<div id="soul-bf-cond2-dropList' + m + '" style="display: none;"><div class="filter-search"><input type="text" placeholder="关键字搜索" class="layui-input"></div><div class="check"><div class="multiOption" data-type="all"><i class="soul-icon">&#xe623;</i> 全选</div><div class="multiOption" data-type="none"><i class="soul-icon">&#xe63e;</i> 清空</div><div class="multiOption" data-type="reverse"><i class="soul-icon">&#xe614;</i>反选</div></div><ul></ul></div>'), V("body").append(a.join("")), l.find(".item-prefix").off("click").on("click", function (e) {
                e.stopPropagation(), V("#main-list" + m).hide(), p.hideDropList(f), p.hideCondition(f), p.hideColumns(f), p.hideBfColumn(f), p.hideBfType(f);
                var i = V(this).offset().top - V("#soul-bf-prefix" + m).outerHeight() - 10, t = V(this).offset().left;
                V("#soul-bf-prefix" + m).find("li.soul-bf-selected").removeClass("soul-bf-selected"), V("#soul-bf-prefix" + m).data("id", V(this).parent().data("id")).data("prefix", V(this).parent().data("prefix")).data("refresh", !0).show().css({
                    top: i,
                    left: t
                }).removeClass().addClass("fadeInUp animated").find('li[data-value="' + V(this).parent().data("prefix") + '"]').addClass("soul-bf-selected")
            }), l.find(".item-field").off("click").on("click", function (e) {
                e.stopPropagation(), V("#main-list" + m).hide(), p.hideDropList(f), p.hideCondition(f), p.hideColumns(f), p.hideBfPrefix(f), p.hideBfType(f);
                var i = V(this).offset().top - V("#soul-bf-column" + m).outerHeight() - 10, t = V(this).offset().left;
                V("#soul-bf-column" + m).find("li.soul-bf-selected").removeClass("soul-bf-selected"), V("#soul-bf-column" + m).data("field", V(this).parent().data("field")).data("id", V(this).parent().data("id")).data("mode", V(this).parent().data("mode")).data("group", V(this).parent().parent().data("id") || "").data("refresh", !0).show().css({
                    top: i,
                    left: t
                }).removeClass().addClass("fadeInUp animated").find('li[data-field="' + V(this).parent().data("field") + '"]').addClass("soul-bf-selected")
            }), l.find(".item-type").on("click", function (e) {
                e.stopPropagation(), V("#main-list" + m).hide(), p.hideDropList(f), p.hideCondition(f), p.hideColumns(f), p.hideBfColumn(f), p.hideBfPrefix(f);
                var i = V(this).parent().data("field");
                V("#soul-bf-type" + m + " li").hide(), d[i] && 0 === d[i].indexOf("date") && V("#soul-bf-type" + m + " li[data-mode=date]").show(), -1 !== n[i].items.indexOf("data") && V("#soul-bf-type" + m + " li[data-mode=in]").show(), -1 !== n[i].items.indexOf("condition") && V("#soul-bf-type" + m + " li[data-mode=condition]").show();
                var t = V(this).offset().top - V("#soul-bf-type" + m).outerHeight() - 10, l = V(this).offset().left;
                switch (V("#soul-bf-type" + m).find("li.soul-bf-selected").removeClass("soul-bf-selected"), V(this).parent().data("mode")) {
                    case"in":
                        V("#soul-bf-type" + m).find('li[data-mode="in"]').addClass("soul-bf-selected");
                        break;
                    case"date":
                        V("#soul-bf-type" + m).find('li[data-mode="date"]').addClass("soul-bf-selected");
                    case"condition":
                        V("#soul-bf-type" + m).find('li[data-value="' + V(this).parent().data("type") + '"]').addClass("soul-bf-selected")
                }
                V("#soul-bf-type" + m).data("type", V(this).parent().data("type")).data("mode", V(this).parent().data("mode")).data("id", V(this).parent().data("id")).data("group", V(this).parent().parent().data("id") || "").data("refresh", !0).show().css({
                    top: t,
                    left: l
                }).removeClass().addClass("fadeInUp animated")
            }), l.find(".item-value").on("click", function (e) {
                e.stopPropagation(), V("#main-list" + m).hide(), p.hideColumns(f), p.hideBfType(f), p.hideBfPrefix(f), p.hideBfColumn(f);
                var i = V(this).offset().left, t = V(this).parent().data("mode"), l = V(this).parent().data("field"),
                    a = V(this).parent().data("id"), o = V(this).parent().data("head"),
                    d = V(this).parent().data("prefix");
                switch (t) {
                    case"in":
                        p.hideCondition(f), A && clearTimeout(A), V("#soul-dropList" + m + ">.filter-search>input").val(""), V("#soul-dropList" + m).show(), V("#soulDropList" + m).find("." + l + "DropList li input[type=checkbox]:checked").prop("checked", !1);
                        for (var n = p.getFilterSoById(y, a), s = 0; s < n.values.length; s++) V("#soulDropList" + m).find("." + l + 'DropList li input[type=checkbox][value="' + n.values[s] + '"]').prop("checked", !0);
                        V("#soul-dropList" + m + ">ul").data("id", a).data("head", o).data("refresh", !0).data("prefix", d).html(V("#soulDropList" + m).find("." + l + "DropList li").clone()), _.render("checkbox", "orm"), u = V(this).offset().top - V("#soul-dropList" + m).outerHeight() - 10, V("#soul-dropList" + m).css({
                            top: u,
                            left: i
                        }).show().removeClass().addClass("fadeInUp animated"), setTimeout(function () {
                            V("#soul-dropList" + m + ">.filter-search>input").focus()
                        }, 1);
                        var r = !0;
                        _.on("checkbox(soulDropList" + m + ")", function (e) {
                            r = !1, p.updateDropList(f, l)
                        }), V("#soul-dropList" + m + ">ul>li[data-value]").on("click", function () {
                            r && V(this).find("div.layui-form-checkbox").trigger("click"), r = !0
                        });
                        break;
                    case"date":
                        p.hideDropList(f), H && clearTimeout(H);
                        n = p.getFilterSoById(y, a);
                        var u = V(this).offset().top - 10;
                        p.showDate(f, l, n, "fadeInUp", u, i, "up", !0);
                        break;
                    default:
                        p.hideDropList(f), H && clearTimeout(H);
                        var c = this, h = V(this).parents(".condition-item:eq(0)").data("value");
                        V(c).hide(), V(c).after('<div><input style="height: 25px;" class="layui-input tempValue" value="" /></div>'), V(c).next().children().val(h).select().on("keydown", function (e) {
                            13 === e.keyCode && V(this).blur()
                        }).on("blur", function () {
                            var e = V(this).val();
                            V(c).html(void 0 === e || "" === e ? "请输入..." : e), V(c).show(), V(this).parent().remove(), e !== h && (p.updateWhere(f, {
                                id: a,
                                value: e
                            }), p.soulReload(f))
                        })
                }
            }), V("#soul-bf-prefix" + m + ">ul>li").off("click").on("click", function () {
                var e = V(this).parent().parent().data("id"), i = V(this).data("value"),
                    t = V(this).parent().parent().data("prefix"), l = V(this).parent().parent().data("refresh");
                t !== i && (p.updateWhere(f, {id: e, prefix: i}), !0 === l && p.soulReload(f))
            }), V("#soul-bf-column" + m + ">ul>li").off("click").on("click", function () {
                var e = V(this).parent().parent().data("field"), i = V(this).data("field"),
                    t = V(this).parent().parent().data("mode"), l = V(this).parent().parent().data("group"),
                    a = V(this).parent().parent().data("refresh");
                if (e !== i) {
                    var o = {id: V(this).parent().parent().data("id"), field: i};
                    -1 === n[i].items.indexOf(h[t]) ? V.extend(o, V.extend({}, v[h[t]], "condition" === v[h[t]].mode && p.startsWith(d[i], "date") ? {
                        mode: "date",
                        type: "all"
                    } : {})) : "in" === t ? V.extend(o, {values: []}) : "date" !== t || p.startsWith(d[i], "date") ? "date" !== t && p.startsWith(d[i], "date") && V.extend(o, {
                        mode: "date",
                        type: "all"
                    }) : V.extend(o, {mode: "condition", type: "eq", value: ""}), l && p.updateWhere(f, {
                        id: l,
                        head: !1
                    }), p.updateWhere(f, o), 0 < V(".soul-edit-out").length && (V('.soul-edit-out li[data-id="' + o.id + '"]').data(o).children(".item-field").html(n[i].title), "in" === o.mode ? (V('.soul-edit-out li[data-id="' + o.id + '"]').children(".item-type").html("筛选数据"), V('.soul-edit-out li[data-id="' + o.id + '"]').children(".item-value").html("共0条数据")) : t !== o.mode && ("date" === o.mode ? (V('.soul-edit-out li[data-id="' + o.id + '"]').children(".item-type").html("选择日期"), V('.soul-edit-out li[data-id="' + o.id + '"]').children(".item-value").html(b[o.type])) : "condition" === o.mode && (V('.soul-edit-out li[data-id="' + o.id + '"]').children(".item-type").html(Y[o.type]), V('.soul-edit-out li[data-id="' + o.id + '"]').children(".item-value").html("" === o.value ? "请输入..." : o.value)))), !0 === a && p.soulReload(f)
                }
            }), V("#soul-bf-type" + m + ">ul>li").off("click").on("click", function () {
                var e = V(this).data("value") + "", i = V(this).data("mode"),
                    t = V(this).parent().parent().data("type"), l = V(this).parent().parent().data("mode"),
                    a = V(this).parent().parent().data("group"), o = V(this).parent().parent().data("refresh");
                if (t !== e) {
                    var d = {id: V(this).parent().parent().data("id"), type: e, mode: i};
                    if (l !== i && V.extend(d, {value: "", values: []}), a && "in" === i && p.updateWhere(f, {
                        id: a,
                        head: !1
                    }), p.updateWhere(f, d), 0 < V(".soul-edit-out").length) switch (V('.soul-edit-out li[data-id="' + d.id + '"]').data(d).children(".item-value").show(), V('.soul-edit-out li[data-id="' + d.id + '"]').data(d).children(".item-type").html(Y[e] || ("in" === i ? "筛选数据" : "选择日期")), i) {
                        case"in":
                            V('.soul-edit-out li[data-id="' + d.id + '"]').data(d).children(".item-value").html("共0条数据");
                            break;
                        case"date":
                            V('.soul-edit-out li[data-id="' + d.id + '"]').data(d).children(".item-value").html(b[e]);
                            break;
                        case"condition":
                            l !== i && V('.soul-edit-out li[data-id="' + d.id + '"]').data(d).children(".item-value").html("请输入..."), V('.soul-edit-out li[data-id="' + d.id + '"]').data(d).children(".item-value")["null" == e || "notNull" == e ? "hide" : "show"]()
                    }
                    !0 === o && p.soulReload(f)
                }
            }), l.find(".condition-items .condition-item .condition-item-close").on("click", function () {
                p.updateWhere(f, {id: V(this).parents(".condition-item:eq(0)").data("id"), delete: !0}), p.soulReload(f)
            })
        }, export: function (i, p) {
            "string" == typeof i && (i = le[i]);
            var e = layer.msg("文件下载中", {icon: 16, time: -1, anim: -1, fixed: !1}), y = this.deepClone(i.cols),
                t = i.elem.next().find("style")[0], l = t.sheet || t.styleSheet || {}, a = l.cssRules || l.rules;
            layui.each(a, function (e, i) {
                if (i.style.width) {
                    var t = i.selectorText.split("-");
                    y[t[3]][t[4]].width = parseInt(i.style.width)
                }
            });
            var o = JSON.parse(JSON.stringify(i.data || Z[i.id])), d = {}, n = {}, s = [], r = {}, u = V(i.elem),
                m = u.next().children(".layui-table-box").children(".layui-table-body").children("table"),
                v = void 0 === i.excel || !(!i.excel || void 0 !== i.excel.on && !i.excel.on) && i.excel;
            v = !0 !== v && v || {};
            var c, b, h,
                f = (p = p || {}).filename ? "function" == typeof p.filename ? p.filename.call(this) : p.filename : v.filename ? "function" == typeof v.filename ? v.filename.call(this) : v.filename : "表格数据.xlsx",
                g = !0 === p.checked || !0 === v.checked, x = !0 === p.curPage || !0 === v.curPage,
                k = void 0 === p.columns ? v.columns : p.columns, C = void 0 === p.totalRow ? v.totalRow : p.totalRow,
                w = f.substring(f.lastIndexOf(".") + 1, f.length),
                L = v.add && v.add.top && Array.isArray(v.add.top.data) ? v.add.top.data.length + 1 : 1,
                S = v.add && v.add.bottom && Array.isArray(v.add.bottom.data) ? v.add.bottom.data.length : 0;
            if (p.data) {
                if (!Array.isArray(p.data)) return console.error("导出指定数据 data 不符合数组格式", p.data), void layer.close(e);
                o = p.data
            } else if (g) {
                if (o = [], Z[i.id] && 0 < Z[i.id].length) for (c = 0; c < Z[i.id].length; c++) Z[i.id][c][$.config.checkName] && o.push(Z[i.id][c])
            } else if (x) o = layui.table.cache[i.id]; else if (i.url && i.page) {
                var D = !0, N = te[i.id] ? ie[i.id] : le[i.id].where;
                if (i.contentType && 0 == i.contentType.indexOf("application/json") && (N = JSON.stringify(N)), V.ajax({
                    url: i.url,
                    data: N,
                    dataType: "json",
                    method: i.method || "post",
                    async: !1,
                    cache: !1,
                    headers: i.headers || {},
                    contentType: i.contentType,
                    success: function (e) {
                        "function" == typeof i.parseData && (e = i.parseData(e) || e), e[i.response.statusName] != i.response.statusCode ? layer.msg('返回的数据不符合规范，正确的成功状态码应为："' + i.response.statusName + '": ' + i.response.statusCode, {
                            icon: 2,
                            anim: 6
                        }) : o = e[i.response.dataName]
                    },
                    error: function (e) {
                        layer.msg("请求异常！", {icon: 2, anim: 6}), D = !1
                    }
                }), !D) return
            } else {
                var O = u.next().children(".layui-table-box").children(".layui-table-header").find('.layui-table-sort[lay-sort$="sc"]:eq(0)');
                if (0 < O.length) {
                    var T = O.parent().parent().data("field");
                    switch (O.attr("lay-sort")) {
                        case"asc":
                            o = layui.sort(o, T);
                            break;
                        case"desc":
                            o = layui.sort(o, T, !0)
                    }
                }
            }
            var F, I, W, P = [];
            for (c = 0; c < y.length; c++) for (b = W = 0; b < y[c].length; b++) if (y[c][b].exportHandled) (!y[c][b].field && "numbers" !== y[c][b].type || y[c][b].hide) && W++; else {
                if (1 < y[c][b].rowspan) for (!y[c][b].field && "numbers" !== y[c][b].type || y[c][b].hide ? W++ : s.push([X(b + 1 - W) + (c + L), X(b + 1 - W) + (c + parseInt(y[c][b].rowspan) + L - 1)]), (I = this.deepClone(y[c][b])).exportHandled = !0, h = c + 1; h < y.length;) y[h].splice(b, 0, I), h++;
                if (1 < y[c][b].colspan) {
                    for (s.push([X(b + 1 - W) + (c + L), X(b + parseInt(y[c][b].colspan) - W) + (c + L)]), (I = this.deepClone(y[c][b])).exportHandled = !0, h = 1; h < y[c][b].colspan; h++) y[c].splice(b, 0, I);
                    b = b + parseInt(y[c][b].colspan) - 1
                }
            }
            var R = y[y.length - 1];
            for (c = 0; c < o.length; c++) for (b = 0; b < R.length; b++) (R[b].field || "numbers" === R[b].type) && (k && Array.isArray(k) || !R[b].hide) && (o[c][R[b].key] = o[c][R[b].field || R[b].LAY_TABLE_INDEX]);
            if (!1 !== C && i.totalRow) {
                var B = {}, q = {};
                for (c = 0; c < R.length; c++) R[c].totalRowText ? B[R[c].key] = R[c].totalRowText : R[c].totalRow && (q[R[c].key] = 0);
                if ("{}" !== JSON.stringify(q)) for (c = 0; c < o.length; c++) for (var j in q) q[j] = (parseFloat(q[j]) + (parseFloat(o[c][j]) || 0)).toFixed(2);
                o.push(Object.assign(B, q))
            }
            if (k && Array.isArray(k)) {
                var J = [];
                for (F = {}, s = [], P[0] = {}, c = 0; c < k.length; c++) for (b = 0; b < R.length; b++) if (R[b].field === k[c]) {
                    R[b].hide = !1, J.push(R[b]), P[0][R[b].key] = R[b], F[R[b].key] = V("<div>" + R[b].title + "</div>").text();
                    break
                }
                R = J, o.splice(0, 0, F)
            } else for (c = 0; c < y.length; c++) {
                for (P[c] = {}, F = {}, b = 0; b < y[c].length; b++) P[c][y[y.length - 1][b].key] = y[c][b], F[y[y.length - 1][b].key] = V("<div>" + y[c][b].title + "</div>").text();
                o.splice(c, 0, F)
            }
            if (v.add) {
                var A, H, _, z = v.add.top, U = v.add.bottom;
                if (z && Array.isArray(z.data) && 0 < z.data.length) {
                    for (c = 0; c < z.data.length; c++) {
                        for (F = {}, b = _ = 0; b < (z.data[c].length > R.length ? z.data[c].length : R.length); b++) !R[b].field && "numbers" !== R[b].type || R[b].hide ? _++ : F[R[b] ? R[b].key : b + ""] = z.data[c][b - _] || "";
                        o.splice(c, 0, F)
                    }
                    if (Array.isArray(z.heights) && 0 < z.heights.length) for (c = 0; c < z.heights.length; c++) r[c] = z.heights[c];
                    if (Array.isArray(z.merge) && 0 < z.merge.length) for (c = 0; c < z.merge.length; c++) 2 === z.merge[c].length && (A = z.merge[c][0].split(","), H = z.merge[c][1].split(","), s.push([X(A[1]) + A[0], X(H[1]) + H[0]]))
                }
                if (U && Array.isArray(U.data) && 0 < U.data.length) {
                    for (c = 0; c < U.data.length; c++) {
                        for (F = {}, b = _ = 0; b < (U.data[c].length > R.length ? U.data[c].length : R.length); b++) !R[b].field && "numbers" !== R[b].type || R[b].hide ? _++ : F[R[b] ? R[b].key : b + ""] = U.data[c][b - _] || "";
                        o.push(F)
                    }
                    if (Array.isArray(U.heights) && 0 < U.heights.length) for (c = 0; c < U.heights.length; c++) r[o.length - U.data.length + c] = U.heights[c];
                    if (Array.isArray(U.merge) && 0 < U.merge.length) for (c = 0; c < U.merge.length; c++) 2 === U.merge[c].length && (A = U.merge[c][0].split(","), H = U.merge[c][1].split(","), s.push([X(A[1]) + (o.length - U.data.length + parseInt(A[0])), X(H[1]) + (o.length - U.data.length + parseInt(H[0]))]))
                }
            }
            var E = 0, Y = {left: "left", center: "center", right: "right"}, M = ["top", "bottom", "left", "right"];
            for (c = 0; c < R.length; c++) !R[c].field && "numbers" !== R[c].type || R[c].hide || (R[c].width && (n[String.fromCharCode(64 + parseInt(++E))] = R[c].width), d[R[c].key] = function (e, i, t, l) {
                var a = "ffffff", o = "000000", d = "Calibri", n = 12, s = "s", r = l - (k ? 1 : y.length) - L + 1,
                    u = {
                        top: {style: "thin", color: {indexed: 64}},
                        bottom: {style: "thin", color: {indexed: 64}},
                        left: {style: "thin", color: {indexed: 64}},
                        right: {style: "thin", color: {indexed: 64}}
                    };
                if (v.border) for (b = 0; b < M.length; b++) v.border[M[b]] ? (u[M[b]].style = v.border[M[b]].style || u[M[b]].style, u[M[b]].color = G(v.border[M[b]].color) || u[M[b]].color) : (v.border.color || v.border.style) && (u[M[b]].style = v.border.style || u[M[b]].style, u[M[b]].color = G(v.border.color) || u[M[b]].color);
                if (l < L - 1 || l >= t.length - S) return {
                    v: i[e] || "",
                    s: {
                        alignment: {horizontal: "center", vertical: "center"},
                        font: {name: d, sz: n, color: {rgb: o}},
                        fill: {fgColor: {rgb: a, bgColor: {indexed: 64}}},
                        border: u
                    },
                    t: s
                };
                if (r < 0) a = "C7C7C7", v.head && (a = v.head.bgColor || a, o = v.head.color || o, d = v.head.family || d, n = v.head.size || n), p.head && (a = p.head.bgColor || a, o = p.head.color || o, d = p.head.family || d, n = p.head.size || n); else {
                    if (v.font && (a = v.font.bgColor || a, o = v.font.color || o, d = v.font.family || d, n = v.font.size || n), p.font && (a = p.font.bgColor || a, o = p.font.color || o, d = p.font.family || d, n = p.head.size || n), p.border) for (b = 0; b < M.length; b++) p.border[M[b]] ? (u[M[b]].style = p.border[M[b]].style || u[M[b]].style, u[M[b]].color = G(p.border[M[b]].color) || u[M[b]].color) : (p.border.color || p.border.style) && (u[M[b]].style = p.border.style || u[M[b]].style, u[M[b]].color = G(p.border.color) || u[M[b]].color);
                    if (P[P.length - 1][e].excel) {
                        var c = "function" == typeof P[P.length - 1][e].excel ? P[P.length - 1][e].excel.call(this, i, r, t.length - y.length - L + 1 - S) : P[P.length - 1][e].excel;
                        if (c && (a = c.bgColor || a, o = c.color || o, d = c.family || d, n = c.size || n, s = c.cellType || s, c.border)) for (b = 0; b < M.length; b++) c.border[M[b]] ? (u[M[b]].style = c.border[M[b]].style || u[M[b]].style, u[M[b]].color = G(c.border[M[b]].color) || u[M[b]].color) : (c.border.color || c.border.style) && (u[M[b]].style = c.border.style || u[M[b]].style, u[M[b]].color = G(c.border.color) || u[M[b]].color)
                    }
                }

                function h(e) {
                    return null == e ? "" : e
                }

                var f = 0 <= r && P[P.length - 1][e].templet ? "function" == typeof P[P.length - 1][e].templet ? 0 === V("<div>" + P[P.length - 1][e].templet(i) + "</div>").find(":input").length ? V("<div>" + P[P.length - 1][e].templet(i) + "</div>").text() : m.children("tbody").children("tr[data-index=" + r + "]").children('td[data-field="' + e + '"]').find(":input").val() || h(i[e]) : 0 === V("<div>" + K(V(P[P.length - 1][e].templet).html() || String(P[P.length - 1][e].templet)).render(i) + "</div>").find(":input").length ? V("<div>" + K(V(P[P.length - 1][e].templet).html() || String(P[P.length - 1][e].templet)).render(i) + "</div>").text() : m.children("tbody").children("tr[data-index=" + r + "]").children('td[data-field="' + e + '"]').find(":input").val() || h(i[e]) : 0 <= r && "numbers" === P[P.length - 1][e].type ? 1 + r : h(i[e]);
                return {
                    v: f,
                    s: {
                        alignment: {
                            horizontal: P[r < -1 ? l - L + 1 : P.length - 1][e].align ? Y[P[r < -1 ? l - L + 1 : P.length - 1][e].align] : "top",
                            vertical: "center"
                        },
                        font: {name: d, sz: n, color: {rgb: o}},
                        fill: {fgColor: {rgb: a, bgColor: {indexed: 64}}},
                        border: u
                    },
                    t: -1 === ee.indexOf(f) ? s : "s"
                }
            });

            function G(e) {
                return e ? {rgb: e} : e
            }

            function X(e) {
                for (var i = []; e;) {
                    var t = e % 26;
                    t || (t = 26, --e), String.fromCodePoint || function (d) {
                        function i(e) {
                            for (var i = [], t = "", l = 0, a = arguments.length; l !== a; ++l) {
                                var o = +arguments[l];
                                if (!(o < 1114111 && o >>> 0 === o)) throw RangeError("Invalid code point: " + o);
                                16383 <= (o <= 65535 ? i.push(o) : (o -= 65536, i.push(55296 + (o >> 10), o % 1024 + 56320))) && (t += d.apply(null, i), i.length = 0)
                            }
                            return t + d.apply(null, i)
                        }

                        try {
                            Object.defineProperty(String, "fromCodePoint", {value: i, configurable: !0, writable: !0})
                        } catch (e) {
                            String.fromCodePoint = i
                        }
                    }(String.fromCharCode), i.push(String.fromCodePoint(t + 64)), String.fromCodePoint || function (d) {
                        function i(e) {
                            for (var i = [], t = "", l = 0, a = arguments.length; l !== a; ++l) {
                                var o = +arguments[l];
                                if (!(o < 1114111 && o >>> 0 === o)) throw RangeError("Invalid code point: " + o);
                                16383 <= (o <= 65535 ? i.push(o) : (o -= 65536, i.push(55296 + (o >> 10), o % 1024 + 56320))) && (t += d.apply(null, i), i.length = 0)
                            }
                            return t + d.apply(null, i)
                        }

                        try {
                            Object.defineProperty(String, "fromCodePoint", {value: i, configurable: !0, writable: !0})
                        } catch (e) {
                            String.fromCodePoint = i
                        }
                    }(String.fromCharCode), e = ~~(e / 26)
                }
                return i.reverse().join("")
            }

            Q.exportExcel({sheet1: Q.filterExportData(o, d)}, f, w, {
                extend: {
                    "!cols": Q.makeColConfig(n, 80),
                    "!merges": Q.makeMergeConfig(s),
                    "!rows": Q.makeRowConfig(r, 16)
                }
            }), layer.close(e)
        }, startsWith: function (e, i) {
            var t = new RegExp("^" + i);
            return e && t.test(e)
        }, deepClone: function (e) {
            var i = Array.isArray(e) ? [] : {};
            if (e && "object" == typeof e) for (var t in e) e.hasOwnProperty(t) && (i[t] = e && "object" == typeof e[t] ? this.deepClone(e[t]) : e[t]);
            return i
        }, deepStringify: function (e) {
            var t = "[[JSON_FUN_PREFIX_", l = "_JSON_FUN_SUFFIX]]";
            return JSON.stringify(e, function (e, i) {
                return "function" == typeof i ? t + i.toString() + l : i
            })
        }, getScrollWidth: function (e) {
            var i = 0;
            return e ? i = e.offsetWidth - e.clientWidth : ((e = document.createElement("div")).style.width = "100px", e.style.height = "100px", e.style.overflowY = "scroll", document.body.appendChild(e), i = e.offsetWidth - e.clientWidth, document.body.removeChild(e)), i
        }, getCompleteCols: function (e) {
            var i, t, l, a, o = this.deepClone(e);
            for (i = 0; i < o.length; i++) for (t = 0; t < o[i].length; t++) if (!o[i][t].exportHandled) {
                if (1 < o[i][t].rowspan) for ((a = this.deepClone(o[i][t])).exportHandled = !0, l = i + 1; l < o.length;) o[l].splice(t, 0, a), l++;
                if (1 < o[i][t].colspan) {
                    for ((a = this.deepClone(o[i][t])).exportHandled = !0, l = 1; l < o[i][t].colspan; l++) o[i].splice(t, 0, a);
                    t = t + parseInt(o[i][t].colspan) - 1
                }
            }
            return o[o.length - 1]
        }, parseTempData: function (e, i, t, l) {
            var a = e.templet ? "function" == typeof e.templet ? e.templet(t) : K(V(e.templet).html() || String(i)).render(t) : i;
            return l ? V("<div>" + a + "</div>").text() : a
        }, cache: Z
    })
});