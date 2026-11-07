function draw(chapter, title, desc, any, apartat, subapartat) {
    // ES5 for IE
    if (!desc) desc=null;

    $('#loading').addClass('spinner');
    $("#gui").hide();

    cleanGui();
    buildGui();

    if (desc && desc !== undefined && desc !== "") 
        desc = ' <i class="fas fa-info-circle" title="'+desc+'"></i>';
    else 
        desc = "";
    $("#infoviz .title").html(title+desc);
    $("#infoviz .suptitle").html(apartat+" / "+subapartat);

    // hide botó COVID per tot menys 2021
    console.log("any", any);
    if (any !== 2021)
        $("button.covid").hide();

    // Dades demogràfiques / La població
    if (apartat === "Dades demogràfiques" && subapartat === "La població") {
        /*if (title === "Gènere") {
            // Hide eix Sexe
            $("#btn0").hide();
        }
        else*/ if (title === "Edat" || title === "Distribució per curs") {
            // Hide eix Curs
            $("#btn1").hide();
        }
        else if (title === "Nivell socioeconòmic del barri del centre" || title === "Distribució socioeconómica del barri del centre") {
            // Hide eix Nivell Socioeconòmic
            $("#btn2").hide();
        }
        else if (title === "Districte del centre educatiu" || title === "Distribució del districte centre educatiu") {
            // Hide eix Districte
            $("#btn3").hide();
        }
        else if (title === "Distribució del país de naixement de l'alumne") {
            // Hide eix Lloc de naixement
            $("#btn4").hide();
        }
    }

    initPlot(chapter, "0", 0, 0, true);
    initPlot(chapter, "a", 1, 1, false, true);
    initPlot(chapter, "b", 2);
    initPlot(chapter, "c", 3);
    initPlot(chapter, "d", 4);
}

/****************
    load data
*****************/
function initPlot(chapter, sub, id, sexe, single) {
    // ES5 for IE
    if (!sexe) sexe=0;
    if (!single) single=false;

    Plotly.d3.tsv(datafolder+chapter+'_'+sub+'_'+sexe+'.csv', function(err, rowsIndef){
        
        if(err) { 
            if (debug) console.log("error", chapter, sub, sexe);
            plot_counter+=3;

            // file doesn't exist, try with man only
            Plotly.d3.tsv(datafolder+chapter+'_'+sub+'_1.csv', function(err, rowsIndef){

            if(err) { 
                if (debug) console.log("error", chapter, sub, sexe);
                if (sub == "a")
                    plot_counter++;
                else
                    plot_counter+=2;

                // file doesn't exist, try with woman only
                Plotly.d3.tsv(datafolder+chapter+'_'+sub+'_2.csv', function(err, rowsIndef){
                    if (err) {
                        if (debug) console.log("error", chapter, sub, sexe);
                        if (sub == "a")
                            plot_counter++;
                        else
                            plot_counter+=2;

                        isLoadingReady();
                    }
                    else {
                        initPlotHeaders(rowsIndef, chapter, sub, id, sexe, single);
                    }
                    //console.log(chapter,sub,id,plot_counter);
                });
            }
            else {
                initPlotHeaders(rowsIndef, chapter, sub, id, sexe, single);
            }
            });
        }
        else {
            initPlotHeaders(rowsIndef, chapter, sub, id, sexe, single);
        }
    });
}

function initPlotHeaders(rows, chapter, sub, id, sexe, single) {
    var headers = [];
    var tableTitle = "";

    // get column headers
    var i = 0;
    headers = ["N"];
    //console.log(rows, datafolder+chapter+'_'+sub+'_'+sexe+'_1.csv');
    for (title in rows[0]) {
        if (rows[0].hasOwnProperty(title)) {
            if (i>0) {
                headers.push(title);
            }
            else {
                tableTitle = title;
            }
            i++;
        }
    }
    headers.push("sort");
    //console.log("headers", headers, tableTitle);

    var tmpColors = colors;

    //console.log(headers);

    // check if only SI/NO
    let binary = false;
    if ((headers.length == 5 && 
        (((headers[1] == "Sí" || headers[1] == "Si") && headers[2] == "No") || 
        (headers[1] == "No" && (headers[2] == "Sí" || headers[2] == "Si")))) ||
        (headers.length == 6 && 
        (((headers[1] == "Sí" || headers[1] == "Si") && headers[2] == "No" && (headers[3] == "NS/NC" || headers[3] == "No ho sé")) || 
        (headers[1] == "No" && (headers[2] == "Sí" || headers[2] == "Si") && (headers[3] == "NS/NC" || headers[3] == "No ho sé"))))) {

        binary = true;
        tmpColors = [colors[0], "#FFFFFF"];
    }

    if (single) {
        drawPlotSingle(chapter, sub, id, sexe, headers, tableTitle, tmpColors, binary);
    } 
    else {
        drawPlot(chapter, sub, id, headers, tableTitle, tmpColors, binary);
    }
}

function drawPlotSingle(chapter, sub, id, sexe, headers, tableTitle, colors, binary) {
    // no estandarditzada
    //console.log("---"+datafolder+chapter+'_'+sub+'_'+sexe+'_1.csv');
    Plotly.d3.tsv(datafolder+chapter+'_'+sub+'_'+sexe+'.csv', function(err, rowsIndef){
        if(err) { 
            // file doesn't exist, don't make loading wait
            plot_counter++;
            //console.log(err, plot_counter); 
            isLoadingReady();
        }
        else {
            rowsIndef = calculateTotals(tableTitle, rowsIndef);

            rowsIndefClean = removeNsNcCol(rowsIndef);
            drawGraficSingle(title, rowsIndefClean, id, 'grafic', colors, binary, chapter+'_'+sub);

            if (sexe == 0) sexe = 'Total';
            else if (sexe == 1) sexe = 'Dones';
            else if (sexe == 2) sexe = 'Homes';
            drawDataTable(tableTitle, rowsIndef, sexe, id, headers);
            $('#plotDiv'+id+' .data').append('<div class="tablefooter">N: nombre de casos (poden excloure mostra per filtres, no resposta i/o no aplica)</div>');
        }
    });
}

function drawPlot(chapter, sub, id, headers, tableTitle, colors, binary) {

    // no estandarditzada
    var onlywoman = false;
    Plotly.d3.tsv(datafolder+chapter+'_'+sub+'_1.csv', function(err, rowsDones){
        if(err) { 
            // only woman?
            drawPlotSingle(chapter, sub, id, 2, headers, tableTitle, colors, binary);
            onlywoman = true;
        }
        else {
            Plotly.d3.tsv(datafolder+chapter+'_'+sub+'_2.csv', function(err, rowsHomes){
                if(err) { 
                    // file doesn't exist, don't make loading wait
                    plot_counter++;
                    //console.log(err, plot_counter); 
                    isLoadingReady();
                }
                else {
                    Plotly.d3.tsv(datafolder+chapter+'_'+sub+'_3.csv', function(err, rowsTotal){
                        if(err) { 
                            // file doesn't exist, don't make loading wait
                            plot_counter++;
                            //console.log(err, plot_counter); 
                            isLoadingReady();
                        }
                        else {
                            rowsDones = calculateTotals(tableTitle, rowsDones);
                            rowsHomes = calculateTotals(tableTitle, rowsHomes);
                            rowsTotal = calculateTotals(tableTitle, rowsTotal);

                            rowsDonesClean = removeNsNcCol(rowsDones);
                            rowsHomesClean = removeNsNcCol(rowsHomes);
                            rowsTotalClean = removeNsNcCol(rowsTotal);

                            if (id == 3 || id == 4)
                                drawGraficHorizontal(title, removeNC(rowsDonesClean).reverse(), removeNC(rowsHomesClean).reverse(), removeNC(rowsTotalClean).reverse(), id, 'grafic', colors, binary);
                            else
                                drawGrafic(title, rowsDonesClean, rowsHomesClean, rowsTotalClean, id, 'grafic', colors, binary);
                            
                            drawDataTable(tableTitle, rowsDones, "Dones", id, headers);
                            drawDataTable(tableTitle, rowsHomes, "Homes", id, headers);
                            drawDataTable(tableTitle, rowsTotal, "Total", id, headers);
                            $('#plotDiv'+id+' .data').append('<div class="tablefooter">N: nombre de casos (poden excloure mostra per filtres, no resposta i/o no aplica)</div>');

                            drawMaps(title, rowsDones, rowsHomes, rowsTotal, id);
                        }
                    });
                }
            });
        }
    });
}

function unpack(rows, key) {
    var unpack = rows.map(function(row) { return row[key]; });
    // remove last element in case last line is empty
    if (unpack[unpack.length-1] === undefined) 
        unpack = unpack.slice(0,unpack.length-1);
    return unpack;
}

function unpack2(rows, key) {
    return rows.map(function(row) { return row[key]+" "; });
}

function getKeys(rows) {
    return Object.keys(rows[0]);
}

function getValues(obj, keys) {
    let arr = [];
    keys.forEach(function(key) {
        arr.push(obj[key]);
    });
    return arr;
}

function normalize(array, arrayTotal) {
    // calculate percentage
    array.forEach(function(ele, i) {
        array[i] = (array[i]/arrayTotal[i]*100).toFixed(2);
    });
    return array;
}

function normalizeSingle(array, total) {
    // calculate percentage
    array.forEach(function(ele, i) {
        array[i] = (array[i]/total*100).toFixed(2);
    });
    return array;
}

function isLoadingReady() {
    //console.log(plot_counter, plot_total);
    if (plot_counter >= plot_total) {
        if (debug) console.log('done ALL plotting');
        $('#loading').removeClass('spinner');
        $('#gui').show();
    }
}

function calculateTotals(title, array) {
    let array_add = [];

    array.forEach(function(row, i) {
        // calculate Total instead of using it from CSV (as sometimes it doesn't sum 100%)
        let total = 0;
        for (let col in row) {
            if (col !== "Total" && col !== "N" && col !== title) total += Number(row[col]);
        }
        row["Total"] = total;
        
        array_add.push(row);
    });

    return array_add;
}

/* remove NS/NC columns from data */
function removeNsNcCol(array) {
    let array_return = [];

    array.forEach(function(row, i) {
        let row_clean = {};
        for (let col in row) {
            if (col !== "NS/NC" && col !== "No ho sé")
                row_clean[col] = row[col];
        }
        array_return.push(row_clean);
    });

    return array_return;
}

function removeNC(array) {
    var array_remove = [];

    array.forEach(function(row, i) {
        if (row["Lloc de Naixement de l'Alumnat"] !== "NS/NC")
            array_remove.push(row);
    });

    return array_remove;
}

window.mobilecheck = function() {
  var check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};