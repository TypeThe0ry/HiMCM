function _1(md){return(
md`# General

Hier sind einige Grundkonfiguationen für die Webgrafiken der Bildungsplanung des Kantons Zürich, welche immer wieder verwendet werden.`
)}

function _2(toc){return(
toc({selector: "h2,h3,h4,h5,h6", heading:"Inhaltsverzeichnis"})
)}

function _3(md){return(
md `## Dropdown-Menü`
)}

function _4(md){return(
md`Der Prototyp Downmenu ermöglicht es ein dropdown-Menü im Layout der Kantons Zürich einzufügen. Es enhält verschiedene Element zum Download und Einbinden der Daten und der Grafik.`
)}

function _5(md){return(
md`### Prototyp`
)}

function _Downmenu(leuDropdown,leuButton,leuDialog,leuRadio,d3,hashCode,createPNG,createSVG,createEmbedCode,createXLSX,createCSV){return(
function (id) {
  leuDropdown;
  leuButton;
  leuDialog;
  leuRadio;
  //create a container for the download menu
  let dropdowncontainer = d3.select("#dropdowncontainer" + id);
  if (dropdowncontainer.empty()) {
    dropdowncontainer = d3.create("div");
  }
  dropdowncontainer
    .attr("id", "dropdowncontainer" + id)
    .attr("class", "dropdown");

  //add a horizontal row at the begining, only activated when the download-menu can be placed a the end of the chart.
  /*if (d3.select("#dropdowncontainer" + id + " hr").empty()) {
    dropdowncontainer.append("hr");
  }*/

  //add the dropdown button
  let dropdownbutton = d3.select("#dropdownbutton" + id);
  if (dropdownbutton.empty()) {
    dropdownbutton = dropdowncontainer.insert("leu-dropdown");
  }
  dropdownbutton.attr("id", "dropdownbutton" + id).attr("label", "Download");

  //add the icon to the button
  let dropdownicon = d3.select("#dropdownbutton" + id + " leu-icon");
  if (dropdownicon.empty()) {
    dropdownicon = dropdownbutton
      .append("leu-icon")
      .attr("slot", "icon")
      .attr("name", "download");
  }

  //add the menu to the button
  let dropdownsub = d3.select("#dropdownbutton" + id + " leu-menu");
  if (dropdownsub.empty()) {
    dropdownsub = dropdownbutton
      .append("leu-menu")
      .attr("role", "menu")
      .attr("selects", "none");
  }

  //function to add actually display the menu
  this.showDropdown = function () {
    return dropdowncontainer.node();
  };

  //function to add the fullscreen menu entry
  this.addSubFullscreen = function () {
    if (!document.getElementById("fullscreen" + id)) {
      dropdownsub
        .insert("leu-menu-item")
        .attr("id", "fullscreen" + id)
        //.attr("href", "#")
        .html(
          `<leu-icon slot="before" name="fullScreen"></leu-icon>
Vollbildanzeige der Grafik`
        )
        .on("mousedown", function () {
          fullscreen(id);
        });
    }
  };

  //function to add the export to png menu entry
  this.addSubPngExport = function (config, label) {
    label = label == undefined ? "Grafik als PNG" : label;
    let dropdownpng = d3.select("#png" + id + hashCode(label));
    if (dropdownpng.empty()) {
      dropdownpng = dropdownsub.insert("leu-menu-item");
    }
    dropdownpng
      .attr("id", "png" + id + hashCode(label))
      //.attr("href", "#")
      .html(
        `<leu-icon slot="before" name="download"></leu-icon>
${label}`
      )
      .on("mousedown", function () {
        createPNG(config);
      });
  };

  //function to add the export to svg menu entry
  this.addSubSvgExport = function (config, label) {
    label = label == undefined ? "Grafik als SVG" : label;
    let dropdownsvg = d3.select("#svg" + id + hashCode(label));
    if (dropdownsvg.empty()) {
      dropdownsvg = dropdownsub.insert("leu-menu-item");
    }
    dropdownsvg
      .attr("id", "svg" + id + hashCode(label))
      //.attr("href", "#")
      .html(
        `<leu-icon slot="before" name="download"></leu-icon>
${label}`
      )
      .on("mousedown", function () {
        createSVG(config);
      });
  };

  //function to add the embed menu entry
  this.addSubEmbed = function () {
    let dropdownembed = d3.select("#embed" + id);
    if (dropdownembed.empty()) {
      dropdownembed = dropdownsub.insert("leu-menu-item");
    }
    dropdownembed
      .attr("id", "embed" + id)
      //.attr("href", "#")
      .html(
        `<leu-icon slot="before" name="share"></leu-icon>
Grafik einbinden`
      )
      .on("mousedown", function () {
        openmodal();
      });

    //generating the actual embed modal view
    let embedmodal = d3.select("#embedmodal" + id);
    if (embedmodal.empty()) {
      embedmodal = d3.select("body").insert("leu-dialog");
    }
    embedmodal
      .attr("id", "embedmodal" + id)
      .attr("label", "Grafik einbinden").html(`
  <!-- Modal content -->
  <leu-radio-group orientation="horizontal">
    <leu-radio value="javascript" checked name="radio-button" tabindex="0" style="margin-bottom: 1rem;">javascript</leu-radio>
    <leu-radio value="iframe" name="radio-button" tabindex="-1">iframe</leu-radio>
</leu-radio-group>
  <div></div>
<textarea class="atm-form_input__input atm-form_input__input--textarea" id="result" 
      cols="1"
      rows="5"
      readonly
      ></textarea>
  <slot slot="actionbar">
    <leu-button id="close" variant="secondary" size="regular" type="button" onclick="document.querySelector('#embedmodal${id}').close()">
      Schliessen
      <leu-icon slot="after" name="close"></leu-icon>
    </leu-button>
    <leu-button id="copycode" size="regular" variant="primary" type="button" onclick="document.querySelector('#embedmodal${id} textarea#result').select();
document.execCommand('copy');">
      Code kopieren
      <leu-icon slot="after" name="files"></leu-icon>
    </leu-button>
  </slot>`);

    document.querySelector("#embedmodal" + id + " leu-radio-group").onchange =
      function (e) {
        document.querySelector("#embedmodal" + id + " textarea#result").value =
          createEmbedCode(id, e.target.value);
      };

    // Get the modal
    let modal = d3.select("#embedmodal" + id).node();

    // When the user clicks on the button, open the modal
    let openmodal = function () {
      document.querySelector("#embedmodal" + id + " textarea#result").value =
        createEmbedCode(
          id,
          document.querySelector("#embedmodal" + id + " leu-radio-group").value
        );
      document.querySelector("#embedmodal" + id).show();
    };
  };

  //function to add the excel export menu entry
  this.addSubExcelExport = function (config, label) {
    label = label == undefined ? "Daten als XLSX" : label;
    let dropdownxlsx = d3.select("#excel" + id + hashCode(label));
    if (dropdownxlsx.empty()) {
      dropdownxlsx = dropdownsub.insert("leu-menu-item");
    }
    dropdownxlsx
      .attr("id", "excel" + id + hashCode(label))
      //.attr("href", "#")
      .html(
        `<leu-icon slot="before" name="download"></leu-icon>
${label}`
      )
      .on("mousedown", function () {
        createXLSX(config);
      });
  };

  //function to add the csv export menu entry
  this.addSubCsvExport = function (config, label) {
    label = label == undefined ? "Daten als CSV" : label;
    let dropdowncsv = d3.select("#csv" + id + hashCode(label));
    if (dropdowncsv.empty()) {
      dropdowncsv = dropdownsub.insert("leu-menu-item");
    }
    dropdowncsv
      .attr("id", "csv" + id + hashCode(label))
      //.attr("href", "#")
      .html(
        `<leu-icon slot="before" name="download"></leu-icon>
${label}`
      )
      .on("mousedown", function () {
        createCSV(config);
      });
  };

  //helper function to create the config for the xlsx export
  this.createXLSXConfig = function (
    data,
    meta,
    filterValues,
    filtered = false
  ) {
    let config = {};
    let columns = [];
    let columnNames = [];
    let types = [];
    let filterText = "";
    if (meta.columns != undefined) {
      //if the collumn is displayed or if it is a filter column and filters are deactivated, add it to the columns for the export.
      let columnsmeta = meta.columns.filter(
        (d) => d.display || (filtered == false && d.filter)
      );
      //order by the column "order"
      columnsmeta.sort((a, b) => a.order - b.order);
      //loop through all the columns
      for (const i of columnsmeta) {
        columns.push(i.columnKey);
        columnNames.push(i.columnName);
        types.push(i.type);
      }
    } else {
      columns = data.columns;
      columnNames = data.columns;
      for (var i = 0; i < columns.length; i++) types.push("string");
    }
    //create config object
    Object.assign(config, {
      data: data,
      columns: columns,
      columnNames: columnNames,
      datatypes: types,
      title: meta.title,
      //Add Filters to the subtitle and the filename
      subtitle:
        meta.subtitle +
        (filtered ? `\nFilter: ` + objToString(filterValues) : ""),
      description: meta.description,
      source: meta.source,
      autofilters: true,
      filename:
        meta.title +
        (filtered ? "; " + objToString(filterValues) : "") +
        ".xlsx"
    });
    return config;
  };

  //helper function to create the config for the csv export
  this.createCSVConfig = function (data, meta, filterValues, filtered = false) {
    let config = {};
    let columns = [];
    let columnNames = [];
    let order = [];
    //loop through all the columns
    if (meta.columns != undefined) {
      //if the collumn is displayed or if it is a filter column and filters are deactivated, add it to the columns for the export.
      let columnsmeta = meta.columns.filter(
        (d) => d.display || (filtered == false && d.filter)
      );
      //order by the column "order"
      columnsmeta.sort((a, b) => a.order - b.order);
      for (const i of meta.columns) {
        columns.push(i.columnKey);
        columnNames.push(i.columnName);
      }
      //create a new data object for the csv export
      data = data.map((obj) => {
        let temp = {};
        for (let i = 0; i < columns.length; ++i) {
          temp[columnNames[i]] = obj[columns[i]];
        }
        return temp;
      });
    }
    //create the config object
    Object.assign(config, {
      data: data,
      //Add Filters to the filename
      filename:
        meta.title + (filtered ? "; " + objToString(filterValues) : "") + ".csv"
    });
    return config;
  };

  function objToString(obj) {
    let str = "";
    for (const [p, val] of Object.entries(obj)) {
      if (str != "") {
        str += "; ";
      }
      str += `${p} = ${val}`;
    }
    return str;
  }

  let fullscreen = function (id) {
    let elem = document.getElementById("dropdowncontainer" + id).parentElement;
    let tag = document
      .getElementById("fullscreen" + id)
      .getElementsByTagName("span")[0];
    if (document.fullscreenElement == null) {
      if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.webkitRequestFullscreen) {
        /* Safari */
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) {
        /* IE11 */
        elem.msRequestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.webkitExitFullscreen) {
        /* Safari */
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) {
        /* IE11 */
        document.msExitFullscreen();
      }
    }
    elem.onfullscreenchange = (event) => {
      if (document.fullscreenElement) {
        elem.classList.add("observable-fullscreen");
        tag.innerHTML = "Vollbild verlassen";
        console.log("Entered fullscreen mode.");
      } else {
        elem.classList.remove("observable-fullscreen");
        console.log("Leaving fullscreen mode.");
        tag.innerHTML = "Vollbild";
      }
    };
  };
}
)}

function _addDropDownContent(){return(
function (
  meta,
  chartconfig,
  containerId,
  uid,
  downmenu,
  data,
  filteredData,
  filterValues
) {
  //console.log(downmenu);
  // add elements to the drop down menu
  if (chartconfig.fullscreen) {
    downmenu.addSubFullscreen();
  }
  if (chartconfig.embed) {
    downmenu.addSubEmbed();
  }
  if (chartconfig.downloadpng) {
    downmenu.addSubPngExport({
      containerId: containerId + uid,
      filename: meta.title + ".png"
    });
  }
  if (chartconfig.downloadsvg) {
    downmenu.addSubSvgExport({
      containerId: containerId + uid,
      filename: meta.title + ".svg"
    });
  }
  if (chartconfig.downloadxlsxall) {
    downmenu.addSubExcelExport(
      downmenu.createXLSXConfig(data, meta, filterValues, false),
      chartconfig.downloadxlsx ? "Daten als XLSX (Alle)" : "Daten als XLSX"
    );
  }
  if (chartconfig.downloadxlsx) {
    downmenu.addSubExcelExport(
      downmenu.createXLSXConfig(filteredData, meta, filterValues, true),
      chartconfig.downloadxlsxall
        ? "Daten als XLSX (Auswahl)"
        : "Daten als XLSX"
    );
  }
  if (chartconfig.downloadcsvall) {
    downmenu.addSubCsvExport(
      downmenu.createCSVConfig(data, meta, filterValues, false),
      chartconfig.downloadcsv ? "Daten als CSV (Alle)" : "Daten als CSV"
    );
  }
  if (chartconfig.downloadcsv) {
    downmenu.addSubCsvExport(
      downmenu.createCSVConfig(filteredData, meta, filterValues, true),
      chartconfig.downloadcsvall ? "Daten als CSV (Auswahl)" : "Daten als CSV"
    );
  }
}
)}

function _8(md){return(
md`### Einbindebeispiel
#### Objekt generieren`
)}

function _downmenu(Downmenu){return(
new Downmenu("2")
)}

function _10(md){return(
md`#### Objekt anzeigen

Eigentliche Links funktionieren nicht, weil nicht konfiguriert.`
)}

function _showDropdown(downmenu){return(
downmenu.showDropdown()
)}

function _12(md){return(
md`#### Methode für Untermenü einfügen`
)}

function _13(md){return(
md`Die eingefügten Knöpfe funktioneren aufgrund der fehlenden Konfiguration nicht. Es wird nur der Knopf eingefügt.`
)}

function _addAllButtons(downmenu)
{
  downmenu.addSubFullscreen();
  downmenu.addSubEmbed();
  downmenu.addSubPngExport();
  downmenu.addSubSvgExport();
  downmenu.addSubExcelExport();
  downmenu.addSubCsvExport();
}


function _dropdownstyle(html){return(
html`<style>

/* The container <div> - needed to position the dropdown content */
.dropdown {
  float: right;
  position: relative;
  clear: right;
  height: 32px;
}

/* Safari */
:-webkit-full-screen {
  background-color: #fff;
  padding: 15px;
  overflow: scroll !important;
}

/* IE11 syntax */
:-ms-fullscreen {
  background-color: #fff;
  padding: 15px;
  overflow: scroll !important;
}

/* Standard syntax */
:fullscreen {
  background-color: #fff;
  padding: 15px;
  overflow: scroll !important;
}

/* Class to hide element, needed for fullscreen metadata display */
.hiddenmeta {display:none;}

.observable-fullscreen .hiddenmeta,
.observable-print .hiddenmeta {display:block;}

.observable-print .noprint {display:none;}

/* Styling selects according to the zhweb design system */
.dataTables_wrapper .dataTables_length select,
select {
  margin-top:5px;
  //-moz-appearance: none;
  //-webkit-appearance: none;
  //appearance: none;
  //background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8nwYAAmoBZ0eMiB8AAAAASUVORK5CYII=) repeat;
  background-color: #fff;
  border: 2px solid rgba(0, 0, 0, 0.6);
  border-radius: 1px;
  box-shadow: 0 0 0px rgba(0, 0, 0, 0.16), 0 0 0px rgba(0, 0, 0, 0.32);
  //color: #fff;
  //cursor: pointer;
  //font-family: 'Open Sans', sans-serif;
  //font-size: 10px;
  height: 40px;
  //outline: none;
  padding-left: 10px;
  width: 100%;
}

.dataTables_wrapper .dataTables_length select:hover,
select:focus {
  border: 2px solid #009ee0;
}

.dataTables_wrapper .dataTables_length select:active,
select:active {
  border: 2px solid #009ee0;
}

.dataTables_wrapper .dataTables_length select option,
select option {
  //color: #fff !important;
  background-color: #fff;
  border-radius: 1px !important;
}

.dataTables_wrapper .dataTables_length select::-ms-expand,
select::-ms-expand {
  display: none;
}

.dataTables_wrapper .dataTables_length select:focus::-ms-value,
select:focus::-ms-value {
  background-color: transparent;
}

label {
  hyphens: auto;
}

/* Styling radio inputs according to the zhweb design system */
label > input[type="radio"] {
  /* Add if not using autoprefixer */
  -webkit-appearance: none;
  /* Remove most all native input styles */
  appearance: none;
  /* For iOS < 15 */
  background-color: var(--form-background);
  /* Not removed via appearance */
  margin: 12px 0 12px 0;

  font: inherit;
  color: #009ee0;
  width: 1.65em;
  height: 1.65em;
  border: 0.15em solid rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  transform: translateY(-0.075em);

  display: grid;
  place-content: center;
}

label > input[type="radio"]:checked {
  border: 0.15em solid #009ee0;
  border-radius: 50%;
}

label > input[type="radio"]:hover {
  border: 0.15em solid #009ee0;
  border-radius: 50%;
}

label > input[type="radio"]::before {
  content: "";
  width: 0.85em;
  height: 0.85em;
  border-radius: 50%;
  transform: scale(0);
  /*transition: 120ms transform ease-in-out;*/
  box-shadow: inset 1.25em 1.25em #009ee0;
  transition:.2s transform ease;
}

label > input[type="radio"]:checked::before {
  transform: scale(1);
}

/* Styling text inputs according to the zhweb design system */
/*input[type=text] {
  padding: .625rem 3rem .625rem 1rem;
  -webkit-appearance: none;
  border: 2px solid #949494;
  border-radius: 2px;
  display: block;
  font-size: 1rem;
  line-height: 1.5;
  order: 1;
  width: 100%;
}

input[type=text]:focus {
  border: 2px solid #009ee0;
}

input[type=text]:active {
  border: 2px solid #009ee0;
}

input[type=text] option {
  //color: #fff !important;
  background-color: #fff;
  border-radius: 1px !important;
}

input[type=text]::-ms-expand {
  display: none;
}

input[type=text]:focus::-ms-value {
  background-color: transparent;
}*/

*,
*::before,
*::after {
  box-sizing: border-box;
}

 /* The Modal (background) */
.embedmodal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1000000; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

.atm-radiobutton input {
  border: none;
}

.bold {
  font-weight: bold !important;
}

/* Figure caption */
.fig-title {
  color: #000;
  font-size: 20px;
  line-height: 1.3;
  margin-bottom: 0;
  margin-top:0;
  font-family:InterBlack,Arial Black,Helvetica,sans-serif;
  font-weight: 400 !important;
  -webkit-hyphens:auto;
  -ms-hyphens:auto;
  hyphens:auto;
}

.fig-subtitle {
  color: rgba(0,0,0,.6);
  font-size: 18px;
  line-height:1.3;
  font-family:InterRegular, Helvetica, sans-serif;
  margin-top:0;
  margin-bottom: 15px;
  -webkit-hyphens:auto;
  -ms-hyphens:auto;
  hyphens:auto;
}

figure.chart {
  margin: 0pt;
  max-width:none;
}
`
)}

function _16(md){return(
md`## Metadatenverarbeitung`
)}

function _17(md){return(
md`In diesem Abschnitt wird ein Prototyp generiert der die standardisierten Metadaten einer Darstellung verarbeitet.`
)}

function _MetaProcessor(hashCode,d3,svgicons,dropdownstyle,leuStyleSheet,readingExample){return(
function (meta, containerId = "container") {
  const uid = hashCode(
    meta.title + meta.subtitle + meta.description + containerId
  );

  //find existing container
  let container = d3.select("#" + containerId + uid);
  //create container if it doesn't exist yet
  if (container.empty()) {
    container = d3
      .create("figure")
      .attr("id", containerId + uid)
      .attr("class", "chart");
  }

  //Append some general
  //container.append(() => stylesheet);
  //container.append(() => manualstylesheet);
  container.append(() => svgicons);
  container.append(() => dropdownstyle);
  container.append(() => leuStyleSheet);

  this.getContainer = function () {
    return container;
  };

  this.getUid = function () {
    return uid;
  };

  this.addMetaTop = function () {
    //Add logo
    let logo = d3.select("#logo" + uid);
    if (logo.empty()) {
      logo = container.append("div");
    }
    logo
      .attr("id", "logo" + uid)
      .attr("class", "biplalogo")
      .attr("style", "float:right;")
      .html(
        `<div style="display:flex; justify-content: flex-end; align-items: center; line-height:1; column-gap: 0.6rem;"><div><svg focusable="false" style="width:4.5rem; height:4.5rem;" ><use href="#ktzh" viewBox="0 0 184 180"></use></svg></div><div style="line-height:1; font-family: InterBlack,Arial Black,Helvetica,sans-serif; font-size: 1rem;color:#000;">Kanton Zürich<br/>Bildungsdirektion<br/>Bildungsplanung</div></div>`
      )
      .classed("hiddenmeta", true);

    //Add figcaption
    //console.log("add figcaption")
    let figcaption = d3.select("#figcaption" + uid);
    if (figcaption.empty()) {
      figcaption = container.append("figcaption");
    }
    figcaption.attr("id", "figcaption" + uid);

    //Add title
    if (meta.title != "") {
      //console.log(meta.title);
      let title = d3.select("#title" + uid);
      if (title.empty()) {
        title = figcaption.append("div");
      }
      title
        .attr("id", "title" + uid)
        .attr("class", "fig-title")
        //.attr("style", "float:left")
        .html(meta.title);
      if (meta.titleHide) {
        title.classed("hiddenmeta", true);
      }
    }

    //Add subtitle
    if (meta.subtitle != "") {
      let subtitle = d3.select("#subtitle" + uid);
      if (subtitle.empty()) {
        subtitle = figcaption.append("div");
      }
      subtitle
        .attr("id", "subtitle" + uid)
        .attr("class", "fig-subtitle")
        //.attr("style", "clear:left;")
        .text(meta.subtitle);
      if (meta.subtitleHide) {
        subtitle.classed("hiddenmeta", true);
      }
    }

    //Add descriptionTop
    if (meta.descriptionTop != "") {
      let descriptionTop = d3.select("#descriptionTop" + uid);
      if (descriptionTop.empty()) {
        descriptionTop = container.append("div");
      }
      descriptionTop
        .attr("id", "descriptionTop" + uid)
        .attr("class", "fig-desc-before")
        .text(meta.descriptionTop);
      if (meta.descriptionTopHide) {
        descriptionTop.classed("hiddenmeta", true);
      }
    }
  };

  this.addFilterContainer = function (bottom = false) {
    //add filtercontainer
    let id = bottom ? "filtersbottom" : "filters";
    let filters = d3.select("#" + id + uid);
    if (filters.empty()) {
      filters = container.append("div");
    }
    filters.attr("id", id + uid).attr("class", id);
    return filters;
  };

  this.addMetaBottom = function () {
    //add data description
    if (meta.description != "") {
      let description = d3.select("#description" + uid);
      if (description.empty()) {
        description = container.append("div");
      }
      description
        .attr("id", "description" + uid)
        .attr("class", "fig-desc-after")
        .html(meta.description);
      if (meta.descriptionHide) {
        description.classed("hiddenmeta", true);
      }
    }
    //add data source and time
    let source = d3.select("#source" + uid);
    if (source.empty()) {
      source = container.append("div");
    }

    //function to format the Date differently if it is only a year
    let formatDate = function (date) {
      if (date == "") {
        return "";
      }
      //return the date as year if it is only an number
      if (typeof date === "number") {
        return ", Jahr der Berechnung: " + date;
      }
      const monthYearRegex = /^[a-zA-ZäöüÄÖÜ]+\s+\d{4}$/;
      if (typeof date === "string" && monthYearRegex.test(date.trim())) {
        return ", Datum der Berechnung: " + date.trim();
      }

      let dateAsDate = new Date(date);
      if (isNaN(dateAsDate.getTime())) {
        return ", Datum der Berechnung: " + date;
      }
      //return only the date if the time is 02:00:00
      if (
        dateAsDate.getHours() === 2 &&
        dateAsDate.getMinutes() === 0 &&
        dateAsDate.getSeconds() === 0
      ) {
        return (
          ", Datum der Berechnung: " + dateAsDate.toLocaleDateString("de-CH")
        );
      }
      //else return the date and time
      return ", Datum der Berechnung: " + dateAsDate.toLocaleString("de-CH");
    };

    source
      .attr("id", "source" + uid)
      .attr("class", "fig-data-source")
      .html(
        "<p>Datenquelle: " + meta.source + formatDate(meta.statusDate) + "</p>"
      );
    //add license
    let license = d3.select("#license" + uid);
    if (license.empty()) {
      license = container.append("div");
    }
    license
      .attr("id", "license" + uid)
      .attr("class", "license")
      .classed("hiddenmeta", true)
      .html(
        "© 2023. Diese Darstellung ist offen lizenziert nach <a href='https://creativecommons.org/licenses/by/4.0/'>CC BY 4.0</a>."
      );

    //add reading example if there is one in the data
    if (
      (meta.readingExampleContent != undefined) &
      (meta.readingExampleContent != "")
    ) {
      //check if the reading-example has already been appended.
      let readingExampleNode = d3.select("#readingExample" + uid);
      //add it if it isn't there yet
      if (readingExampleNode.empty()) {
        readingExampleNode = container.append("div");
        readingExampleNode
          .attr("id", "readingExample" + uid)
          .classed("noprint", true)
          .html(readingExample(meta.readingExampleContent).outerHTML);
        if (meta.readingExampleHide == true) {
          readingExampleNode.classed("hiddenmeta", true);
        }
      }
    }

    //add "limits of data" if there is one in the data
    if (
      (meta.dataLimitsContent != undefined) &
      (meta.dataLimitsContent != "")
    ) {
      //check if the reading-example has already been appended.
      let dataLimitsNode = d3.select("#dataLimits" + uid);
      //add it if it isn't there yet
      if (dataLimitsNode.empty()) {
        dataLimitsNode = container.append("div");
        dataLimitsNode
          .attr("id", "dataLimits" + uid)
          .classed("noprint", true)
          .html(
            readingExample(meta.dataLimitsContent, "Grenzen der Aussagekraft")
              .outerHTML
          );
        if (meta.dataLimitsHide == true) {
          dataLimitsNode.classed("hiddenmeta", true);
        }
      }
    }
  };

  this.addFormating = function () {
    //some formating
    container
      .select("input[type=text]")
      .attr("class", "atm-form_input__input dirty");
    container
      .select("input[type=text]")
      .select(function () {
        return this.parentNode;
      })
      .attr(
        "class",
        "atm-form_input atm-form_input--small atm-form_input--icon valid"
      );
  };

  function objToString(obj) {
    let str = "";
    for (const [p, val] of Object.entries(obj)) {
      if (str != "") {
        str += "; ";
      }
      str += `${p} = ${val}`;
    }
    return str;
  }
}
)}

function _19(md){return(
md`## HashCode-Generator`
)}

function _hashCode(){return(
function(s) {
  var hash = 0;
  for (var i = 0; i < s.length; i++) {
    var character = s.charCodeAt(i);
    hash = ((hash<<5)-hash)+character;
    hash = hash & hash; // Convert to 32bit integer
  }
  return hash;
}
)}

function _21(hashCode){return(
hashCode(
  "zuwachsrate-der-15--bis-19-jaehrigen-wohnbevoelkerung-im-kanton-zuerich-nach-region"
)
)}

function _23(md){return(
md`## Helper Functions`
)}

function _basicapi(URLSearchParams,d3){return(
new (function () {
  /**
   * basicapi provides a range of functions to access data from the basic api. This function has no parameters, but returns the functions basicapi.data, basicapi.file and basicapi.securedData
   * @example
   *
   *     basicapi.data('p_entwicklung_der_lernenden_an_gymnasialen_mittelschulen', refreshcache = false)
   */
  /**
   * The base URL for the production API.
   * @type {string}
   */
  this.url = "https://www.bista.zh.ch/basicapi/";
  /**
   * The base URL for the test API environment.
   * @type {string}
   */
  this.testurl = "https://test.bista.zh.ch/basicapi/";
  /**
   * The default route for standard data requests.
   * @type {string}
   */
  this.route = "zhweb/";
  /**
   * The default route for standard data requests.
   * @type {string}
   */
  this.securedRoute = "secured/";
  /**
   * Fetches JSON data from the standard production route.
   * @param {string} uri - The specific API endpoint path.
   * @param {boolean} [refreshcache=false] - Whether to bypass the server-side cache.
   * @returns {Promise<Object>} A D3-JSON promise containing the fetched data.
   */
  this.data = function (uri, refreshcache = false, params = {}) {
    const searchParams = new URLSearchParams({ refreshcache, ...params });
    const fullUrl = `${this.url}${this.route}${uri}?${searchParams.toString()}`;

    //console.log(fullUrl);
    return d3.json(fullUrl);
  };
  /**
   * Fetches JSON data from the test route.
   * @param {string} uri - The specific API endpoint path.
   * @param {boolean} [refreshcache=false] - Whether to bypass the server-side cache.
   * @returns {Promise<Object>} A D3-JSON promise containing the fetched data.
   */
  this.testdata = function (uri, refreshcache = false, params = {}) {
    const searchParams = new URLSearchParams({ refreshcache, ...params });
    const fullUrl = `${this.testurl}${
      this.route
    }${uri}?${searchParams.toString()}`;

    //console.log(fullUrl);
    return d3.json(fullUrl);
  };
  /**
   * Fetches JSON data from the production file route.
   * @param {string} uri - The specific API endpoint path.
   * @returns {Promise<Object>} A D3-JSON promise containing the fetched data.
   */
  this.file = function (uri, prod = true) {
    let url = this.url;
    if (prod == false) {
      url = this.testurl;
    }
    return d3.json(url + "files/" + uri);
  };
  /**
   * Fetches data from a secured endpoint using a secret key.
   * @param {string} uri - The specific API endpoint path.
   * @param {string} secret - The authentication secret required for access.
   * @param {boolean} [refreshcache=false] - Whether to bypass the server-side cache.
   * @returns {Promise<Object>} A D3-JSON promise containing the secured data.
   */
  this.securedData = function (uri, secret, refreshcache = false) {
    return d3.json(
      this.url +
        this.securedRoute +
        uri +
        "?refreshcache=" +
        refreshcache +
        "&secret=" +
        secret
    );
  };
})()
)}

function _25(basicapi){return(
basicapi.data("p_entwicklung_der_lernenden_an_gymnasialen_mittelschulen")
)}

function _swatches(html){return(
function swatches({
  color,
  columns = null,
  format = (x) => x,
  swatchSize = 16,
  swatchWidth = swatchSize,
  swatchHeight = swatchSize,
  marginLeft = 0,
  asButtons = false
}) {
  /**
   * swatches creates color swatches for displaying the color codes used in a chart
   *
   * @param {function<d3.scaleOrdinal()>} color The colorscale function used for the swatches.
   * @param {string} [columns] allows to define a fixed width for all items to be aranged in columns (for example "180px").
   * @param {function(string|number)} [format = (x) => x] A function to format the text values provided (mainly used to format numbers)
   * @param {number} [swatchSize=16] The size of the color square in pixel.
   * @param {number} [swatchWidth=swatchSize] The width of the color square in pixel.
   * @param {number} [swatchHeight=swatchSize] The height of the color square in pixel.
   * @param {number} [marginLeft=0] The margin to the left of the swatches in pixel.
   * @param {Boolean} [asButtons=false] An optional indicator to create buttons an not divs.
   */

  const id = "swatches";

  let entity = function (character) {
    return `&#${character.charCodeAt(0).toString()};`;
  };

  if (columns !== null)
    return html`<div style="display:flex; align-items: center; margin-left: ${+marginLeft}px; min-height: 33px; font: 0.8rem InterRegular, Helvetica, sans-serif;">
  <style>

.${id}-item {
  break-inside: avoid;
  display: flex;
  align-items: center;
  padding-bottom: 5px;
  padding-top: 5px;
}

.${id}-label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: calc(100% - ${+swatchWidth}px - 0.5em);
}

.${id}-swatch {
  width: ${+swatchWidth}px;
  height: ${+swatchHeight}px;
  margin: 0 0.5em 0 0;
}

.item-box {
    box-sizing: border-box;
    height: 0.75rem;
    min-width: 0.75rem;
    flex: 0 0 auto;
    border-radius: 2px;
    background-color: var(--_color);
}

.item-box--disabled {
    background-color: transparent;
    border: 2px solid var(--_color);
}

  </style>
  <div style="width: 100%; columns: ${columns};" id="swatches">${color
      .domain()
      .map((value) => {
        const label = format(value);
        return html`<div class="${id}-item" 
        title="${label.replace(/["&]/g, entity)}">
      <div class="${id}-swatch" style="background:${color(value)};"></div>
      <div class="${id}-label" title="${label.replace(
          /["&]/g,
          entity
        )}">${document.createTextNode(label)}</div>
    </div>`;
      })}
  </div>
</div>`;

  return html`<div style="display: flex; align-items: center; min-height: 33px; margin-left: ${+marginLeft}px; font: 0.8rem InterRegular, Helvetica, sans-serif;">
  <style>

.clickable {
    cursor: pointer;
    display: inline-block;
}

.clickable:hover {
    background-color: #f0f0f0;
    border-radius: 0.125rem;
}

.swatch-item {
    display: inline-flex;
    gap: 0.5rem;
    align-items: center;
    background: transparent;
    border: none;
    text-align: left;
    font-size: 0.875rem;
    padding: 0.125rem 0.25rem ;
    margin-right: 1em;
}

.item-box {
    box-sizing: border-box;
    height: 0.75rem;
    min-width: 0.75rem;
    flex: 0 0 auto;
    border-radius: 2px;
    background-color: var(--_color);    
}

.item--disabled {
    opacity: 0.5;
    text-decoration: line-through;
}

.item-box--disabled {
    background-color: transparent;
    border: 2px solid var(--_color);
}

  </style>
  <div id="swatches">${color.domain().map(
    (value) =>
      html`<${
        asButtons ? "button" : "div"
      } class="${id} swatch-item" value="${value}" data-value="${value}">
        <span class="item-box" style="--_color:${color(value)};"></span>
        <span class="item-text">${document.createTextNode(
          format(value)
        )}</span></${asButtons ? "button" : "div"}>`
  )}</div>`;
}
)}

function _brightnessByColor(){return(
function brightnessByColor(color, opacity = 1) {
  var colorStr = "" + color;
  var r,
    g,
    b,
    a = 1; // 'a' for alpha (opacity)

  const isHEX = colorStr.indexOf("#") === 0;
  const isRGB = colorStr.indexOf("rgb") === 0;

  if (isHEX) {
    const hasFullSpec = colorStr.length === 7; // #RRGGBB
    const hasShortSpec = colorStr.length === 4; // #RGB

    if (hasFullSpec || hasShortSpec) {
      // Extract R, G, B values from HEX
      const m = colorStr.substr(1).match(hasFullSpec ? /(\S{2})/g : /(\S{1})/g);
      if (m) {
        r = parseInt(m[0] + (hasFullSpec ? "" : m[0]), 16);
        g = parseInt(m[1] + (hasFullSpec ? "" : m[1]), 16);
        b = parseInt(m[2] + (hasFullSpec ? "" : m[2]), 16);
      }
      // Apply the separate opacity parameter for HEX colors
      a = opacity;
    }
  } else if (isRGB) {
    // Match numbers for rgb(R,G,B) or rgba(R,G,B,A)
    const matchRGBA = colorStr.match(/(\d+){3}(?:,\s*([\d.]+))?/); // Matches R,G,B and optionally A
    if (matchRGBA) {
      r = parseInt(matchRGBA[1], 10);
      g = parseInt(matchRGBA[2], 10);
      b = parseInt(matchRGBA[3], 10);
      // If an alpha value exists in rgba(), use it. Otherwise, use the provided 'opacity' parameter.
      a = matchRGBA[4] !== undefined ? parseFloat(matchRGBA[4]) : opacity;
    }
  }

  // If RGB values are successfully parsed
  if (
    typeof r !== "undefined" &&
    typeof g !== "undefined" &&
    typeof b !== "undefined"
  ) {
    // If alpha is less than 1, blend the color with a white background (common approach)
    // The perceived brightness will be influenced by the background.
    if (a < 1) {
      // Calculate blended RGB values over a white background (255, 255, 255)
      r = r * a + 255 * (1 - a);
      g = g * a + 255 * (1 - a);
      b = b * a + 255 * (1 - a);
    }
    return (r * 299 + g * 587 + b * 114) / 1000;
  }

  // Return undefined or throw an error if the color format is not recognised
  return undefined;
}
)}

function _rotateX(getTransformation,d3,addStaticText,wrap){return(
function rotateX(svgcontainer, heightChart, classedAs) {
  function delay(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
  }

  function rotateOneNode(node, svgcontainer, heightChart) {
    let origLegendHeight = node.node().getBBox().height;
    //Breite eines Zwischenstrichs bestimmen
    //console.log("Stufe 1");
    let tickwidth;
    if (node.selectAll("g.tick").size() > 1) {
      tickwidth =
        //position of second tick
        getTransformation(
          d3.select(node.selectAll("g.tick")._groups[0][1]).attr("transform")
        ).translateX -
        //position of first tick
        getTransformation(
          d3.select(node.selectAll("g.tick")._groups[0][0]).attr("transform")
        ).translateX;
    } else {
      tickwidth =
        getTransformation(
          d3.select(node.selectAll("g.tick")._groups[0][0]).attr("transform")
        ).translateX * 2;
    }

    let allTexts = node.selectAll("g.tick text");

    //1. Schritt
    //Zeilen umbrechen
    //der Gesamte Text muss persistiert werden, damit beim wiederholten wrappen nicht Leerschläge verloren gehen.
    allTexts.call(addStaticText);

    //Zeilen umbrechen, wenn breiter als Zwischenstrich
    allTexts.call(wrap, tickwidth);

    //Maximale Breite und Höhe der Skalenbezeichner bestimmen
    let maxwidth = 0;
    let maxheight = 0;
    allTexts.attr("transform", function (d) {
      let coordx = this.getBBox().width;
      if (maxwidth < coordx) {
        maxwidth = coordx;
      }
      let coordy = this.getBBox().height;
      if (maxheight < coordy) {
        maxheight = coordy;
      }
    });

    //2. Schritt
    //Wenn immer noch zu breit dann rotieren
    //console.log("Stufe 2");
    if (maxwidth > tickwidth) {
      allTexts.call(wrap, Math.min(150, maxwidth));
      allTexts.style("text-anchor", "start");
      allTexts.attr("transform", function (d) {
        var moveleft = -this.getBBox().height / 2 - 8;
        return "rotate(90), translate(10," + moveleft + ")";
      });
    }
  }

  delay(0).then(() => {
    let xAxis;
    //if no class is provided, the axis is selected using id = xAxis
    if (typeof classedAs == "undefined") {
      xAxis = svgcontainer.select("#xAxis");
      let origLegendHeight = xAxis.node().getBBox().height;
      rotateOneNode(xAxis, svgcontainer, heightChart);
      //Höhe der Grafik den neuen Begebenheiten anpassen (height und viewBox)
      let newlegendHeight = xAxis.node().getBBox().height;
      let newHeightChart = heightChart + newlegendHeight - origLegendHeight;

      //svgcontainer.attr("height", newHeightChart);
      let viewBox = svgcontainer.attr("viewBox").split(",");
      viewBox[3] = newHeightChart.toString();
      svgcontainer.attr("viewBox", viewBox.join(","));
    }
    //if a class is provided, the class is used to select all xAxis'
    else {
      xAxis = svgcontainer.selectAll("." + classedAs);
      let origLegendHeight = [];
      let newLegendHeight = [];
      xAxis.each(function (d, i) {
        origLegendHeight.push(d3.select(this).node().getBBox().height);
        rotateOneNode(d3.select(this), svgcontainer, heightChart);
        newLegendHeight.push(d3.select(this).node().getBBox().height);
      });
      let newHeightChart =
        heightChart + d3.max(newLegendHeight) - d3.max(origLegendHeight);
      let viewBox = svgcontainer.attr("viewBox").split(",");
      viewBox[3] = newHeightChart.toString();
      svgcontainer.attr("viewBox", viewBox.join(","));
    }
  });
}
)}

function _linebreakY(addStaticText,wrap,d3){return(
function linebreakY(svgcontainer, widthChart, marginLeft = 100, classedAs) {
  function delay(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
  }

  delay(200).then(() => {
    let yAxis = svgcontainer.select("#yAxis");
    let prevHeights = [];
    let afterHeights = [];
    yAxis.selectAll("g.tick").each(function () {
      prevHeights.push(this.getBBox().height);
    });
    yAxis.selectAll("g.tick text").call(addStaticText);
    yAxis.selectAll("g.tick text").call(wrap, marginLeft);
    yAxis.selectAll("g.tick").each(function () {
      afterHeights.push(this.getBBox().height);
    });
    yAxis.selectAll("g.tick text").each(function (d, i) {
      d3.select(this).attr(
        "transform",
        "translate(0, " + (prevHeights[i] / 2 - afterHeights[i] / 2) + ")"
      );
    });
  });
}
)}

function _getTransformation(){return(
function getTransformation(transform) {
  // Create a dummy g for calculation purposes only. This will never
  // be appended to the DOM and will be discarded once this function
  // returns.
  var g = document.createElementNS("http://www.w3.org/2000/svg", "g");

  // Set the transform attribute to the provided string value.
  g.setAttributeNS(null, "transform", transform);

  // consolidate the SVGTransformList containing all transformations
  // to a single SVGTransform of type SVG_TRANSFORM_MATRIX and get
  // its SVGMatrix.
  var matrix = g.transform.baseVal.consolidate().matrix;

  // Below calculations are taken and adapted from the private function
  // transform/decompose.js of D3's module d3-interpolate.
  var { a, b, c, d, e, f } = matrix; // ES6, if this doesn't work, use below assignment
  // var a=matrix.a, b=matrix.b, c=matrix.c, d=matrix.d, e=matrix.e, f=matrix.f; // ES5
  var scaleX, scaleY, skewX;
  if ((scaleX = Math.sqrt(a * a + b * b))) (a /= scaleX), (b /= scaleX);
  if ((skewX = a * c + b * d)) (c -= a * skewX), (d -= b * skewX);
  if ((scaleY = Math.sqrt(c * c + d * d)))
    (c /= scaleY), (d /= scaleY), (skewX /= scaleY);
  if (a * d < b * c) (a = -a), (b = -b), (skewX = -skewX), (scaleX = -scaleX);
  return {
    translateX: e,
    translateY: f,
    rotate: (Math.atan2(b, a) * 180) / Math.PI,
    skewX: (Math.atan(skewX) * 180) / Math.PI,
    scaleX: scaleX,
    scaleY: scaleY
  };
}
)}

function _addStaticText(d3){return(
function (text) {
  text.each(function () {
    let text = d3.select(this);
    text._groups[0][0].__staticText__ = text.text();
  });
}
)}

function _wrap(d3){return(
function (text, width) {
  text.each(function () {
    let breakChars = ["&"],
      text = d3.select(this),
      textContent = text._groups[0][0].__staticText__, //text.text(), //text._groups[0][0].__data__,
      spanContent;

    if (textContent == "undefined") {
      textContent = text.text();
    }

    if (typeof textContent == "string") {
      breakChars.forEach(function (char) {
        // Add a space after each break char for the function to use to determine line breaks
        textContent = textContent.replace(char, char + " ");
      });

      var words = textContent.split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.2, // ems
        x = text.attr("x") || 0,
        y = text.attr("y") || 0,
        dy = parseFloat(text.attr("dy") || 0),
        tspan = text
          .text(null)
          .append("tspan")
          .attr("x", x)
          .attr("y", y)
          .attr("dy", dy + "em");
      while ((word = words.pop())) {
        let manualbreak = false;
        if (word.includes("<br>")) {
          manualbreak = true;
          word = word.replaceAll("<br>", " "); //remove line break html-tag;
        }
        line.push(word + " ");
        tspan.text(line.join(" "));
        if (
          manualbreak || //manual line breaks using html-tag
          tspan.node().getComputedTextLength() > width
        ) {
          line.pop();
          spanContent = line.join(" ");
          breakChars.forEach(function (char) {
            // Remove spaces trailing breakChars that were added above
            spanContent = spanContent.replace(char + " ", char);
          });

          tspan.text(spanContent);
          line = [word];
          tspan = text
            .append("tspan")
            .attr("x", x)
            .attr("y", y)
            .attr("dy", ++lineNumber * lineHeight + dy + "em")
            .text(word);
        }
      }
    }
  });
}
)}

function _mouseOut(d3){return(
function (uid) {
  d3.select("#mouseOverL").remove();
  d3.select("#tooltip" + uid).remove();
}
)}

function _disarray(){return(
function (arr) {
  if (Array.isArray(arr) && arr.length === 1) {
    return String(arr[0]); // Convert the single element to a string
  } else {
    return arr; // Return the array as is if it's not a single-element array
  }
}
)}

function _35(md){return(
md`### Formatierungen`
)}

function _germanFormater(d3){return(
d3.formatLocale({
  decimal: ".",
  thousands: "'",
  grouping: [3],
  currency: ["CHF", ""],
  dateTime: "%a %b %e %X %Y",
  date: "%d.%m.%Y",
  time: "%H:%M:%S",
  periods: ["AM", "PM"],
  days: [
    "Sonntag",
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag"
  ],
  shortDays: ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"],
  months: [
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember"
  ],
  shortMonths: [
    "Jan",
    "Feb",
    "Mär",
    "Apr",
    "Mai",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Okt",
    "Nov",
    "Dez"
  ]
})
)}

function _formater(germanFormater,d3){return(
function formater(type, value) {
  /**
   * formater returns eigther a formated value or a function to format a value if a value is not provided as parameter
   *
   * @param {string("string" | "year" | "integer" | "int" | "float" | "float2" | "float6" | "percentage" | "percent" | "date" | "datemonthyear" | "dateyear" | "week" | "miochf" | "chf" | "floatha" | "terrajoule")} type Defines the type of value to be formated.
   * @param {string|number} [value] The value to be formated. If no value is provided the function returns a function to apply the formating.
   */

  if (value == undefined) {
    if (type == "string" || type == "year") {
      return value;
    } else if (type == "integer" || type == "int") {
      return germanFormater.format(",.0f");
    } else if (type == "float") {
      return germanFormater.format(",.1f");
    } else if (type == "float2") {
      return germanFormater.format(",.2f");
    } else if (type == "float6") {
      return germanFormater.format(",.6f");
    } else if (type == "percentage" || type == "percent") {
      return d3.format(".1%");
    } else if (type == "date") {
      return d3.time.format("%d.%m.%Y");
    } else if (type == "datemonthyear") {
      return d3.time.format("%B %Y");
    } else if (type == "dateyear") {
      return d3.time.format("%Y");
    }
  }
  if (type == "string" || type == "year") {
    return value;
  }
  if (isNaN(value)) {
    return "keine Angabe";
  } else if (type == "integer" || type == "int") {
    return germanFormater.format(",.0f")(parseInt(value));
  } else if (type == "float") {
    return germanFormater.format(",.1f")(parseFloat(value));
  } else if (type == "float2") {
    return germanFormater.format(",.2f")(parseFloat(value));
  } else if (type == "float6") {
    return germanFormater.format(",.6f")(parseFloat(value));
  } else if (type == "float2variable") {
    if (parseFloat(value) % 1) {
      var werte = germanFormater.format(",.2f")(parseFloat(value));
    } else {
      werte = germanFormater.format(",")(parseFloat(value));
    }
    return werte;
  } else if (type == "percentage" || type == "percent") {
    return d3.format(".1%")(value);
  } else if (type == "date") {
    return d3.time.format("%d.%m.%Y")(new Date(value));
  } else if (type == "week") {
    return "Woche vom " + d3.time.format("%d.%m.%Y")(new Date(value));
  } else if (type == "datemonthyear") {
    return d3.time.format("%B %Y")(new Date(value));
  } else if (type == "dateyear") {
    return d3.time.format("%Y")(new Date(value));
  } else if (type == "miochf") {
    return "" + germanFormater.format(",f")(parseInt(value)) + " Mio Franken";
  } else if (type == "chf") {
    return "Fr. " + germanFormater.format(",.2f")(parseInt(value)) + "";
  } else if (type == "floatha") {
    return "" + germanFormater.format(",.2f")(parseFloat(value)) + " ha";
  } else if (type == "terrajoule") {
    return "" + germanFormater.format(",f")(parseFloat(value)) + " TJ";
  }
}
)}

function _38(md){return(
md `## Farben`
)}

function _39(md){return(
md`### Grafikfarben gemäss Designstandards

https://www.zh.ch/de/webangebote-entwickeln-und-gestalten/inhalt/designsystem/design-grundlagen/infografiken-und-visualisierungen.html`
)}

function _graphicsColors(){return(
{
  Cyan: "#29A1C2",
  Blau: "#2885d1",
  Dunkelblau: "#0864a6",
  Aquamarine: "#83cfc6",
  Türkis: "#22968C",
  Dunkelgrün: "#066F5E",
  Grasgrün: "#6A7E30",
  Gold: "#ad911f",
  Orange: "#D6741F",
  Rot: "#D93C1A",
  Braun: "#96170F",
  Rose: "#D16174",
  Magenta: "#D4356D",
  Bordeaux: "#B01657",
  Dunkelrot: "#7A0049",
  Hellviolett: "#7f33a9",
  Violett: "#653289",
  Dunkelviolett: "#54268E",
  Black100ZH: "#000000",
  Black80ZH: "#333333",
  Black60ZH: "#666666",
  Black40ZH: "#949494",
  Black20ZH: "#CCCCCC",
  Black10ZH: "#F0F0F0",
  Black5ZH: "#F7F7F7"
}
)}

function _graphiccolorsshow(showColors,graphicsColors){return(
showColors(Object.values(graphicsColors))
)}

function _42(md){return(
md`### Zusätzliche Grafikfarben gemäss Designstandards

Umfasst Farben, welche verwendet werden, aber nicht explizit definiert werden.`
)}

function _additionalGraphicsColors(){return(
{
  Hellblau: "#9dc1e5",
  Hellorange: "#e9bb9d",
  Lila: "#bc9dd2",
  Hellgold: "#d8c68a",
  Gelb: "#FFCC00",
  Grün: "#1A7F1F",
  Grasgrün: "#8A8C00"
}
)}

function _additionalgraphicscolorsshow(showColors,additionalGraphicsColors){return(
showColors(
  Object.values(additionalGraphicsColors)
)
)}

function _45(md){return(
md`### Kategoriale Farben

Wenn nicht eine spezifische Farbe für eine Ausprägung vorgesehen ist.`
)}

function _fixedCategorialColors(graphicsColors){return(
[
  graphicsColors.Blau,
  graphicsColors.Magenta,
  graphicsColors.Türkis,
  graphicsColors.Hellviolett,
  graphicsColors.Gold,
  graphicsColors.Cyan,
  graphicsColors.Dunkelrot,
  graphicsColors.Dunkelgrün,
  graphicsColors.Dunkelblau
]
)}

function _fixedCategorialColorsshow(showColors,fixedCategorialColors){return(
showColors(fixedCategorialColors)
)}

function _48(md){return(
md`Zusätzliche Kategoriale Farben, wenn die 9 nicht ausreichen. Sollte wenn möglich vermieden werden.`
)}

function _emergencyCategorialColors(graphicsColors){return(
[
  graphicsColors.Orange,
  graphicsColors.Grasgrün,
  graphicsColors.Rose,
  graphicsColors.Violett,
  graphicsColors.Bordeaux
]
)}

function _50(showColors,emergencyCategorialColors){return(
showColors(emergencyCategorialColors)
)}

function _51(md){return(
md`### Semantische Farben für bestimmte Ausprägungen

#### Funktion zur Verwendung in observable`
)}

function _getColor(d3,additionalGraphicsColors,graphicsColors,primaryColors,sonderschulColors,fixedCategorialColors,emergencyCategorialColors){return(
function (name, index, brightness = 0) {
  /**
   * getColor returns a hex-color code from the color scheme of canton of Zurich, depending on the parameters. It looks at the provided name first. If there is no color code for the particular name defined, it will return the color for the index provided, selecting one of the nine default categorial colors. If no index is provided it will return any of the nine default categorial colors at random.
   *
   * @param {string|number} [name] - The name of the variable for which a color is needed. If name is a number and index is omited, name is used as index.
   * @param {number} [index] - An index for color selection if the name does not select a color
   * @return {string} A hex color code
   *
   * @example
   *
   *     getColor('Kindergarten', 2)
   */
  if (typeof name == "object") {
    return d3.interpolate(eval(name.color), "#FFFFFF")(name.brightness);
  }
  if (typeof name == "number" && typeof index == "undefined") {
    index = name;
  }
  //if the name is a specific color name from the palette, the actual colot is returned.
  if (
    typeof name == "string" &&
    (name.includes("graphicsColors") ||
      name.includes("additionalGraphicsColors"))
  ) {
    return eval(name);
  }
  switch (name) {
    case "Kindergarten":
    case "Primarstufe 1-2":
    case "Primarstufe 1-2 (Kindergarten)":
      return additionalGraphicsColors.Gelb;
    case "Primarschule":
    case "Primarstufe 3-8":
    case "Primarstufe 3-8 (Primarschule)":
    case "Primarstufe 6-8":
    case "Primarstufe 6-8 (Primarschule Mittelstufe)":
      return graphicsColors.Orange;
    case "Primarstufe 3-5":
    case "Primarstufe 3-5 (Primarschule Unterstufe)":
      return primaryColors(3)[1];
    case "Sonderschule":
    case "Heim- und Sonderschule":
    case "Sonderschulung":
    case "Separierte Sonderschulung":
    case "Separiert, Sonderschule":
    case "Lösung an einer bewilligten Sonderschule":
      return graphicsColors.Dunkelblau;
    case "Separiert, Lösung an Privatschule":
    case "Lösung an Privatschule (Ultima Ratio)":
      return graphicsColors.Grasgrün;
    case "Separiert, Kategorie unbekannt":
      return graphicsColors.Cyan;
    case "Integrierte Sonderschulung":
    case "Integrierte Sonderschulung (in einer Regelschule)":
      return graphicsColors.Dunkelgrün;
    case "Typ A: Beeinträchtigung in den Bereichen Verhalten, Lernen oder Sprache":
      return sonderschulColors(3)[0];
    case "Typ B: Körper-, Sinnes- oder Mehrfachbeeinträchtigungen":
      return sonderschulColors(3)[1];
    case "Typ C: kognitive Beeinträchtigungen":
      return sonderschulColors(3)[2];
    case "Berufsmaturität (BM2)":
      return graphicsColors.Dunkelblau;
    case "Eigener Lehrplan":
    case "Eigener_Lehrplan":
    case "Schule mit eigenem Programm":
    case "Berufsmaturität (BM1)":
      return graphicsColors.Blau;
    case "Wechsel vom Langgymnasium in die Sekundarschule":
      return graphicsColors.Aquamarine;
    case "Sekundarschule":
    case "Sekundarstufe I":
    case "Untergymnasium":
    case "Ausschliesslich Sekundarschule":
      return graphicsColors.Türkis;
    case "Sekundarstufe II":
    case "Gymnasiale Oberstufe":
    case "Sekundarschule und anschliessend Kurzgymnasium":
      return additionalGraphicsColors.Grün;
    case "Tertiärstufe":
      return graphicsColors.Dunkelviolett;
    case "Mittelschule":
    case "Total gymnasiale Mittelschule":
    case "Gymnasium":
      return additionalGraphicsColors.Grün;
    case "Berufsfachschule":
    case "Berufsschule":
    case "Langgymnasium":
      return graphicsColors.Dunkelgrün;
    //damit es sich genügend von den Mittelschulen Unterscheidet:
    case "Berufsbildung":
      return graphicsColors.Blau;
    case "Brückenangebot":
    case "Berufsmaturität insgesamt":
      return graphicsColors.Aquamarine;
    case "Höhere Berufsbildung":
      return graphicsColors.Hellviolett;
    case "Fachhochschule":
      return graphicsColors.Violett;
    case "Universität":
    case "Hochschule":
      return graphicsColors.Dunkelviolett;
    case "Volksschule":
      return graphicsColors.Blau;
    case "Regelschule":
    case "Regelschulung":
      return graphicsColors.Cyan;
    case "Andere allgemeinbildende Ausbildung":
    case "Andere_allgemeinbildende_Ausbildung":
    case "Andere":
    case "Informationen nicht durchgehend vorhanden":
      return graphicsColors.Black60ZH;
    case "stufenübergreifend":
      return graphicsColors.Cyan;
    case "Anzahl Weiblich":
    case "Anteil Weiblich":
    case "Anzahl weiblich":
    case "Anteil weiblich":
    case "Anzahl Frauen":
    case "Anteil Frauen":
    case "Weiblich":
      return graphicsColors.Hellviolett;
    case "Anzahl Männlich":
    case "Anteil Männlich":
    case "Anzahl männlich":
    case "Anteil männlich":
    case "Anzahl Männer":
    case "Anteil Männer":
    case "Männlich":
      return graphicsColors.Türkis;
    case "Anzahl Schweizer/in":
    case "Anteil Schweizer/in":
    case "Schweiz":
      return graphicsColors.Rot;
    case "Anzahl Ausländer/in":
    case "Anteil Ausländer/in":
    case "Ausland":
      return graphicsColors.Gold;
    case "Deutsch":
      return graphicsColors.Bordeaux;
    case "Nicht Deutsch":
      return graphicsColors.Dunkelgrün;
    case "Anzahl an öffentlich finanzierten Einrichtungen":
    case "Anteil an öffentlich finanzierten Einrichtungen":
      return graphicsColors.Orange;
    case "Anzahl an privat finanzierten Einrichtungen":
    case "Anteil an privat finanzierten Einrichtungen":
      return additionalGraphicsColors.Grün;
    case "Sozial benachteiligte Gruppe":
      return graphicsColors.Violett;
    case "Sozial mittlere Gruppe":
      return graphicsColors.Black20ZH;
    case "Sozial privilegierte Gruppe":
      return graphicsColors.Dunkelgrün;
    case "Ende obligatorische Schulzeit":
      return additionalGraphicsColors.Grün;
    case "Fünfte Erhebung":
      return graphicsColors.Bordeaux;
    case "Lehrpersonen":
      return graphicsColors.Blau;
    case "Personal für schulische Heilpädagogik":
      return graphicsColors.Orange;
    case "Personal für Förderunterricht für fremdsprachige Lernende":
      return graphicsColors.Braun;
    case "Personal für Logopädie":
      return graphicsColors.Dunkelviolett;
    case "Personal für Psychomotoriktherapie":
      return graphicsColors.Türkis;
    case "Weiteres sonderpädagogisches Fachpersonal":
      return graphicsColors.Cyan;
    case "Schulleitungspersonal":
      return graphicsColors.Dunkelgrün;
    case "Anteil A":
    case "Anzahl A":
    case "Anteil Abteilung A":
    case "Anzahl Abteilung A":
    case "Abteilung A":
    case "Sekundarschule Abteilung A":
      return graphicsColors.Türkis;
    case "Anteil B":
    case "Anzahl B":
    case "Anteil Abteilung B":
    case "Anzahl Abteilung B":
    case "Abteilung B":
    case "Sekundarschule Abteilung B":
      return graphicsColors.Blau;
    case "Anteil C":
    case "Anzahl C":
    case "Anteil Abteilung C":
    case "Anzahl Abteilung C":
    case "Abteilung C":
    case "Sekundarschule Abteilung C":
      return graphicsColors.Violett;
    case "Anteil A/B":
    case "Anzahl A/B":
      return graphicsColors.Orange;
    case "Anteil A/C":
    case "Anzahl A/C":
      return graphicsColors.Rot;
    case "Anteil B/C":
    case "Anzahl B/C":
      return graphicsColors.Braun;
    case "Anteil A/B/C":
    case "Anzahl A/B/C":
    case "3 Abteilungen (A, B, C)":
      return graphicsColors.Magenta;
    case "2 Abteilungen (A, B)":
      return graphicsColors.Blau;
    case "Anzahl Bachelor":
    case "Anteil Bachelor":
    case "Bachelor":
      return graphicsColors.Violett;
    case "Anzahl Master":
    case "Anteil Master":
    case "Master":
      return graphicsColors.Türkis;
    case "Anzahl Doktorat":
    case "Anteil Doktorat":
    case "Doktorat":
      return graphicsColors.Rot;
    case "Kanton Zürich":
      return graphicsColors.Cyan;
    case "ausserkantonal":
      return graphicsColors.Aquamarine;
    //case "Ausland":
    //  return additionalGraphicsColors.Hellorange;
    default:
      //If no index is provided, generate it at random
      if (typeof index === undefined) {
        index = Math.round(Math.random() * 8);
        /*console.log(
          "There was no color index provided. Default color was selected at random."
        );*/
      }
      //If the index is out or range start again from the beginning
      if (index > fixedCategorialColors.length - 1) {
        /*console.log(
          "The color index (" +
            index +
            ") is greater than the number of available colors. Too many colors to select specific ones, emergency colors are used"
        );
        console.log(
          "Emergency Color selected for: " + name + ", index: " + index
        );*/
        index = index - fixedCategorialColors.length;
        return emergencyCategorialColors[index];
      }
      //console.log("Default Color selected for: " + name + ", index: " + index);
      return fixedCategorialColors[index];
  }
}
)}

function _53(getColor){return(
getColor("Sekundarschule und anschliessend Kurzgymnasium")
)}

function _54(getColor){return(
getColor("bla", 1)
)}

function _55(getColor){return(
getColor("graphicsColors.Cyan")
)}

function _getColorScale(d3,getColor){return(
function (columns, colors) {
  if (typeof colors == "undefined") {
    return d3
      .scaleOrdinal()
      .domain(columns)
      .range(columns.map((d, i) => getColor(d, i)));
  } else {
    return d3
      .scaleOrdinal()
      .domain(columns)
      .range(columns.map((d, i) => getColor(colors[i], i)));
  }
}
)}

function _57(md){return(
md`#### Schulstufen`
)}

function _Stufen(){return(
[
  "Kindergarten",
  "Primarschule",
  "Sonderschule",
  "Eigener Lehrplan",
  "Sekundarschule",
  "Mittelschule",
  "Berufsschule",
  "Brückenangebot",
  "Andere allgemeinbildende Ausbildung",
  "Höhere Berufsbildung",
  "Hochschule"
]
)}

function _59(colorTable,Stufen,getColor){return(
colorTable(
  Stufen,
  Stufen.map((d) => getColor(d))
)
)}

function _60(Stufen,getColor){return(
Stufen.map((d) => getColor(d))
)}

function _61(md){return(
md`#### Sonderschulkategorien`
)}

function _sonderschulColors(d3,graphicsColors){return(
function sonderschulColors(levels) {
  return d3.quantize(
    d3.interpolateRgbBasis([graphicsColors.Cyan, graphicsColors.Dunkelblau]),
    levels
  );
}
)}

function _63(sonderschulColors){return(
sonderschulColors(3)
)}

function _sonderschulTypen(){return(
["Typ A", "Typ B", "Typ C"]
)}

function _65(colorTable,sonderschulTypen,sonderschulColors){return(
colorTable(sonderschulTypen, sonderschulColors(3))
)}

function _66(md){return(
md`#### Primarschulstufen und Klassen`
)}

function _primaryColors(d3,graphicsColors){return(
function primaryColors(levels) {
  return d3.quantize(
    d3.interpolateRgbBasis([graphicsColors.Gold, graphicsColors.Orange]),
    levels
  );
}
)}

function _68(md){return(
md`##### Stufen`
)}

function _69(primaryColors){return(
primaryColors(3)
)}

function _primaryStufen(){return(
["Primarstufe 1-2", "Primarstufe 3-5", "Primarstufe 6-8"]
)}

function _71(colorTable,primaryStufen,primaryColors){return(
colorTable(primaryStufen, primaryColors(3))
)}

function _72(primaryColors){return(
primaryColors(3)[1]
)}

function _73(md){return(
md`##### Klassen`
)}

function _74(primaryColors){return(
primaryColors(8)
)}

function _primaryKlassen(){return(
["1. Kindergarten (Harmos 1)","2. Kindergarten (Harmos 2)","1. Primarklasse (Harmos 3)","2. Primarklasse (Harmos 4)","3. Primarklasse (Harmos 5)","4. Primarklasse (Harmos 6)","5. Primarklasse (Harmos 7)","6. Primarklasse (Harmos 8)"]
)}

function _76(colorTable,primaryKlassen,primaryColors){return(
colorTable(primaryKlassen, primaryColors(8))
)}

function _77(md){return(
md`#### Sekundarstufe I`
)}

function _78(md){return(
md`##### Klassen`
)}

function _secondaryIColors(d3,graphicsColors){return(
function secondaryIColors(levels) {
  return d3.quantize(
    d3.interpolateRgbBasis([graphicsColors.Aquamarine, graphicsColors.Blau]),
    levels
  );
}
)}

function _80(secondaryIColors){return(
secondaryIColors(4)
)}

function _secondaryIKlassen(){return(
["1. Sekundarklasse (Harmos 9)","2. Sekundarklasse (Harmos 10)", "3. Sekundarklasse (Harmos 11)","Brückenangebote"]
)}

function _82(colorTable,secondaryIKlassen,secondaryIColors){return(
colorTable(secondaryIKlassen, secondaryIColors(4))
)}

function _83(md){return(
md`##### Sekundarschulniveaus`
)}

function _secondaryINiveauColors(d3,graphicsColors,additionalGraphicsColors){return(
function secondaryINiveauColors(levels) {
  let colors = d3.quantize(
    d3.interpolateRgbBasis([
      graphicsColors.Aquamarine,
      additionalGraphicsColors.Grün
    ]),
    levels
  );
  colors.push(graphicsColors.Black60ZH);
  return colors;
}
)}

function _85(secondaryINiveauColors){return(
secondaryINiveauColors(4)
)}

function _secondaryINiveau(){return(
["Sek C", "Sek B", "Sek A", "Mittelschule ( Harmos 9-11)", "Übrige"]
)}

function _87(colorTable,secondaryINiveau,secondaryINiveauColors){return(
colorTable(secondaryINiveau, secondaryINiveauColors(4))
)}

function _88(md){return(
md`#### Sekundarstufe II`
)}

function _89(md){return(
md`##### Klassen`
)}

function _secondaryIIColors(d3,additionalGraphicsColors,graphicsColors){return(
function secondaryIIColors(levels) {
  return d3.quantize(
    d3.interpolateRgbBasis([
      additionalGraphicsColors.Grün,
      graphicsColors.Dunkelgrün
    ]),
    levels
  );
}
)}

function _91(secondaryIIColors){return(
secondaryIIColors(4)
)}

function _secondaryIIKlassen(){return(
["Schuljahr 12", "Schuljahr 13", "Schuljahr 14", "Schuljahr 14"]
)}

function _93(colorTable,secondaryIIKlassen,secondaryIIColors){return(
colorTable(secondaryIIKlassen, secondaryIIColors(4))
)}

function _94(md){return(
md`##### Mittelschulprofile`
)}

function _secondaryIIProfileColors(d3,additionalGraphicsColors,graphicsColors){return(
function secondaryIIProfileColors(levels) {
  let colors = d3.quantize(
    d3.interpolateRgbBasis([
      additionalGraphicsColors.Grün,
      additionalGraphicsColors.Grasgrün,
      graphicsColors.Dunkelgrün
    ]),
    levels
  );
  colors.push(graphicsColors.Black60ZH);
  return colors;
}
)}

function _96(secondaryIIProfileColors){return(
secondaryIIProfileColors(6)
)}

function _secondaryIIProfiles(){return(
["Altsprachliches Profil (A)", "Neusprachliches Profil (N)","Math.-naturw. Profil (MN)","Wirtsch.-recht. Profil (WR)","Musisches Profil (M)","Nicht gymn. Mittelschulen","Übrige"]
)}

function _98(colorTable,secondaryIIProfiles,secondaryIIProfileColors){return(
colorTable(secondaryIIProfiles, secondaryIIProfileColors(6))
)}

function _99(md){return(
md`#### Schultypen`
)}

function _schultypen(){return(
[
  "Volksschule",
  "Heim und Sonderschulen",
  "Mittelschulen",
  "Brückenangebote",
  "Berufsschule",
  "Höhere Berufsbildung",
  "Fachhochschule und PH",
  "Universitäre Hochschulen"
]
)}

function _schultypenColors(graphicsColors,additionalGraphicsColors){return(
[
  graphicsColors.Orange,
  graphicsColors.Dunkelblau,
  additionalGraphicsColors.Grün,
  graphicsColors.Aquamarine,
  graphicsColors.Dunkelgrün,
  graphicsColors.Hellviolett,
  graphicsColors.Violett,
  graphicsColors.Dunkelviolett
]
)}

function _102(colorTable,schultypen,schultypenColors){return(
colorTable(schultypen, schultypenColors)
)}

function _103(md){return(
md`#### Geschlecht`
)}

function _gender(){return(
["Weiblich","Männlich"]
)}

function _genderColors(graphicsColors){return(
[graphicsColors.Hellviolett, graphicsColors.Türkis]
)}

function _106(colorTable,gender,genderColors){return(
colorTable(gender,genderColors)
)}

function _107(md){return(
md`#### Nationalität`
)}

function _nationality(){return(
["Schweizer/in","Ausländer/in"]
)}

function _nationalityColors(graphicsColors){return(
[graphicsColors.Rot, graphicsColors.Gold]
)}

function _110(colorTable,nationality,nationalityColors){return(
colorTable(nationality,nationalityColors)
)}

function _111(md){return(
md`#### Trägerschaft`
)}

function _ownership(){return(
["öffentlich","privat"]
)}

function _ownershipColors(graphicsColors,additionalGraphicsColors){return(
[graphicsColors.Orange, additionalGraphicsColors.Grün]
)}

function _114(colorTable,ownership,ownershipColors){return(
colorTable(ownership,ownershipColors)
)}

function _115(md){return(
md`### Parteifarben gemäss Designstandards`
)}

function _partyColors(additionalGraphicsColors,graphicsColors){return(
{
  SVP: additionalGraphicsColors.Grün,
  SP: graphicsColors.Rot,
  FDP: "#0070B4",
  CVP: "#DC7700",
  Grüne: "#00544C",
  GLP: "#8A8C00",
  EVP: "#009EE0",
  EDU: "#96170F",
  Lega: "#7F3DA7",
  AL: "#D40053",
  SD: "#00407C",
  BDP: "#f3bf00",
  CSP: "#0fa693",
  CVP: "#ff9e16",
  Andere: graphicsColors.Black60ZH
}
)}

function _117(colorTable,partyColors){return(
colorTable(Object.keys(partyColors), Object.values(partyColors))
)}

function _118(md){return(
md`### Allgemeine Farben`
)}

function _categorialColors(d3,graphicsColors,additionalGraphicsColors){return(
function categorialColors(levels, other) {
  let colors = d3.quantize(
    d3.interpolateRgbBasis([
      graphicsColors.Gold,
      additionalGraphicsColors.Grün,
      graphicsColors.Türkis,
      graphicsColors.Blau,
      graphicsColors.Violett
    ]),
    levels
  );
  if (other == true) {
    colors.push(graphicsColors.Black60ZH);
  }
  return colors;
}
)}

function _120(categorialColors){return(
categorialColors(9, false)
)}

function _showColors(d3,width){return(
function showColors(colors) {
  if (typeof colors === "string") {
    colors = [colors];
  }
  const svg = d3.create("svg").attr("width", width).attr("height", 30);
  svg
    .selectAll()
    .data(colors)
    .enter()
    .append("rect")
    .attr("width", 30)
    .attr("height", 30)
    .attr("fill", function (d) {
      return d;
    })
    .attr("x", function (d, i) {
      return 30 * i;
    })
    .attr("stroke", "white");
  return svg.node();
}
)}

function _122(showColors,categorialColors){return(
showColors(categorialColors(8, true))
)}

function _monochromeBlueZH(){return(
["#125c96", "#559ee1"]
)}

function _124(showColors,monochromeBlueZH){return(
showColors(monochromeBlueZH)
)}

function _monochromeBlueExtZH(monochromeBlueZH){return(
[...monochromeBlueZH, "#cfdfef"]
)}

function _monochromeBlueExtZHshow(showColors,monochromeBlueExtZH){return(
showColors(monochromeBlueExtZH)
)}

function _monochromeMagentaZH(){return(
["#9e1d4d", "#e26d8d"]
)}

function _128(showColors,monochromeMagentaZH){return(
showColors(monochromeMagentaZH)
)}

function _monochromeMagentaExtZH(monochromeMagentaZH){return(
[...monochromeMagentaZH, "#eed6db"]
)}

function _monochromeMagentaExtZHshow(showColors,monochromeMagentaExtZH){return(
showColors(monochromeMagentaExtZH)
)}

function _monochromeGreenZH(){return(
["#15665f", "#3eada2"]
)}

function _132(showColors,monochromeGreenZH){return(
showColors(monochromeGreenZH)
)}

function _monochromeGreenExtZH(monochromeGreenZH){return(
[...monochromeGreenZH, "#c0e6e1"]
)}

function _monochromeGreenExtZHshow(showColors,monochromeGreenExtZH){return(
showColors(monochromeGreenExtZH)
)}

function _monochromeOrangeZH(){return(
["#86450a", "#dd7c2f"]
)}

function _136(showColors,monochromeOrangeZH){return(
showColors(monochromeOrangeZH)
)}

function _monochromeOrangeExtZH(monochromeOrangeZH){return(
[...monochromeOrangeZH, "#eed8cb"]
)}

function _138(showColors,monochromeOrangeExtZH){return(
showColors(monochromeOrangeExtZH)
)}

function _monochromeVioletZH(){return(
["#782fa1", "#ae86c9"]
)}

function _140(showColors,monochromeVioletZH){return(
showColors(monochromeVioletZH)
)}

function _monochromeVioletExtZH(monochromeVioletZH){return(
[...monochromeVioletZH, "#e0dae5"]
)}

function _142(showColors,monochromeVioletExtZH){return(
showColors(monochromeVioletExtZH)
)}

function _monochromeGoldZH(){return(
["#695810", "#b39727"]
)}

function _144(showColors,monochromeGoldZH){return(
showColors(monochromeGoldZH)
)}

function _monochromeGoldExtZH(monochromeGoldZH){return(
[...monochromeGoldZH, "#e6ddbf"]
)}

function _146(showColors,monochromeGoldExtZH){return(
showColors(monochromeGoldExtZH)
)}

function _divergingRedBlueZH(){return(
[
  "#9e1d4d",
  "#bf2960",
  "#d94274",
  "#e26d8d",
  "#e594a7",
  "#e8b7c1",
  "#eed6db",
  "#f1f1f1",
  "#cfdfef",
  "#aacae9",
  "#80b4e6",
  "#559ee1",
  "#2c88d3",
  "#1b72b6",
  "#125c96"
]
)}

function _148(showColors,divergingRedBlueZH){return(
showColors(divergingRedBlueZH)
)}

function _show1(ramp,d3,divergingRedBlueZH){return(
ramp(
  d3
    .scaleSequential()
    .domain([1, 100])
    .interpolator(d3.piecewise(d3.interpolateRgb, divergingRedBlueZH))
)
)}

function _divergingBlueRedZH(divergingRedBlueZH){return(
divergingRedBlueZH.toReversed()
)}

function _151(showColors,divergingBlueRedZH){return(
showColors(divergingBlueRedZH)
)}

function _divergingOrangeAquamarineZH(){return(
[
  "#86450a",
  "#a4560f",
  "#c26817",
  "#dd7c2f",
  "#e79b65",
  "#eabb9c",
  "#eed8cb",
  "#f1f1f1",
  "#c0e6e1",
  "#8dd6cd",
  "#60c3b8",
  "#3eada2",
  "#22968c",
  "#1b7e75",
  "#15665f"
]
)}

function _153(showColors,divergingOrangeAquamarineZH){return(
showColors(divergingOrangeAquamarineZH)
)}

function _show2(ramp,d3,divergingOrangeAquamarineZH){return(
ramp(
  d3
    .scaleSequential()
    .domain([1, 100])
    .interpolator(d3.piecewise(d3.interpolateRgb, divergingOrangeAquamarineZH))
)
)}

function _divergingAquamarineOrangeZH(divergingOrangeAquamarineZH){return(
divergingOrangeAquamarineZH.toReversed()
)}

function _156(showColors,divergingAquamarineOrangeZH){return(
showColors(divergingAquamarineOrangeZH)
)}

function _157(md){return(
md`### Basisfarben gemäss VADE

Werden nur im VADE verwendet. Im Web sollten die Farben von oben verwendet werden.`
)}

function _basicColors(){return(
{
  cyanZH: "#009ee0",
  yellowZH: "#ffcc00",
  orangeZH: "#eb690b",
  turquoiseZH: "#00a1a3",
  greenZH: "#3ea743",
  violetZH: "#885ea0",
  magentaZH: "#e30059",
  redZH: "#e2001a",
  blueZH: "#0070B4",
  greyZH: "#6b6b6b",
  olivegreenZH: "#4a4e11",
  darkgreenZH: "#296029",
  darkvioletZH: "#892d55"
}
)}

function _159(showColors,basicColors){return(
showColors(Object.values(basicColors))
)}

function _160(d3,monochromeBlueZH){return(
d3.scaleSequential(d3.interpolate(monochromeBlueZH)).domain([1, 100])(1)
)}

function _163(ramp,d3,monochromeBlueExtZH){return(
ramp(
  d3
    .scaleSequential(d3.interpolateRgbBasis(monochromeBlueExtZH))
    .domain([1, 100])
)
)}

function _$(){return(
import("https://unpkg.com/jquery?module")
)}

function _colorTable(Inputs,showColors){return(
function colorTable (labels, colors) {
  //Tabelleninhalt generieren
  var output = labels.map(function (labelsVal, row) {
    return {"Label": labelsVal, "Farbcode": colors[row], "Farbe": colors[row]};
  });
  //Tabelle generieren
  var colortable = Inputs.table(output, {
    format: {
      Farbe: x => showColors([x])
    },
    maxWidth:"500px",
    width: {
      Farbe: "40px",
      Farbcode: 85
    },
    height: "auto"
  })
  return colortable
}
)}

function _stylesheet(html){return(
html`<link rel='stylesheet' href='https://www.web.statistik.zh.ch/bista/zhwebstyle.css'/>`
)}

function _leuVersion(){return(
"0.24.0"
)}

function _leuStyleSheet(html,leuVersion){return(
html`<link rel="stylesheet" href="https://esm.sh/@statistikzh/leu@${leuVersion}/dist/theme.css">`
)}

function _manualstylesheet(html){return(
html`
<style>
html {
  -ms-overflow-style:-ms-autohiding-scrollbar;
  background:#fff;
  color:#000;
  font-family:InterRegular, Helvetica, sans-serif;
  font-size:100%;
  line-height:1.5;
  scroll-behavior:smooth;
  scroll-padding-top:7.5rem
}
.icon {
  height:1.5rem;
  width:1.5rem
}
.atm-button,
.mdl-locations__details_location .mdl-contact__subtitle-link {
  align-items:center;
  background:#000;
  border:none;
  border-radius:1px;
  color:#fff;
  cursor:pointer;
  display:flex;
  font-family:InterBlack,Arial Black,Helvetica,sans-serif;
  font-size:1rem;
  height:3rem;
  line-height:1.4;
  max-width:100%;
  min-width:3rem;
  padding:1px 24px 0;
  position:relative;
  transition:background .1s ease
}
.atm-button:not(button),
.mdl-locations__details_location .mdl-contact__subtitle-link:not(button) {
  display:inline-flex;
  text-decoration:none
}
.atm-button__text {
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap
}
.atm-button use,
.mdl-locations__details_location .mdl-contact__subtitle-link use {
  fill:#fff
}
.atm-button__text:not(.visuallyhidden)+.atm-button__icon {
  margin-left:.75rem
}
.atm-button:hover,
.mdl-locations__details_location .mdl-contact__subtitle-link:hover {
  background:#333
}
.atm-button--icon-only {
  justify-content:center;
  padding:0
}
.atm-button--small,
.mdl-locations__details_location .mdl-contact__subtitle-link {
  font-size:.875rem;
  height:2rem;
  min-width:2rem
}
.atm-button--small .atm-button__icon,
.mdl-locations__details_location .mdl-contact__subtitle-link .atm-button__icon {
  transform:scale(.667)
}
.atm-button--big {
  height:3.5rem
}
.atm-button--big .atm-button__icon {
  margin-left:0!important;
  margin-right:.75rem;
  order:1
}
.atm-button--big .atm-button__text {
  order:2
}
.atm-button--secondary,
.mdl-locations__details_location .mdl-contact__subtitle-link {
  background:#0000001a;
  color:#666;
  transition:color .1s ease
}
.atm-button--secondary use,
.mdl-locations__details_location .mdl-contact__subtitle-link use {
  fill:#666;
  transition:fill .1s ease
}
.atm-button--secondary:hover,
.mdl-locations__details_location .mdl-contact__subtitle-link:hover {
  color:#000
}
.atm-button--secondary:hover use,
.mdl-locations__details_location .mdl-contact__subtitle-link:hover use {
  fill:#000
}
.atm-button--secondary:hover,
.mdl-locations__details_location .mdl-contact__subtitle-link:hover {
  background:#0003
}
.atm-button--secondary:active,
.mdl-locations__details_location .mdl-contact__subtitle-link:active {
  background:#000;
  color:#fff
}
.atm-button--secondary:active use,
.mdl-locations__details_location .mdl-contact__subtitle-link:active use {
  fill:#fff
}
.atm-button--disabled {
  background-color:#d9d9d9;
  cursor:not-allowed
}
.atm-button--disabled use {
  fill:#fff
}
.atm-button--disabled:hover {
  background-color:#d9d9d9
}
.atm-button--disabled:hover use {
  fill:#fff
}
.atm-button .cv-inverted,
.atm-button--cv-inverted,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted,
.mdl-locations__details_location [class*="--cv-inverted"] .mdl-contact__subtitle-link,
[class*="--cv-inverted"] .atm-button,
[class*="--cv-inverted"] .mdl-locations__details_location .mdl-contact__subtitle-link {
  background:#fff;
  color:#000
}
.atm-button .cv-inverted use,
.atm-button--cv-inverted use,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted use,
.mdl-locations__details_location [class*="--cv-inverted"] .mdl-contact__subtitle-link use,
[class*="--cv-inverted"] .atm-button use,
[class*="--cv-inverted"] .mdl-locations__details_location .mdl-contact__subtitle-link use {
  fill:#000
}
.atm-button .cv-inverted:hover,
.atm-button--cv-inverted:hover,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted:hover,
.mdl-locations__details_location [class*="--cv-inverted"] .mdl-contact__subtitle-link:hover,
[class*="--cv-inverted"] .atm-button:hover,
[class*="--cv-inverted"] .mdl-locations__details_location .mdl-contact__subtitle-link:hover {
  background:#ffffffb3
}
.atm-button .cv-inverted.atm-button--secondary,
.atm-button .mdl-locations__details_location .cv-inverted.mdl-contact__subtitle-link,
.atm-button--cv-inverted.atm-button--secondary,
.mdl-locations__details_location .atm-button .cv-inverted.mdl-contact__subtitle-link,
.mdl-locations__details_location .atm-button--cv-inverted.mdl-contact__subtitle-link,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.atm-button--secondary,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.mdl-contact__subtitle-link,
.mdl-locations__details_location [class*="--cv-inverted"] .mdl-contact__subtitle-link,
[class*="--cv-inverted"] .atm-button.atm-button--secondary,
[class*="--cv-inverted"] .mdl-locations__details_location .mdl-contact__subtitle-link {
  background:#0003;
  color:#fff
}
.atm-button .cv-inverted.atm-button--secondary use,
.atm-button .mdl-locations__details_location .cv-inverted.mdl-contact__subtitle-link use,
.atm-button--cv-inverted.atm-button--secondary use,
.mdl-locations__details_location .atm-button .cv-inverted.mdl-contact__subtitle-link use,
.mdl-locations__details_location .atm-button--cv-inverted.mdl-contact__subtitle-link use,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.atm-button--secondary use,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.mdl-contact__subtitle-link use,
.mdl-locations__details_location [class*="--cv-inverted"] .mdl-contact__subtitle-link use,
[class*="--cv-inverted"] .atm-button.atm-button--secondary use,
[class*="--cv-inverted"] .mdl-locations__details_location .mdl-contact__subtitle-link use {
  fill:#fff
}
.atm-button .cv-inverted.atm-button--secondary:hover,
.atm-button .mdl-locations__details_location .cv-inverted.mdl-contact__subtitle-link:hover,
.atm-button--cv-inverted.atm-button--secondary:hover,
.mdl-locations__details_location .atm-button .cv-inverted.mdl-contact__subtitle-link:hover,
.mdl-locations__details_location .atm-button--cv-inverted.mdl-contact__subtitle-link:hover,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.atm-button--secondary:hover,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.mdl-contact__subtitle-link:hover,
.mdl-locations__details_location [class*="--cv-inverted"] .mdl-contact__subtitle-link:hover,
[class*="--cv-inverted"] .atm-button.atm-button--secondary:hover,
[class*="--cv-inverted"] .mdl-locations__details_location .mdl-contact__subtitle-link:hover {
  background:#0006
}
.atm-button .cv-inverted.atm-button--secondary:active,
.atm-button .mdl-locations__details_location .cv-inverted.mdl-contact__subtitle-link:active,
.atm-button--cv-inverted.atm-button--secondary:active,
.mdl-locations__details_location .atm-button .cv-inverted.mdl-contact__subtitle-link:active,
.mdl-locations__details_location .atm-button--cv-inverted.mdl-contact__subtitle-link:active,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.atm-button--secondary:active,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.mdl-contact__subtitle-link:active,
.mdl-locations__details_location [class*="--cv-inverted"] .mdl-contact__subtitle-link:active,
[class*="--cv-inverted"] .atm-button.atm-button--secondary:active,
[class*="--cv-inverted"] .mdl-locations__details_location .mdl-contact__subtitle-link:active {
  background:#fff;
  color:#000
}
.atm-button .cv-inverted.atm-button--secondary:active use,
.atm-button .mdl-locations__details_location .cv-inverted.mdl-contact__subtitle-link:active use,
.atm-button--cv-inverted.atm-button--secondary:active use,
.mdl-locations__details_location .atm-button .cv-inverted.mdl-contact__subtitle-link:active use,
.mdl-locations__details_location .atm-button--cv-inverted.mdl-contact__subtitle-link:active use,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.atm-button--secondary:active use,
.mdl-locations__details_location .mdl-contact__subtitle-link .cv-inverted.mdl-contact__subtitle-link:active use,
.mdl-locations__details_location [class*="--cv-inverted"] .mdl-contact__subtitle-link:active use,
[class*="--cv-inverted"] .atm-button.atm-button--secondary:active use,
[class*="--cv-inverted"] .mdl-locations__details_location .mdl-contact__subtitle-link:active use {
  fill:#000
}
.atm-button--tag {
  border-radius:75.5px;
  display:inline-flex;
  min-width:auto;
  padding:0 16px
}
.atm-button--tag:hover:not(.atm-button--cv-inverted) {
  background:#00000026
}
.atm-button--tag:hover:not(.atm-button--cv-inverted):not(.atm-button--secondary) {
  background:#000c
}
.atm-button--tag:not(.atm-button--tag-top) {
  font-family:InterRegular, Helvetica, sans-serif;
}
.atm-button--tag-filter {
  box-sizing:border-box;
  padding:0 32px 0 16px;
  transition:border-color .25s ease
}
.atm-button--tag-filter:not(.atm-button--cv-inverted) {
  border:1px solid #0000
}
.atm-button--tag-filter:not(.atm-button--cv-inverted):hover {
  border:1px solid #0000006b
}
.atm-button--tag-filter .atm-button__icon {
  margin-left:0;
  position:absolute;
  right:11.25px;
  top:2px;
  transform:scale(.3958) translateX(50%)
}
.atm-button--tag-topic {
  background:#000;
  border-radius:12px;
  color:#fff;
  font-size:12px;
  height:1.5rem;
  padding:0 8px
}
.atm-button--tag-topic:hover {
  background:#000c
}
.atm-button--tag-top {
  font-size:1.125rem;
  height:40px;
  padding:0 12px
}
.atm-button--tag-top:not(.atm-button--small) {
  font-size:2rem;
  height:3rem;
  padding:0 24px
}
.atm-button--tag-edit {
  display:inline-flex;
  flex-direction:row-reverse
}
.atm-button--tag-edit .icon.atm-button__icon {
  margin-left:0;
  margin-right:9px;
  transform:scale(.625)
}
.atm-button__spinner,
.atm-button__spinner:after {
  box-sizing:border-box;
  position:relative
}
.atm-button__spinner {
  color:#fff;
  display:none;
  height:24px;
  left:50%;
  position:absolute;
  top:50%;
  transform:translate(-50%,-50%);
  width:24px
}
.atm-button__spinner:after {
  animation:ball-clip-rotate .75s linear infinite;
  background:#0000;
  border:2px solid;
  border-bottom:2px solid #0000;
  border-radius:100%;
  content:"";
  display:inline-block;
  height:100%;
  width:100%
}
.atm-button--loading {
  pointer-events:none
}
.atm-button--loading .atm-button__spinner {
  display:block
}
.atm-button--loading .atm-button__icon,
.atm-button--loading .atm-button__text {
  visibility:hidden
}
.atm-button--plain-text {
  background:none;
  color:#666;
  font-family:InterRegular, Helvetica, sans-serif;
  padding:0;
  transition:color .1s ease
}
.atm-button--plain-text use {
  fill:#666;
  transition:fill .1s ease
}
.atm-button--plain-text:hover {
  color:#000
}
.atm-button--plain-text:hover use {
  fill:#000
}
.atm-button--plain-text .atm-button__icon {
  margin-left:0!important;
  order:1
}
.atm-button--plain-text .atm-button__text {
  order:2
}
.atm-button--plain-text:hover {
  background:none
}
.mdl-download_list .mdl-context_menu {
  display:none
}
.mdl-context_menu {
  background:#fff;
  border-radius:1px;
  box-shadow:0 0 1rem #00000029,0 0 2px #00000052;
  min-width:320px;
  padding:.5rem 0;
  position:absolute
}
.mdl-context_menu__list {
  list-style-type:none;
  margin:0;
  padding:0
}
.mdl-context_menu__break {
  border:0;
  border-top:1px solid #ccc;
  height:0;
  margin:0
}
.atm-context_menu_item {
  align-items:center;
  color:#666;
  display:flex;
  font-size:1rem;
  min-height:3rem;
  padding:0 12px;
  text-decoration:none;
  transition:color .1s ease;
  width:100%
}
.atm-context_menu_item--selected,
.atm-context_menu_item:active,
.atm-context_menu_item:hover:not(:disabled) {
  background:#f7f7f7;
  color:#000
}
.atm-context_menu_item--selected .atm-context_menu_item__icon use,
.atm-context_menu_item:active .atm-context_menu_item__icon use,
.atm-context_menu_item:hover:not(:disabled) .atm-context_menu_item__icon use {
  fill:#000
}
.atm-context_menu_item:disabled {
  pointer-events:none
}
.atm-context_menu_item:focus {
  outline:none
}
.atm-context_menu_item--selected,
.atm-context_menu_item:active {
  background:#009ee0
}
.atm-context_menu_item--selectable .atm-context_menu_item__icon:first-child {
  opacity:0;
  transition:opacity .1s ease
}
.atm-context_menu_item--selectable.atm-context_menu_item--selected .atm-context_menu_item__icon:first-child {
  opacity:1
}
.atm-context_menu_item__label {
  flex-grow:1
}
.atm-context_menu_item__icon use {
  fill:#666;
  transition:fill .1s ease
}
.atm-context_menu_item__icon:last-child {
  margin-right:.3125rem
}
.atm-context_menu_item__icon:first-child {
  margin-right:.5rem
}
.atm-context_menu_item--hidden {
  display:none
}
.atm-paragraph p {
  margin-bottom: inherit;
  margin-top: inherit;
}

</style>`
)}

function _173(md){return(
md`## SVG-icons`
)}

function _174(md){return(
md`Eine wichtige Quelle für Fragen zur Darstellung in zhweb ist [https://styleguide.zh.ch/](https://styleguide.zh.ch/)

Hier die Icons, welche in zhweb zur Verfügung stehen:`
)}

function _175(html){return(
html`<div><ul class="mdl-button_group" data-init="buttonGroup">
	<li class="mdl-button_group__item"><button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#add-new" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#angle_drop_down" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
  </li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#angle_drop_up" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#angle_left" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#angle_right" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#arrow-down" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#arrow-left" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#arrow-right" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#arrow-up" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#avatar" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#calendar" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#caution" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#chat-message" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#check" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
<ul>
</div>
<div>
<ul class="mdl-button_group" data-init="buttonGroup">
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#clear" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#close" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#comments" viewBox="0 0 16 14"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#conference" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#confirm-plain" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#confirm" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#delete" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#directions" viewBox="0 0 18 18"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#documents" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#download" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#edit" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#email" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#exit" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#facebook" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
<ul>
</div>
<div>
<ul class="mdl-button_group" data-init="buttonGroup">
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#fast-forward" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#fast-rewind" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#file-outline" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#file" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#files" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#filter" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#floppy" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#forward" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#full-screen" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#get-information" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#google" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#heart" viewBox="0 0 16 14"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#hide" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#home" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
<ul>
</div>
<div>
<ul class="mdl-button_group" data-init="buttonGroup">
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#inspect" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#instagram" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#ktzh" viewBox="0 0 184 180"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#ktzh_inverted" viewBox="0 0 184 180"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#kununu" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#layer1-1" viewBox="0 0 17 3"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#layer1" viewBox="0 0 16 16"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#like" viewBox="0 0 14 14"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#link" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#linkedIn" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#locate" viewBox="0 0 22 22"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#location" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#logout-user" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#logout" viewBox="0 0 21.15 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#map location" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#map pin" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#menu-1" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#menu-list" viewBox="0 0 21 15"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
<ul>
</div>
<div>
<ul class="mdl-button_group" data-init="buttonGroup">
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#menu-overflow" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#minus" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#next" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#open mail" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#overflow" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#paperplane" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#pause" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#phone-call" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#pin" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#play-button" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#play" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#plus-horizontal" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#plus-vertical" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#plus" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
<ul>
</div>
<div>
<ul class="mdl-button_group" data-init="buttonGroup">
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#previous" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#remove" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#repost" viewBox="0 0 16 12"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#resize-text" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#search" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#share" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#show" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#skip-next" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#skip-previous" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#snapchat" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#stop" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#tick" viewBox="0 0 36 28"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#time" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#twitter" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
<ul>
</div>
<div>
<ul class="mdl-button_group" data-init="buttonGroup">
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#undo" viewBox="0 0 16 15"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#upload" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#user" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#vote" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#xing" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#youtube-logo" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
	<li class="mdl-button_group__item">
<button class="atm-button atm-button--cv-inverted"><span class="atm-button__text "></span><svg class="icon atm-button__icon" focusable="false"><use href="#youtube" viewBox="0 0 24 24"></use></svg><span class="atm-button__spinner"></span></button>
	</li>
<ul>
</div>`
)}

function _svgicons(htl){return(
htl.html`<div id="m-svgsprites" data-svgsprites="wrapper" style="display: none"><svg xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="clip0002"><path d="M0 0h24v24H0z"></path></clipPath><clipPath id="clip0001"><path d="M0 0h24v24H0z"></path></clipPath></defs><symbol id="add-new" viewBox="0 0 24 24"><path d="M12 1C5.926 1 1 5.925 1 12s4.926 11 11 11 11-4.925 11-11S18.074 1 12 1zm5 12h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"></path></symbol><symbol id="angle_drop_down" viewBox="0 0 24 24"><path d="M17 9.5l-5 5-5-5h10z"></path></symbol><symbol id="angle_drop_up" viewBox="0 0 24 24"><path d="M7 14.5l5-5 5 5H7z"></path></symbol><symbol id="angle_left" viewBox="0 0 24 24"><path d="M14.5 7l-5 5 5 5V7z"></path></symbol><symbol id="angle_right" viewBox="0 0 24 24"><path d="M9.5 17l5-5-5-5v10z"></path></symbol><symbol id="arrow-down" viewBox="0 0 24 24"><path d="M17.25 12.96L12 18l-5.25-5.04 1.392-1.337L11 14.383V5h2v9.383l2.858-2.76 1.392 1.337z"></path></symbol><symbol id="arrow-left" viewBox="0 0 24 24"><path d="M11.04 17.25L6 12l5.04-5.25 1.337 1.392L9.617 11H19v2H9.617l2.76 2.858-1.337 1.392z"></path></symbol><symbol id="arrow-right" viewBox="0 0 24 24"><path d="M13.96 6.75L19 12l-5.04 5.25-1.337-1.392L15.383 13H6v-2h9.383l-2.76-2.858L13.96 6.75z"></path></symbol><symbol id="arrow-up" viewBox="0 0 24 24"><path d="M6.75 10.04L12 5l5.25 5.04-1.392 1.337L13 8.617V18h-2V8.617l-2.858 2.76L6.75 10.04z"></path></symbol><symbol id="avatar" viewBox="0 0 24 24"><path d="M17.25 9.75c0 3.728-2.351 6.75-5.25 6.75-2.9 0-5.25-3.022-5.25-6.75v-3.6c0-3.9 2.764-5.4 5.25-5.4 2.484 0 5.25 1.5 5.25 5.4v3.6zm1.494 9.375c-2.812-.538-3.515-1.327-3.69-2.005a5.65 5.65 0 01-6.103-.005c-.17.688-.862 1.497-3.695 2.01A5.455 5.455 0 00.902 23.25h22.196a5.51 5.51 0 00-4.354-4.125z"></path></symbol><symbol id="calendar" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 0H5v2H0v22h24V2h-5V0h-2v2h-4V0h-2v2H7V0zm10 4h-4v2h-2V4H7v2H5V4H2v18h20V4h-3v2h-2V4zM4 8h4v5H4V8zm10 0h-4v5h4V8zm2 0h4v5h-4V8zm-8 7H4v5h4v-5zm2 0h4v5h-4v-5zm10 0h-4v5h4v-5z" fill="#000"></path></symbol><symbol id="caution" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 24c6.627 0 12-5.373 12-12S18.627 0 12 0 0 5.373 0 12s5.373 12 12 12zm1-10l.5-9h-3l.5 9h2zm-1 5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path></symbol><symbol id="chat-message" viewBox="0 0 24 24"><path d="M18.363 3.578A9.07 9.07 0 0012 1a9.07 9.07 0 00-6.363 2.578C4.008 5.17 3 7.57 3 10c0 2.43 1.008 4.43 2.637 6.021A9.07 9.07 0 0012 18.6V23l6.363-6.611C19.992 14.703 21 12.572 21 10c0-2.43-1.008-4.83-2.637-6.422zM7.499 12a2 2 0 110-4 2 2 0 01.001 4h-.001z"></path></symbol><symbol id="check" viewBox="0 0 24 24"><path d="M17.25 6.75l-7.875 7.5L6 10.875l-1.5 1.5 4.875 4.875 9.375-9-1.5-1.5z"></path></symbol><symbol id="clear" viewBox="0 0 24 24"><path d="M12 1C5.926 1 1 5.926 1 12s4.926 11 11 11 11-4.926 11-11S18.074 1 12 1zm5.25 14.75l-1.5 1.5L12 13.5l-3.75 3.75-1.5-1.5L10.5 12 6.75 8.25l1.5-1.5L12 10.5l3.75-3.75 1.5 1.5L13.5 12l3.75 3.75z"></path></symbol><symbol id="close" viewBox="0 0 24 24"><path d="M12 1C5.926 1 1 5.926 1 12s4.926 11 11 11 11-4.926 11-11S18.074 1 12 1zm5.25 14.75l-1.5 1.5L12 13.5l-3.75 3.75-1.5-1.5L10.5 12 6.75 8.25l1.5-1.5L12 10.5l3.75-3.75 1.5 1.5L13.5 12l3.75 3.75z"></path></symbol><symbol id="comments" viewBox="0 0 16 14"><path d="M.5.625v10H5v2.75l3-2.75h7.5v-10H.5z"></path></symbol><symbol id="conference" viewBox="0 0 24 24"><path d="M21 15.75v-4.5a3 3 0 00-6 0v4.5a3 3 0 002.25 2.887v3.113h-1.5a.75.75 0 100 1.5h4.5a.75.75 0 100-1.5h-1.5v-3.113A3 3 0 0021 15.75z"></path><path d="M13.5 15.75v-4.5a4.5 4.5 0 013.712-4.425c0-.15.038-.3.038-.45C17.25 3.263 14.887.75 12 .75S6.75 3.263 6.75 6.375a5.738 5.738 0 002.287 4.65A9.037 9.037 0 003 19.5h12.525a4.5 4.5 0 01-2.025-3.75z"></path></symbol><symbol id="confirm-plain" viewBox="0 0 24 24"><path d="M9 20.25l-7.875-8.066 1.98-1.89L9 16.125l11.915-12 1.96 2.25L9 20.25z"></path></symbol><symbol id="confirm" viewBox="0 0 24 24"><path d="M12 1C5.926 1 1 5.926 1 12s4.926 11 11 11 11-4.926 11-11S18.074 1 12 1zm-1.5 15.5L6 12l1.5-1.5 3 3 5.956-5.956 1.5 1.413L10.5 16.5z"></path></symbol><symbol id="delete" viewBox="0 0 24 24"><path d="M21.75 3.75H16.5V0H6v3.75H.75a.75.75 0 000 1.5h1.5V24h18V5.25h1.5a.75.75 0 100-1.5zM7.5 1.5H15v2.25H7.5V1.5zm.75 18a.75.75 0 11-1.5 0V8.25a.75.75 0 011.5 0V19.5zm3.75 0a.75.75 0 11-1.5 0V8.25a.75.75 0 111.5 0V19.5zm3.75 0a.75.75 0 11-1.5 0V8.25a.75.75 0 111.5 0V19.5z"></path></symbol><symbol id="directions" viewBox="0 0 18 18"><path d="M18 0L0 5.824 9 9l3.177 9L18 0z"></path></symbol><symbol id="documents" viewBox="0 0 24 24"><path d="M16.5 1.387V5.25h3.863L16.5 1.387zM11.25 9h3.863L11.25 5.137V9z"></path><path d="M9.75 4.5H3v18.75h12.75V10.5h-6v-6z"></path><path d="M15 6.75v-6H8.25V3h2.363a1.5 1.5 0 011.05.45l.637.638 3.863 3.862.637.638a1.5 1.5 0 01.45 1.05V19.5H21V6.75h-6z"></path></symbol><symbol id="download" viewBox="0 0 24 24"><path d="M18.446 11.645l-1.642-1.54-3.679 3.925V.75h-2.25V13.9L7.218 9.756l-1.686 1.488 6.443 7.303 6.47-6.902zM2 21h20v2H2v-2z"></path></symbol><symbol id="edit" viewBox="0 0 24 24"><path d="M4 16L15 5l4 4L8 20l-4-4zM17 3l2-2 4 4-2 2-4-4zM1 23l3.668-1.466-2.202-2.202L1 23z"></path></symbol><symbol id="email" viewBox="0 0 24 24"><path d="M12 3L1 9v12h22V9L12 3zm0 14.145l-9.486-5.271.972-1.748L12 14.856l8.515-4.729.971 1.748L12 17.145z"></path></symbol><symbol id="exit" viewBox="0 0 24 24"><path stroke="null" id="svg_1" d="M23.507 3.267L20.958.717l-8.846 8.846L3.267.718.717 3.267l8.846 8.845-8.845 8.846 2.549 2.549 8.845-8.846 8.846 8.846 2.549-2.549-8.846-8.846 8.846-8.845z"></path></symbol><symbol id="facebook" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M8.996 7.846H6.5v4.103h2.496V24h4.799V11.898h3.348l.357-4.052h-3.705V5.539c0-.955.19-1.334 1.108-1.334h2.596V0h-3.323c-3.571 0-5.181 1.584-5.181 4.615v3.231z"></path></symbol><symbol id="fast-forward" viewBox="0 0 24 24"><path d="M21.75 12l-12-8.25v5.175L2.25 3.75v16.5l7.5-5.137v5.137l12-8.25z"></path></symbol><symbol id="fast-rewind" viewBox="0 0 24 24"><path d="M2.25 12l12-8.25v5.175l7.5-5.175v16.5l-7.5-5.137v5.137L2.25 12z"></path></symbol><symbol id="file-outline" viewBox="0 0 24 24"><path d="M13.5 3L18 7.5h-4.5V3z"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M14.414 1H3.5v22H20V6.586L14.414 1zM5.5 21V3h8L18 7.5V21H5.5z"></path></symbol><symbol id="file" viewBox="0 0 24 24"><path d="M14.625 1.5V6h4.5l-4.5-4.5z"></path><path d="M13.125.75h-9v22.5h15.75V7.5h-6.75V.75z"></path></symbol><symbol id="files" viewBox="0 0 24 24"><path d="M15.75 1.387V5.25h3.863L15.75 1.387z"></path><path d="M14.25 6.75v-6H7.5V19.5h12.75V6.75h-6z"></path><path d="M6 4.5H3.75v18.75H16.5V21H6V4.5z"></path></symbol><symbol id="filter" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M23.25.75H.75v3l9 9v10.5l4.5-4.5v-6l9-9v-3z"></path></symbol><symbol id="floppy" viewBox="0 0 24 24"><path d="M13.125 10.875a1.162 1.162 0 00-.338-.787 1.127 1.127 0 100 1.612 1.162 1.162 0 00.338-.825z"></path><path d="M.75.75v19.5l3 3h19.5V.75H.75zm18.75 21h-15v-4.5h15v4.5zM7.875 10.875a4.125 4.125 0 118.25 0 4.125 4.125 0 01-8.25 0zM19.5 4.5h-15V2.25h15V4.5z"></path></symbol><symbol id="forward" viewBox="0 0 24 24"><path d="M1 12c0 6.074 4.926 11 11 11s11-4.926 11-11S18.074 1 12 1 1 5.926 1 12zm5-1h8l-3-3 2-1.977L19 12l-6 6-2-2 3-3H6v-2z"></path></symbol><symbol id="full-screen" viewBox="0 0 24 24"><path d="M21 19.41l-5.58-5.58-1.59 1.59L19.41 21h-3.285v2.25h7.125v-7.125H21v3.284zM16.125.75V3h3.284l-5.58 5.58 1.591 1.59L21 4.591v3.284h2.25V.75h-7.125zM7.875 3V.75H.75v7.125H3V4.591l5.58 5.579 1.59-1.591L4.591 3h3.284zm.705 10.832L3 19.41v-3.285H.75v7.125h7.125V21H4.591l5.58-5.577-1.591-1.591z"></path></symbol><symbol id="get-information" viewBox="0 0 24 24"><path d="M12 1C5.926 1 1 5.926 1 12s4.926 11 11 11 11-4.926 11-11S18.074 1 12 1zm-.5 5a1.5 1.5 0 110 3.001A1.5 1.5 0 0111.5 6zM15 18H9v-2h2v-4H9v-2h4v6h2v2z"></path></symbol><symbol id="google" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M14.738.5H8.672c-.805 0-1.668.093-2.588.28-.93.216-1.826.678-2.688 1.384-1.256 1.21-1.884 2.554-1.884 4.038 0 1.227.443 2.303 1.33 3.227.846.99 2.078 1.497 3.692 1.516.305 0 .63-.019.974-.058-.057.157-.12.33-.186.518-.075.178-.113.4-.113.667 0 .445.099.825.299 1.141.17.327.366.633.585.92-.708.02-1.597.107-2.668.263a9.493 9.493 0 00-3.096 1.118c-.875.519-1.479 1.122-1.813 1.808C.172 18.008 0 18.631 0 19.191c0 1.146.529 2.131 1.586 2.956 1.048.881 2.634 1.333 4.759 1.353 2.538-.04 4.48-.644 5.827-1.813 1.296-1.13 1.946-2.426 1.946-3.89-.019-1.03-.256-1.866-.71-2.504a10.322 10.322 0 00-1.681-1.724l-1.03-.838a6.35 6.35 0 01-.458-.517c-.185-.206-.278-.467-.278-.781 0-.324.09-.61.27-.854.154-.236.32-.448.503-.634.316-.275.614-.545.893-.81a8.3 8.3 0 00.72-.87c.46-.648.7-1.512.718-2.592 0-.59-.067-1.105-.201-1.548a5.744 5.744 0 00-1.23-2.018 4.095 4.095 0 00-.642-.516h1.871L14.738.503V.5zm-3.325 16.472c.502.57.752 1.238.752 2.004 0 .943-.366 1.715-1.1 2.313-.754.61-1.845.924-3.274.944-1.594-.02-2.85-.374-3.767-1.06-.966-.69-1.45-1.564-1.45-2.624 0-.542.112-1.003.334-1.385.193-.364.43-.67.71-.914.29-.236.575-.418.855-.546.28-.119.497-.206.652-.265a13.202 13.202 0 011.927-.428c.638-.059 1.034-.079 1.187-.059.262 0 .488.011.682.03 1.13.786 1.96 1.45 2.492 1.99zm-.984-8.887a3.143 3.143 0 01-.495 1.181c-.533.541-1.198.828-1.997.857a2.668 2.668 0 01-1.686-.576 4.668 4.668 0 01-1.204-1.403c-.642-1.18-.963-2.318-.963-3.41-.02-.827.2-1.575.66-2.244.545-.64 1.228-.97 2.05-.99.62.02 1.17.202 1.649.546a4 4 0 011.132 1.418c.612 1.21.918 2.412.918 3.602 0 .277-.022.616-.066 1.02h.002zM20.8 10.016V6.844h-1.599v3.172h-3.2v1.586h3.2v3.173h1.6v-3.173H24v-1.586h-3.2z"></path></symbol><symbol id="heart" viewBox="0 0 16 14"><path d="M15.5 4.2A3.75 3.75 0 0011.75.45C10.125.45 8.525 1.5 8 2.95 7.475 1.473 5.875.45 4.25.45A3.75 3.75 0 00.5 4.1v.1c0 .38.06.76.175 1.124C1.525 8.5 5.35 11.724 8 13.95c2.65-2.2 6.45-5.675 7.3-8.6.054-.171.096-.347.125-.525V4.75c.029-.173.046-.349.05-.525L15.5 4.2z"></path></symbol><symbol id="hide" viewBox="0 0 24 24"><path d="M23.786.214a.748.748 0 00-1.047 0L16.905 6.01a11.407 11.407 0 00-4.862-1.16C5.31 4.89.598 11.471.41 11.733l-.299.449.3.411a19.823 19.823 0 005.123 4.825L.3 22.654A.748.748 0 101.346 23.7l22.44-22.44a.748.748 0 000-1.047zM7.555 11.994a4.488 4.488 0 014.488-4.487 4.45 4.45 0 012.58.823l-6.245 6.245a4.45 4.45 0 01-.823-2.58zM19.56 7.62l-3.179 3.179a4.488 4.488 0 01-5.535 5.498L8.34 18.8c1.186.436 2.439.664 3.703.674 6.732 0 11.444-6.583 11.631-6.882l.3-.411-.3-.412A19.932 19.932 0 0019.56 7.62z" fill="#000"></path></symbol><symbol id="home" viewBox="0 0 24 24"><path d="M23 10L12.007 1 1 10v2l10.992-9L23 12v-2z"></path><path d="M3.375 12v11H9v-6h6v6h5.625V12L12 5l-8.625 7z"></path></symbol><symbol id="inspect" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M.75 9a8.251 8.251 0 0116.5 0A8.251 8.251 0 01.75 9zm16.5 6.25L15 17.5l6 5.75L23.25 21l-6-5.75zM9 15c-3.308 0-6-2.692-6-6s2.692-6 6-6 6 2.692 6 6-2.692 6-6 6z"></path></symbol><symbol id="instagram" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M18.447 4.101a1.4 1.4 0 100 2.8 1.4 1.4 0 000-2.8zm3.321 13.227a4.444 4.444 0 01-4.44 4.44H6.672a4.445 4.445 0 01-4.441-4.44V6.672a4.446 4.446 0 014.441-4.441h10.656a4.445 4.445 0 014.44 4.441v10.656zM17.328 0H6.672A6.68 6.68 0 000 6.672v10.656A6.68 6.68 0 006.672 24h10.656A6.68 6.68 0 0024 17.328V6.672A6.68 6.68 0 0017.328 0zM12 16.144A4.15 4.15 0 017.854 12 4.15 4.15 0 0112 7.854 4.15 4.15 0 0116.144 12 4.147 4.147 0 0112 16.144zm0-10.52A6.384 6.384 0 005.624 12 6.384 6.384 0 0012 18.376 6.385 6.385 0 0018.376 12 6.384 6.384 0 0012 5.624z"></path></symbol><symbol id="ktzh" viewBox="0 0 184 180"><path fill-rule="evenodd" clip-rule="evenodd" d="M149.131 71.339v34.868H184l-34.869-34.868z" fill="#009EE0"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M149.131 106.207H184V71.339h-34.869v34.868zm1.017-1.016h32.835V72.356h-32.835v32.835zM48.9 175.507c.644.198 1.34.584 1.671 1.093.813-.969 1.928-3.248 1.442-5.347-1.526 0-2.937 2.385-3.112 4.254zm3.915-6.46c.58 1.127.895 3.11.73 4.322.214.022.482.107.724.212.473-1.176.959-4.014-.097-5.892-.495.082-1.22.616-1.357 1.358zm3.756 1.423c.622-1.827.44-4.041-.212-4.904-.164-.223-1.11.305-1.275.963.52.888 1.022 2.713.968 3.843a1.3 1.3 0 01.52.098zm43.426-2.525c.852.138 1.657.484 2.126.781.415-.69 1.466-3.488.863-5.02-1.728.164-3.017 3.011-2.989 4.239zm3.957-6.09c.427.763.776 2.28.802 3.241.227.017.515.017.721.075.621-1.869.416-4.141-.206-4.97-.376-.124-1.033.863-1.317 1.654zm3.517-1.35c.207-1.046 0-2.995-.556-3.721-.39-.245-.848.496-1.047 1.384.45.65.992 1.663 1.109 2.337.166-.016.317-.016.494 0zm-39.893-54.438c-2.422.89-5.455 2.945-5.546 3.522-.204 1.334-.285 3.261-.285 4.699 1.58-.912 2.029-2.551 3.805-3.96 3.203-2.515 4.759-2.88 4.589-3.248-.37-.676-1.87-1.013-2.563-1.013zm34.709 47.312c-4.833-.504-9.489 3.833-12.535 1.917-1.387-.872-3.242-2.872-4.6-4.865-.855-1.241-3.26-4.829-3.04-6.27.09-.602 1.048-1.044 2.734-2.116 2.946-1.858 5.593-3.726 8.045-5.71 2.985-2.404 7.579-6.042 7.623-10.763.032-3.251-2.118-6.79-3.796-8.963-2.948-3.817-8.024-7.448-12.863-10.205-2.127-1.207-6.1-3.282-8.578-4.264-2.437 1.368-3.64 1.739-5.705 2.85 1.515.61 2.76 1.587 2.514 2.42-.153.519-.535.633-2.347 1.834-1.059.708-2.357 1.729-2.96 2.28-1.334 1.225-2.064 2.583-3.198 3.934-.688.814-1.124 1.118-1.817 1.636-.006.682-.045 1.311-.086 2.174 7.894.221 15.036 2.501 18.479 6.914.492.633 1.255 1.726 1.562 2.539 1.55 4.117-1.08 7.473-3.287 8.931-2.193 1.448-7.192 2.331-8.602 3.662-1.085 1.022-1.183 2.872-2.474 4.468-.578.725-1.263 1.153-2.075 1.621.44.833 2.129 1.564 3.334 1.433.467-.453.935-.765 1.418-1.498.369-.56.693-1.457.667-2.445-.006-.247.342-.519.498.303.784 4.1-3.978 4.577-3.12 9.161.873-.584 2.27-1.281 3.769-.903.376-.8.914-1.27 1.348-1.952.261-.411.569-1.054.53-2.23-.01-.297.391-.411.555.625.472 2.955-2.655 3.704-1.363 8.378.842-.724 2.082-1.044 3.274-1.013.31-.667 1.066-1.342.885-2.822-.04-.328.312-.657.571.436.52 2.189-1.327 3.011-.379 5.899 3.293-1.33 4.134 1.048 5.594 2.922.833 1.081 1.932 2.774 2.8 3.441 2.212 1.695 8.401.238 13.095.732.303-2.552 1.955-4.831 3.967-5.308-.951-3.161-5.124-3.91-7.182-1.794-.312.321-.117-.528.492-1.044 1.975-1.664 5.515-1.153 7.263 1.135.348-.866 1.023-1.622 1.541-1.644-1.479-3.146-5.79-3.848-8.159-1.918-.185.147-.246-.266.411-.841 1.831-1.605 5.748-1.49 8.057.971.158-.896.624-1.564 1.09-1.564-.637-1.029-2.38-2.328-3.95-2.484zm26.062-67.49c-1.496 1.01-1.501 3.382-1.241 4.888.792-.138 1.448-.115 2.143.103.476-1.568-.006-4.08-.902-4.99zm2.803 1.108c.034-1.795-.942-4.295-2.002-5.207-.513.081-.618 1.295-.561 2.097 1.007.873 1.68 2.146 2 3.205.194-.042.41-.09.563-.095zm-1.574-6.525c.72.75 1.459 1.85 1.807 2.815.119-.03.32-.082.449-.082.087-1.275-.707-3.55-1.758-4.457-.452-.124-.616 1.138-.498 1.724zm-5.984-42.384c-1.014-1.578-3.111-2.182-4.2-2.08-.382 1.54 1.616 3.319 2.957 3.816.431-.982.859-1.475 1.243-1.736zm-2.653-3.985c-.956-.927-3.416-2.07-5.184-1.487-.143.718.852 1.681 1.571 2.112.867-.327 2.088-.469 3.401-.167.053-.138.121-.278.212-.458zm-9.811 4.809c-.654-1.802-.537-3.14.182-4.695.351-.76 1.155-1.62 1.699-2.029-.95-.212-1.308-.704-1.427-1.135-5.17 2.763-2.477 8.114-3.008 12.879-.33 2.963-4.096 4.02-6.575 5.57-2.132 1.334-4.22 2.768-5.691 4.271 2.668 6.311.84 7.696 3.818 10.742-.506.61-1.46 1.034-2.159 1.037-.042 2.673-.279 5.095-.966 7.484 2.177-.884 3.796.582 5.611-1.184-1.669-1.27-1.738-3.627-1.311-4.94.25-.76.573-.667.573-.456 0 .383.049.73.136.977.969.25 3.024.347 4.384-.544-2.323-3.97 2.121-7.463 5.487-9.659 2.334-1.522 5.701-3.203 7.366-5.452 2.247-3.028 1.143-6.32 2.585-10.807-1.696-.848-3.94-2.525-3.693-4.927-1.783.224-3.878 2.431-2.729 6.17.192.647-.203.46-.577-.145-1.461-2.74-.158-5.87 1.508-6.786-.936-.595-1.715-1.762-1.618-2.383-2.703.982-3.559 3.326-2.974 6.441.093.459-.291.473-.621-.43zm5.645-8.444c-.956-.452-2.777-.693-4.02.025-.407.358.104.853 1.276 1.093a6.883 6.883 0 012.672-.638c0-.191.026-.264.072-.48zm-33.389-4.52c-.102-.05-.178.18-.334.424a6.31 6.31 0 01-1.112 1.302c.505-.03 1.483.038 1.939.142.057-.676-.341-1.797-.493-1.867zm-10.169 1.68c.62 2.07 4.31.105 7.19-.093.907-.747 1.609-1.502 1.99-2.167-3.514-.703-7.4-.247-9.18 2.26zm10.924-6.646c.281.654.47 1.386.51 1.658.04.286.027.538.178.46.503-.25 1.357-1.386 1.5-2.17-.6.105-1.675.087-2.188.052zM72.55 25.674c2.42-2.007 5.925-2.762 11.066-1.88-.044-.88-.536-2.16-.95-2.774-5.145-.848-10.01-.93-10.116 4.654zm-15-23.54c-7.703-.234-10.384.977-15.113 1.179-.91-.024-1.634-.27-1.912-.396-.226.523-.313 1.838-.01 2.468-2.6 1.553-2.905 4.591-6.331 4.041-.22.937.358 2.22 1.015 2.7.35-.137 1.074-.39.965-.038-1.383 3.917-1.11 5.597-1.46 7.57-.207 1.18-1.888 2.267-3.42 2.567-.11 1.042.556 2.61 2.012 2.872.875-1.776 2.168-2.05 1.944-1.506-.373.903-.68 2.512-.707 3.665-.092 3.873.895 7.793 2.13 10.666 2.407 5.596 5.394 10.066 1.243 12.687.54 1.3 3.225 2.204 5.208 1.41.824-2.16.303-3.777.192-4.311-.036-.188.148-.228.353-.063 1.21 1.017 1.28 3.017 1.047 4.604-.613 4.207-4.21 9.41-1.725 14.303.741-.677 1.888-1.23 2.93-1.462.17-2.555.977-4.358 2.459-5.432.87-.63 1.02-.232.783.033-1.828 2.23-1.702 6.425-1.214 10.19.61 4.703-.874 7.468-2.288 8.21 1.74 1.096 4.628.433 6.115-.342 1.09-.567 2.778-1.973 3.422-3.26-1.644-2.818-1.75-5.456-1.332-7.152.344-1.396 1.124-1.879.978-1.207-1.05 5.93 4.596 8.65 4.47 14.428 2.927-.963 4.202-4.491 3.965-7.81.052-.447.404-.223.567.226 1.661 4.729-1.352 11.319-6.946 10.745.785-2.795-.132-6.072-.944-7.663-.717 1.474-2.078 2.713-3.372 3.443-.173 1.471-.504 2.762-.76 3.833-.924 3.875-2.546 6.573-4.958 9.041-5.273 5.4-7.226 5.836-10.671 10.839-.752.773-3.03 2.008-4.346 2.526-10.437 4.108-19.186-1.482-18.49-12.665.28-4.492 2.627-10.409 4.498-14.684 5.469-12.503 10.615-22.96 11.273-32.497.541-7.842-2.833-15.66-10.991-15.743-5.544-.056-10.886 4.49-11.003 13.606-.069 5.372.055 9.43-2.25 13.096-.488.785-.731 1.172-1.395 2.03 3.177.528 6.533-1.269 8.769-3.828.212.379.553.982.697 1.567 2.353-2.252 2.726-6.404 1.857-9.698 1.533.443 2.912-.491 3.46-1.789-3.539-.467-5.906-3.825-5.349-7.507.332-2.176 2.257-4.555 4.866-4.861 6.804-.803 8.8 6.093 8.707 12.633-.121 8.29-5.13 17.452-9.568 26.743-3.572 7.48-7.625 15.073-8.037 22.175-.458 7.884 3.153 21.973 22.777 18.92.787-2.289 1.757-3.177 2.343-2.913.19.098.05.459-.058 1.194-.354 2.427-.475 3.941-.354 6.534.229 5.103 2.453 10.203 2.714 13.891.413 5.832-2.603 6.508-7.376 7.043-2.005.23-4.993.156-6.818 1.03-1.06.509-1.758 3.141-2.793 4.467-1.018 1.308-2.42 1.958-4.121 2.289.517 1.316 2.286 2.263 4.21 2.312.697-.519 1.46-1.762 1.783-3.244.066-.303.442-.525.401.619-.102 3.067-2.936 6.417-6.1 6.897.57 1.464 2.812 2.576 4.564 2.367 1.372-.732 2.46-2.038 2.962-3.892.129-.525.464-.287.443.403-.04 1.829-.985 3.325-2.227 4.47-1.244 1.142-2.048 2.667-1.643 4.452.82-.411 2.406-.494 3.595-.231.605-.567 1.452-1.514 1.696-2.88.082-.454.546-.355.465.717-.19 2.541-2.287 3.71-1.752 6.115 4.996-2.388 5.543 6.484 9.428 9.158 3.22 2.213 9.192.889 14.622 1.275.39-2.386 1.915-4.83 4.032-5.282-.905-3.417-4.865-3.285-6.678-2.108-.393.263-.279-.262.165-.632 2.2-1.631 5.386-1.13 6.907.757.37-.692 1.106-1.261 1.701-1.359-1.562-3.258-5.292-3.876-7.99-2.221-.488.319-.347-.393.513-.89 3.234-1.876 6.66-.411 8.182 1.984.31-.511.98-1.144 1.493-1.103-.885-2.116-3.189-3.613-6.123-3.555-5.095.09-9.387 3.474-11.252.864-2.1-2.962-4.707-8.334-4.91-14.756 0-.542.02-1.053.504-1.226 3.945-.894 7.672-1.639 11.003-2.714 3.583-1.17 7.15-2.404 9.715-5.416 2.732-3.2 3.478-10.426 3.943-16.285.222-2.8.497-6.947.713-10.017.346-4.914 1.383-8.057 3.307-8.955.489-.228.733.01.354.687-.49.813-.896 2.327-1.087 3.708.858-.674 1.964-1.406 2.732-1.824 2.523-1.368 4.211-2.108 6.994-3.563 2.656-1.393 5.198-3.243 7.095-4.727 1.202-.944 2.597-2.072 3.797-3.692a6.9 6.9 0 01-.751-1.262c-1.354 1.827-4.14 3.341-6.331 3.153.58-1.835-.086-4.401-1.626-5.67-1.704-1.399-2.77-2.183-3.843-3.363-3.58-3.918-.526-12.19-4.197-17.18-.259-.513.299-.375.901.194 2.136 2.022 2.542 5.131 2.981 8.25.334 2.34.47 5.13 1.584 6.878 1.983 3.115 6.5 3.798 6.302 8.489 1.439-.379 3.211-1.77 3.281-2.996-.067-.56-.345-1.822-1.11-2.393-.186-.144-.068-.43.502-.25 1.063.332 1.585 1.64 2.04 2.601.493 1.041 1.004 1.983 1.729 2.825 1.304 1.504 2.905 2.271 3.127 4.714 1.207-.377 2.818-1.62 2.964-3.234-.643-1.819-.226-3.532-2.123-4.789-.248-.165-.135-.583.893-.157 2.418 1.013 2.052 3.902 3.225 5.482.782 1.052 1.719 1.94 3.31 2.294.166-1.479.799-3.077 2.112-3.924-.124-.824-.25-1.317-1.18-2.042-.248-.196-.202-.592.851-.058 2.192 1.112 1.55 4.23 4.481 5.474.834-2.585 3.989-1.694 6.984-.922 1.493.387 3.326.84 4.928.922 5.948.289 6.938-3.711 12.155-5.005-.374-2.598.163-4.982 1.829-5.977-2.18-2.575-5.785-1.257-7.008.504-.271.353-.237-.268.18-.869 1.568-2.367 4.747-2.611 6.684-1.48-.04-.811.272-2.137.766-2.17-1.425-1.6-5.604-2.255-7.867.48-.274.31-.207-.284.123-.77 1.652-2.254 5.377-2.893 7.902-1.011-.023-.528.251-1.666.866-1.694-1.066-1.26-3.19-2.002-5.27-1.793-5.993.6-7.631 7.212-14.093 6.67-1.494-.125-2.94-1.083-5.832-2.076-1.516-.522-3.376-1.036-5.061-1.431-4.626-1.082-8.92-1.14-11.302-4.255-.805-1.05-1.501-2.319-1.772-4.186-.145-.862.192-1.253.432-.678 1.42 2.787 2.9 5.37 6.42 6.054 1.44-2.739 2.52-7.408 2.342-11.448-1.533-.69-1.522-1.383-2.016-1.592.22 3.07-.934 6.276-1.892 7.234-.44-2.876-2.832-5.006-5.293-5.672-.316-.086-.357-.602.983-.513.901.062 3.021.62 3.954 1.855.85-2.96.34-5.731-.707-8.42-.566-1.459-1.92-3.36-3.423-4.461-.327-.24-.191-.61.876-.06 2.737 1.41 4.843 4.172 5.31 8.004 1.445.845 2.05 2.735 4.082 2.194-1.74-1.947-.87-5.206-3.611-9.949-1.457-2.523-3.41-4.338-6.695-5.948-4.05-1.986-8.929-3.384-12.053-4.635-3.276-1.312-5.09-2.763-5.52-7.484-1.098-.493-1.74-1.2-2.392-2.02-.597.52-.964 1.665-.989 2.411-2.126-1.026-3.262-3.186-3.461-5.075-.666.098-2.014 3.94-6.938 2.102 2.925-3.055-1.085-5.464 2.074-9.099.591-.737 1.483-.923 1.091-.375-2.878 4.114.593 5.533-.753 8.223 3.12.293 3.307-3.83 6.044-3.764-.378 1.826.048 4.313 1.157 5.09.656-1.154 1.459-1.913 2.668-2.379.532 2.26 2.128 3.47 4.079 3.904 2.946.652 6.26-1.09 8.667-.748 1.454.205 2.751 1.056 3.27 2.28 1.203-1.176 2.302-5.632 1.825-5.963-4.689-2.93-12.292 3.343-14.512-1.96-.393-.938-.584-2.133-.418-3.197.655-4.282 3.493-6.351 8.59-5.981 2.237.163 7.139 1.216 8.446.247 1.084-.804.786-3.828.129-5.15-1.318-.353-2.845-1.24-2.766-2.21.08-.864.882.952 2.637.409.491-.223.76-1.998.44-2.107-2.817-1.05-6.693-1.712-10.119-1.352-.507 1.531-1.713 1.687-1.815 2.86-.176 2.012-.805 3.666-1.659 4.324-.331.222-.31-.118-.115-.755.242-.785.518-2.094.152-2.904-.782-1.712-4.138-1.473-4.213-3.367-.05-.772.402-.687 3.721.088 1.404.325 1.545.347 1.746-.084.553-1.24-1.351-1.904-3.029-2.31-5.05-1.218-9.703-1.059-11.677-.294 1.994.947 2.51 2.852 1.879 3.761-.435.58-.124-.941-2.367-2.292-2.45-1.475-6.775-1.713-7.62-.524-.475.671-.609 2.663-.461 3.567.25 1.553.75 3.075 2.468 4.225 2.36 1.58 3.949.703 3.728 1.206-.498 1.07-3.575.92-5.376-.512-1.496-1.187-2.605-2.755-2.897-4.982-.205-1.583.006-3.964.73-4.824.98-1.16 3.765-1.416 6.367-.906 2.095-.642 4.866-1.047 6.996-.897-1.49-1.249-4.442-1.89-7.054-1.97zm30.127 19.064c-.51 1.053-1.408 2.406-2.37 2.865 1.523.272 4.113.812 6.025.606 2.389-.26 3.825-2.476 2.553-4.726-.09-.157-.048-.607.542-.286 2.958 1.598 2.345 5.916-.74 7.02-2.945 1.055-6.607-.53-9.192-.959.385.694.653 1.576.705 2.08.723.194 2.525.711 2.457 1.382-.26 2.041-.648 4.491-1.495 6.383-.755 1.685-2.12 3.635-3.788 3.855.34-5.837-6.164-1.81-9.84-3.018-.33 4.152 6.18 5.255 13.137 8.23 3.622 1.552 7.17 3.472 9.532 7.075 2.752-2.093 5.083-3.35 8.727-5.201 1.368-.695 2.63-1.33 2.893-2.627.21-1.028.098-3.742-.118-5.358-1.087-8.101 6.783-12.567 12.081-8.455-.145.238-.296.61-.333 1.003 1.639.42 3.38 1.48 4.492 2.56-.347.396-.615.814-.779 1.296 1.315.57 3.048 1.993 3.6 3.426-.659.577-1.434 1.758-1.716 2.353-.991 2.08-1.001 4.717-1.446 7.093-.389 2.065-1.181 4.367-2.504 5.932-2.881 3.405-8.798 5.295-11.719 8.881-.995 1.224-1.004 3.852.718 4.473-1.65 2.075-4.405 2.401-6.18 2.185.309 1.3 1.769 2.027 2.511 2.1-2.477 4.95-6.855 2.475-8.984 3.82a13.377 13.377 0 01-.553 1.464c3.599.62 7.418 1.893 9.597 2.777 1.908.777 4.806 2.48 7.512 1.487 1.651-.607 3.218-2.3 4.714-3.429 1.988-1.498 4.191-3.214 8.364-2.718 3.706.441 7.618 3.967 7.299 9.718a3.598 3.598 0 00-1.081 0c.171.881.393 2.829.226 4.005a3.83 3.83 0 00-1.303.016c.085 1.065-.221 3.251-.933 4.55-1.062-.353-2.66-.618-4.062-.165-3.909 1.26-6.508 5.482-12.699 4.964-1.457-.125-3.337-.453-4.799-.79-1.383-.311-3.377-1.053-4.336-.915-1.121.159-1.188.88-1.396 2.091-2.745-.459-4.37-2-4.78-3.561-1.218.871-1.118 2.443-1.14 3.858-2.366-.214-4.52-1.087-5.709-2.797-.855 1.72-3.075 3.364-5.663 3.3.158-1.08-.015-2.818-1.189-3.927-1.56 1.916-3.31 3.374-5.838 5.178 4.71 2.36 10.004 5.446 14.608 9.39 4.194 3.587 9.147 9.257 9.411 15.042.283 6.228-4.201 9.827-7.793 12.476-3.557 2.634-6.524 4.755-9.919 7.027-.316.198-.296.37-.21.624.815 2.363 2.028 4.692 3.38 6.421.767.986 2.303 2.798 3.834 2.84 2.359.074 5.71-2.076 8.409-2.414 5.898-.746 10.173 4.197 8.292 10.626a2.404 2.404 0 00-1.222-.232c.062 1.927-.583 3.96-1.136 5.071a3.741 3.741 0 00-1.405-.544c-.291 1.598-1.164 3.728-2.26 4.79-.768-.675-2.003-1.037-2.715-1.118-8.387-.347-12.26.764-15.25-1.171-.953-.616-2.018-2.27-2.875-3.398-.894-1.176-1.884-2.994-2.817-3.226-1.174-.289-1.904.173-2.505.781-.828-1.051-1.348-2.648-1.112-3.991-1.087-.269-2.381.65-3.128 1.391-.914-1.232-1.445-3.514-1.144-5.415-1.455-.328-2.876.644-3.66 1.565-1.43-2.33-1.133-4.88-.266-6.327-1.97-.397-3.688-1.762-4.372-3.672 3.346-1.424 3.814-3.572 4.92-5.959 1.457-3.151 10.76-3.506 11.743-7.95.315-1.415-.157-3.266-.66-4.198-2.496-4.638-10.416-6.103-17.2-6.054-.263 3.843-.676 7.126-1.435 9.973-.712 2.668-1.9 5.244-3.575 7.119-2.229 2.484-6.125 3.884-9.676 4.937-3.558 1.055-6.684 1.753-10.429 2.633-.616.066.305 6.429 2.227 10.551 1.046 2.237 1.438 3.448 3.304 3.167 2.324-.354 5.5-1.917 8.44-1.81 5.988.215 10.176 6.576 6.888 13.071-.385-.224-.673-.373-1.005-.431-.225 1.467-.849 2.913-1.447 3.886a4.302 4.302 0 00-1.345-.667c-.594 1.835-1.779 3.373-2.805 4.056-.745-.756-1.758-1.448-3.216-1.505-9.044-.34-12.946.988-16.62-2.353-1.2-1.097-2.146-2.889-2.933-4.717-1.536-3.563-2.756-5.52-5.394-2.92-1.086-1.639-1.21-3.704-.499-5.069-1.18-.381-2.787.14-3.746.614-.956-1.684-.834-4.441.198-5.799-2.485-.248-4.846-2.305-5.302-5.054 1.418.041 3.21-.715 4.208-1.702-2.307-.471-4.155-2.476-4.691-5.16 1.526 0 3.259-.34 4.232-1.096 2.196-1.719 1.505-5.176 4.906-6.312 4.08-1.366 12.062.478 12.293-4.617.1-2.131-1.459-6.204-2.123-8.746a33.682 33.682 0 01-1.1-8.64C12.149 117.87 6.12 105.402 6.65 95.279c.436-8.261 3.415-13.994 8.203-23.528 5.902-11.747 10.187-20.203 9.824-28.272-.166-3.68-1.521-8.016-4.263-8.782-5.235-1.466-7.236 4.471-4.696 7.529.858 1.031 2.516 1.789 4.502 1.585.067 2.733-1.323 4.41-3.259 4.866.675 5.005-1.375 9.228-4.947 11.184-.043-.575-.192-1.034-.341-1.588C9.106 60.279 3.586 62.385 0 59.963c1.057-1.208 1.598-1.839 2.279-2.776 1.403-1.925 2.574-4.244 2.742-6.906.176-2.782.29-5.507.346-7.782.174-7.174 4.938-14.587 13.694-13.935 7.376.546 11.556 6.572 11.935 14.636.437 9.296-4.26 19.965-10.62 34.873-2.528 5.917-4.88 12.075-4.69 16.827.236 5.836 4.14 9.923 9.652 10.066 3.361.081 7.512-1.539 9.253-3.309.243-.248.479-.593 1.42-1.9 4.205-5.835 12.825-9.605 13.339-18.803-2.886.886-6.601-.893-7.227-3.017 2.574-.951 4.413-3.04 3.774-8.4-.044-.501-.11-1.214-.135-1.831-1.424.238-2.59 1.253-3.264 2.347-4.679-4.826-2.261-10.987-.674-15.275-3.598.177-6.482-2.58-6.85-5.029 1.74-.227 2.835-1.498 2.792-3.025-.034-1.263-.919-3.18-1.612-4.689-1.982-4.317-3.898-8.656-3.789-14.542-2.576-1.215-3.71-4.226-3.636-6.597 2.21-.161 3.781-1.213 3.848-2.625.055-1.124.242-3.223.71-4.608-.843-.822-2.194-3.338-.868-6.291.942.219 2.422.26 3.32-.234.39-.218 1.152-1.579 2.45-2.527-.19-.92-.013-2.975 1.012-4.277.632.286 1.654.565 2.66.666 4.359.442 14.727-2.637 22.39.25 1.597.604 2.951 1.516 3.947 2.512 1.522.163 3.433.49 5.318.915 3.752.84 3.676 1.515 5.076 1.788.569.11 2.14.222 3.712.357 1.675.143 6.498 1.021 7.453 2.048.869.94-.02 2.628.03 4.473.044 1.704.9 4.719-.26 6.746-.376.654-1.117.984-1.85 1.109zm-26.073-9.122c-.229 1.076-1.16 1.342-1.165.538-.01-2.292-2.413-3.458-4.953-3.684-.673-.062-.001-.551.7-.617 2.429-.232 5.94 1.303 5.418 3.763zm-20.736 20.45c-.86 4.887 1.792 5.198 1.935 8.8 1.764.334 3.705-.949 4.773-2.63.177-.28.343.005.188.624-.63 2.528-3.867 5.009-6.983 3.923 1.402-3.29-2.66-6.463-.487-10.484.43-.787.636-.636.575-.233zm8.73 13.258c.283-.352.53-.257.429.09-2.435 8.105 3.548 8.682 4.004 15.67 2.486-.67 3.603-2.682 4.423-5.081.193-.648.527-.29.48.578-.098 1.803-.595 3.269-1.166 4.136-1.025 1.559-3.362 3.513-6.326 3.02 1.883-6.097-3.25-8.366-3.266-13.84-.003-1.274.507-3.515 1.422-4.573zm31.757 14.61c-.197-.286-.21-.815.865.169 4.852 4.442.07 12.18 3.325 16.006-4.468 1.747-8.745-1.337-9.245-3.975-.233-1.296.698.434 1.93 1.249 1.034.686 3.047 1.392 4.1 1.15-1.253-4.759 2.612-8.796-.975-14.599z" fill="#000"></path></symbol><symbol id="ktzh_inverted" viewBox="0 0 184 180"><path fill-rule="evenodd" clip-rule="evenodd" d="M184 106.207V71.338h-34.869L184 106.207z" fill="#FFFFFE"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M149.131 106.208H184V71.339h-34.869v34.869zm1.017-1.017h32.835V72.356h-32.835v32.835zM48.9 175.507c.644.198 1.34.584 1.671 1.093.813-.969 1.928-3.248 1.442-5.347-1.526 0-2.937 2.385-3.112 4.254zm3.915-6.46c.58 1.127.895 3.11.73 4.322.214.022.482.106.724.212.473-1.176.959-4.015-.097-5.892-.495.082-1.22.616-1.357 1.358zm3.756 1.423c.622-1.827.44-4.041-.212-4.904-.164-.223-1.11.305-1.275.963.52.888 1.022 2.713.968 3.843a1.3 1.3 0 01.52.098zm43.426-2.525c.852.138 1.657.484 2.126.781.415-.69 1.466-3.488.863-5.02-1.728.164-3.017 3.011-2.989 4.239zm3.957-6.09c.427.763.776 2.28.802 3.241.227.017.515.017.721.075.621-1.869.416-4.141-.206-4.97-.376-.124-1.034.863-1.317 1.654zm3.517-1.35c.207-1.046 0-2.995-.556-3.721-.39-.245-.848.496-1.047 1.384.45.649.992 1.663 1.109 2.337.166-.016.317-.016.494 0zm-39.893-54.438c-2.422.89-5.455 2.945-5.546 3.522-.204 1.334-.285 3.261-.285 4.699 1.58-.912 2.029-2.551 3.805-3.96 3.203-2.515 4.759-2.88 4.589-3.248-.37-.676-1.87-1.013-2.563-1.013zm34.709 47.312c-4.833-.504-9.489 3.833-12.535 1.917-1.387-.872-3.242-2.872-4.601-4.865-.854-1.241-3.259-4.829-3.038-6.27.09-.602 1.047-1.044 2.733-2.116 2.946-1.858 5.593-3.727 8.045-5.71 2.985-2.404 7.579-6.042 7.623-10.763.032-3.251-2.118-6.79-3.796-8.963-2.948-3.817-8.024-7.448-12.863-10.205-2.127-1.207-6.1-3.282-8.578-4.264-2.437 1.368-3.64 1.738-5.705 2.85 1.515.61 2.76 1.587 2.514 2.42-.153.519-.535.633-2.347 1.834-1.059.708-2.357 1.728-2.96 2.28-1.334 1.225-2.064 2.583-3.198 3.934-.688.814-1.124 1.118-1.817 1.636-.006.682-.045 1.311-.086 2.173 7.894.222 15.036 2.502 18.478 6.915.493.633 1.256 1.726 1.563 2.539 1.55 4.117-1.08 7.473-3.287 8.931-2.193 1.448-7.192 2.331-8.602 3.662-1.085 1.022-1.183 2.872-2.474 4.467-.578.726-1.263 1.154-2.075 1.622.44.832 2.129 1.563 3.334 1.433.467-.453.935-.765 1.418-1.499.369-.559.693-1.456.667-2.444-.006-.247.342-.519.498.303.784 4.1-3.978 4.577-3.12 9.161.873-.584 2.27-1.281 3.769-.903.376-.8.914-1.27 1.348-1.952.261-.411.569-1.054.53-2.23-.01-.297.39-.411.555.625.472 2.955-2.655 3.704-1.363 8.377.842-.723 2.082-1.043 3.274-1.013.31-.666 1.066-1.341.885-2.821-.04-.328.312-.657.571.436.52 2.189-1.327 3.011-.379 5.899 3.293-1.33 4.134 1.048 5.594 2.922.833 1.081 1.932 2.774 2.8 3.441 2.212 1.695 8.401.238 13.095.732.303-2.552 1.955-4.831 3.967-5.308-.951-3.161-5.124-3.91-7.182-1.794-.312.321-.117-.528.492-1.044 1.975-1.664 5.515-1.153 7.263 1.135.348-.866 1.023-1.622 1.541-1.644-1.48-3.146-5.79-3.848-8.159-1.918-.185.147-.246-.266.411-.841 1.831-1.605 5.748-1.49 8.057.971.158-.897.624-1.564 1.09-1.564-.638-1.029-2.38-2.328-3.95-2.484zm26.062-67.49c-1.497 1.01-1.501 3.382-1.241 4.888.792-.138 1.448-.115 2.143.103.476-1.568-.006-4.08-.902-4.99zm2.803 1.108c.034-1.795-.942-4.295-2.002-5.207-.513.081-.618 1.295-.561 2.097 1.007.873 1.68 2.146 2 3.205.194-.042.41-.09.563-.095zm-1.574-6.525c.72.75 1.459 1.85 1.807 2.815.119-.031.32-.082.449-.082.087-1.275-.707-3.55-1.758-4.457-.452-.124-.616 1.138-.498 1.724zm-5.985-42.384c-1.013-1.578-3.11-2.182-4.199-2.08-.382 1.54 1.616 3.319 2.957 3.816.431-.982.859-1.475 1.242-1.736zm-2.652-3.985c-.956-.927-3.416-2.07-5.184-1.487-.143.718.852 1.681 1.571 2.112.867-.327 2.088-.469 3.401-.167a5.01 5.01 0 01.212-.458zm-9.811 4.809c-.654-1.802-.537-3.14.182-4.695.351-.76 1.155-1.62 1.699-2.029-.95-.212-1.308-.704-1.427-1.135-5.17 2.763-2.477 8.114-3.008 12.879-.33 2.963-4.096 4.02-6.575 5.57-2.132 1.334-4.22 2.768-5.691 4.271 2.668 6.311.84 7.696 3.818 10.742-.506.609-1.46 1.034-2.159 1.037-.042 2.673-.279 5.095-.966 7.484 2.177-.884 3.796.582 5.611-1.184-1.669-1.27-1.738-3.627-1.311-4.94.25-.76.573-.667.573-.456 0 .383.049.73.136.977.969.25 3.024.347 4.384-.544-2.323-3.97 2.121-7.463 5.487-9.659 2.334-1.522 5.701-3.203 7.366-5.452 2.247-3.028 1.143-6.32 2.585-10.807-1.696-.848-3.94-2.525-3.693-4.927-1.783.224-3.878 2.431-2.729 6.17.192.647-.203.46-.578-.145-1.46-2.74-.157-5.87 1.509-6.786-.936-.595-1.715-1.762-1.618-2.383-2.703.982-3.56 3.326-2.974 6.441.093.459-.291.473-.621-.43zm5.645-8.444c-.956-.452-2.777-.693-4.02.025-.407.358.104.853 1.276 1.093a6.883 6.883 0 012.672-.638c0-.191.026-.264.072-.48zm-33.389-4.52c-.102-.05-.178.18-.334.424-.22.334-.589.85-1.112 1.302.505-.03 1.483.038 1.939.142.057-.676-.341-1.797-.493-1.867zm-10.169 1.68c.62 2.07 4.31.105 7.19-.093.907-.747 1.609-1.502 1.99-2.167-3.514-.703-7.4-.247-9.18 2.26zm10.924-6.646c.281.654.47 1.386.51 1.658.04.286.027.538.178.46.503-.25 1.357-1.386 1.5-2.17-.6.105-1.675.087-2.188.052zM72.55 25.674c2.42-2.007 5.925-2.762 11.066-1.88-.044-.88-.536-2.16-.95-2.774-5.145-.848-10.01-.93-10.116 4.654zm-15-23.54c-7.702-.234-10.383.977-15.112 1.179-.91-.024-1.634-.27-1.912-.396-.226.523-.313 1.838-.01 2.468-2.6 1.553-2.905 4.591-6.331 4.041-.22.937.358 2.22 1.015 2.7.35-.137 1.074-.39.965-.038-1.383 3.917-1.11 5.597-1.46 7.57-.207 1.18-1.888 2.267-3.42 2.567-.11 1.042.556 2.61 2.012 2.872.875-1.776 2.168-2.05 1.944-1.506-.373.903-.68 2.512-.707 3.665-.092 3.873.895 7.793 2.13 10.666 2.407 5.596 5.394 10.066 1.243 12.687.54 1.3 3.225 2.204 5.208 1.41.824-2.16.303-3.777.192-4.311-.036-.188.148-.228.353-.063 1.21 1.017 1.28 3.017 1.047 4.604-.613 4.207-4.21 9.41-1.725 14.303.741-.677 1.888-1.23 2.93-1.462.17-2.555.977-4.358 2.459-5.432.87-.63 1.02-.232.783.033-1.828 2.23-1.702 6.425-1.214 10.19.61 4.703-.874 7.468-2.288 8.21 1.74 1.096 4.628.432 6.115-.342 1.09-.567 2.778-1.973 3.422-3.26-1.644-2.818-1.75-5.456-1.332-7.152.344-1.396 1.124-1.879.978-1.207-1.05 5.93 4.596 8.65 4.47 14.428 2.927-.963 4.202-4.491 3.965-7.81.052-.447.404-.223.567.226 1.661 4.729-1.352 11.319-6.946 10.745.785-2.795-.132-6.072-.944-7.664-.717 1.475-2.078 2.714-3.372 3.444-.173 1.471-.504 2.762-.76 3.833-.924 3.875-2.546 6.573-4.958 9.041-5.273 5.4-7.226 5.836-10.671 10.839-.752.773-3.03 2.008-4.346 2.526-10.437 4.108-19.186-1.482-18.49-12.665.28-4.492 2.627-10.41 4.498-14.684 5.469-12.503 10.615-22.96 11.273-32.497.541-7.842-2.833-15.66-10.991-15.743-5.544-.056-10.886 4.49-11.003 13.606-.069 5.372.055 9.43-2.25 13.096-.488.785-.731 1.172-1.395 2.03 3.177.528 6.533-1.27 8.769-3.828.212.379.553.982.697 1.567 2.353-2.252 2.726-6.404 1.857-9.698 1.533.443 2.912-.491 3.46-1.789-3.539-.467-5.906-3.825-5.349-7.507.332-2.176 2.257-4.555 4.866-4.861 6.804-.803 8.8 6.093 8.707 12.633-.121 8.29-5.13 17.452-9.568 26.743-3.572 7.48-7.625 15.073-8.037 22.175-.458 7.884 3.153 21.973 22.777 18.92.787-2.289 1.757-3.177 2.343-2.913.19.098.05.459-.058 1.194-.354 2.427-.475 3.941-.354 6.534.229 5.103 2.453 10.203 2.714 13.89.413 5.833-2.603 6.509-7.376 7.044-2.005.23-4.993.156-6.818 1.03-1.06.509-1.758 3.141-2.793 4.467-1.018 1.308-2.42 1.958-4.121 2.289.517 1.316 2.286 2.263 4.21 2.312.697-.519 1.46-1.762 1.783-3.244.066-.303.442-.525.401.619-.102 3.067-2.936 6.417-6.1 6.897.57 1.464 2.812 2.576 4.564 2.367 1.372-.732 2.46-2.038 2.962-3.892.129-.525.464-.287.443.403-.04 1.829-.985 3.325-2.227 4.47-1.244 1.142-2.048 2.667-1.643 4.452.82-.411 2.406-.494 3.595-.231.605-.567 1.452-1.514 1.696-2.88.082-.454.546-.355.465.717-.19 2.541-2.287 3.71-1.752 6.115 4.996-2.388 5.543 6.484 9.428 9.158 3.22 2.213 9.192.889 14.622 1.275.39-2.386 1.915-4.831 4.032-5.282-.905-3.417-4.865-3.285-6.678-2.108-.393.263-.28-.262.165-.633 2.2-1.63 5.386-1.129 6.907.758.37-.692 1.106-1.261 1.701-1.359-1.562-3.258-5.292-3.876-7.99-2.222-.488.32-.347-.392.513-.889 3.234-1.876 6.66-.411 8.182 1.984.31-.511.98-1.144 1.493-1.103-.885-2.116-3.189-3.613-6.124-3.555-5.094.089-9.386 3.474-11.25.864-2.1-2.962-4.708-8.334-4.911-14.756 0-.542.02-1.053.504-1.227 3.945-.893 7.672-1.638 11.003-2.713 3.583-1.17 7.15-2.404 9.715-5.416 2.732-3.2 3.478-10.426 3.943-16.286.222-2.799.497-6.946.713-10.016.346-4.914 1.383-8.057 3.307-8.955.488-.228.733.01.354.687-.49.813-.896 2.327-1.087 3.708.858-.674 1.964-1.406 2.732-1.824 2.523-1.368 4.211-2.108 6.994-3.563 2.656-1.393 5.198-3.243 7.095-4.727 1.202-.944 2.597-2.072 3.797-3.692a6.898 6.898 0 01-.751-1.262c-1.354 1.827-4.14 3.34-6.331 3.153.58-1.835-.086-4.401-1.626-5.67-1.704-1.399-2.77-2.183-3.843-3.363-3.58-3.918-.526-12.19-4.197-17.18-.259-.513.299-.375.901.194 2.136 2.022 2.542 5.131 2.981 8.25.334 2.34.47 5.13 1.584 6.878 1.983 3.115 6.5 3.798 6.302 8.489 1.439-.379 3.211-1.77 3.281-2.996-.067-.56-.345-1.822-1.11-2.393-.186-.144-.068-.43.502-.25 1.063.332 1.585 1.64 2.04 2.601.493 1.041 1.004 1.983 1.729 2.825 1.304 1.504 2.905 2.271 3.127 4.714 1.207-.377 2.818-1.62 2.964-3.234-.643-1.819-.226-3.532-2.123-4.789-.249-.165-.135-.583.893-.157 2.418 1.013 2.051 3.902 3.225 5.482.782 1.052 1.719 1.94 3.31 2.294.166-1.479.799-3.077 2.112-3.925-.124-.823-.25-1.316-1.18-2.041-.248-.197-.202-.592.851-.058 2.192 1.112 1.55 4.23 4.481 5.474.834-2.585 3.989-1.694 6.984-.922 1.492.387 3.326.84 4.928.922 5.948.289 6.938-3.711 12.155-5.005-.374-2.598.162-4.982 1.829-5.977-2.18-2.575-5.785-1.257-7.008.504-.271.353-.237-.268.18-.869 1.568-2.367 4.747-2.611 6.684-1.48-.04-.811.272-2.137.766-2.17-1.425-1.6-5.604-2.255-7.867.48-.274.31-.207-.284.123-.77 1.652-2.254 5.377-2.893 7.901-1.011-.022-.528.252-1.666.867-1.694-1.066-1.26-3.19-2.002-5.27-1.793-5.993.6-7.631 7.212-14.093 6.67-1.494-.125-2.94-1.083-5.832-2.076-1.516-.522-3.377-1.036-5.061-1.431-4.626-1.082-8.92-1.14-11.302-4.255-.805-1.05-1.501-2.319-1.772-4.186-.145-.862.192-1.253.432-.678 1.42 2.787 2.9 5.37 6.42 6.054 1.44-2.739 2.52-7.408 2.342-11.448-1.533-.69-1.522-1.383-2.016-1.592.22 3.07-.934 6.276-1.892 7.234-.44-2.876-2.832-5.006-5.293-5.672-.316-.086-.357-.602.983-.513.9.062 3.021.62 3.954 1.855.85-2.96.34-5.731-.707-8.42-.566-1.459-1.92-3.36-3.423-4.461-.327-.24-.191-.61.876-.06 2.737 1.41 4.843 4.172 5.31 8.004 1.445.845 2.05 2.735 4.082 2.194-1.74-1.947-.87-5.206-3.611-9.949-1.457-2.523-3.41-4.338-6.695-5.948-4.05-1.986-8.929-3.384-12.053-4.635-3.276-1.312-5.09-2.763-5.52-7.484-1.098-.493-1.74-1.2-2.392-2.02-.597.52-.964 1.665-.989 2.411-2.126-1.026-3.262-3.186-3.461-5.075-.666.098-2.014 3.94-6.938 2.102 2.925-3.055-1.085-5.464 2.074-9.099.591-.737 1.483-.923 1.091-.375-2.879 4.114.593 5.533-.753 8.223 3.12.293 3.307-3.83 6.044-3.764-.378 1.826.047 4.313 1.157 5.09.656-1.154 1.459-1.913 2.668-2.379.532 2.26 2.128 3.47 4.079 3.904 2.946.652 6.26-1.09 8.667-.748 1.454.205 2.751 1.056 3.27 2.28 1.203-1.176 2.302-5.632 1.825-5.963-4.689-2.93-12.292 3.343-14.512-1.96-.393-.938-.584-2.133-.419-3.197.656-4.282 3.494-6.351 8.59-5.981 2.238.163 7.14 1.216 8.447.247 1.084-.804.786-3.828.129-5.15-1.319-.353-2.845-1.24-2.766-2.21.08-.864.882.952 2.637.409.491-.223.76-1.998.44-2.107-2.817-1.05-6.693-1.712-10.119-1.352-.507 1.531-1.713 1.687-1.815 2.86-.176 2.012-.805 3.666-1.659 4.324-.331.222-.31-.118-.115-.755.242-.785.518-2.094.152-2.904-.782-1.712-4.138-1.473-4.213-3.367-.05-.772.402-.687 3.721.088 1.404.325 1.545.347 1.746-.084.553-1.24-1.351-1.904-3.029-2.31-5.05-1.218-9.703-1.059-11.677-.294 1.994.947 2.51 2.852 1.879 3.761-.435.58-.124-.941-2.367-2.292-2.45-1.475-6.775-1.713-7.62-.524-.475.671-.609 2.663-.461 3.567.25 1.553.75 3.075 2.468 4.225 2.36 1.58 3.949.703 3.728 1.206-.498 1.07-3.575.92-5.376-.512-1.496-1.187-2.605-2.755-2.897-4.982-.205-1.583.006-3.964.73-4.824.98-1.16 3.765-1.416 6.367-.906 2.095-.642 4.866-1.047 6.996-.897-1.49-1.249-4.442-1.89-7.054-1.97zm30.128 19.064c-.51 1.053-1.408 2.406-2.37 2.865 1.523.272 4.113.812 6.025.606 2.389-.26 3.825-2.476 2.553-4.726-.09-.157-.048-.607.542-.286 2.958 1.598 2.345 5.916-.74 7.02-2.945 1.055-6.607-.53-9.192-.959.385.694.653 1.576.705 2.08.723.194 2.525.711 2.457 1.382-.26 2.041-.648 4.491-1.495 6.383-.755 1.685-2.12 3.635-3.788 3.855.34-5.837-6.164-1.81-9.84-3.018-.33 4.152 6.18 5.255 13.137 8.23 3.622 1.552 7.17 3.472 9.532 7.075 2.752-2.093 5.083-3.35 8.727-5.201 1.368-.695 2.63-1.33 2.892-2.627.211-1.028.099-3.742-.117-5.358-1.087-8.101 6.783-12.567 12.081-8.455-.145.238-.297.61-.333 1.003 1.639.42 3.38 1.48 4.492 2.56-.347.396-.615.814-.78 1.296 1.316.57 3.049 1.993 3.601 3.426-.659.577-1.434 1.758-1.716 2.353-.991 2.08-1.001 4.717-1.446 7.093-.389 2.065-1.181 4.367-2.504 5.932-2.881 3.405-8.798 5.295-11.719 8.881-.995 1.224-1.004 3.852.718 4.473-1.65 2.075-4.405 2.401-6.18 2.185.309 1.3 1.769 2.027 2.511 2.1-2.477 4.95-6.855 2.475-8.984 3.82a13.376 13.376 0 01-.553 1.464c3.599.62 7.418 1.893 9.597 2.777 1.908.777 4.806 2.48 7.512 1.487 1.651-.607 3.218-2.3 4.714-3.429 1.988-1.498 4.191-3.214 8.364-2.718 3.706.441 7.618 3.967 7.299 9.718a3.605 3.605 0 00-1.081 0c.171.881.393 2.829.226 4.005a3.828 3.828 0 00-1.303.016c.085 1.065-.221 3.251-.933 4.55-1.063-.353-2.66-.618-4.062-.165-3.909 1.26-6.508 5.482-12.699 4.964-1.457-.125-3.337-.453-4.799-.79-1.383-.311-3.377-1.054-4.336-.915-1.121.159-1.188.88-1.396 2.09-2.745-.458-4.37-1.998-4.78-3.56-1.218.871-1.119 2.443-1.14 3.858-2.366-.214-4.52-1.087-5.709-2.797-.855 1.72-3.075 3.364-5.663 3.3.158-1.08-.015-2.818-1.189-3.927-1.56 1.916-3.31 3.374-5.838 5.178 4.709 2.36 10.004 5.446 14.608 9.39 4.194 3.587 9.147 9.257 9.411 15.042.283 6.228-4.201 9.827-7.793 12.476-3.557 2.634-6.524 4.755-9.919 7.027-.316.198-.296.37-.21.624.815 2.363 2.028 4.692 3.38 6.421.767.986 2.303 2.797 3.834 2.84 2.359.074 5.71-2.076 8.409-2.414 5.898-.746 10.173 4.197 8.292 10.626-.373-.19-.889-.271-1.222-.232.062 1.927-.583 3.96-1.136 5.071a3.741 3.741 0 00-1.405-.544c-.291 1.598-1.165 3.728-2.26 4.79-.768-.675-2.003-1.037-2.715-1.119-8.387-.346-12.26.765-15.25-1.17-.953-.616-2.018-2.27-2.875-3.398-.894-1.176-1.884-2.994-2.817-3.226-1.174-.289-1.904.173-2.505.78-.828-1.05-1.348-2.647-1.112-3.99-1.087-.269-2.381.65-3.128 1.391-.914-1.232-1.445-3.514-1.144-5.415-1.455-.328-2.876.644-3.66 1.565-1.43-2.33-1.133-4.88-.266-6.327-1.97-.397-3.688-1.762-4.372-3.672 3.346-1.424 3.814-3.572 4.92-5.959 1.457-3.151 10.76-3.506 11.743-7.95.315-1.415-.157-3.266-.66-4.198-2.496-4.638-10.416-6.103-17.2-6.054-.263 3.843-.676 7.126-1.435 9.973-.712 2.667-1.9 5.244-3.575 7.119-2.229 2.484-6.125 3.884-9.676 4.936-3.558 1.056-6.684 1.754-10.429 2.634-.616.066.305 6.429 2.227 10.551 1.046 2.237 1.438 3.448 3.304 3.167 2.324-.354 5.5-1.917 8.44-1.81 5.988.215 10.176 6.576 6.888 13.071-.385-.224-.673-.373-1.006-.431-.224 1.467-.848 2.913-1.446 3.885a4.32 4.32 0 00-1.345-.666c-.594 1.835-1.779 3.373-2.805 4.056-.745-.756-1.758-1.448-3.216-1.505-9.044-.34-12.946.988-16.62-2.353-1.2-1.097-2.146-2.889-2.933-4.717-1.536-3.563-2.756-5.52-5.394-2.92-1.086-1.639-1.21-3.704-.499-5.069-1.18-.381-2.787.14-3.746.614-.956-1.684-.834-4.441.198-5.799-2.485-.248-4.846-2.305-5.302-5.054 1.418.041 3.21-.715 4.208-1.702-2.307-.471-4.155-2.476-4.691-5.16 1.526 0 3.259-.34 4.232-1.096 2.196-1.719 1.505-5.176 4.906-6.312 4.08-1.366 12.062.478 12.293-4.617.1-2.131-1.459-6.204-2.123-8.746a33.684 33.684 0 01-1.1-8.641C12.149 117.87 6.12 105.402 6.65 95.279c.436-8.261 3.415-13.994 8.203-23.528 5.902-11.747 10.187-20.203 9.824-28.272-.166-3.68-1.521-8.016-4.263-8.782-5.235-1.466-7.236 4.471-4.696 7.529.858 1.031 2.516 1.789 4.502 1.585.067 2.733-1.323 4.41-3.259 4.866.675 5.005-1.375 9.228-4.947 11.184-.043-.575-.192-1.034-.341-1.588C9.106 60.279 3.586 62.385 0 59.963c1.057-1.208 1.598-1.839 2.279-2.776 1.403-1.925 2.574-4.244 2.742-6.906.176-2.782.29-5.507.346-7.782.174-7.174 4.938-14.587 13.694-13.935 7.376.546 11.556 6.572 11.935 14.636.437 9.296-4.26 19.965-10.62 34.873-2.528 5.917-4.88 12.075-4.69 16.827.236 5.836 4.14 9.923 9.652 10.066 3.361.081 7.512-1.539 9.253-3.309.243-.248.479-.593 1.42-1.9 4.205-5.835 12.825-9.605 13.339-18.803-2.886.886-6.601-.893-7.227-3.017 2.574-.951 4.413-3.04 3.774-8.4-.044-.501-.11-1.214-.135-1.831-1.424.238-2.59 1.253-3.264 2.347-4.679-4.826-2.261-10.987-.674-15.275-3.598.177-6.482-2.58-6.85-5.029 1.74-.227 2.835-1.498 2.792-3.025-.034-1.263-.919-3.18-1.612-4.689-1.982-4.317-3.898-8.656-3.789-14.542-2.576-1.215-3.71-4.226-3.636-6.597 2.21-.161 3.781-1.213 3.848-2.625.055-1.124.242-3.223.71-4.608-.843-.822-2.194-3.338-.868-6.291.942.219 2.422.26 3.32-.234.39-.218 1.152-1.579 2.45-2.527-.19-.92-.013-2.975 1.012-4.277.632.286 1.654.565 2.66.666 4.359.442 14.727-2.637 22.39.25 1.597.604 2.951 1.516 3.947 2.512 1.522.163 3.433.49 5.318.915 3.752.84 3.676 1.515 5.076 1.788.569.11 2.14.222 3.712.357 1.675.143 6.498 1.021 7.453 2.048.869.94-.02 2.628.03 4.473.044 1.704.9 4.719-.26 6.746-.376.654-1.117.984-1.85 1.109zm-26.073-9.122c-.229 1.076-1.16 1.342-1.165.538-.01-2.292-2.413-3.458-4.953-3.684-.674-.062-.001-.551.7-.617 2.429-.232 5.94 1.303 5.418 3.763zm-20.736 20.45c-.86 4.887 1.792 5.198 1.935 8.8 1.764.334 3.705-.949 4.773-2.63.177-.28.343.005.188.624-.63 2.528-3.867 5.009-6.983 3.923 1.402-3.29-2.66-6.463-.487-10.484.43-.787.636-.636.575-.233zm8.73 13.258c.283-.352.53-.257.429.09-2.435 8.105 3.548 8.682 4.004 15.67 2.486-.67 3.603-2.682 4.423-5.081.193-.648.527-.29.48.578-.098 1.803-.595 3.269-1.166 4.136-1.025 1.559-3.362 3.513-6.326 3.02 1.883-6.097-3.25-8.366-3.266-13.84-.003-1.274.507-3.515 1.422-4.573zm31.757 14.61c-.197-.286-.21-.815.865.169 4.852 4.442.07 12.18 3.325 16.006-4.468 1.747-8.745-1.337-9.245-3.975-.233-1.296.698.434 1.93 1.249 1.034.686 3.047 1.392 4.1 1.15-1.253-4.759 2.612-8.796-.975-14.599z" fill="#FFFFFE"></path></symbol><symbol id="kununu" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M19.999 18.326c0-1.897-.72-3.627-1.896-4.936a7.356 7.356 0 001.842-4.872v-1.24h-.015a.611.611 0 00-.603-.508h-3.666a.611.611 0 00-.599.508l-.077 1.24a2.416 2.416 0 01-2.415 2.412v.015h-1.24c-.855 0-1.675.15-2.44.417V.612A.613.613 0 008.278 0H4.611A.613.613 0 004 .611v22.777c0 .336.273.612.611.612h3.693a.613.613 0 00.612-.612v-5.063a2.415 2.415 0 012.412-2.415h1.296a2.418 2.418 0 012.412 2.415v5.063c0 .336.275.612.612.612h3.68a.61.61 0 00.61-.612L20 19.56v-1.235h-.001z"></path></symbol><symbol id="layer1-1" viewBox="0 0 17 3"><path d="M.5.5h15.75v2.25H.5V.5z"></path></symbol><symbol id="layer1" viewBox="0 0 16 16"><path d="M15.875 6.875h-6.75V.125h-2.25v6.75H.125v2.25h6.75v6.75h2.25v-6.75h6.75v-2.25z"></path></symbol><symbol id="like" viewBox="0 0 14 14"><path d="M12.5 7.75h.5a1 1 0 100-2H7.5a20.25 20.25 0 00.5-4.5 1 1 0 00-2 0s-1 5.5-4.5 5.5H0v6h2.5c1 0 3 1 4 1h5a1 1 0 000-2h.5a1 1 0 000-2h.5a1 1 0 100-2z"></path></symbol><symbol id="link" viewBox="0 0 24 24"><path d="M22.224 3.635l-1.86-1.859a3.505 3.505 0 00-4.956 0L12.31 4.875a3.505 3.505 0 000 4.957l.31.31.562.562 1.24-1.239-.563-.562-.31-.31a1.753 1.753 0 010-2.479l3.098-3.098a1.753 1.753 0 012.478 0l1.86 1.859a1.753 1.753 0 010 2.478l-3.099 3.098a1.752 1.752 0 01-2.199.227l-1.253 1.253a3.506 3.506 0 004.691-.24l3.099-3.099a3.505 3.505 0 000-4.956zM10.45 17.886l-3.098 3.098a1.753 1.753 0 01-2.478 0l-1.86-1.859a1.752 1.752 0 010-2.478l3.099-3.098a1.753 1.753 0 012.479 0l.309.31.562.562 1.24-1.239-.563-.563-.31-.31a3.505 3.505 0 00-4.956 0l-3.099 3.099a3.505 3.505 0 000 4.957l1.86 1.859a3.506 3.506 0 004.957 0l3.097-3.099a3.506 3.506 0 00.24-4.691l-1.253 1.252a1.753 1.753 0 01-.226 2.2z" fill="currentColor"></path><path d="M17.042 6.958a.877.877 0 010 1.24L8.058 17.18a.875.875 0 01-1.496-.62.88.88 0 01.257-.62l8.984-8.983a.877.877 0 011.239 0z" fill="currentColor"></path></symbol><symbol id="linkedIn" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M5.86 2.952c0 1.631-1.312 2.952-2.93 2.952A2.94 2.94 0 010 2.952C0 1.322 1.312 0 2.93 0c1.617 0 2.93 1.322 2.93 2.952zM.476 24H5.43V8H.477v16zM13.352 8H8.6v16h4.752v-8.399c0-2.25 1.035-3.589 3.019-3.589 1.822 0 2.698 1.286 2.698 3.589V24H24V13.869c0-4.286-2.429-6.357-5.823-6.357-3.396 0-4.825 2.643-4.825 2.643V8z"></path></symbol><symbol id="locate" viewBox="0 0 22 22"><path d="M11 14a3 3 0 100-6 3 3 0 000 6z"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M12.125 18.922a8.005 8.005 0 006.797-6.797h2.953v-2.25h-2.953a8.005 8.005 0 00-6.797-6.797V.125h-2.25v2.953a8.005 8.005 0 00-6.797 6.797H.125v2.25h2.953a8.005 8.005 0 006.797 6.797v2.953h2.25v-2.953zM11 17a6 6 0 100-12 6 6 0 000 12z"></path></symbol><symbol id="location" viewBox="0 0 24 24"><path d="M18.363 3.578A9.067 9.067 0 0012 1a9.067 9.067 0 00-6.363 2.578A8.671 8.671 0 003 9.8a9.475 9.475 0 002.637 6.591L12 23l6.363-6.609A9.475 9.475 0 0021 9.8a8.673 8.673 0 00-2.637-6.222zM12 13c-1.661 0-3-1.34-3-3.001A2.995 2.995 0 0112 7c1.661 0 3 1.34 3 2.999A2.996 2.996 0 0112 13z"></path></symbol><symbol id="lock" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M4.002 15.185c-.057 2.233.9 4.455 2.768 6.005 3.004 2.49 7.456 2.49 10.46 0 1.869-1.55 2.825-3.773 2.768-6.006a7.962 7.962 0 00-1.248-4.48V6.48C18.75 2.901 15.728 0 12 0S5.25 2.901 5.25 6.48v4.224a7.963 7.963 0 00-1.248 4.481zM12 17a2 2 0 110-4 2 2 0 010 4zm4.25-8.779A7.963 7.963 0 0012 7a7.962 7.962 0 00-4.25 1.221V6.48C7.75 4.227 9.653 2.4 12 2.4s4.25 1.827 4.25 4.08v1.741z"></path></symbol><symbol id="logout-user" viewBox="0 0 24 24"><path clip-rule="evenodd" d="M17.707 7.293L22.414 12l-4.707 4.707-1.414-1.414L18.586 13H9v-2h9.586l-2.293-2.293 1.414-1.414z"></path><path clip-rule="evenodd" d="M3 1h7v2H5v18h5v2H3V1z"></path></symbol><symbol id="logout" viewBox="0 0 21.15 24"><path d="M9.356 4.855v13.043h2.44V4.713l3.992 4.257 1.78-1.67L10.576 0 3.56 7.735 5.39 9.35z"></path><path d="M18.712 17.085v4.474H2.44v-4.474H0V24h21.153v-6.915z"></path></symbol><symbol id="map location" viewBox="0 0 24 24"><path d="M12 .75a6.788 6.788 0 00-6.787 6.787C5.213 13.65 12 19.65 12 19.65s6.788-6 6.788-12.112A6.788 6.788 0 0012 .75zm0 9a2.25 2.25 0 110-4.5 2.25 2.25 0 010 4.5z"></path><path d="M16.05 17.475a27.971 27.971 0 01-3.038 3.262l-1.012.9-.975-.862a27.974 27.974 0 01-3.038-3.262c-3.825.412-6.487 1.5-6.487 2.737 0 1.238 4.688 3 10.5 3 5.813 0 10.5-1.35 10.5-3s-2.663-2.325-6.45-2.775z"></path></symbol><symbol id="map pin" viewBox="0 0 24 24"><path d="M12 .75a7.5 7.5 0 00-7.5 7.5c0 6.75 7.5 15 7.5 15s7.5-8.25 7.5-15A7.5 7.5 0 0012 .75z"></path></symbol><symbol id="menu-1" viewBox="0 0 24 24"><path d="M.75 3h22.5v3H.75V3zm0 7.5h22.5v3H.75v-3zm0 7.5h22.5v3H.75v-3z"></path></symbol><symbol id="menu-list" viewBox="0 0 21 15"><path d="M3 0H0v3h3V0zm17 0H6v3h14V0zM0 6h3v3H0V6zm20 0H6v3h14V6zM0 12h3v3H0v-3zm20 0H6v3h14v-3z"></path></symbol><symbol id="menu-overflow" viewBox="0 0 24 24"><path d="M3 15a3 3 0 100-6 3 3 0 000 6zm18 0a3 3 0 100-6 3 3 0 000 6zm-9 0a3 3 0 100-6 3 3 0 000 6z"></path></symbol><symbol id="minus" viewBox="0 0 24 24"><path d="M4.5 10.5h15.75v2.25H4.5V10.5z"></path></symbol><symbol id="next" viewBox="0 0 24 24"><path d="M3 20.175L15 12 3 3.825v16.35zM18 3v18h3V3h-3z"></path></symbol><symbol id="open mail" viewBox="0 0 24 24"><path d="M.75 11.4v10.763l6.3-6.338L.75 11.4zm16.2 4.425l6.3 6.338v-10.65l-6.3 4.312zm-1.087-1.05l6.862-4.725L12 1.05 1.35 9.975l6.787 4.8c1.8-1.688 5.963-1.688 7.726 0z"></path><path d="M9.113 15.863L1.8 23.25h20.4l-7.313-7.387c-1.2-1.163-4.575-1.163-5.774 0z"></path></symbol><symbol id="overflow" viewBox="0 0 24 24"><path d="M1.5 10.5h3v3h-3v-3zm9 0h3v3h-3v-3zm12 0h-3v3h3v-3z"></path></symbol><symbol id="paperplane" viewBox="0 0 24 24"><path d="M1.537 10.65l7.95 3.15L20.925 2.212 1.537 10.65zm9.375 3.862l8.325 5.138 3.226-16.875-11.55 11.737zm-.674 7.276l2.925-4.2-2.925-1.8v6z"></path></symbol><symbol id="pause" viewBox="0 0 24 24"><path d="M4.5 1.5H9v21H4.5v-21zm10.5 0h4.5v21H15v-21z"></path></symbol><symbol id="phone-call" viewBox="0 0 24 24"><path d="M18 1l-4.533 5.133 1.466 2.2-6.599 6.601-2.201-1.467L1 17l2 6c3.666-1.466 8.267-4.399 11.933-8.066C18.601 11.267 21.533 6.667 23 3l-5-2z"></path></symbol><symbol id="pin" viewBox="0 0 24 24"><path d="M12 .75a7.5 7.5 0 00-7.5 7.5c0 6.75 7.5 15 7.5 15s7.5-8.25 7.5-15A7.5 7.5 0 0012 .75zm0 10.5a3 3 0 110-5.999 3 3 0 010 5.999z"></path></symbol><symbol id="play-button" viewBox="0 0 24 24"><path d="M19.35 4.5H4.65a3.9 3.9 0 00-3.9 3.9v7.2a3.9 3.9 0 003.9 3.9h14.7a3.9 3.9 0 003.9-3.9V8.4a3.9 3.9 0 00-3.9-3.9zM9 15.75v-7.5L16.5 12 9 15.75z"></path></symbol><symbol id="play" viewBox="0 0 24 24"><path d="M2.25.75L21.75 12 2.25 23.25V.75z"></path></symbol><symbol id="plus-horizontal" viewBox="0 0 24 24"><path d="M4.1 10.6v2.2h15.8v-2.2H4.1z"></path></symbol><symbol id="plus-vertical" viewBox="0 0 24 24"><path d="M13.1 4.1h-2.2v15.8h2.2V4.1z"></path></symbol><symbol id="plus" viewBox="0 0 24 24"><path d="M13.1 4.1h-2.2v15.8h2.2V4.1z"></path><path d="M4.1 10.6v2.2h15.8v-2.2H4.1z"></path></symbol><symbol id="previous" viewBox="0 0 24 24"><path d="M15.75 8.925l7.5-5.1v16.35l-7.5-5.1v5.1L3.75 12v-.037l12-8.138v5.1zM3.75 3v18h-3V3h3z"></path></symbol><symbol id="remove" viewBox="0 0 24 24"><path d="M12 1C5.926 1 1 5.925 1 12s4.926 11 11 11 11-4.925 11-11S18.074 1 12 1zm5 12H7v-2h10v2z"></path></symbol><symbol id="repost" viewBox="0 0 16 12"><path d="M8.25 3.499V.5l7 5-7 5v-3c-2.783.001-5.318.109-7.5 4 0-2.472.363-7.932 7.5-8.001z"></path></symbol><symbol id="resize-text" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M17 8V5h3v3h-3zm-6 6h3v-3h-3v3zm-3 6H5v-3h3v3zm6 0h-3v-3h3v3zm3-6h3v-3h-3v3zm3 6h-3v-3h3v3z"></path></symbol><symbol id="share" viewBox="0 0 24 24"><g clip-path="url(#clip0)"><path d="M18.075 16.012a3.982 3.982 0 00-2.438.825l-6.974-4.2c.04-.21.066-.423.075-.637a3.304 3.304 0 00-.075-.637L15.637 7.2a3.903 3.903 0 002.438.825 4.013 4.013 0 10-4.012-4.013c.004.215.029.428.074.638L7.163 8.812a3.903 3.903 0 00-2.438-.824 4.013 4.013 0 102.475 7.2l6.975 4.162c-.043.21-.069.423-.075.637a4.013 4.013 0 008.025 0 4.066 4.066 0 00-4.05-3.974z"></path></g></symbol><symbol id="show" viewBox="0 0 24 24"><path d="M22.724 11.662C22.552 11.415 18.207 6 12 6S1.448 11.415 1.276 11.662L1 12l.276.338C1.448 12.585 5.793 18 12 18s10.552-5.415 10.724-5.662L23 12l-.276-.338zM12 15.538a4.501 4.501 0 01-2.299-.623 3.818 3.818 0 01-1.524-1.657 3.324 3.324 0 01-.235-2.133 3.589 3.589 0 011.132-1.89 4.313 4.313 0 012.119-1.011 4.604 4.604 0 012.39.21c.757.28 1.403.753 1.858 1.36.454.607.697 1.32.697 2.051 0 .98-.436 1.919-1.212 2.611-.776.692-1.829 1.082-2.926 1.082z" fill="#000"></path></symbol><symbol id="skip-next" viewBox="0 0 24 24"><path d="M8.25 8.925l-7.5-5.1v16.35l7.5-5.1v5.1l12-8.175v-.037l-12-8.138v5.1zM20.25 3v18h3V3h-3z"></path></symbol><symbol id="skip-previous" viewBox="0 0 24 24"><path d="M21 20.175L9 12l12-8.175v16.35zM6 3v18H3V3h3z"></path></symbol><symbol id="snapchat" viewBox="0 0 24 24"><path d="M11.99.5h-.001c-.962 0-1.898.193-2.784.572a7.216 7.216 0 00-2.274 1.541 7.217 7.217 0 00-1.539 2.272 7.035 7.035 0 00-.57 2.773c-.001.47-.011.926-.03 1.363l-.375-.087a1.859 1.859 0 00-1.556.338c-.337.26-.574.632-.666 1.045a2.014 2.014 0 001.271 2.324l1.125.452c-.745 2.274-2.117 2.71-3.042 3.004a4.637 4.637 0 00-.659.244c-.803.397-.89 1.07-.89 1.341 0 .519.247.992.694 1.333.223.17.5.31.845.427.47.162 1.016.264 1.459.346a3.2 3.2 0 00.106.516c.22.735.683 1.065 1.034 1.211.332.14.676.155.905.155.225 0 .462-.017.713-.036.27-.02.548-.04.823-.04.426 0 .743.05.97.155.31.143.64.335.99.54.97.567 2.072 1.211 3.461 1.211 1.39 0 2.49-.644 3.462-1.212.349-.204.678-.396.99-.54.226-.103.543-.154.969-.154.275 0 .553.02.823.04.251.019.488.036.713.036.23 0 .573-.016.905-.155.35-.146.815-.476 1.034-1.21a3.29 3.29 0 00.106-.517c.443-.082.989-.184 1.46-.346.345-.118.62-.258.844-.427.447-.341.694-.814.694-1.333 0-.27-.087-.944-.89-1.34-.202-.1-.414-.167-.66-.245-.924-.294-2.296-.73-3.04-3.004l1.123-.452a2.014 2.014 0 001.272-2.324 1.825 1.825 0 00-.666-1.045 1.866 1.866 0 00-1.556-.338l-.375.087a32.762 32.762 0 01-.03-1.363 7.002 7.002 0 00-.575-2.776 7.226 7.226 0 00-1.547-2.271 7.256 7.256 0 00-2.28-1.54A7.068 7.068 0 0011.99.5z"></path></symbol><symbol id="stop" viewBox="0 0 24 24"><path d="M3 3h18v18H3V3z"></path></symbol><symbol id="tick" viewBox="0 0 36 28"><path d="M32.125.875l-19.688 18.75L4 11.187l-3.75 3.75 12.188 12.188 23.437-22.5-3.75-3.75z" fill="#1A7F1F"></path></symbol><symbol id="time" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 24c6.627 0 12-5.373 12-12S18.627 0 12 0 0 5.373 0 12s5.373 12 12 12zm1-12.515V4h-2v8.515l3.919 2.799 1.162-1.628-3.081-2.2z"></path></symbol><symbol id="twitter" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M23.998 4.75a9.998 9.998 0 01-2.828.754 4.829 4.829 0 002.165-2.653c-.951.55-2.005.949-3.126 1.164A4.979 4.979 0 0016.615 2.5c-3.178 0-5.514 2.89-4.796 5.89-4.092-.2-7.721-2.11-10.149-5.012-1.29 2.155-.669 4.977 1.524 6.404a4.994 4.994 0 01-2.23-.6c-.053 2.222 1.582 4.299 3.949 4.763a5.078 5.078 0 01-2.224.082c.627 1.906 2.445 3.293 4.6 3.332A10.091 10.091 0 010 19.345 14.215 14.215 0 007.548 21.5c9.142 0 14.307-7.523 13.995-14.269A9.87 9.87 0 0024 4.748l-.002.001z"></path></symbol><symbol id="undo" viewBox="0 0 16 15"><path d="M5.926 6.3L2.657 9.28 0 5.616l1.235-.82.888 1.086a7.122 7.122 0 012.5-3.968A7.24 7.24 0 019.066.333C12.938.333 16 3.632 16 7.465c.007.904-.167 1.8-.513 2.637a6.808 6.808 0 01-1.501 2.236 6.883 6.883 0 01-2.258 1.487 6.936 6.936 0 01-2.661.508 7.216 7.216 0 01-5.055-2.04l1.132-1.12a5.62 5.62 0 003.923 1.575 5.32 5.32 0 002.05-.387 5.279 5.279 0 001.738-1.144 5.221 5.221 0 001.154-1.721 5.184 5.184 0 00.39-2.031c0-2.96-2.343-5.547-5.332-5.547a5.627 5.627 0 00-3.422 1.216A5.536 5.536 0 003.7 6.176l1.143-1.042 1.083 1.167z"></path></symbol><symbol id="upload" viewBox="0 0 24 24"><path d="M10.875 5.6v12.025h2.25V5.47l3.68 3.925 1.64-1.54L12 1.125 5.532 8.256l1.686 1.488 3.657-4.143zM2 21h20v2H2v-2z"></path></symbol><symbol id="user" viewBox="0 0 24 24"><path d="M12 15.001a7 7 0 100-14 7 7 0 000 14zM18 17H6c-1.616 0-3 1.382-3 3v3h18v-3c0-1.618-1.383-3-3-3z"></path></symbol><symbol id="vote" viewBox="0 0 24 24"><path d="M20.25 5.75l-7.875 7.5L9 9.875l-1.5 1.5 4.875 4.875 9.375-9-1.5-1.5z"></path><path clip-rule="evenodd" d="M2.375 2.375H16.5v2.25H4.625v14.75h14.75V14h2.25v7.625H2.375V2.375z"></path></symbol><symbol id="xing" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M17.598 0l-8.02 14.333L14.869 24h4.85l-5.238-9.667L22.499 0h-4.9zM2.838 4.748L5.59 9.563 1.5 16.819h4.884l4.091-7.271-2.729-4.8H2.84z"></path></symbol><symbol id="youtube-logo" viewBox="0 0 24 24"><g clip-path="url(#clip0)"><path d="M14.975 2.26v5.27c-.017.333.025.668.123.987a.74.74 0 00.782.494c.454 0 .906-.288 1.36-.825v.741h1.234V2.26h-1.235v5.105c-.288.37-.535.576-.782.576-.165 0-.247-.082-.288-.288V2.26h-1.194zm-2.8 6.793a1.628 1.628 0 001.4-.7 2.65 2.65 0 00.37-1.565V4.442a2.656 2.656 0 00-.37-1.565 1.68 1.68 0 00-1.4-.7 1.628 1.628 0 00-1.399.7 2.654 2.654 0 00-.37 1.565v2.346a2.654 2.654 0 00.37 1.564 1.68 1.68 0 001.4.7zM11.6 4.195c0-.618.206-.906.576-.906.371 0 .577.288.577.906v2.8c0 .617-.206.946-.577.946-.37 0-.576-.33-.576-.947v-2.8zM8.76 8.97V5.348l1.605-5.352H9.006L8.1 3.495l-.947-3.5h-1.4c.247.742.536 1.565.865 2.512.332.93.608 1.878.825 2.84V8.97h1.316zm12.513 2.1a2.284 2.284 0 00-1.358-.618c-1.647-.165-4.117-.288-7.41-.288a66.176 66.176 0 00-7.41.288 2.588 2.588 0 00-1.359.618 2.42 2.42 0 00-.782 1.317c-.247 1.029-.329 2.593-.329 4.693a25.32 25.32 0 00.33 4.693c.11.512.385.974.781 1.317.371.352.85.57 1.36.618 2.462.234 4.936.33 7.41.288a65.679 65.679 0 007.41-.288 2.086 2.086 0 001.358-.618 2.42 2.42 0 00.782-1.317c.247-1.03.33-2.594.33-4.693a25.313 25.313 0 00-.33-4.693 2.523 2.523 0 00-.783-1.317zm-13.05 2.676h-1.44v7.615H5.424v-7.616h-1.4V12.47h4.158v1.275h.041zm3.582 7.615h-1.192v-.74c-.494.534-.947.824-1.36.824a.74.74 0 01-.781-.494 2.872 2.872 0 01-.124-.988v-5.23h1.235v5.31c.041.207.123.289.288.289.247 0 .494-.206.782-.577v-5.022h1.193l-.041 6.628zm4.57-2.017c.024.443-.017.887-.124 1.317a.925.925 0 01-.947.741 1.686 1.686 0 01-1.235-.74v.659h-1.194v-8.85h1.194v2.923a1.559 1.559 0 011.235-.741.924.924 0 01.947.74c.104.432.146.875.123 1.318v2.633zm4.528-1.07h-2.388v1.151c0 .618.206.906.618.906.288 0 .453-.165.535-.494 0-.083.041-.37.041-.825h1.235v.164c.02.262.007.525-.041.783a1.85 1.85 0 01-.288.74 1.834 1.834 0 01-2.882 0 2.654 2.654 0 01-.37-1.564v-2.302a2.654 2.654 0 01.37-1.564 1.702 1.702 0 011.44-.7 1.628 1.628 0 011.4.7c.282.47.412 1.017.37 1.564l-.04 1.44z"></path><path d="M19.092 15.722c-.413 0-.618.287-.618.905v.618h1.194v-.618c.04-.577-.165-.905-.576-.905zm-4.446 0a.857.857 0 00-.618.287v4.035a.857.857 0 00.618.288c.329 0 .535-.288.535-.906v-2.84c0-.536-.165-.864-.535-.864z"></path></g></symbol><symbol id="youtube" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M9.522 15.135l-.001-6.79 6.483 3.407-6.483 3.383zm14.237-7.967s-.234-1.666-.955-2.399c-.912-.963-1.935-.968-2.404-1.024-3.359-.245-8.395-.245-8.395-.245h-.012s-5.036 0-8.395.245c-.47.056-1.491.06-2.404 1.024C.474 5.503.24 7.168.24 7.168S0 9.124 0 11.079v1.834c0 1.956.24 3.913.24 3.913s.234 1.665.954 2.4c.913.963 2.112.932 2.646 1.031 1.92.187 8.16.243 8.16.243s5.042-.008 8.401-.252c.47-.056 1.492-.06 2.404-1.023.721-.735.955-2.4.955-2.4s.24-1.956.24-3.913v-1.834c0-1.955-.24-3.911-.24-3.911h-.001z"></path></symbol></svg></div>`
)}

function _leuDropdown(leuVersion)
{
  import(
    `https://esm.sh/@statistikzh/leu@${leuVersion}/leu-dropdown.js`
  );
}


function _leuDialog(leuVersion){return(
import(
  `https://esm.sh/@statistikzh/leu@${leuVersion}/leu-dialog.js`
)
)}

function _leuButton(leuVersion){return(
import(
  `https://esm.sh/@statistikzh/leu@${leuVersion}/leu-button.js`
)
)}

function _leuRadio(importLeuFromCDN,leuVersion)
{
  importLeuFromCDN("leu-radio-group.js", leuVersion);
  importLeuFromCDN("leu-radio.js", leuVersion);
  importLeuFromCDN("leu-input.js", leuVersion);
}


export default function define(runtime, observer) {
  const main = runtime.module();
  main.define("module 1", async () => runtime.module((await import("/d/a33468b95d0b15b0@817.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.define("module 2", async () => runtime.module((await import("/d/f69f0d836059a035@761.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.define("module 3", async () => runtime.module((await import("/d/0d64f2229c613239@129.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.define("module 4", async () => runtime.module((await import("/@bildungsplanungzh/export-functions.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.define("module 5", async () => runtime.module((await import("/@bildungsplanungzh/lesebeispiel-plugin.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.define("module 6", async () => runtime.module((await import("/d/9ec53725f102b578@738.js?v=4&resolutions=2ebdda3eb4cd0353@1488")).default));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer()).define(["toc"], _2);
  main.variable(observer()).define(["md"], _3);
  main.variable(observer()).define(["md"], _4);
  main.variable(observer()).define(["md"], _5);
  main.variable(observer("Downmenu")).define("Downmenu", ["leuDropdown","leuButton","leuDialog","leuRadio","d3","hashCode","createPNG","createSVG","createEmbedCode","createXLSX","createCSV"], _Downmenu);
  main.variable(observer("addDropDownContent")).define("addDropDownContent", _addDropDownContent);
  main.variable(observer()).define(["md"], _8);
  main.variable(observer("downmenu")).define("downmenu", ["Downmenu"], _downmenu);
  main.variable(observer()).define(["md"], _10);
  main.variable(observer("showDropdown")).define("showDropdown", ["downmenu"], _showDropdown);
  main.variable(observer()).define(["md"], _12);
  main.variable(observer()).define(["md"], _13);
  main.variable(observer("addAllButtons")).define("addAllButtons", ["downmenu"], _addAllButtons);
  main.variable(observer("dropdownstyle")).define("dropdownstyle", ["html"], _dropdownstyle);
  main.variable(observer()).define(["md"], _16);
  main.variable(observer()).define(["md"], _17);
  main.variable(observer("MetaProcessor")).define("MetaProcessor", ["hashCode","d3","svgicons","dropdownstyle","leuStyleSheet","readingExample"], _MetaProcessor);
  main.variable(observer()).define(["md"], _19);
  main.variable(observer("hashCode")).define("hashCode", _hashCode);
  main.variable(observer()).define(["hashCode"], _21);
  main.variable(observer()).define(["md"], _23);
  main.variable(observer("basicapi")).define("basicapi", ["URLSearchParams","d3"], _basicapi);
  main.variable(observer()).define(["basicapi"], _25);
  main.variable(observer("swatches")).define("swatches", ["html"], _swatches);
  main.variable(observer("brightnessByColor")).define("brightnessByColor", _brightnessByColor);
  main.variable(observer("rotateX")).define("rotateX", ["getTransformation","d3","addStaticText","wrap"], _rotateX);
  main.variable(observer("linebreakY")).define("linebreakY", ["addStaticText","wrap","d3"], _linebreakY);
  main.variable(observer("getTransformation")).define("getTransformation", _getTransformation);
  main.variable(observer("addStaticText")).define("addStaticText", ["d3"], _addStaticText);
  main.variable(observer("wrap")).define("wrap", ["d3"], _wrap);
  main.variable(observer("mouseOut")).define("mouseOut", ["d3"], _mouseOut);
  main.variable(observer("disarray")).define("disarray", _disarray);
  main.variable(observer()).define(["md"], _35);
  main.variable(observer("germanFormater")).define("germanFormater", ["d3"], _germanFormater);
  main.variable(observer("formater")).define("formater", ["germanFormater","d3"], _formater);
  main.variable(observer()).define(["md"], _38);
  main.variable(observer()).define(["md"], _39);
  main.variable(observer("graphicsColors")).define("graphicsColors", _graphicsColors);
  main.variable(observer("graphiccolorsshow")).define("graphiccolorsshow", ["showColors","graphicsColors"], _graphiccolorsshow);
  main.variable(observer()).define(["md"], _42);
  main.variable(observer("additionalGraphicsColors")).define("additionalGraphicsColors", _additionalGraphicsColors);
  main.variable(observer("additionalgraphicscolorsshow")).define("additionalgraphicscolorsshow", ["showColors","additionalGraphicsColors"], _additionalgraphicscolorsshow);
  main.variable(observer()).define(["md"], _45);
  main.variable(observer("fixedCategorialColors")).define("fixedCategorialColors", ["graphicsColors"], _fixedCategorialColors);
  main.variable(observer("fixedCategorialColorsshow")).define("fixedCategorialColorsshow", ["showColors","fixedCategorialColors"], _fixedCategorialColorsshow);
  main.variable(observer()).define(["md"], _48);
  main.variable(observer("emergencyCategorialColors")).define("emergencyCategorialColors", ["graphicsColors"], _emergencyCategorialColors);
  main.variable(observer()).define(["showColors","emergencyCategorialColors"], _50);
  main.variable(observer()).define(["md"], _51);
  main.variable(observer("getColor")).define("getColor", ["d3","additionalGraphicsColors","graphicsColors","primaryColors","sonderschulColors","fixedCategorialColors","emergencyCategorialColors"], _getColor);
  main.variable(observer()).define(["getColor"], _53);
  main.variable(observer()).define(["getColor"], _54);
  main.variable(observer()).define(["getColor"], _55);
  main.variable(observer("getColorScale")).define("getColorScale", ["d3","getColor"], _getColorScale);
  main.variable(observer()).define(["md"], _57);
  main.variable(observer("Stufen")).define("Stufen", _Stufen);
  main.variable(observer()).define(["colorTable","Stufen","getColor"], _59);
  main.variable(observer()).define(["Stufen","getColor"], _60);
  main.variable(observer()).define(["md"], _61);
  main.variable(observer("sonderschulColors")).define("sonderschulColors", ["d3","graphicsColors"], _sonderschulColors);
  main.variable(observer()).define(["sonderschulColors"], _63);
  main.variable(observer("sonderschulTypen")).define("sonderschulTypen", _sonderschulTypen);
  main.variable(observer()).define(["colorTable","sonderschulTypen","sonderschulColors"], _65);
  main.variable(observer()).define(["md"], _66);
  main.variable(observer("primaryColors")).define("primaryColors", ["d3","graphicsColors"], _primaryColors);
  main.variable(observer()).define(["md"], _68);
  main.variable(observer()).define(["primaryColors"], _69);
  main.variable(observer("primaryStufen")).define("primaryStufen", _primaryStufen);
  main.variable(observer()).define(["colorTable","primaryStufen","primaryColors"], _71);
  main.variable(observer()).define(["primaryColors"], _72);
  main.variable(observer()).define(["md"], _73);
  main.variable(observer()).define(["primaryColors"], _74);
  main.variable(observer("primaryKlassen")).define("primaryKlassen", _primaryKlassen);
  main.variable(observer()).define(["colorTable","primaryKlassen","primaryColors"], _76);
  main.variable(observer()).define(["md"], _77);
  main.variable(observer()).define(["md"], _78);
  main.variable(observer("secondaryIColors")).define("secondaryIColors", ["d3","graphicsColors"], _secondaryIColors);
  main.variable(observer()).define(["secondaryIColors"], _80);
  main.variable(observer("secondaryIKlassen")).define("secondaryIKlassen", _secondaryIKlassen);
  main.variable(observer()).define(["colorTable","secondaryIKlassen","secondaryIColors"], _82);
  main.variable(observer()).define(["md"], _83);
  main.variable(observer("secondaryINiveauColors")).define("secondaryINiveauColors", ["d3","graphicsColors","additionalGraphicsColors"], _secondaryINiveauColors);
  main.variable(observer()).define(["secondaryINiveauColors"], _85);
  main.variable(observer("secondaryINiveau")).define("secondaryINiveau", _secondaryINiveau);
  main.variable(observer()).define(["colorTable","secondaryINiveau","secondaryINiveauColors"], _87);
  main.variable(observer()).define(["md"], _88);
  main.variable(observer()).define(["md"], _89);
  main.variable(observer("secondaryIIColors")).define("secondaryIIColors", ["d3","additionalGraphicsColors","graphicsColors"], _secondaryIIColors);
  main.variable(observer()).define(["secondaryIIColors"], _91);
  main.variable(observer("secondaryIIKlassen")).define("secondaryIIKlassen", _secondaryIIKlassen);
  main.variable(observer()).define(["colorTable","secondaryIIKlassen","secondaryIIColors"], _93);
  main.variable(observer()).define(["md"], _94);
  main.variable(observer("secondaryIIProfileColors")).define("secondaryIIProfileColors", ["d3","additionalGraphicsColors","graphicsColors"], _secondaryIIProfileColors);
  main.variable(observer()).define(["secondaryIIProfileColors"], _96);
  main.variable(observer("secondaryIIProfiles")).define("secondaryIIProfiles", _secondaryIIProfiles);
  main.variable(observer()).define(["colorTable","secondaryIIProfiles","secondaryIIProfileColors"], _98);
  main.variable(observer()).define(["md"], _99);
  main.variable(observer("schultypen")).define("schultypen", _schultypen);
  main.variable(observer("schultypenColors")).define("schultypenColors", ["graphicsColors","additionalGraphicsColors"], _schultypenColors);
  main.variable(observer()).define(["colorTable","schultypen","schultypenColors"], _102);
  main.variable(observer()).define(["md"], _103);
  main.variable(observer("gender")).define("gender", _gender);
  main.variable(observer("genderColors")).define("genderColors", ["graphicsColors"], _genderColors);
  main.variable(observer()).define(["colorTable","gender","genderColors"], _106);
  main.variable(observer()).define(["md"], _107);
  main.variable(observer("nationality")).define("nationality", _nationality);
  main.variable(observer("nationalityColors")).define("nationalityColors", ["graphicsColors"], _nationalityColors);
  main.variable(observer()).define(["colorTable","nationality","nationalityColors"], _110);
  main.variable(observer()).define(["md"], _111);
  main.variable(observer("ownership")).define("ownership", _ownership);
  main.variable(observer("ownershipColors")).define("ownershipColors", ["graphicsColors","additionalGraphicsColors"], _ownershipColors);
  main.variable(observer()).define(["colorTable","ownership","ownershipColors"], _114);
  main.variable(observer()).define(["md"], _115);
  main.variable(observer("partyColors")).define("partyColors", ["additionalGraphicsColors","graphicsColors"], _partyColors);
  main.variable(observer()).define(["colorTable","partyColors"], _117);
  main.variable(observer()).define(["md"], _118);
  main.variable(observer("categorialColors")).define("categorialColors", ["d3","graphicsColors","additionalGraphicsColors"], _categorialColors);
  main.variable(observer()).define(["categorialColors"], _120);
  main.variable(observer("showColors")).define("showColors", ["d3","width"], _showColors);
  main.variable(observer()).define(["showColors","categorialColors"], _122);
  main.variable(observer("monochromeBlueZH")).define("monochromeBlueZH", _monochromeBlueZH);
  main.variable(observer()).define(["showColors","monochromeBlueZH"], _124);
  main.variable(observer("monochromeBlueExtZH")).define("monochromeBlueExtZH", ["monochromeBlueZH"], _monochromeBlueExtZH);
  main.variable(observer("monochromeBlueExtZHshow")).define("monochromeBlueExtZHshow", ["showColors","monochromeBlueExtZH"], _monochromeBlueExtZHshow);
  main.variable(observer("monochromeMagentaZH")).define("monochromeMagentaZH", _monochromeMagentaZH);
  main.variable(observer()).define(["showColors","monochromeMagentaZH"], _128);
  main.variable(observer("monochromeMagentaExtZH")).define("monochromeMagentaExtZH", ["monochromeMagentaZH"], _monochromeMagentaExtZH);
  main.variable(observer("monochromeMagentaExtZHshow")).define("monochromeMagentaExtZHshow", ["showColors","monochromeMagentaExtZH"], _monochromeMagentaExtZHshow);
  main.variable(observer("monochromeGreenZH")).define("monochromeGreenZH", _monochromeGreenZH);
  main.variable(observer()).define(["showColors","monochromeGreenZH"], _132);
  main.variable(observer("monochromeGreenExtZH")).define("monochromeGreenExtZH", ["monochromeGreenZH"], _monochromeGreenExtZH);
  main.variable(observer("monochromeGreenExtZHshow")).define("monochromeGreenExtZHshow", ["showColors","monochromeGreenExtZH"], _monochromeGreenExtZHshow);
  main.variable(observer("monochromeOrangeZH")).define("monochromeOrangeZH", _monochromeOrangeZH);
  main.variable(observer()).define(["showColors","monochromeOrangeZH"], _136);
  main.variable(observer("monochromeOrangeExtZH")).define("monochromeOrangeExtZH", ["monochromeOrangeZH"], _monochromeOrangeExtZH);
  main.variable(observer()).define(["showColors","monochromeOrangeExtZH"], _138);
  main.variable(observer("monochromeVioletZH")).define("monochromeVioletZH", _monochromeVioletZH);
  main.variable(observer()).define(["showColors","monochromeVioletZH"], _140);
  main.variable(observer("monochromeVioletExtZH")).define("monochromeVioletExtZH", ["monochromeVioletZH"], _monochromeVioletExtZH);
  main.variable(observer()).define(["showColors","monochromeVioletExtZH"], _142);
  main.variable(observer("monochromeGoldZH")).define("monochromeGoldZH", _monochromeGoldZH);
  main.variable(observer()).define(["showColors","monochromeGoldZH"], _144);
  main.variable(observer("monochromeGoldExtZH")).define("monochromeGoldExtZH", ["monochromeGoldZH"], _monochromeGoldExtZH);
  main.variable(observer()).define(["showColors","monochromeGoldExtZH"], _146);
  main.variable(observer("divergingRedBlueZH")).define("divergingRedBlueZH", _divergingRedBlueZH);
  main.variable(observer()).define(["showColors","divergingRedBlueZH"], _148);
  main.variable(observer("show1")).define("show1", ["ramp","d3","divergingRedBlueZH"], _show1);
  main.variable(observer("divergingBlueRedZH")).define("divergingBlueRedZH", ["divergingRedBlueZH"], _divergingBlueRedZH);
  main.variable(observer()).define(["showColors","divergingBlueRedZH"], _151);
  main.variable(observer("divergingOrangeAquamarineZH")).define("divergingOrangeAquamarineZH", _divergingOrangeAquamarineZH);
  main.variable(observer()).define(["showColors","divergingOrangeAquamarineZH"], _153);
  main.variable(observer("show2")).define("show2", ["ramp","d3","divergingOrangeAquamarineZH"], _show2);
  main.variable(observer("divergingAquamarineOrangeZH")).define("divergingAquamarineOrangeZH", ["divergingOrangeAquamarineZH"], _divergingAquamarineOrangeZH);
  main.variable(observer()).define(["showColors","divergingAquamarineOrangeZH"], _156);
  main.variable(observer()).define(["md"], _157);
  main.variable(observer("basicColors")).define("basicColors", _basicColors);
  main.variable(observer()).define(["showColors","basicColors"], _159);
  main.variable(observer()).define(["d3","monochromeBlueZH"], _160);
  main.define("legend", ["module 1", "@variable"], (_, v) => v.import("legend", _));
  main.define("ramp", ["module 2", "@variable"], (_, v) => v.import("ramp", _));
  main.variable(observer()).define(["ramp","d3","monochromeBlueExtZH"], _163);
  main.define("toc", ["module 3", "@variable"], (_, v) => v.import("toc", _));
  main.define("createCSV", ["module 4", "@variable"], (_, v) => v.import("createCSV", _));
  main.define("createXLSX", ["module 4", "@variable"], (_, v) => v.import("createXLSX", _));
  main.define("createPNG", ["module 4", "@variable"], (_, v) => v.import("createPNG", _));
  main.define("createSVG", ["module 4", "@variable"], (_, v) => v.import("createSVG", _));
  main.define("createEmbedCode", ["module 4", "@variable"], (_, v) => v.import("createEmbedCode", _));
  main.variable(observer("$")).define("$", _$);
  main.variable(observer("colorTable")).define("colorTable", ["Inputs","showColors"], _colorTable);
  main.variable(observer("stylesheet")).define("stylesheet", ["html"], _stylesheet);
  main.variable(observer("leuVersion")).define("leuVersion", _leuVersion);
  main.variable(observer("leuStyleSheet")).define("leuStyleSheet", ["html","leuVersion"], _leuStyleSheet);
  main.variable(observer("manualstylesheet")).define("manualstylesheet", ["html"], _manualstylesheet);
  main.variable(observer()).define(["md"], _173);
  main.variable(observer()).define(["md"], _174);
  main.variable(observer()).define(["html"], _175);
  main.variable(observer("svgicons")).define("svgicons", ["htl"], _svgicons);
  main.define("readingExample", ["module 5", "@variable"], (_, v) => v.import("readingExample", _));
  main.define("fonts", ["module 6", "@variable"], (_, v) => v.import("fonts", _));
  main.define("importLeuFromCDN", ["module 6", "@variable"], (_, v) => v.import("importLeuFromCDN", _));
  main.variable(observer("leuDropdown")).define("leuDropdown", ["leuVersion"], _leuDropdown);
  main.variable(observer("leuDialog")).define("leuDialog", ["leuVersion"], _leuDialog);
  main.variable(observer("leuButton")).define("leuButton", ["leuVersion"], _leuButton);
  main.variable(observer("leuRadio")).define("leuRadio", ["importLeuFromCDN","leuVersion"], _leuRadio);
  return main;
}
