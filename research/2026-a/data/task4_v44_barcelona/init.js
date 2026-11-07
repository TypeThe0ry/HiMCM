const debug = false,
    axis = {
        "Sexe": "0",
        "Curs": "a",
        "Nivell Socioeconòmic": "b",
        "Districte": "c",
        "Lloc de Naixement": "d"
    },
    plot_total = 13,
    colors = [
        "#558b2f",  // green
        "#ff9c37",  // orange
        "#d13359",  // red
        "#4798d9",  // blue
        "#725ca0",  // lila
        "#d270a5",  // rosa
    ],
    colorsDones = [
        "#558b2f",  // green
        "#ffffff",  // white
        "#558b2f",  // green
        "#7cb342",
        "#aed581",
        "#c5e1a5",
        "#dcedc8",
        "#cccccc",
        "#5555ff",
    ],
    colorsHomes = [
        "#ff9c37",  // orange
        "#ffffff",  // white
        "#ff9c37",  // orange
        "#ffc68f",
        "#ffd5ab",
        "#fee3c6",
        "#fff1e4",
        "#cccccc",
        "#7777ff",
    ],    
    colorsTotal = [
        "#545454",  // grey
        "#ffffff",  // white
        "#545454",  // grey
        "#717171",
        "#8d8d8d",
        "#a9a9a9",
        "#c5c5c5",
    ],
    colorsDistrictesDones = [
        "#008000",
        "#666633",
        "#008080",
        "#669900",
        "#00cc99",
        "#33cc33",
        "#99ff33",
        "#4cffb7",
        "#99ff99",
        "#ccffcc",
    ],
    colorsDistrictesHomes = [
        "#663300",
        "#806000",
        "#990033",
        "#cc0000",
        "#ff3300",
        "#ff6600",
        "#ff9900",
        "#ffb794",
        "#ffcc99",
        "#ffffcc",
    ],
    colorsDistrictesTotal = [
        "#000000",
        "#1b1b1b",
        "#303030",
        "#474747",
        "#5e5e5e",
        "#777777",
        "#919191",
        "#ababab",
        "#c6c6c6",
        "#e2e2e2",
    ],
    colorsEvolution = [
        "#558b2f",  // green
        "#ff9c37",  // orange
        "#545454",  // grey
    ],
    colorsEdat = [
        "#d13359",  // red
        "#4798d9",  // blue
        "#00ff00",  // green
    ],
    colorsRenta = [
        "#d270a5",  // rosa
        "#725ca0",  // lila
    ],
    mapColorMin = "#CDE7EA",
    mapColorMax = colors[0],
    mapColors = ["#CDE7EA", "#93bfc4", "#4a8c93", "#0E636C"],
    years = [2025, 2021, 2016, 2012, 2008, 2004];

var datafolder = null,
    plot_counter = 0,
    any = years[years.length-1];

$(document).ready(function() {

    //if (window.innerWidth < 1140) {
    if (window.mobilecheck()) {
        $('#resolutionModal').css("width", window.innerWidth);
        $('#resolutionModal').css("height", window.innerHeight);
        $('#resolutionModal').modal("show");
    }

    // home slider
    $(".slider").sss({
        slideShow : true, // Set to false to prevent SSS from automatically animating.
        //startOn : 0, // Slide to display first. Uses array notation (0 = first slide).
        transition : 1000, // Length (in milliseconds) of the fade transition.
        speed : 8000, // Slideshow speed in milliseconds.
        //showNav : true // Set to false to hide navigation arrows.
    });
    $("#home.content").show();

    // slider height 100% of space left by header+menu+sliderstripes+footer
    var h = window.innerHeight - 123 - 47 - 108 - 130;
    //if (h < 420) h = 420;
    //$("#home.content").css("height", h+"px");
    $("#slideWrap .textonly").css("height", h+"px");

    //console.log(h);
    if (h>490) {
        $(".infografia").attr("src", "assets/eixos_tematics_bigscreen.png");
    }
    else if (h>340) {
        var top = (h-340)/2;
        $("#slideWrap .textonly").css("padding-top", top+"px");
    }
    else {
        $("#slideWrap .textonly").addClass("low");
        $("#about").addClass("low");
    }    

    var w = h*1.5;
    $("img.ssslide").css("width", w+"px");
    var left = (1110-w)/2;
    $("img.ssslide").css("left", left+"px");

    // select page to show
    if (getGetParameter("p")) {
        if (getGetParameter("p") === "about") {
            selectMenu($(".about .nav-link"));
        }
    }

    // load evolution menu  
    loadMenuEvolucio();

    // load selected year by GET variables
    if (getGetParameter("any") === "evolution") {
        isEvolution = true;
    }
    else if (Number.isInteger(parseInt(getGetParameter("any")))) {
        any = parseInt(getGetParameter("any"));
        if (!any || isNaN(any)) {
            any = years[years.length-1];
        }
    }
    // add title to export image
    let anyStr = any;

    loadMenu(any);
    showActiveYear(any);

    $(document).keyup(function(e) { 
        //Escape
        if (e.keyCode === 27) {
            closeSearchIfActive();
    
            // close embed textarea
            $("#btnEmbed").removeClass("active");
            $(".embed_iframe").empty();
        }
    });

    $(".seguir").click(function() {
        selectMenu($(".about .nav-link"));
    });

    $(".infografia").click(function() {
        // select first infoviz of most actual year
        loadDefaultVariable(any);
        loadInfoviz();
    });

    $("#home button").click(function() {
        $(".infografia").click();
    });

    $(".nav-link").click(function() {
        selectMenu($(this));
    });

    $("#btnEmbed").click(function() {
        if ($(".embed_iframe").children().length == 0) {
            $(this).addClass("active");

            let url = window.location.href.replace("index.html", "embed.html");

            $(".embed_iframe").empty();
            $(".embed_iframe").append("<textarea><iframe width='1220' height='700' src='"+url+"' frameborder='0' allowfullscreen></iframe></textarea>");
        }
        else {
            $(this).removeClass("active");
            $(".embed_iframe").empty();
        }
    });

    $("#btnExport").click(function() {

        var id = $(".plotDiv.active").attr("id");
        id = Number(id.substring(id.length-1));

        if ($('#btnGrafic').hasClass("active")) {

            // chart
            var element;
            if (isEvolution) {
                // !!! only first of 3 elements
                element = $(".plotDiv.active").find(".js-plotly-plot").first();

                element = "evolution_grafic .js-plotly-plot";
                /*if (element.hasClass("evolution_grafic")) {
                    element = "evolution_grafic .js-plotly-plot";
                }
                else if (element.hasClass("evolution_grafic_norm")) {
                    element = "evolution_grafic_norm .js-plotly-plot";
                }*/

                variableTitle = variableEvolucioTitle;
            }
            else {
                element = $(".plotDiv").find(".js-plotly-plot.active");

                if (element.hasClass("grafic")) {
                    element = "grafic";
                }
                else if (element.hasClass("grafic_norm")) {
                    element = "grafic_norm";
                }
            }

            if (debug) console.log(element, id);
            
            //var plotDivGrafic = document.getElementsByClassName(element)[id];

            let ele = $("."+element)[id];
            if (!ele.hasOwnProperty("layout")) 
                ele = $("#plotDiv"+id+" ."+element+".active .graficTotal")[0];
            
            ele.layout.title = {
                text: "ASPB - FRESC " + anyStr + " - " + variableTitle + " - " + $(".btn-cat.active").text(),
                font: {
                    size: 24,
                    color: "#000",
                },
            };
            ele.layout.margin.t = 100;

            Plotly.downloadImage(ele, {
                format: 'png',
                height: 500,
                width: 1110,
                filename: 'ASPB - FRESC ' + anyStr + ' - '+variableTitle + " - " + $(".btn-cat.active").text(),
            });
        }
        else if ($('#btnMap').hasClass("active")) {

            // maps
            var element = $(".plotDiv").find(".map_div.active");
            if (element.hasClass("map")) {
                element = "map";
            }
            else if (element.hasClass("map_norm")) {
                element = "map_norm";
            }

            var html = d3.select("#plotDiv"+id+" ."+element+" svg")
                .attr("xmlns", "http://www.w3.org/2000/svg")
                .node().parentNode.innerHTML;

            var imgsrc = 'data:image/svg+xml;base64,' + btoa(html);

            $("body canvas").remove();
            var canvas = d3.select('body').append('canvas').node();
            canvas.width = 1200;
            canvas.height = 500;
            $("body canvas").css("display", "none");

            var ctx = canvas.getContext("2d");
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            var image = new Image();
            image.onload = function () {
                ctx.drawImage(image, 0, 0);
                var canvasdata = canvas.toDataURL("image/svg");
                var link = document.createElement("a");
                link.download = 'ASPB - FRESC ' + anyStr + ' - ' + variableTitle + '.png';
                link.href = canvasdata;
                document.body.appendChild(link);
                link.click();
            };
            image.src = imgsrc;
        }
        else if ($('#btnData').hasClass("active")) {

            // datatables
        }
    });

    $("#btnTwitter").click(function() {

        var msg = "Enquesta de Factors de Risc en Estudiants de Secundària de @salutpublicabcn - ";
        msg += $(".suptitle").text();
        msg += ": "
        msg += window.location.href;
        msg += " #FRESC";

        var conf = "height=300,width=600,left=200,top=200,menubar=no,location=no,resizable=yes,scrollbars=no,status=no";
        window.open("https://twitter.com/intent/tweet?text=" + encodeURIComponent(msg), "FRESC Twitter", conf);
    });

    $('#btnFacebook').click(function(e) {
        e.preventDefault();
        window.open('https://www.facebook.com/sharer/sharer.php?u=http%3A%2F%2Fwww.aspb.cat', 'fbShareWindow', 'height=450, width=550, top=' + ($(window).height() / 2 - 275) + ', left=' + ($(window).width() / 2 - 225) + ', toolbar=0, location=0, menubar=0, directories=0, scrollbars=0');
        return false;
    });

    $(".covid").click(function() {
        apartat = 'COVID-19';
        subapartat = 'COVID-19';
        variable = 'diag_covid';
        variableTitle = "Haver estat diagnosticat/da de Covid-19";
        variableDesc = "";
        loadInfoviz();
    });
});