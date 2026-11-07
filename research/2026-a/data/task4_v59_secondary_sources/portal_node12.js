import{s as Ds,d as h,i as p,a as Dn,b as he,c as w,h as Es,e as Ce,f as En,g as Vl,j as _,k as Be,l as ql,m as Ks,o as Js,n as zs,p as Fs,q as hn,r as Ls,t as Zs,u as Ns}from"../chunks/scheduler.CmNYRVFQ.js";import{S as Os,i as Vs,d as v,t as u,a as i,c as I,m as x,b,e as y,g as j}from"../chunks/index.DXm0Gnml.js";import{S as qs,C as Cs,R as Bs,K as Qs,a as Cl,G as Us,Q as H,B as Ws,O as Nl,b as Ol,c as Bl}from"../chunks/ScrollX.wcOFGWlZ.js";import{L as Xs,C as $s,A as Gs}from"../chunks/LgaPrefetch.k_W9YDKU.js";import{e as et,s as at,Q as k,p as nt,a as Ql,r as Ul,C as lt}from"../chunks/VennDiagram.svelte_svelte_type_style_lang.BJQzWOXY.js";import{w as st}from"../chunks/entry.DrGKXdTj.js";import{h as m,p as tt}from"../chunks/setTrackProxy.DjIbdjlZ.js";import{p as ot}from"../chunks/stores.WgdentSZ.js";function rt(t){let a,n=B.title+"",e;return{c(){a=Be("h1"),e=Ns(n),this.h()},l(o){a=Ce(o,"H1",{class:!0});var d=Ls(a);e=Zs(d,n),d.forEach(h),this.h()},h(){he(a,"class","title")},m(o,d){p(o,a,d),Dn(a,e)},p:hn,d(o){o&&h(a)}}}function dt(t){return{c(){this.h()},l(a){this.h()},h(){document.title="Evidence"},m:hn,p:hn,d:hn}}function it(t){let a,n,e,o,d;return document.title=a=B.title,{c(){n=_(),e=Be("meta"),o=_(),d=Be("meta"),this.h()},l(s){n=w(s),e=Ce(s,"META",{property:!0,content:!0}),o=w(s),d=Ce(s,"META",{name:!0,content:!0}),this.h()},h(){var s,M;he(e,"property","og:title"),he(e,"content",((s=B.og)==null?void 0:s.title)??B.title),he(d,"name","twitter:title"),he(d,"content",((M=B.og)==null?void 0:M.title)??B.title)},m(s,M){p(s,n,M),p(s,e,M),p(s,o,M),p(s,d,M)},p(s,M){M&0&&a!==(a=B.title)&&(document.title=a)},d(s){s&&(h(n),h(e),h(o),h(d))}}}function ut(t){var d;let a,n,e=ct(),o=((d=B.og)==null?void 0:d.image)&&ft();return{c(){e&&e.c(),a=_(),o&&o.c(),n=En()},l(s){e&&e.l(s),a=w(s),o&&o.l(s),n=En()},m(s,M){e&&e.m(s,M),p(s,a,M),o&&o.m(s,M),p(s,n,M)},p(s,M){var ve;e.p(s,M),(ve=B.og)!=null&&ve.image&&o.p(s,M)},d(s){s&&(h(a),h(n)),e&&e.d(s),o&&o.d(s)}}}function ct(t){let a,n,e,o,d;return{c(){a=Be("meta"),n=_(),e=Be("meta"),o=_(),d=Be("meta"),this.h()},l(s){a=Ce(s,"META",{name:!0,content:!0}),n=w(s),e=Ce(s,"META",{property:!0,content:!0}),o=w(s),d=Ce(s,"META",{name:!0,content:!0}),this.h()},h(){var s,M;he(a,"name","description"),he(a,"content",B.description),he(e,"property","og:description"),he(e,"content",((s=B.og)==null?void 0:s.description)??B.description),he(d,"name","twitter:description"),he(d,"content",((M=B.og)==null?void 0:M.description)??B.description)},m(s,M){p(s,a,M),p(s,n,M),p(s,e,M),p(s,o,M),p(s,d,M)},p:hn,d(s){s&&(h(a),h(n),h(e),h(o),h(d))}}}function ft(t){let a,n,e;return{c(){a=Be("meta"),n=_(),e=Be("meta"),this.h()},l(o){a=Ce(o,"META",{property:!0,content:!0}),n=w(o),e=Ce(o,"META",{name:!0,content:!0}),this.h()},h(){var o,d;he(a,"property","og:image"),he(a,"content",Ql((o=B.og)==null?void 0:o.image)),he(e,"name","twitter:image"),he(e,"content",Ql((d=B.og)==null?void 0:d.image))},m(o,d){p(o,a,d),p(o,n,d),p(o,e,d)},p:hn,d(o){o&&(h(a),h(n),h(e))}}}function Wl(t){let a,n;return a=new H({props:{queryID:"kpis_total",queryResult:t[1]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&2&&(d.queryResult=e[1]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function Xl(t){let a,n;return a=new H({props:{queryID:"kpis_public",queryResult:t[2]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&4&&(d.queryResult=e[2]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function $l(t){let a,n;return a=new H({props:{queryID:"kpis_private",queryResult:t[3]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&8&&(d.queryResult=e[3]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function Gl(t){let a,n;return a=new H({props:{queryID:"reporting",queryResult:t[4]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&16&&(d.queryResult=e[4]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function es(t){let a,n;return a=new H({props:{queryID:"benchmark",queryResult:t[5]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&32&&(d.queryResult=e[5]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ht(t){let a,n;return a=new Ws({props:{rows:t[5],unitLabel:"Lagos State",stateLabel:""}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&32&&(d.rows=e[5]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function as(t){let a,n;return a=new H({props:{queryID:"enrol_total",queryResult:t[6]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&64&&(d.queryResult=e[6]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ns(t){let a,n;return a=new H({props:{queryID:"enrol_public",queryResult:t[7]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&128&&(d.queryResult=e[7]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ls(t){let a,n;return a=new H({props:{queryID:"enrol_private",queryResult:t[8]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&256&&(d.queryResult=e[8]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ss(t){let a,n;return a=new H({props:{queryID:"sex_total",queryResult:t[9]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&512&&(d.queryResult=e[9]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ts(t){let a,n;return a=new H({props:{queryID:"sex_public",queryResult:t[10]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&1024&&(d.queryResult=e[10]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function os(t){let a,n;return a=new H({props:{queryID:"sex_private",queryResult:t[11]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&2048&&(d.queryResult=e[11]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function rs(t){let a,n;return a=new H({props:{queryID:"schools_total",queryResult:t[12]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&4096&&(d.queryResult=e[12]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ds(t){let a,n;return a=new H({props:{queryID:"schools_public",queryResult:t[13]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&8192&&(d.queryResult=e[13]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function is(t){let a,n;return a=new H({props:{queryID:"schools_private",queryResult:t[14]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&16384&&(d.queryResult=e[14]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function us(t){let a,n;return a=new H({props:{queryID:"ownership_enrol",queryResult:t[15]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&32768&&(d.queryResult=e[15]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function cs(t){let a,n;return a=new H({props:{queryID:"schools_ownership",queryResult:t[16]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&65536&&(d.queryResult=e[16]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function fs(t){let a,n;return a=new H({props:{queryID:"children_map_total",queryResult:t[17]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&131072&&(d.queryResult=e[17]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function hs(t){let a,n;return a=new H({props:{queryID:"children_map_public",queryResult:t[18]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&262144&&(d.queryResult=e[18]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ms(t){let a,n;return a=new H({props:{queryID:"children_map_private",queryResult:t[19]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&524288&&(d.queryResult=e[19]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function mt(t){let a,n;return a=new Gs({props:{data:t[0],geoJsonUrl:"/portal/asc/lgas-H2ZhSMudlMI.geojson",geoId:"id",areaCol:"id",value:"learners",link:"link",title:"Learners by LGA · Tap to Explore",tooltip:[{id:"name",showColumnTitles:!1},{id:"learners",fmt:"#,##0"}],height:300,basemap:"https://basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}{r}.png?key=cb1_2qow_1_fd0b7c4553690499ffe5f00a"}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&1&&(d.data=e[0]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function pt(t){let a,n;return a=new Ol({props:{data:t[0],x:"level",y:"enrolment",yFmt:"#,##0",title:"Learners by Education Level",swapXY:"true",sort:"false"}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&1&&(d.data=e[0]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function wt(t){let a,n;return a=new Ol({props:{data:t[0],x:"level",y:"learners",series:"sex",type:"grouped",yFmt:"#,##0",title:"Learners by Gender & Level",swapXY:"true",sort:"false"}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&1&&(d.data=e[0]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function _t(t){let a,n,e,o,d,s,M,ve,pe,Ke,S,xe;return a=new Nl({props:{total:t[17],pub:t[18],priv:t[19],$$slots:{default:[mt,({data:c})=>({0:c}),({data:c})=>[c?1:0]]},$$scope:{ctx:t}}}),e=new Nl({props:{total:t[6],pub:t[7],priv:t[8],$$slots:{default:[pt,({data:c})=>({0:c}),({data:c})=>[c?1:0]]},$$scope:{ctx:t}}}),d=new Nl({props:{total:t[9],pub:t[10],priv:t[11],$$slots:{default:[wt,({data:c})=>({0:c}),({data:c})=>[c?1:0]]},$$scope:{ctx:t}}}),M=new Ol({props:{data:t[13],x:"label",y:"value",yFmt:"#,##0",title:"Public Schools by Level",swapXY:"true",sort:"false",emptySet:"pass",emptyMessage:"No data available at this level"}}),pe=new Bl({props:{data:t[15],title:"Learners by Ownership"}}),S=new Bl({props:{data:t[16],title:"Schools by Ownership"}}),{c(){y(a.$$.fragment),n=_(),y(e.$$.fragment),o=_(),y(d.$$.fragment),s=_(),y(M.$$.fragment),ve=_(),y(pe.$$.fragment),Ke=_(),y(S.$$.fragment)},l(c){b(a.$$.fragment,c),n=w(c),b(e.$$.fragment,c),o=w(c),b(d.$$.fragment,c),s=w(c),b(M.$$.fragment,c),ve=w(c),b(pe.$$.fragment,c),Ke=w(c),b(S.$$.fragment,c)},m(c,g){x(a,c,g),p(c,n,g),x(e,c,g),p(c,o,g),x(d,c,g),p(c,s,g),x(M,c,g),p(c,ve,g),x(pe,c,g),p(c,Ke,g),x(S,c,g),xe=!0},p(c,g){const we={};g[0]&131072&&(we.total=c[17]),g[0]&262144&&(we.pub=c[18]),g[0]&524288&&(we.priv=c[19]),g[0]&1|g[7]&131072&&(we.$$scope={dirty:g,ctx:c}),a.$set(we);const Se={};g[0]&64&&(Se.total=c[6]),g[0]&128&&(Se.pub=c[7]),g[0]&256&&(Se.priv=c[8]),g[0]&1|g[7]&131072&&(Se.$$scope={dirty:g,ctx:c}),e.$set(Se);const _e={};g[0]&512&&(_e.total=c[9]),g[0]&1024&&(_e.pub=c[10]),g[0]&2048&&(_e.priv=c[11]),g[0]&1|g[7]&131072&&(_e.$$scope={dirty:g,ctx:c}),d.$set(_e);const ye={};g[0]&8192&&(ye.data=c[13]),M.$set(ye);const me={};g[0]&32768&&(me.data=c[15]),pe.$set(me);const Qe={};g[0]&65536&&(Qe.data=c[16]),S.$set(Qe)},i(c){xe||(i(a.$$.fragment,c),i(e.$$.fragment,c),i(d.$$.fragment,c),i(M.$$.fragment,c),i(pe.$$.fragment,c),i(S.$$.fragment,c),xe=!0)},o(c){u(a.$$.fragment,c),u(e.$$.fragment,c),u(d.$$.fragment,c),u(M.$$.fragment,c),u(pe.$$.fragment,c),u(S.$$.fragment,c),xe=!1},d(c){c&&(h(n),h(o),h(s),h(ve),h(Ke)),v(a,c),v(e,c),v(d,c),v(M,c),v(pe,c),v(S,c)}}}function ps(t){let a,n;return a=new H({props:{queryID:"lvl_total_total",queryResult:t[20]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&1048576&&(d.queryResult=e[20]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ws(t){let a,n;return a=new H({props:{queryID:"lvl_total_public",queryResult:t[21]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&2097152&&(d.queryResult=e[21]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function _s(t){let a,n;return a=new H({props:{queryID:"lvl_total_private",queryResult:t[22]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&4194304&&(d.queryResult=e[22]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function vs(t){let a,n;return a=new H({props:{queryID:"lvl_primary_total",queryResult:t[23]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&8388608&&(d.queryResult=e[23]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function xs(t){let a,n;return a=new H({props:{queryID:"lvl_primary_public",queryResult:t[24]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&16777216&&(d.queryResult=e[24]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function bs(t){let a,n;return a=new H({props:{queryID:"lvl_primary_private",queryResult:t[25]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&33554432&&(d.queryResult=e[25]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ys(t){let a,n;return a=new H({props:{queryID:"lvl_jss_total",queryResult:t[26]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&67108864&&(d.queryResult=e[26]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function Ss(t){let a,n;return a=new H({props:{queryID:"lvl_jss_public",queryResult:t[27]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&134217728&&(d.queryResult=e[27]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function Ms(t){let a,n;return a=new H({props:{queryID:"lvl_jss_private",queryResult:t[28]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&268435456&&(d.queryResult=e[28]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function gs(t){let a,n;return a=new H({props:{queryID:"lvl_sss_total",queryResult:t[29]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&536870912&&(d.queryResult=e[29]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function Is(t){let a,n;return a=new H({props:{queryID:"lvl_sss_public",queryResult:t[30]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&1073741824&&(d.queryResult=e[30]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function js(t){let a,n;return a=new H({props:{queryID:"lvl_sss_private",queryResult:t[31]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[1]&1&&(d.queryResult=e[31]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function ks(t){let a,n;return a=new H({props:{queryID:"lvl_iqs_total",queryResult:t[32]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[1]&2&&(d.queryResult=e[32]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function Hs(t){let a,n;return a=new H({props:{queryID:"lvl_iqs_public",queryResult:t[33]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[1]&4&&(d.queryResult=e[33]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function Ts(t){let a,n;return a=new H({props:{queryID:"lvl_iqs_private",queryResult:t[34]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[1]&8&&(d.queryResult=e[34]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function Ys(t){let a,n;return a=new H({props:{queryID:"lvl_techvoc_total",queryResult:t[35]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[1]&16&&(d.queryResult=e[35]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function Rs(t){let a,n;return a=new H({props:{queryID:"lvl_techvoc_public",queryResult:t[36]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[1]&32&&(d.queryResult=e[36]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function As(t){let a,n;return a=new H({props:{queryID:"lvl_techvoc_private",queryResult:t[37]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[1]&64&&(d.queryResult=e[37]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function vt(t){let a,n;return a=new $s({props:{tabs:[{label:"Total",total:t[20],public:t[21],private:t[22]},{label:"Primary",total:t[23],public:t[24],private:t[25]},{label:"JSS",total:t[26],public:t[27],private:t[28]},{label:"SSS",total:t[29],public:t[30],private:t[31]},{label:"IQS",total:t[32],public:t[33],private:t[34]},{label:"Tech/Voc",total:t[35],public:t[36],private:t[37]}],columns:[{key:"enrolment",label:"Learners"},{key:"lt",label:"Learner:Teacher"},{key:"lc",label:"Learner:Classroom"},{key:"ltoilet",label:"Learner:Toilet"},{key:"female_l",label:"Female Learners %"},{key:"femt",label:"Female Teachers %"},{key:"special",label:"Special Needs"}]}}),{c(){y(a.$$.fragment)},l(e){b(a.$$.fragment,e)},m(e,o){x(a,e,o),n=!0},p(e,o){const d={};o[0]&2146435072|o[1]&127&&(d.tabs=[{label:"Total",total:e[20],public:e[21],private:e[22]},{label:"Primary",total:e[23],public:e[24],private:e[25]},{label:"JSS",total:e[26],public:e[27],private:e[28]},{label:"SSS",total:e[29],public:e[30],private:e[31]},{label:"IQS",total:e[32],public:e[33],private:e[34]},{label:"Tech/Voc",total:e[35],public:e[36],private:e[37]}]),a.$set(d)},i(e){n||(i(a.$$.fragment,e),n=!0)},o(e){u(a.$$.fragment,e),n=!1},d(e){v(a,e)}}}function xt(t){let a,n,e,o,d,s,M,ve,pe,Ke,S,xe,c,g,we,Se,_e,ye,me,Qe='<a href="#key-indicators">Key Indicators</a>',_a,Fe,va,Me,ge,Le,Xe,$e,Ge,Ie,je,Ze,ea,aa,na,ke,He,Te,xa,Ue,ba,Ye,Re,Ne,la,sa,ta,Ae,Pe,Oe,oa,ra,da,De,Ee,Ve,ia,ua,ca,be,fa='<a href="#indicators-by-lga">Indicators by LGA</a>',ha,qe,ya,Je=typeof B<"u"&&B.title&&B.hide_title!==!0&&rt();function wa(l,r){return typeof B<"u"&&B.title?it:dt}let We=wa()(t),ze=typeof B=="object"&&ut(),Q=t[1]&&Wl(t),U=t[2]&&Xl(t),T=t[3]&&$l(t),Y=t[4]&&Gl(t),Z=t[5]&&es(t);S=new qs({props:{crumbs:[{name:"Nigeria",link:"/portal/"},{name:"Lagos State",link:null}]}}),c=new Cs({}),we=new Bs({props:{data:t[4]}}),_e=new Qs({props:{total:t[1],pub:t[2],priv:t[3],kpis:[{dx:"jwjKmtVK2wj",title:"Learners",fmt:"int",icon:"users"},{dx:"Dw7f4gs9RcS",title:"Teachers",fmt:"int",icon:"chalkboard-user"},{dx:"DvMfSq5pZSA",title:"Classrooms",fmt:"int",icon:"school"},{dx:"vDmeu4io2Fs",title:"Toilets",fmt:"int",icon:"toilet"}]}}),Fe=new Cl({props:{$$slots:{default:[ht]},$$scope:{ctx:t}}});let W=t[6]&&as(t),X=t[7]&&ns(t),$=t[8]&&ls(t),R=t[9]&&ss(t),A=t[10]&&ts(t),N=t[11]&&os(t),G=t[12]&&rs(t),ee=t[13]&&ds(t),ae=t[14]&&is(t),P=t[15]&&us(t),D=t[16]&&cs(t),O=t[17]&&fs(t),ne=t[18]&&hs(t),le=t[19]&&ms(t);Te=new Us({props:{cols:"2",$$slots:{default:[_t]},$$scope:{ctx:t}}}),Ue=new Xs({});let se=t[20]&&ps(t),E=t[21]&&ws(t),K=t[22]&&_s(t),V=t[23]&&vs(t),te=t[24]&&xs(t),oe=t[25]&&bs(t),re=t[26]&&ys(t),J=t[27]&&Ss(t),z=t[28]&&Ms(t),q=t[29]&&gs(t),de=t[30]&&Is(t),ie=t[31]&&js(t),ue=t[32]&&ks(t),F=t[33]&&Hs(t),L=t[34]&&Ts(t),C=t[35]&&Ys(t),ce=t[36]&&Rs(t),fe=t[37]&&As(t);return qe=new Cl({props:{$$slots:{default:[vt]},$$scope:{ctx:t}}}),{c(){Je&&Je.c(),a=_(),We.c(),n=Be("meta"),e=Be("meta"),ze&&ze.c(),o=En(),d=_(),Q&&Q.c(),s=_(),U&&U.c(),M=_(),T&&T.c(),ve=_(),Y&&Y.c(),pe=_(),Z&&Z.c(),Ke=_(),y(S.$$.fragment),xe=_(),y(c.$$.fragment),g=_(),y(we.$$.fragment),Se=_(),y(_e.$$.fragment),ye=_(),me=Be("h2"),me.innerHTML=Qe,_a=_(),y(Fe.$$.fragment),va=_(),W&&W.c(),Me=_(),X&&X.c(),ge=_(),$&&$.c(),Le=_(),R&&R.c(),Xe=_(),A&&A.c(),$e=_(),N&&N.c(),Ge=_(),G&&G.c(),Ie=_(),ee&&ee.c(),je=_(),ae&&ae.c(),Ze=_(),P&&P.c(),ea=_(),D&&D.c(),aa=_(),O&&O.c(),na=_(),ne&&ne.c(),ke=_(),le&&le.c(),He=_(),y(Te.$$.fragment),xa=_(),y(Ue.$$.fragment),ba=_(),se&&se.c(),Ye=_(),E&&E.c(),Re=_(),K&&K.c(),Ne=_(),V&&V.c(),la=_(),te&&te.c(),sa=_(),oe&&oe.c(),ta=_(),re&&re.c(),Ae=_(),J&&J.c(),Pe=_(),z&&z.c(),Oe=_(),q&&q.c(),oa=_(),de&&de.c(),ra=_(),ie&&ie.c(),da=_(),ue&&ue.c(),De=_(),F&&F.c(),Ee=_(),L&&L.c(),Ve=_(),C&&C.c(),ia=_(),ce&&ce.c(),ua=_(),fe&&fe.c(),ca=_(),be=Be("h2"),be.innerHTML=fa,ha=_(),y(qe.$$.fragment),this.h()},l(l){Je&&Je.l(l),a=w(l);const r=Es("svelte-2igo1p",document.head);We.l(r),n=Ce(r,"META",{name:!0,content:!0}),e=Ce(r,"META",{name:!0,content:!0}),ze&&ze.l(r),o=En(),r.forEach(h),d=w(l),Q&&Q.l(l),s=w(l),U&&U.l(l),M=w(l),T&&T.l(l),ve=w(l),Y&&Y.l(l),pe=w(l),Z&&Z.l(l),Ke=w(l),b(S.$$.fragment,l),xe=w(l),b(c.$$.fragment,l),g=w(l),b(we.$$.fragment,l),Se=w(l),b(_e.$$.fragment,l),ye=w(l),me=Ce(l,"H2",{class:!0,id:!0,"data-svelte-h":!0}),Vl(me)!=="svelte-6tnj8d"&&(me.innerHTML=Qe),_a=w(l),b(Fe.$$.fragment,l),va=w(l),W&&W.l(l),Me=w(l),X&&X.l(l),ge=w(l),$&&$.l(l),Le=w(l),R&&R.l(l),Xe=w(l),A&&A.l(l),$e=w(l),N&&N.l(l),Ge=w(l),G&&G.l(l),Ie=w(l),ee&&ee.l(l),je=w(l),ae&&ae.l(l),Ze=w(l),P&&P.l(l),ea=w(l),D&&D.l(l),aa=w(l),O&&O.l(l),na=w(l),ne&&ne.l(l),ke=w(l),le&&le.l(l),He=w(l),b(Te.$$.fragment,l),xa=w(l),b(Ue.$$.fragment,l),ba=w(l),se&&se.l(l),Ye=w(l),E&&E.l(l),Re=w(l),K&&K.l(l),Ne=w(l),V&&V.l(l),la=w(l),te&&te.l(l),sa=w(l),oe&&oe.l(l),ta=w(l),re&&re.l(l),Ae=w(l),J&&J.l(l),Pe=w(l),z&&z.l(l),Oe=w(l),q&&q.l(l),oa=w(l),de&&de.l(l),ra=w(l),ie&&ie.l(l),da=w(l),ue&&ue.l(l),De=w(l),F&&F.l(l),Ee=w(l),L&&L.l(l),Ve=w(l),C&&C.l(l),ia=w(l),ce&&ce.l(l),ua=w(l),fe&&fe.l(l),ca=w(l),be=Ce(l,"H2",{class:!0,id:!0,"data-svelte-h":!0}),Vl(be)!=="svelte-zuc6mt"&&(be.innerHTML=fa),ha=w(l),b(qe.$$.fragment,l),this.h()},h(){he(n,"name","twitter:card"),he(n,"content","summary_large_image"),he(e,"name","twitter:site"),he(e,"content","@evidence_dev"),he(me,"class","markdown"),he(me,"id","key-indicators"),he(be,"class","markdown"),he(be,"id","indicators-by-lga")},m(l,r){Je&&Je.m(l,r),p(l,a,r),We.m(document.head,null),Dn(document.head,n),Dn(document.head,e),ze&&ze.m(document.head,null),Dn(document.head,o),p(l,d,r),Q&&Q.m(l,r),p(l,s,r),U&&U.m(l,r),p(l,M,r),T&&T.m(l,r),p(l,ve,r),Y&&Y.m(l,r),p(l,pe,r),Z&&Z.m(l,r),p(l,Ke,r),x(S,l,r),p(l,xe,r),x(c,l,r),p(l,g,r),x(we,l,r),p(l,Se,r),x(_e,l,r),p(l,ye,r),p(l,me,r),p(l,_a,r),x(Fe,l,r),p(l,va,r),W&&W.m(l,r),p(l,Me,r),X&&X.m(l,r),p(l,ge,r),$&&$.m(l,r),p(l,Le,r),R&&R.m(l,r),p(l,Xe,r),A&&A.m(l,r),p(l,$e,r),N&&N.m(l,r),p(l,Ge,r),G&&G.m(l,r),p(l,Ie,r),ee&&ee.m(l,r),p(l,je,r),ae&&ae.m(l,r),p(l,Ze,r),P&&P.m(l,r),p(l,ea,r),D&&D.m(l,r),p(l,aa,r),O&&O.m(l,r),p(l,na,r),ne&&ne.m(l,r),p(l,ke,r),le&&le.m(l,r),p(l,He,r),x(Te,l,r),p(l,xa,r),x(Ue,l,r),p(l,ba,r),se&&se.m(l,r),p(l,Ye,r),E&&E.m(l,r),p(l,Re,r),K&&K.m(l,r),p(l,Ne,r),V&&V.m(l,r),p(l,la,r),te&&te.m(l,r),p(l,sa,r),oe&&oe.m(l,r),p(l,ta,r),re&&re.m(l,r),p(l,Ae,r),J&&J.m(l,r),p(l,Pe,r),z&&z.m(l,r),p(l,Oe,r),q&&q.m(l,r),p(l,oa,r),de&&de.m(l,r),p(l,ra,r),ie&&ie.m(l,r),p(l,da,r),ue&&ue.m(l,r),p(l,De,r),F&&F.m(l,r),p(l,Ee,r),L&&L.m(l,r),p(l,Ve,r),C&&C.m(l,r),p(l,ia,r),ce&&ce.m(l,r),p(l,ua,r),fe&&fe.m(l,r),p(l,ca,r),p(l,be,r),p(l,ha,r),x(qe,l,r),ya=!0},p(l,r){typeof B<"u"&&B.title&&B.hide_title!==!0&&Je.p(l,r),We.p(l,r),typeof B=="object"&&ze.p(l,r),l[1]?Q?(Q.p(l,r),r[0]&2&&i(Q,1)):(Q=Wl(l),Q.c(),i(Q,1),Q.m(s.parentNode,s)):Q&&(j(),u(Q,1,1,()=>{Q=null}),I()),l[2]?U?(U.p(l,r),r[0]&4&&i(U,1)):(U=Xl(l),U.c(),i(U,1),U.m(M.parentNode,M)):U&&(j(),u(U,1,1,()=>{U=null}),I()),l[3]?T?(T.p(l,r),r[0]&8&&i(T,1)):(T=$l(l),T.c(),i(T,1),T.m(ve.parentNode,ve)):T&&(j(),u(T,1,1,()=>{T=null}),I()),l[4]?Y?(Y.p(l,r),r[0]&16&&i(Y,1)):(Y=Gl(l),Y.c(),i(Y,1),Y.m(pe.parentNode,pe)):Y&&(j(),u(Y,1,1,()=>{Y=null}),I()),l[5]?Z?(Z.p(l,r),r[0]&32&&i(Z,1)):(Z=es(l),Z.c(),i(Z,1),Z.m(Ke.parentNode,Ke)):Z&&(j(),u(Z,1,1,()=>{Z=null}),I());const ma={};r[0]&16&&(ma.data=l[4]),we.$set(ma);const pa={};r[0]&2&&(pa.total=l[1]),r[0]&4&&(pa.pub=l[2]),r[0]&8&&(pa.priv=l[3]),_e.$set(pa);const un={};r[0]&32|r[7]&131072&&(un.$$scope={dirty:r,ctx:l}),Fe.$set(un),l[6]?W?(W.p(l,r),r[0]&64&&i(W,1)):(W=as(l),W.c(),i(W,1),W.m(Me.parentNode,Me)):W&&(j(),u(W,1,1,()=>{W=null}),I()),l[7]?X?(X.p(l,r),r[0]&128&&i(X,1)):(X=ns(l),X.c(),i(X,1),X.m(ge.parentNode,ge)):X&&(j(),u(X,1,1,()=>{X=null}),I()),l[8]?$?($.p(l,r),r[0]&256&&i($,1)):($=ls(l),$.c(),i($,1),$.m(Le.parentNode,Le)):$&&(j(),u($,1,1,()=>{$=null}),I()),l[9]?R?(R.p(l,r),r[0]&512&&i(R,1)):(R=ss(l),R.c(),i(R,1),R.m(Xe.parentNode,Xe)):R&&(j(),u(R,1,1,()=>{R=null}),I()),l[10]?A?(A.p(l,r),r[0]&1024&&i(A,1)):(A=ts(l),A.c(),i(A,1),A.m($e.parentNode,$e)):A&&(j(),u(A,1,1,()=>{A=null}),I()),l[11]?N?(N.p(l,r),r[0]&2048&&i(N,1)):(N=os(l),N.c(),i(N,1),N.m(Ge.parentNode,Ge)):N&&(j(),u(N,1,1,()=>{N=null}),I()),l[12]?G?(G.p(l,r),r[0]&4096&&i(G,1)):(G=rs(l),G.c(),i(G,1),G.m(Ie.parentNode,Ie)):G&&(j(),u(G,1,1,()=>{G=null}),I()),l[13]?ee?(ee.p(l,r),r[0]&8192&&i(ee,1)):(ee=ds(l),ee.c(),i(ee,1),ee.m(je.parentNode,je)):ee&&(j(),u(ee,1,1,()=>{ee=null}),I()),l[14]?ae?(ae.p(l,r),r[0]&16384&&i(ae,1)):(ae=is(l),ae.c(),i(ae,1),ae.m(Ze.parentNode,Ze)):ae&&(j(),u(ae,1,1,()=>{ae=null}),I()),l[15]?P?(P.p(l,r),r[0]&32768&&i(P,1)):(P=us(l),P.c(),i(P,1),P.m(ea.parentNode,ea)):P&&(j(),u(P,1,1,()=>{P=null}),I()),l[16]?D?(D.p(l,r),r[0]&65536&&i(D,1)):(D=cs(l),D.c(),i(D,1),D.m(aa.parentNode,aa)):D&&(j(),u(D,1,1,()=>{D=null}),I()),l[17]?O?(O.p(l,r),r[0]&131072&&i(O,1)):(O=fs(l),O.c(),i(O,1),O.m(na.parentNode,na)):O&&(j(),u(O,1,1,()=>{O=null}),I()),l[18]?ne?(ne.p(l,r),r[0]&262144&&i(ne,1)):(ne=hs(l),ne.c(),i(ne,1),ne.m(ke.parentNode,ke)):ne&&(j(),u(ne,1,1,()=>{ne=null}),I()),l[19]?le?(le.p(l,r),r[0]&524288&&i(le,1)):(le=ms(l),le.c(),i(le,1),le.m(He.parentNode,He)):le&&(j(),u(le,1,1,()=>{le=null}),I());const cn={};r[0]&1028033|r[7]&131072&&(cn.$$scope={dirty:r,ctx:l}),Te.$set(cn),l[20]?se?(se.p(l,r),r[0]&1048576&&i(se,1)):(se=ps(l),se.c(),i(se,1),se.m(Ye.parentNode,Ye)):se&&(j(),u(se,1,1,()=>{se=null}),I()),l[21]?E?(E.p(l,r),r[0]&2097152&&i(E,1)):(E=ws(l),E.c(),i(E,1),E.m(Re.parentNode,Re)):E&&(j(),u(E,1,1,()=>{E=null}),I()),l[22]?K?(K.p(l,r),r[0]&4194304&&i(K,1)):(K=_s(l),K.c(),i(K,1),K.m(Ne.parentNode,Ne)):K&&(j(),u(K,1,1,()=>{K=null}),I()),l[23]?V?(V.p(l,r),r[0]&8388608&&i(V,1)):(V=vs(l),V.c(),i(V,1),V.m(la.parentNode,la)):V&&(j(),u(V,1,1,()=>{V=null}),I()),l[24]?te?(te.p(l,r),r[0]&16777216&&i(te,1)):(te=xs(l),te.c(),i(te,1),te.m(sa.parentNode,sa)):te&&(j(),u(te,1,1,()=>{te=null}),I()),l[25]?oe?(oe.p(l,r),r[0]&33554432&&i(oe,1)):(oe=bs(l),oe.c(),i(oe,1),oe.m(ta.parentNode,ta)):oe&&(j(),u(oe,1,1,()=>{oe=null}),I()),l[26]?re?(re.p(l,r),r[0]&67108864&&i(re,1)):(re=ys(l),re.c(),i(re,1),re.m(Ae.parentNode,Ae)):re&&(j(),u(re,1,1,()=>{re=null}),I()),l[27]?J?(J.p(l,r),r[0]&134217728&&i(J,1)):(J=Ss(l),J.c(),i(J,1),J.m(Pe.parentNode,Pe)):J&&(j(),u(J,1,1,()=>{J=null}),I()),l[28]?z?(z.p(l,r),r[0]&268435456&&i(z,1)):(z=Ms(l),z.c(),i(z,1),z.m(Oe.parentNode,Oe)):z&&(j(),u(z,1,1,()=>{z=null}),I()),l[29]?q?(q.p(l,r),r[0]&536870912&&i(q,1)):(q=gs(l),q.c(),i(q,1),q.m(oa.parentNode,oa)):q&&(j(),u(q,1,1,()=>{q=null}),I()),l[30]?de?(de.p(l,r),r[0]&1073741824&&i(de,1)):(de=Is(l),de.c(),i(de,1),de.m(ra.parentNode,ra)):de&&(j(),u(de,1,1,()=>{de=null}),I()),l[31]?ie?(ie.p(l,r),r[1]&1&&i(ie,1)):(ie=js(l),ie.c(),i(ie,1),ie.m(da.parentNode,da)):ie&&(j(),u(ie,1,1,()=>{ie=null}),I()),l[32]?ue?(ue.p(l,r),r[1]&2&&i(ue,1)):(ue=ks(l),ue.c(),i(ue,1),ue.m(De.parentNode,De)):ue&&(j(),u(ue,1,1,()=>{ue=null}),I()),l[33]?F?(F.p(l,r),r[1]&4&&i(F,1)):(F=Hs(l),F.c(),i(F,1),F.m(Ee.parentNode,Ee)):F&&(j(),u(F,1,1,()=>{F=null}),I()),l[34]?L?(L.p(l,r),r[1]&8&&i(L,1)):(L=Ts(l),L.c(),i(L,1),L.m(Ve.parentNode,Ve)):L&&(j(),u(L,1,1,()=>{L=null}),I()),l[35]?C?(C.p(l,r),r[1]&16&&i(C,1)):(C=Ys(l),C.c(),i(C,1),C.m(ia.parentNode,ia)):C&&(j(),u(C,1,1,()=>{C=null}),I()),l[36]?ce?(ce.p(l,r),r[1]&32&&i(ce,1)):(ce=Rs(l),ce.c(),i(ce,1),ce.m(ua.parentNode,ua)):ce&&(j(),u(ce,1,1,()=>{ce=null}),I()),l[37]?fe?(fe.p(l,r),r[1]&64&&i(fe,1)):(fe=As(l),fe.c(),i(fe,1),fe.m(ca.parentNode,ca)):fe&&(j(),u(fe,1,1,()=>{fe=null}),I());const fn={};r[0]&2146435072|r[1]&127|r[7]&131072&&(fn.$$scope={dirty:r,ctx:l}),qe.$set(fn)},i(l){ya||(i(Q),i(U),i(T),i(Y),i(Z),i(S.$$.fragment,l),i(c.$$.fragment,l),i(we.$$.fragment,l),i(_e.$$.fragment,l),i(Fe.$$.fragment,l),i(W),i(X),i($),i(R),i(A),i(N),i(G),i(ee),i(ae),i(P),i(D),i(O),i(ne),i(le),i(Te.$$.fragment,l),i(Ue.$$.fragment,l),i(se),i(E),i(K),i(V),i(te),i(oe),i(re),i(J),i(z),i(q),i(de),i(ie),i(ue),i(F),i(L),i(C),i(ce),i(fe),i(qe.$$.fragment,l),ya=!0)},o(l){u(Q),u(U),u(T),u(Y),u(Z),u(S.$$.fragment,l),u(c.$$.fragment,l),u(we.$$.fragment,l),u(_e.$$.fragment,l),u(Fe.$$.fragment,l),u(W),u(X),u($),u(R),u(A),u(N),u(G),u(ee),u(ae),u(P),u(D),u(O),u(ne),u(le),u(Te.$$.fragment,l),u(Ue.$$.fragment,l),u(se),u(E),u(K),u(V),u(te),u(oe),u(re),u(J),u(z),u(q),u(de),u(ie),u(ue),u(F),u(L),u(C),u(ce),u(fe),u(qe.$$.fragment,l),ya=!1},d(l){l&&(h(a),h(d),h(s),h(M),h(ve),h(pe),h(Ke),h(xe),h(g),h(Se),h(ye),h(me),h(_a),h(va),h(Me),h(ge),h(Le),h(Xe),h($e),h(Ge),h(Ie),h(je),h(Ze),h(ea),h(aa),h(na),h(ke),h(He),h(xa),h(ba),h(Ye),h(Re),h(Ne),h(la),h(sa),h(ta),h(Ae),h(Pe),h(Oe),h(oa),h(ra),h(da),h(De),h(Ee),h(Ve),h(ia),h(ua),h(ca),h(be),h(ha)),Je&&Je.d(l),We.d(l),h(n),h(e),ze&&ze.d(l),h(o),Q&&Q.d(l),U&&U.d(l),T&&T.d(l),Y&&Y.d(l),Z&&Z.d(l),v(S,l),v(c,l),v(we,l),v(_e,l),v(Fe,l),W&&W.d(l),X&&X.d(l),$&&$.d(l),R&&R.d(l),A&&A.d(l),N&&N.d(l),G&&G.d(l),ee&&ee.d(l),ae&&ae.d(l),P&&P.d(l),D&&D.d(l),O&&O.d(l),ne&&ne.d(l),le&&le.d(l),v(Te,l),v(Ue,l),se&&se.d(l),E&&E.d(l),K&&K.d(l),V&&V.d(l),te&&te.d(l),oe&&oe.d(l),re&&re.d(l),J&&J.d(l),z&&z.d(l),q&&q.d(l),de&&de.d(l),ie&&ie.d(l),ue&&ue.d(l),F&&F.d(l),L&&L.d(l),C&&C.d(l),ce&&ce.d(l),fe&&fe.d(l),v(qe,l)}}}const B={title:"Lagos State Education Statistics 2024 — Annual School Census | Nigeria DNEMIS",description:"Lagos State education statistics from Nigeria's 2024 Annual School Census: schools, learners, teachers, classrooms and key indicators by LGA — from the Federal Ministry of Education (DNEMIS)."};function bt(t,a,n){let e,o;ql(t,ot,f=>n(187,e=f)),ql(t,Ul,f=>n(193,o=f));let{data:d}=a,{data:s={},customFormattingSettings:M,__db:ve,inputs:pe}=d;Ks(Ul,o="5ef846daf4b912ae3002fb35d3130e07",o);let Ke=et(st(pe));Js(Ke.subscribe(f=>pe=f)),zs(lt,{getCustomFormats:()=>M.customFormats||[]});const S=(f,Ps)=>tt(ve.query,f,{query_name:Ps});at(S),e.params,Fs(()=>!0);let xe={initialData:void 0,initialError:void 0},c=m`select dx, value from census.fact
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`,g=`select dx, value from census.fact
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`;s.kpis_total_data&&(s.kpis_total_data instanceof Error?xe.initialError=s.kpis_total_data:xe.initialData=s.kpis_total_data,s.kpis_total_columns&&(xe.knownColumns=s.kpis_total_columns));let we,Se=!1;const _e=k.createReactive({callback:f=>{n(1,we=f)},execFn:S},{id:"kpis_total",...xe});_e(g,{noResolve:c,...xe}),globalThis[Symbol.for("kpis_total")]={get value(){return we}};let ye={initialData:void 0,initialError:void 0},me=m`select dx, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and category_name like 'Public%' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`,Qe=`select dx, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and category_name like 'Public%' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`;s.kpis_public_data&&(s.kpis_public_data instanceof Error?ye.initialError=s.kpis_public_data:ye.initialData=s.kpis_public_data,s.kpis_public_columns&&(ye.knownColumns=s.kpis_public_columns));let _a,Fe=!1;const va=k.createReactive({callback:f=>{n(2,_a=f)},execFn:S},{id:"kpis_public",...ye});va(Qe,{noResolve:me,...ye}),globalThis[Symbol.for("kpis_public")]={get value(){return _a}};let Me={initialData:void 0,initialError:void 0},ge=m`select dx, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and category_name like 'Private%' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`,Le=`select dx, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and category_name like 'Private%' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`;s.kpis_private_data&&(s.kpis_private_data instanceof Error?Me.initialError=s.kpis_private_data:Me.initialData=s.kpis_private_data,s.kpis_private_columns&&(Me.knownColumns=s.kpis_private_columns));let Xe,$e=!1;const Ge=k.createReactive({callback:f=>{n(3,Xe=f)},execFn:S},{id:"kpis_private",...Me});Ge(Le,{noResolve:ge,...Me}),globalThis[Symbol.for("kpis_private")]={get value(){return Xe}};let Ie={initialData:void 0,initialError:void 0},je=m`select 'total' as mode,
      sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR') then value else 0 end) as submitted,
      sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end) as expected,
      case when sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR') then value else 0 end)
                         / sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR','dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF')
union all
select 'public' as mode,
      sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM') then value else 0 end) as submitted,
      sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end) as expected,
      case when sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM') then value else 0 end)
                         / sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1')
union all
select 'private' as mode,
      sum(case when dx in ('Jx7wWJI1WpR') then value else 0 end) as submitted,
      sum(case when dx in ('q5mnwKasEpF') then value else 0 end) as expected,
      case when sum(case when dx in ('q5mnwKasEpF') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('Jx7wWJI1WpR') then value else 0 end)
                         / sum(case when dx in ('q5mnwKasEpF') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('Jx7wWJI1WpR','q5mnwKasEpF')`,Ze=`select 'total' as mode,
      sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR') then value else 0 end) as submitted,
      sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end) as expected,
      case when sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR') then value else 0 end)
                         / sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR','dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF')
union all
select 'public' as mode,
      sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM') then value else 0 end) as submitted,
      sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end) as expected,
      case when sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM') then value else 0 end)
                         / sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1')
union all
select 'private' as mode,
      sum(case when dx in ('Jx7wWJI1WpR') then value else 0 end) as submitted,
      sum(case when dx in ('q5mnwKasEpF') then value else 0 end) as expected,
      case when sum(case when dx in ('q5mnwKasEpF') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('Jx7wWJI1WpR') then value else 0 end)
                         / sum(case when dx in ('q5mnwKasEpF') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('Jx7wWJI1WpR','q5mnwKasEpF')`;s.reporting_data&&(s.reporting_data instanceof Error?Ie.initialError=s.reporting_data:Ie.initialData=s.reporting_data,s.reporting_columns&&(Ie.knownColumns=s.reporting_columns));let ea,aa=!1;const na=k.createReactive({callback:f=>{n(4,ea=f)},execFn:S},{id:"reporting",...Ie});na(Ze,{noResolve:je,...Ie}),globalThis[Symbol.for("reporting")]={get value(){return ea}};let ke={initialData:void 0,initialError:void 0},He=m`select * from (
select 'total' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='eie1tIO5HtX'
union all
select 'public' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='eie1tIO5HtX'
union all
select 'private' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='eie1tIO5HtX'
union all
select 'total' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='YN2pzjKpi3l'
union all
select 'public' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='YN2pzjKpi3l'
union all
select 'private' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='YN2pzjKpi3l'
union all
select 'total' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='uWkPykwyYn2'
union all
select 'public' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='uWkPykwyYn2'
union all
select 'private' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='uWkPykwyYn2'
union all
select 'total' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'public' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'private' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'total' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='Nc9bgbCb6eO'
union all
select 'public' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='Nc9bgbCb6eO'
union all
select 'private' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='Nc9bgbCb6eO'
union all
select 'total' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
union all
select 'public' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
union all
select 'private' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
) order by mode, ord`,Te=`select * from (
select 'total' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='eie1tIO5HtX'
union all
select 'public' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='eie1tIO5HtX'
union all
select 'private' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='eie1tIO5HtX'
union all
select 'total' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='YN2pzjKpi3l'
union all
select 'public' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='YN2pzjKpi3l'
union all
select 'private' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='YN2pzjKpi3l'
union all
select 'total' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='uWkPykwyYn2'
union all
select 'public' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='uWkPykwyYn2'
union all
select 'private' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='uWkPykwyYn2'
union all
select 'total' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'public' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'private' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'total' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='Nc9bgbCb6eO'
union all
select 'public' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='Nc9bgbCb6eO'
union all
select 'private' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='Nc9bgbCb6eO'
union all
select 'total' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
union all
select 'public' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
union all
select 'private' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
) order by mode, ord`;s.benchmark_data&&(s.benchmark_data instanceof Error?ke.initialError=s.benchmark_data:ke.initialData=s.benchmark_data,s.benchmark_columns&&(ke.knownColumns=s.benchmark_columns));let xa,Ue=!1;const ba=k.createReactive({callback:f=>{n(5,xa=f)},execFn:S},{id:"benchmark",...ke});ba(Te,{noResolve:He,...ke}),globalThis[Symbol.for("benchmark")]={get value(){return xa}};let Ye={initialData:void 0,initialError:void 0},Re=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`,Ne=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`;s.enrol_total_data&&(s.enrol_total_data instanceof Error?Ye.initialError=s.enrol_total_data:Ye.initialData=s.enrol_total_data,s.enrol_total_columns&&(Ye.knownColumns=s.enrol_total_columns));let la,sa=!1;const ta=k.createReactive({callback:f=>{n(6,la=f)},execFn:S},{id:"enrol_total",...Ye});ta(Ne,{noResolve:Re,...Ye}),globalThis[Symbol.for("enrol_total")]={get value(){return la}};let Ae={initialData:void 0,initialError:void 0},Pe=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`,Oe=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`;s.enrol_public_data&&(s.enrol_public_data instanceof Error?Ae.initialError=s.enrol_public_data:Ae.initialData=s.enrol_public_data,s.enrol_public_columns&&(Ae.knownColumns=s.enrol_public_columns));let oa,ra=!1;const da=k.createReactive({callback:f=>{n(7,oa=f)},execFn:S},{id:"enrol_public",...Ae});da(Oe,{noResolve:Pe,...Ae}),globalThis[Symbol.for("enrol_public")]={get value(){return oa}};let De={initialData:void 0,initialError:void 0},Ee=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`,Ve=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`;s.enrol_private_data&&(s.enrol_private_data instanceof Error?De.initialError=s.enrol_private_data:De.initialData=s.enrol_private_data,s.enrol_private_columns&&(De.knownColumns=s.enrol_private_columns));let ia,ua=!1;const ca=k.createReactive({callback:f=>{n(8,ia=f)},execFn:S},{id:"enrol_private",...De});ca(Ve,{noResolve:Ee,...De}),globalThis[Symbol.for("enrol_private")]={get value(){return ia}};let be={initialData:void 0,initialError:void 0},fa=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`,ha=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`;s.sex_total_data&&(s.sex_total_data instanceof Error?be.initialError=s.sex_total_data:be.initialData=s.sex_total_data,s.sex_total_columns&&(be.knownColumns=s.sex_total_columns));let qe,ya=!1;const Je=k.createReactive({callback:f=>{n(9,qe=f)},execFn:S},{id:"sex_total",...be});Je(ha,{noResolve:fa,...be}),globalThis[Symbol.for("sex_total")]={get value(){return qe}};let wa={initialData:void 0,initialError:void 0},Sa=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`,We=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`;s.sex_public_data&&(s.sex_public_data instanceof Error?wa.initialError=s.sex_public_data:wa.initialData=s.sex_public_data,s.sex_public_columns&&(wa.knownColumns=s.sex_public_columns));let ze,Q=!1;const U=k.createReactive({callback:f=>{n(10,ze=f)},execFn:S},{id:"sex_public",...wa});U(We,{noResolve:Sa,...wa}),globalThis[Symbol.for("sex_public")]={get value(){return ze}};let T={initialData:void 0,initialError:void 0},Y=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`,Z=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`;s.sex_private_data&&(s.sex_private_data instanceof Error?T.initialError=s.sex_private_data:T.initialData=s.sex_private_data,s.sex_private_columns&&(T.knownColumns=s.sex_private_columns));let W,X=!1;const $=k.createReactive({callback:f=>{n(11,W=f)},execFn:S},{id:"sex_private",...T});$(Z,{noResolve:Y,...T}),globalThis[Symbol.for("sex_private")]={get value(){return W}};let R={initialData:void 0,initialError:void 0},A=m`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`,N=`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`;s.schools_total_data&&(s.schools_total_data instanceof Error?R.initialError=s.schools_total_data:R.initialData=s.schools_total_data,s.schools_total_columns&&(R.knownColumns=s.schools_total_columns));let G,ee=!1;const ae=k.createReactive({callback:f=>{n(12,G=f)},execFn:S},{id:"schools_total",...R});ae(N,{noResolve:A,...R}),globalThis[Symbol.for("schools_total")]={get value(){return G}};let P={initialData:void 0,initialError:void 0},D=m`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`,O=`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`;s.schools_public_data&&(s.schools_public_data instanceof Error?P.initialError=s.schools_public_data:P.initialData=s.schools_public_data,s.schools_public_columns&&(P.knownColumns=s.schools_public_columns));let ne,le=!1;const se=k.createReactive({callback:f=>{n(13,ne=f)},execFn:S},{id:"schools_public",...P});se(O,{noResolve:D,...P}),globalThis[Symbol.for("schools_public")]={get value(){return ne}};let E={initialData:void 0,initialError:void 0},K=m`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`,V=`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`;s.schools_private_data&&(s.schools_private_data instanceof Error?E.initialError=s.schools_private_data:E.initialData=s.schools_private_data,s.schools_private_columns&&(E.knownColumns=s.schools_private_columns));let te,oe=!1;const re=k.createReactive({callback:f=>{n(14,te=f)},execFn:S},{id:"schools_private",...E});re(V,{noResolve:K,...E}),globalThis[Symbol.for("schools_private")]={get value(){return te}};let J={initialData:void 0,initialError:void 0},z=m`select category_name, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and dx = 'jwjKmtVK2wj' and periodType = 'YEARLY' and pe = '2024'`,q=`select category_name, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and dx = 'jwjKmtVK2wj' and periodType = 'YEARLY' and pe = '2024'`;s.ownership_enrol_data&&(s.ownership_enrol_data instanceof Error?J.initialError=s.ownership_enrol_data:J.initialData=s.ownership_enrol_data,s.ownership_enrol_columns&&(J.knownColumns=s.ownership_enrol_columns));let de,ie=!1;const ue=k.createReactive({callback:f=>{n(15,de=f)},execFn:S},{id:"ownership_enrol",...J});ue(q,{noResolve:z,...J}),globalThis[Symbol.for("ownership_enrol")]={get value(){return de}};let F={initialData:void 0,initialError:void 0},L=m`select 'Public' as category_name, sum(case when dx = 'U8ytqWQMFwD' then value else 0 end) as value
from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024'
union all
select 'Private', sum(case when dx = 'BXTUMWSq4zQ' then value else 0 end)
from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024'`,C=`select 'Public' as category_name, sum(case when dx = 'U8ytqWQMFwD' then value else 0 end) as value
from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024'
union all
select 'Private', sum(case when dx = 'BXTUMWSq4zQ' then value else 0 end)
from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024'`;s.schools_ownership_data&&(s.schools_ownership_data instanceof Error?F.initialError=s.schools_ownership_data:F.initialData=s.schools_ownership_data,s.schools_ownership_columns&&(F.knownColumns=s.schools_ownership_columns));let ce,fe=!1;const l=k.createReactive({callback:f=>{n(16,ce=f)},execFn:S},{id:"schools_ownership",...F});l(C,{noResolve:L,...F}),globalThis[Symbol.for("schools_ownership")]={get value(){return ce}};let r={initialData:void 0,initialError:void 0},ma=m`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024'`,pa=`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024'`;s.children_map_total_data&&(s.children_map_total_data instanceof Error?r.initialError=s.children_map_total_data:r.initialData=s.children_map_total_data,s.children_map_total_columns&&(r.knownColumns=s.children_map_total_columns));let un,cn=!1;const fn=k.createReactive({callback:f=>{n(17,un=f)},execFn:S},{id:"children_map_total",...r});fn(pa,{noResolve:ma,...r}),globalThis[Symbol.for("children_map_total")]={get value(){return un}};let Ma={initialData:void 0,initialError:void 0},ga=m`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact_ownership f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%'`,mn=`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact_ownership f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%'`;s.children_map_public_data&&(s.children_map_public_data instanceof Error?Ma.initialError=s.children_map_public_data:Ma.initialData=s.children_map_public_data,s.children_map_public_columns&&(Ma.knownColumns=s.children_map_public_columns));let Kn,Jn=!1;const zn=k.createReactive({callback:f=>{n(18,Kn=f)},execFn:S},{id:"children_map_public",...Ma});zn(mn,{noResolve:ga,...Ma}),globalThis[Symbol.for("children_map_public")]={get value(){return Kn}};let Ia={initialData:void 0,initialError:void 0},ja=m`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact_ownership f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%'`,pn=`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact_ownership f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%'`;s.children_map_private_data&&(s.children_map_private_data instanceof Error?Ia.initialError=s.children_map_private_data:Ia.initialData=s.children_map_private_data,s.children_map_private_columns&&(Ia.knownColumns=s.children_map_private_columns));let Fn,Ln=!1;const Zn=k.createReactive({callback:f=>{n(19,Fn=f)},execFn:S},{id:"children_map_private",...Ia});Zn(pn,{noResolve:ja,...Ia}),globalThis[Symbol.for("children_map_private")]={get value(){return Fn}};let ka={initialData:void 0,initialError:void 0},Ha=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' 
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,wn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' 
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_total_total_data&&(s.lvl_total_total_data instanceof Error?ka.initialError=s.lvl_total_total_data:ka.initialData=s.lvl_total_total_data,s.lvl_total_total_columns&&(ka.knownColumns=s.lvl_total_total_columns));let Nn,On=!1;const Vn=k.createReactive({callback:f=>{n(20,Nn=f)},execFn:S},{id:"lvl_total_total",...ka});Vn(wn,{noResolve:Ha,...ka}),globalThis[Symbol.for("lvl_total_total")]={get value(){return Nn}};let Ta={initialData:void 0,initialError:void 0},Ya=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_ownership f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,_n=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_ownership f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_total_public_data&&(s.lvl_total_public_data instanceof Error?Ta.initialError=s.lvl_total_public_data:Ta.initialData=s.lvl_total_public_data,s.lvl_total_public_columns&&(Ta.knownColumns=s.lvl_total_public_columns));let qn,Cn=!1;const Bn=k.createReactive({callback:f=>{n(21,qn=f)},execFn:S},{id:"lvl_total_public",...Ta});Bn(_n,{noResolve:Ya,...Ta}),globalThis[Symbol.for("lvl_total_public")]={get value(){return qn}};let Ra={initialData:void 0,initialError:void 0},Aa=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_ownership f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,vn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_ownership f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_total_private_data&&(s.lvl_total_private_data instanceof Error?Ra.initialError=s.lvl_total_private_data:Ra.initialData=s.lvl_total_private_data,s.lvl_total_private_columns&&(Ra.knownColumns=s.lvl_total_private_columns));let Qn,Un=!1;const Wn=k.createReactive({callback:f=>{n(22,Qn=f)},execFn:S},{id:"lvl_total_private",...Ra});Wn(vn,{noResolve:Aa,...Ra}),globalThis[Symbol.for("lvl_total_private")]={get value(){return Qn}};let Pa={initialData:void 0,initialError:void 0},Da=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'Q9AZ29igB6j'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,xn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'Q9AZ29igB6j'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_primary_total_data&&(s.lvl_primary_total_data instanceof Error?Pa.initialError=s.lvl_primary_total_data:Pa.initialData=s.lvl_primary_total_data,s.lvl_primary_total_columns&&(Pa.knownColumns=s.lvl_primary_total_columns));let Xn,$n=!1;const Gn=k.createReactive({callback:f=>{n(23,Xn=f)},execFn:S},{id:"lvl_primary_total",...Pa});Gn(xn,{noResolve:Da,...Pa}),globalThis[Symbol.for("lvl_primary_total")]={get value(){return Xn}};let Ea={initialData:void 0,initialError:void 0},Ka=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'Q9AZ29igB6j' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,bn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'Q9AZ29igB6j' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_primary_public_data&&(s.lvl_primary_public_data instanceof Error?Ea.initialError=s.lvl_primary_public_data:Ea.initialData=s.lvl_primary_public_data,s.lvl_primary_public_columns&&(Ea.knownColumns=s.lvl_primary_public_columns));let el,al=!1;const nl=k.createReactive({callback:f=>{n(24,el=f)},execFn:S},{id:"lvl_primary_public",...Ea});nl(bn,{noResolve:Ka,...Ea}),globalThis[Symbol.for("lvl_primary_public")]={get value(){return el}};let Ja={initialData:void 0,initialError:void 0},za=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'Q9AZ29igB6j' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,yn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'Q9AZ29igB6j' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_primary_private_data&&(s.lvl_primary_private_data instanceof Error?Ja.initialError=s.lvl_primary_private_data:Ja.initialData=s.lvl_primary_private_data,s.lvl_primary_private_columns&&(Ja.knownColumns=s.lvl_primary_private_columns));let ll,sl=!1;const tl=k.createReactive({callback:f=>{n(25,ll=f)},execFn:S},{id:"lvl_primary_private",...Ja});tl(yn,{noResolve:za,...Ja}),globalThis[Symbol.for("lvl_primary_private")]={get value(){return ll}};let Fa={initialData:void 0,initialError:void 0},La=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'LWv2iy1xoW5'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,Sn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'LWv2iy1xoW5'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_jss_total_data&&(s.lvl_jss_total_data instanceof Error?Fa.initialError=s.lvl_jss_total_data:Fa.initialData=s.lvl_jss_total_data,s.lvl_jss_total_columns&&(Fa.knownColumns=s.lvl_jss_total_columns));let ol,rl=!1;const dl=k.createReactive({callback:f=>{n(26,ol=f)},execFn:S},{id:"lvl_jss_total",...Fa});dl(Sn,{noResolve:La,...Fa}),globalThis[Symbol.for("lvl_jss_total")]={get value(){return ol}};let Za={initialData:void 0,initialError:void 0},Na=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'LWv2iy1xoW5' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,Mn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'LWv2iy1xoW5' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_jss_public_data&&(s.lvl_jss_public_data instanceof Error?Za.initialError=s.lvl_jss_public_data:Za.initialData=s.lvl_jss_public_data,s.lvl_jss_public_columns&&(Za.knownColumns=s.lvl_jss_public_columns));let il,ul=!1;const cl=k.createReactive({callback:f=>{n(27,il=f)},execFn:S},{id:"lvl_jss_public",...Za});cl(Mn,{noResolve:Na,...Za}),globalThis[Symbol.for("lvl_jss_public")]={get value(){return il}};let Oa={initialData:void 0,initialError:void 0},Va=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'LWv2iy1xoW5' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,gn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'LWv2iy1xoW5' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_jss_private_data&&(s.lvl_jss_private_data instanceof Error?Oa.initialError=s.lvl_jss_private_data:Oa.initialData=s.lvl_jss_private_data,s.lvl_jss_private_columns&&(Oa.knownColumns=s.lvl_jss_private_columns));let fl,hl=!1;const ml=k.createReactive({callback:f=>{n(28,fl=f)},execFn:S},{id:"lvl_jss_private",...Oa});ml(gn,{noResolve:Va,...Oa}),globalThis[Symbol.for("lvl_jss_private")]={get value(){return fl}};let qa={initialData:void 0,initialError:void 0},Ca=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'o62AI6qkSgS'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,In=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'o62AI6qkSgS'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_sss_total_data&&(s.lvl_sss_total_data instanceof Error?qa.initialError=s.lvl_sss_total_data:qa.initialData=s.lvl_sss_total_data,s.lvl_sss_total_columns&&(qa.knownColumns=s.lvl_sss_total_columns));let pl,wl=!1;const _l=k.createReactive({callback:f=>{n(29,pl=f)},execFn:S},{id:"lvl_sss_total",...qa});_l(In,{noResolve:Ca,...qa}),globalThis[Symbol.for("lvl_sss_total")]={get value(){return pl}};let Ba={initialData:void 0,initialError:void 0},Qa=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'o62AI6qkSgS' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,jn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'o62AI6qkSgS' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_sss_public_data&&(s.lvl_sss_public_data instanceof Error?Ba.initialError=s.lvl_sss_public_data:Ba.initialData=s.lvl_sss_public_data,s.lvl_sss_public_columns&&(Ba.knownColumns=s.lvl_sss_public_columns));let vl,xl=!1;const bl=k.createReactive({callback:f=>{n(30,vl=f)},execFn:S},{id:"lvl_sss_public",...Ba});bl(jn,{noResolve:Qa,...Ba}),globalThis[Symbol.for("lvl_sss_public")]={get value(){return vl}};let Ua={initialData:void 0,initialError:void 0},Wa=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'o62AI6qkSgS' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,kn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'o62AI6qkSgS' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_sss_private_data&&(s.lvl_sss_private_data instanceof Error?Ua.initialError=s.lvl_sss_private_data:Ua.initialData=s.lvl_sss_private_data,s.lvl_sss_private_columns&&(Ua.knownColumns=s.lvl_sss_private_columns));let yl,Sl=!1;const Ml=k.createReactive({callback:f=>{n(31,yl=f)},execFn:S},{id:"lvl_sss_private",...Ua});Ml(kn,{noResolve:Wa,...Ua}),globalThis[Symbol.for("lvl_sss_private")]={get value(){return yl}};let Xa={initialData:void 0,initialError:void 0},$a=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'QdjMpXKVYEs'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,Hn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'QdjMpXKVYEs'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_iqs_total_data&&(s.lvl_iqs_total_data instanceof Error?Xa.initialError=s.lvl_iqs_total_data:Xa.initialData=s.lvl_iqs_total_data,s.lvl_iqs_total_columns&&(Xa.knownColumns=s.lvl_iqs_total_columns));let gl,Il=!1;const jl=k.createReactive({callback:f=>{n(32,gl=f)},execFn:S},{id:"lvl_iqs_total",...Xa});jl(Hn,{noResolve:$a,...Xa}),globalThis[Symbol.for("lvl_iqs_total")]={get value(){return gl}};let Ga={initialData:void 0,initialError:void 0},en=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'QdjMpXKVYEs' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,Tn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'QdjMpXKVYEs' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_iqs_public_data&&(s.lvl_iqs_public_data instanceof Error?Ga.initialError=s.lvl_iqs_public_data:Ga.initialData=s.lvl_iqs_public_data,s.lvl_iqs_public_columns&&(Ga.knownColumns=s.lvl_iqs_public_columns));let kl,Hl=!1;const Tl=k.createReactive({callback:f=>{n(33,kl=f)},execFn:S},{id:"lvl_iqs_public",...Ga});Tl(Tn,{noResolve:en,...Ga}),globalThis[Symbol.for("lvl_iqs_public")]={get value(){return kl}};let an={initialData:void 0,initialError:void 0},nn=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'QdjMpXKVYEs' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,Yn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'QdjMpXKVYEs' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_iqs_private_data&&(s.lvl_iqs_private_data instanceof Error?an.initialError=s.lvl_iqs_private_data:an.initialData=s.lvl_iqs_private_data,s.lvl_iqs_private_columns&&(an.knownColumns=s.lvl_iqs_private_columns));let Yl,Rl=!1;const Al=k.createReactive({callback:f=>{n(34,Yl=f)},execFn:S},{id:"lvl_iqs_private",...an});Al(Yn,{noResolve:nn,...an}),globalThis[Symbol.for("lvl_iqs_private")]={get value(){return Yl}};let ln={initialData:void 0,initialError:void 0},sn=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'buScFFQAJ1g'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,Rn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'buScFFQAJ1g'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_techvoc_total_data&&(s.lvl_techvoc_total_data instanceof Error?ln.initialError=s.lvl_techvoc_total_data:ln.initialData=s.lvl_techvoc_total_data,s.lvl_techvoc_total_columns&&(ln.knownColumns=s.lvl_techvoc_total_columns));let Pl,Dl=!1;const El=k.createReactive({callback:f=>{n(35,Pl=f)},execFn:S},{id:"lvl_techvoc_total",...ln});El(Rn,{noResolve:sn,...ln}),globalThis[Symbol.for("lvl_techvoc_total")]={get value(){return Pl}};let tn={initialData:void 0,initialError:void 0},on=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'buScFFQAJ1g' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,An=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'buScFFQAJ1g' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_techvoc_public_data&&(s.lvl_techvoc_public_data instanceof Error?tn.initialError=s.lvl_techvoc_public_data:tn.initialData=s.lvl_techvoc_public_data,s.lvl_techvoc_public_columns&&(tn.knownColumns=s.lvl_techvoc_public_columns));let Kl,Jl=!1;const zl=k.createReactive({callback:f=>{n(36,Kl=f)},execFn:S},{id:"lvl_techvoc_public",...tn});zl(An,{noResolve:on,...tn}),globalThis[Symbol.for("lvl_techvoc_public")]={get value(){return Kl}};let rn={initialData:void 0,initialError:void 0},dn=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'buScFFQAJ1g' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`,Pn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'buScFFQAJ1g' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`;s.lvl_techvoc_private_data&&(s.lvl_techvoc_private_data instanceof Error?rn.initialError=s.lvl_techvoc_private_data:rn.initialData=s.lvl_techvoc_private_data,s.lvl_techvoc_private_columns&&(rn.knownColumns=s.lvl_techvoc_private_columns));let Fl,Ll=!1;const Zl=k.createReactive({callback:f=>{n(37,Fl=f)},execFn:S},{id:"lvl_techvoc_private",...rn});return Zl(Pn,{noResolve:dn,...rn}),globalThis[Symbol.for("lvl_techvoc_private")]={get value(){return Fl}},t.$$set=f=>{"data"in f&&n(38,d=f.data)},t.$$.update=()=>{t.$$.dirty[1]&128&&n(0,{data:s={},customFormattingSettings:M,__db:ve}=d,s),t.$$.dirty[0]&1&&nt.set(Object.keys(s).length>0),t.$$.dirty[6]&2&&e.params,t.$$.dirty[1]&3840&&(c||!Se?c||(_e(g,{noResolve:c,...xe}),n(42,Se=!0)):_e(g,{noResolve:c})),t.$$.dirty[1]&61440&&(me||!Fe?me||(va(Qe,{noResolve:me,...ye}),n(46,Fe=!0)):va(Qe,{noResolve:me})),t.$$.dirty[1]&983040&&(ge||!$e?ge||(Ge(Le,{noResolve:ge,...Me}),n(50,$e=!0)):Ge(Le,{noResolve:ge})),t.$$.dirty[1]&15728640&&(je||!aa?je||(na(Ze,{noResolve:je,...Ie}),n(54,aa=!0)):na(Ze,{noResolve:je})),t.$$.dirty[1]&251658240&&(He||!Ue?He||(ba(Te,{noResolve:He,...ke}),n(58,Ue=!0)):ba(Te,{noResolve:He})),t.$$.dirty[1]&1879048192|t.$$.dirty[2]&1&&(Re||!sa?Re||(ta(Ne,{noResolve:Re,...Ye}),n(62,sa=!0)):ta(Ne,{noResolve:Re})),t.$$.dirty[2]&30&&(Pe||!ra?Pe||(da(Oe,{noResolve:Pe,...Ae}),n(66,ra=!0)):da(Oe,{noResolve:Pe})),t.$$.dirty[2]&480&&(Ee||!ua?Ee||(ca(Ve,{noResolve:Ee,...De}),n(70,ua=!0)):ca(Ve,{noResolve:Ee})),t.$$.dirty[2]&7680&&(fa||!ya?fa||(Je(ha,{noResolve:fa,...be}),n(74,ya=!0)):Je(ha,{noResolve:fa})),t.$$.dirty[2]&122880&&(Sa||!Q?Sa||(U(We,{noResolve:Sa,...wa}),n(78,Q=!0)):U(We,{noResolve:Sa})),t.$$.dirty[2]&1966080&&(Y||!X?Y||($(Z,{noResolve:Y,...T}),n(82,X=!0)):$(Z,{noResolve:Y})),t.$$.dirty[2]&31457280&&(A||!ee?A||(ae(N,{noResolve:A,...R}),n(86,ee=!0)):ae(N,{noResolve:A})),t.$$.dirty[2]&503316480&&(D||!le?D||(se(O,{noResolve:D,...P}),n(90,le=!0)):se(O,{noResolve:D})),t.$$.dirty[2]&1610612736|t.$$.dirty[3]&3&&(K||!oe?K||(re(V,{noResolve:K,...E}),n(94,oe=!0)):re(V,{noResolve:K})),t.$$.dirty[3]&60&&(z||!ie?z||(ue(q,{noResolve:z,...J}),n(98,ie=!0)):ue(q,{noResolve:z})),t.$$.dirty[3]&960&&(L||!fe?L||(l(C,{noResolve:L,...F}),n(102,fe=!0)):l(C,{noResolve:L})),t.$$.dirty[3]&15360&&(ma||!cn?ma||(fn(pa,{noResolve:ma,...r}),n(106,cn=!0)):fn(pa,{noResolve:ma})),t.$$.dirty[3]&245760&&(ga||!Jn?ga||(zn(mn,{noResolve:ga,...Ma}),n(110,Jn=!0)):zn(mn,{noResolve:ga})),t.$$.dirty[3]&3932160&&(ja||!Ln?ja||(Zn(pn,{noResolve:ja,...Ia}),n(114,Ln=!0)):Zn(pn,{noResolve:ja})),t.$$.dirty[3]&62914560&&(Ha||!On?Ha||(Vn(wn,{noResolve:Ha,...ka}),n(118,On=!0)):Vn(wn,{noResolve:Ha})),t.$$.dirty[3]&1006632960&&(Ya||!Cn?Ya||(Bn(_n,{noResolve:Ya,...Ta}),n(122,Cn=!0)):Bn(_n,{noResolve:Ya})),t.$$.dirty[3]&1073741824|t.$$.dirty[4]&7&&(Aa||!Un?Aa||(Wn(vn,{noResolve:Aa,...Ra}),n(126,Un=!0)):Wn(vn,{noResolve:Aa})),t.$$.dirty[4]&120&&(Da||!$n?Da||(Gn(xn,{noResolve:Da,...Pa}),n(130,$n=!0)):Gn(xn,{noResolve:Da})),t.$$.dirty[4]&1920&&(Ka||!al?Ka||(nl(bn,{noResolve:Ka,...Ea}),n(134,al=!0)):nl(bn,{noResolve:Ka})),t.$$.dirty[4]&30720&&(za||!sl?za||(tl(yn,{noResolve:za,...Ja}),n(138,sl=!0)):tl(yn,{noResolve:za})),t.$$.dirty[4]&491520&&(La||!rl?La||(dl(Sn,{noResolve:La,...Fa}),n(142,rl=!0)):dl(Sn,{noResolve:La})),t.$$.dirty[4]&7864320&&(Na||!ul?Na||(cl(Mn,{noResolve:Na,...Za}),n(146,ul=!0)):cl(Mn,{noResolve:Na})),t.$$.dirty[4]&125829120&&(Va||!hl?Va||(ml(gn,{noResolve:Va,...Oa}),n(150,hl=!0)):ml(gn,{noResolve:Va})),t.$$.dirty[4]&2013265920&&(Ca||!wl?Ca||(_l(In,{noResolve:Ca,...qa}),n(154,wl=!0)):_l(In,{noResolve:Ca})),t.$$.dirty[5]&15&&(Qa||!xl?Qa||(bl(jn,{noResolve:Qa,...Ba}),n(158,xl=!0)):bl(jn,{noResolve:Qa})),t.$$.dirty[5]&240&&(Wa||!Sl?Wa||(Ml(kn,{noResolve:Wa,...Ua}),n(162,Sl=!0)):Ml(kn,{noResolve:Wa})),t.$$.dirty[5]&3840&&($a||!Il?$a||(jl(Hn,{noResolve:$a,...Xa}),n(166,Il=!0)):jl(Hn,{noResolve:$a})),t.$$.dirty[5]&61440&&(en||!Hl?en||(Tl(Tn,{noResolve:en,...Ga}),n(170,Hl=!0)):Tl(Tn,{noResolve:en})),t.$$.dirty[5]&983040&&(nn||!Rl?nn||(Al(Yn,{noResolve:nn,...an}),n(174,Rl=!0)):Al(Yn,{noResolve:nn})),t.$$.dirty[5]&15728640&&(sn||!Dl?sn||(El(Rn,{noResolve:sn,...ln}),n(178,Dl=!0)):El(Rn,{noResolve:sn})),t.$$.dirty[5]&251658240&&(on||!Jl?on||(zl(An,{noResolve:on,...tn}),n(182,Jl=!0)):zl(An,{noResolve:on})),t.$$.dirty[5]&1879048192|t.$$.dirty[6]&1&&(dn||!Ll?dn||(Zl(Pn,{noResolve:dn,...rn}),n(186,Ll=!0)):Zl(Pn,{noResolve:dn}))},n(40,c=m`select dx, value from census.fact
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`),n(41,g=`select dx, value from census.fact
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`),n(44,me=m`select dx, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and category_name like 'Public%' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`),n(45,Qe=`select dx, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and category_name like 'Public%' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`),n(48,ge=m`select dx, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and category_name like 'Private%' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`),n(49,Le=`select dx, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and category_name like 'Private%' and dx in ('jwjKmtVK2wj','Dw7f4gs9RcS','DvMfSq5pZSA','vDmeu4io2Fs')`),n(52,je=m`select 'total' as mode,
      sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR') then value else 0 end) as submitted,
      sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end) as expected,
      case when sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR') then value else 0 end)
                         / sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR','dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF')
union all
select 'public' as mode,
      sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM') then value else 0 end) as submitted,
      sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end) as expected,
      case when sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM') then value else 0 end)
                         / sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1')
union all
select 'private' as mode,
      sum(case when dx in ('Jx7wWJI1WpR') then value else 0 end) as submitted,
      sum(case when dx in ('q5mnwKasEpF') then value else 0 end) as expected,
      case when sum(case when dx in ('q5mnwKasEpF') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('Jx7wWJI1WpR') then value else 0 end)
                         / sum(case when dx in ('q5mnwKasEpF') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('Jx7wWJI1WpR','q5mnwKasEpF')`),n(53,Ze=`select 'total' as mode,
      sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR') then value else 0 end) as submitted,
      sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end) as expected,
      case when sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR') then value else 0 end)
                         / sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','Jx7wWJI1WpR','dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1','q5mnwKasEpF')
union all
select 'public' as mode,
      sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM') then value else 0 end) as submitted,
      sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end) as expected,
      case when sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM') then value else 0 end)
                         / sum(case when dx in ('dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('QLfdf8Jd9dc','Yr6FePoHpHP','OTZHZUXsMeN','zH11dcmH2Pg','SYwA4fNOprM','dh9fliYibms','S2cH9F1T7MU','jZtYw0T5xJl','jSbbKIsSvK3','stoCrMx0ED1')
union all
select 'private' as mode,
      sum(case when dx in ('Jx7wWJI1WpR') then value else 0 end) as submitted,
      sum(case when dx in ('q5mnwKasEpF') then value else 0 end) as expected,
      case when sum(case when dx in ('q5mnwKasEpF') then value else 0 end) > 0
        then round(100.0 * sum(case when dx in ('Jx7wWJI1WpR') then value else 0 end)
                         / sum(case when dx in ('q5mnwKasEpF') then value else 0 end), 1)
        else null end as completeness
    from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024' and dx in ('Jx7wWJI1WpR','q5mnwKasEpF')`),n(56,He=m`select * from (
select 'total' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='eie1tIO5HtX'
union all
select 'public' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='eie1tIO5HtX'
union all
select 'private' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='eie1tIO5HtX'
union all
select 'total' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='YN2pzjKpi3l'
union all
select 'public' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='YN2pzjKpi3l'
union all
select 'private' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='YN2pzjKpi3l'
union all
select 'total' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='uWkPykwyYn2'
union all
select 'public' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='uWkPykwyYn2'
union all
select 'private' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='uWkPykwyYn2'
union all
select 'total' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'public' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'private' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'total' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='Nc9bgbCb6eO'
union all
select 'public' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='Nc9bgbCb6eO'
union all
select 'private' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='Nc9bgbCb6eO'
union all
select 'total' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
union all
select 'public' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
union all
select 'private' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
) order by mode, ord`),n(57,Te=`select * from (
select 'total' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='eie1tIO5HtX'
union all
select 'public' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='eie1tIO5HtX'
union all
select 'private' as mode, 1 as ord, 'Learner–Teacher Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='eie1tIO5HtX'
union all
select 'total' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='YN2pzjKpi3l'
union all
select 'public' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='YN2pzjKpi3l'
union all
select 'private' as mode, 2 as ord, 'Learner–Classroom Ratio' as indicator, 'ratio' as fmt, 35 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='YN2pzjKpi3l'
union all
select 'total' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='uWkPykwyYn2'
union all
select 'public' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='uWkPykwyYn2'
union all
select 'private' as mode, 3 as ord, 'Learner–Toilet Ratio' as indicator, 'ratio' as fmt, 30 as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='uWkPykwyYn2'
union all
select 'total' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'public' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'private' as mode, 4 as ord, 'Learner–School Ratio' as indicator, 'ratio' as fmt, null as std,
    round(1*sum(case when ou='H2ZhSMudlMI' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='wVjDYI2HuQb' then value end),0),1) as unit,
    round(1*sum(case when ou='' and dx in ('jwjKmtVK2wj') then value else 0 end)/nullif(max(case when ou='' and dx='wVjDYI2HuQb' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx in ('jwjKmtVK2wj','wVjDYI2HuQb')
union all
select 'total' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx='Nc9bgbCb6eO'
union all
select 'public' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx='Nc9bgbCb6eO'
union all
select 'private' as mode, 5 as ord, 'Female Learners (%)' as indicator, 'pct' as fmt, null as std,
      round(max(case when ou='H2ZhSMudlMI' then value end),1) as unit,
      round(max(case when ou='' then value end),1) as state
    from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx='Nc9bgbCb6eO'
union all
select 'total' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024'  and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
union all
select 'public' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Public%' and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
union all
select 'private' as mode, 6 as ord, 'Female Teachers (%)' as indicator, 'pct' as fmt, null as std,
    round(100*sum(case when ou='H2ZhSMudlMI' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='H2ZhSMudlMI' and dx='ABJrmFcIpT3' then value end),0),1) as unit,
    round(100*sum(case when ou='' and dx in ('PbzDc38hOsx') then value else 0 end)/nullif(max(case when ou='' and dx='ABJrmFcIpT3' then value end),0),1) as state
  from census.fact_ownership where ou in ('H2ZhSMudlMI', '') and periodType='YEARLY' and pe='2024' and category_name like 'Private%' and dx in ('PbzDc38hOsx','ABJrmFcIpT3')
) order by mode, ord`),n(60,Re=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`),n(61,Ne=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`),n(64,Pe=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`),n(65,Oe=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`),n(68,Ee=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`),n(69,Ve=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5))
select lv.level as level, coalesce(agg.enrolment, 0) as enrolment, lv.ord as ord
from lv left join (
  select case f.dx when 'DiEriq7urPG' then 'Primary' when 'd8qCE7aPWtD' then 'Primary' when 'wDf8ZOwWgib' then 'JSS' when 'IYNEmLyFgbe' then 'SSS' when 'g1ozV2n8G88' then 'IQS' when 'u4ogrV7WUcz' then 'Tech/Voc' end as level, sum(f.value) as enrolment
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('DiEriq7urPG','d8qCE7aPWtD','wDf8ZOwWgib','IYNEmLyFgbe','g1ozV2n8G88','u4ogrV7WUcz') group by 1
) agg on agg.level = lv.level order by lv.ord`),n(72,fa=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`),n(73,ha=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`),n(76,Sa=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`),n(77,We=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`),n(80,Y=m`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`),n(81,Z=`with lv(level, ord) as (values ('Primary',1),('JSS',2),('SSS',3),('IQS',4),('Tech/Voc',5)), sx(sex) as (values ('Male'),('Female'))
select lv.level as level, sx.sex as sex, coalesce(agg.learners, 0) as learners, lv.ord as ord
from lv cross join sx left join (
  select case f.dx when 'L7wp6IPJGhV' then 'Primary' when 'yjH9LAuAMrk' then 'Primary' when 'NnvopxD62MT' then 'Primary' when 'Qwjg1QG0Hws' then 'Primary' when 'gAfSf7sfxib' then 'JSS' when 'uSfibhbGRT1' then 'JSS' when 'i8dMJSyq5hO' then 'SSS' when 'vZA5RaodnuH' then 'SSS' when 'kxJmBoDtD9t' then 'IQS' when 'VzPMQzTjenn' then 'IQS' when 'j3cxHeBhZ4m' then 'Tech/Voc' when 'STJaOAJl6eG' then 'Tech/Voc' end as level, case f.dx when 'L7wp6IPJGhV' then 'Male' when 'yjH9LAuAMrk' then 'Male' when 'NnvopxD62MT' then 'Female' when 'Qwjg1QG0Hws' then 'Female' when 'gAfSf7sfxib' then 'Male' when 'uSfibhbGRT1' then 'Female' when 'i8dMJSyq5hO' then 'Male' when 'vZA5RaodnuH' then 'Female' when 'kxJmBoDtD9t' then 'Male' when 'VzPMQzTjenn' then 'Female' when 'j3cxHeBhZ4m' then 'Male' when 'STJaOAJl6eG' then 'Female' end as sex, sum(f.value) as learners
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('L7wp6IPJGhV','yjH9LAuAMrk','NnvopxD62MT','Qwjg1QG0Hws','gAfSf7sfxib','uSfibhbGRT1','i8dMJSyq5hO','vZA5RaodnuH','kxJmBoDtD9t','VzPMQzTjenn','j3cxHeBhZ4m','STJaOAJl6eG') group by 1, 2
) agg on agg.level = lv.level and agg.sex = sx.sex order by lv.ord, sx.sex desc`),n(84,A=m`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`),n(85,N=`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024'  and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`),n(88,D=m`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`),n(89,O=`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%' and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`),n(92,K=m`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`),n(93,V=`select label, value, ord from (
  select case f.dx when 'v31dkf4PhmH' then 'Primary' when 'I8JeN23lKHn' then 'JSS' when 'tuku316VSXL' then 'SSS' when 'CKMgwHERBfg' then 'IQS' when 'uDBB1WrCkST' then 'Tech/Voc' end as label, case f.dx when 'v31dkf4PhmH' then 1 when 'I8JeN23lKHn' then 2 when 'tuku316VSXL' then 3 when 'CKMgwHERBfg' then 4 when 'uDBB1WrCkST' then 5 end as ord, f.value as value
  from census.fact_ownership f where f.ou = 'H2ZhSMudlMI' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%' and f.dx in ('v31dkf4PhmH','I8JeN23lKHn','tuku316VSXL','CKMgwHERBfg','uDBB1WrCkST')
) order by ord`),n(96,z=m`select category_name, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and dx = 'jwjKmtVK2wj' and periodType = 'YEARLY' and pe = '2024'`),n(97,q=`select category_name, value from census.fact_ownership
where ou = 'H2ZhSMudlMI' and dx = 'jwjKmtVK2wj' and periodType = 'YEARLY' and pe = '2024'`),n(100,L=m`select 'Public' as category_name, sum(case when dx = 'U8ytqWQMFwD' then value else 0 end) as value
from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024'
union all
select 'Private', sum(case when dx = 'BXTUMWSq4zQ' then value else 0 end)
from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024'`),n(101,C=`select 'Public' as category_name, sum(case when dx = 'U8ytqWQMFwD' then value else 0 end) as value
from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024'
union all
select 'Private', sum(case when dx = 'BXTUMWSq4zQ' then value else 0 end)
from census.fact where ou = 'H2ZhSMudlMI' and periodType = 'YEARLY' and pe = '2024'`),n(104,ma=m`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024'`),n(105,pa=`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024'`),n(108,ga=m`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact_ownership f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%'`),n(109,mn=`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact_ownership f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Public%'`),n(112,ja=m`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact_ownership f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%'`),n(113,pn=`select o.id as id, regexp_replace(o.name, '^[a-z]{2} ', '') as name, f.value as learners, '/portal/asc/lga/' || o.id as link
from census.fact_ownership f join census.ou o on f.ou = o.id
where o.parent_id = 'H2ZhSMudlMI' and f.dx = 'jwjKmtVK2wj' and f.periodType = 'YEARLY' and f.pe = '2024' and category_name like 'Private%'`),n(116,Ha=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' 
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(117,wn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' 
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(120,Ya=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_ownership f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(121,_n=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_ownership f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(124,Aa=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_ownership f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(125,vn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_ownership f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(128,Da=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'Q9AZ29igB6j'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(129,xn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'Q9AZ29igB6j'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(132,Ka=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'Q9AZ29igB6j' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(133,bn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'Q9AZ29igB6j' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(136,za=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'Q9AZ29igB6j' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(137,yn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'Q9AZ29igB6j' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(140,La=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'LWv2iy1xoW5'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(141,Sn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'LWv2iy1xoW5'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(144,Na=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'LWv2iy1xoW5' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(145,Mn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'LWv2iy1xoW5' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(148,Va=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'LWv2iy1xoW5' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(149,gn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'LWv2iy1xoW5' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(152,Ca=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'o62AI6qkSgS'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(153,In=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'o62AI6qkSgS'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(156,Qa=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'o62AI6qkSgS' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(157,jn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'o62AI6qkSgS' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(160,Wa=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'o62AI6qkSgS' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(161,kn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'o62AI6qkSgS' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(164,$a=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'QdjMpXKVYEs'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(165,Hn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'QdjMpXKVYEs'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(168,en=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'QdjMpXKVYEs' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(169,Tn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'QdjMpXKVYEs' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(172,nn=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'QdjMpXKVYEs' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(173,Yn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'QdjMpXKVYEs' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(176,sn=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'buScFFQAJ1g'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(177,Rn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_schooltype f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.category_id = 'buScFFQAJ1g'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(180,on=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'buScFFQAJ1g' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(181,An=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'buScFFQAJ1g' and f.cat2_name like 'Public%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(184,dn=m`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'buScFFQAJ1g' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),n(185,Pn=`select regexp_replace(o.name, '^[a-z]{2} ', '') as ou_name, '/portal/asc/lga/' || o.id as link,
  sum(case when f.dx = 'jwjKmtVK2wj' then f.value else 0 end) as enrolment,
  max(case when f.dx = 'Nc9bgbCb6eO' then f.value end) as female_l,
  max(case when f.dx = 'eie1tIO5HtX' then f.value end) as lt,
  max(case when f.dx = 'YN2pzjKpi3l' then f.value end) as lc,
  max(case when f.dx = 'uWkPykwyYn2' then f.value end) as ltoilet,
  case when max(case when f.dx = 'ABJrmFcIpT3' then f.value end) > 0
    then round(100.0 * max(case when f.dx = 'PbzDc38hOsx' then f.value end)
                     / max(case when f.dx = 'ABJrmFcIpT3' then f.value end), 1) end as femt,
  sum(case when f.dx in ('Rszp9Ippq5N','Mmn0SEDyzOC','bCMrPV3785Y','X4cRpKnxayU','kitIA5LU69N') then f.value else 0 end) as special
from census.ou o left join census.fact_typeown f on f.ou = o.id and f.periodType = 'YEARLY' and f.pe = '2024' and f.cat1_id = 'buScFFQAJ1g' and f.cat2_name like 'Private%'
where o.parent_id = 'H2ZhSMudlMI' group by o.name, o.id order by ou_name`),[s,we,_a,Xe,ea,xa,la,oa,ia,qe,ze,W,G,ne,te,de,ce,un,Kn,Fn,Nn,qn,Qn,Xn,el,ll,ol,il,fl,pl,vl,yl,gl,kl,Yl,Pl,Kl,Fl,d,xe,c,g,Se,ye,me,Qe,Fe,Me,ge,Le,$e,Ie,je,Ze,aa,ke,He,Te,Ue,Ye,Re,Ne,sa,Ae,Pe,Oe,ra,De,Ee,Ve,ua,be,fa,ha,ya,wa,Sa,We,Q,T,Y,Z,X,R,A,N,ee,P,D,O,le,E,K,V,oe,J,z,q,ie,F,L,C,fe,r,ma,pa,cn,Ma,ga,mn,Jn,Ia,ja,pn,Ln,ka,Ha,wn,On,Ta,Ya,_n,Cn,Ra,Aa,vn,Un,Pa,Da,xn,$n,Ea,Ka,bn,al,Ja,za,yn,sl,Fa,La,Sn,rl,Za,Na,Mn,ul,Oa,Va,gn,hl,qa,Ca,In,wl,Ba,Qa,jn,xl,Ua,Wa,kn,Sl,Xa,$a,Hn,Il,Ga,en,Tn,Hl,an,nn,Yn,Rl,ln,sn,Rn,Dl,tn,on,An,Jl,rn,dn,Pn,Ll,e]}class Tt extends Os{constructor(a){super(),Vs(this,a,bt,xt,Ds,{data:38},null,[-1,-1,-1,-1,-1,-1,-1,-1])}}export{Tt as component};
