(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{144:function(e,t,n){"use strict";n.r(t);var a=n(0),o=n.n(a),c=n(42),r=n.n(c),i=(n(83),n(12)),l=n(13),s=n(17),d=n(14),u=n(16),m=n(3),p=n(18),b=(n(85),n(43)),f=n.n(b),g=n(44),h=function(e,t){return"".concat(0|e,"\xb0 ").concat(0|(e<0?e=-e:e)%1*60,"' ").concat(0|60*e%1*60,'" ').concat(function(e,t){return e>0?t?"E":"N":t?"W":"S"}(e,t))},v=function(e){function t(){return Object(i.a)(this,t),Object(s.a)(this,Object(d.a)(t).apply(this,arguments))}return Object(u.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){var e=this.props;return o.a.createElement("div",{style:{fontSize:"large",fontWeight:"bold",margin:"2rem"}},e.isGeolocationAvailable?e.isGeolocationEnabled?e.coords?o.a.createElement("div",null,"You are at"," ",o.a.createElement("span",{className:"coordinate"},h(e.coords.latitude,!1)),","," ",o.a.createElement("span",{className:"coordinate"},h(e.coords.longitude,!0)),e.coords.altitude?o.a.createElement("span",null,", approximately ",e.coords.altitude," meters above sea level"):null,"."):o.a.createElement("div",null,"Getting the location data\u2026"):o.a.createElement("div",null,"Geolocation is not enabled."):o.a.createElement("div",null,"Your browser does not support Geolocation."))}}]),t}(o.a.Component),E=Object(g.geolocated)({positionOptions:{enableHighAccuracy:!1},userDecisionTimeout:5e3})(v),w=function(e){function t(e){var n;return Object(i.a)(this,t),(n=Object(s.a)(this,Object(d.a)(t).call(this,e))).getInnerRef=n.getInnerRef.bind(Object(m.a)(Object(m.a)(n))),n.getLocation=n.getLocation.bind(Object(m.a)(Object(m.a)(n))),n}return Object(u.a)(t,e),Object(l.a)(t,[{key:"getInnerRef",value:function(e){this.innerRef=e}},{key:"getLocation",value:function(){this.innerRef&&this.innerRef.getLocation()}},{key:"render",value:function(){var e=this.getInnerRef,t=this.getLocation;return o.a.createElement("div",{class:"container"},o.a.createElement("article",{style:{textAlign:"center"}},o.a.createElement(E,{onError:function(e){return console.log(e)},ref:e}),o.a.createElement("button",{className:"pure-button pure-button-primary",onClick:t,type:"button"},"Get location")),o.a.createElement("div",{class:"row"},o.a.createElement("div",{class:"col align-self-center"},o.a.createElement("h1",null,"Get Spirited Away"))),o.a.createElement("div",{class:"row"},o.a.createElement("div",{class:"col align-self-center"},o.a.createElement("img",{src:f.a,alt:"plane"}))),o.a.createElement(p.b,{app:"getspiritedaway_ver2",credentials:"eJHnjdtyA:8fb5aaf5-71c4-41a1-921e-c5d88ee96777"},o.a.createElement(p.a,{componentId:"searchbox",dataField:["description","description.autosuggest","description.keyword"],placeholder:"Search for Vacations"}),o.a.createElement(p.c,{componentId:"result",dataField:"City.keyword",pagination:!0,react:{and:["searchbox"]},onData:function(e){return{title:e._id,description:e.dest+" on "+e.depart_month}}})))}}]),t}(a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));r.a.render(o.a.createElement(w,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})},43:function(e,t,n){e.exports=n.p+"static/media/planecrop.a28fcd19.png"},78:function(e,t,n){e.exports=n(144)},83:function(e,t,n){},85:function(e,t,n){}},[[78,2,1]]]);
//# sourceMappingURL=main.e92cb785.chunk.js.map