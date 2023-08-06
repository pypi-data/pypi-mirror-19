/*global $ */

$(function () {
    $(".purpose").text("");
    $(".purpose").typed(
        {
            stringsElement: $('#typed-strings'),
            typeSpeed: 70,
            backDelay: 1000,
            loop: true
        }
    );
    $('.carousel').carousel();
    $("#cookie_close").click(function (e) {
        document.cookie = "_eu_cookie_accepted=yes; expires=Tue, 01 Jan 2030 12:00:00 UTC; path=/";
        $("#cookie").slideUp();
        e.preventDefault();
        return true;
    });
    if (document.cookie.search("_eu_cookie_accepted") >= 0) {
        $("#cookie").remove();
    }
});

var _paq = _paq || [];
_paq.push(["disableCookies"]);
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function () {
    var u = "https://piwik.glokta.rami.io/";
    _paq.push(['setTrackerUrl', u + 'piwik.php']);
    _paq.push(['setSiteId', '6']);
    var d = document, g = d.createElement('script'), s = d.getElementsByTagName('script')[0];
    g.type = 'text/javascript';
    g.async = true;
    g.defer = true;
    g.src = u + 'piwik.js';
    s.parentNode.insertBefore(g, s);
})();
