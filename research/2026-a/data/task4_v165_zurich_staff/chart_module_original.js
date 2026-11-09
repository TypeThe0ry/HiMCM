function _1(data,md){return(
md`# ${data.meta.title} ${data.meta.subtitle} `
)}

function _linecontainer(initMultiLineChart){return(
initMultiLineChart.getChart()
)}

function _initMultiLineChart(makeMultiLineChart,data){return(
new makeMultiLineChart(data.data, data.meta, data.chart)
)}

function _refreshCache(Inputs){return(
Inputs.toggle({ label: "Refresh cache", value: false })
)}

function _data(refreshCache,basicapi,uri)
{
  let refresh = refreshCache;
  return basicapi.data(uri, refresh);
}


function _uri(){return(
"p_entwicklung_der_anzahl_vollzeiteinheiten_an_mittelschulen_und_berufsfachschulen"
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  main.define("module 1", async () => runtime.module((await import("/@bildungsplanungzh/prototyp-line.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.define("module 2", async () => runtime.module((await import("/@bildungsplanungzh/general.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.define("module 3", async () => runtime.module((await import("/d/37f68a80161fefa3@284.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.define("module 4", async () => runtime.module((await import("/@bildungsplanungzh/leucheckboxes.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.variable(observer()).define(["data","md"], _1);
  main.variable(observer("linecontainer")).define("linecontainer", ["initMultiLineChart"], _linecontainer);
  main.variable(observer("initMultiLineChart")).define("initMultiLineChart", ["makeMultiLineChart","data"], _initMultiLineChart);
  main.variable(observer("viewof refreshCache")).define("viewof refreshCache", ["Inputs"], _refreshCache);
  main.variable(observer("refreshCache")).define("refreshCache", ["Generators", "viewof refreshCache"], (G, _) => G.input(_));
  main.variable(observer("data")).define("data", ["refreshCache","basicapi","uri"], _data);
  main.variable(observer("uri")).define("uri", _uri);
  main.define("makeMultiLineChart", ["module 1", "@variable"], (_, v) => v.import("makeMultiLineChart", _));
  main.define("Downmenu", ["module 2", "@variable"], (_, v) => v.import("Downmenu", _));
  main.define("addDropDownContent", ["module 2", "@variable"], (_, v) => v.import("addDropDownContent", _));
  main.define("MetaProcessor", ["module 2", "@variable"], (_, v) => v.import("MetaProcessor", _));
  main.define("formater", ["module 2", "@variable"], (_, v) => v.import("formater", _));
  main.define("getColorScale", ["module 2", "@variable"], (_, v) => v.import("getColorScale", _));
  main.define("swatches", ["module 2", "@variable"], (_, v) => v.import("swatches", _));
  main.define("rotateX", ["module 2", "@variable"], (_, v) => v.import("rotateX", _));
  main.define("mouseOut", ["module 2", "@variable"], (_, v) => v.import("mouseOut", _));
  main.define("basicapi", ["module 2", "@variable"], (_, v) => v.import("basicapi", _));
  main.define("distincts", ["module 3", "@variable"], (_, v) => v.import("distincts", _));
  main.define("style", ["module 3", "@variable"], (_, v) => v.import("style", _));
  main.define("InputsLeuCheckboxGroup", ["module 4", "@variable"], (_, v) => v.import("InputsLeuCheckboxGroup", _));
  return main;
}
