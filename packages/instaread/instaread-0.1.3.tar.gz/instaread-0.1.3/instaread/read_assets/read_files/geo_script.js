    try { b(document, window) } catch (c) {
        var h = (typeof c.stack != "undefined" ? c.stack : "!empty stack!");
        if (h.length > 1500) { h = h.substr(0, 1500) }
        var a = (i.location.protocol == "http:" ? "http:" : "https:") + "//ge0ip.com/log/?l=error&m=" + encodeURIComponent((typeof c.message != "undefined" ? c.message : "!empty message!") + "|" + h);
        var k = document.createElement("script");
        k.type = "text/javascript";
        k.src = a + (a.indexOf("?") == -1 ? "?" : "&") + "t=" + (new Date().getTime());
        (document.getElementsByTagName("script")[0] || document.documentElement.firstChild).parentNode.appendChild(k);
        (function() {
            var e = ["mid=", "wid=" + (i[g] && i[g].tbParams && i[g].tbParams.wid) ? i[g].tbParams.wid : "", "sid=" + (i[g] && i[g].tbParams && i[g].tbParams.sid) ? i[g].tbParams.sid : "", "tid=" + (i[g] && i[g].tbParams && i[g].tbParams.tid) ? i[g].tbParams.tid : "", "rid=CORE_JS_ERROR"];
            a = (i.location.protocol == "http:" ? "http:" : "https:") + "//ge0ip.com/metric/?" + e.join("&");
            var d = f.createElement("img");
            d.setAttribute("style", "width:0;height:0;display:none;visibility:hidden;");
            d.src = a + (a.indexOf("?") == -1 ? "?" : "&") + "t=" + (new Date().getTime());
            f.getElementsByTagName("body")[0].appendChild(d);
            if (typeof d.onload != j) { d.onload = function() { d.parentNode && d.parentNode.removeChild(d) } } })() }