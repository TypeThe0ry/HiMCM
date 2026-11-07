// load default visualization and select menus
// ?any=2021&apartat=H%C3%A0bits&subapartat=Alimentacio%20saludable&variable=AM80_2R
var any = 2025,
	isEvolution = false,
	apartat = null,
	subapartat = null,
	variable = null,
	variableTitle = null,
	variableDesc = null,
	apartats = null,
	searchJson = {},
	searchArray = [];

function loadMenu(year, callback=null) {

	datafolder = "fresc"+year+"/";

	$('.eixos').empty();

	// load menu structure
	$.when(
		$.getJSON("data/fresc"+year+".json", function( menujson ) {
			apartats = menujson;
		})
    ).then(function() { 
        //console.log("guio.json loaded!", apartats);

		// check if get variables to select menu
		if (getGetParameter("apartat") && getGetParameter("subapartat") && (getGetParameter("variable") || getGetParameter("variableTitle"))) {
			apartat = getGetParameter("apartat");
			subapartat = getGetParameter("subapartat");

			if (getGetParameter("variable")) {
				variable = getGetParameter("variable");
			}
			else {
				// chance year -> get variable
				variableTitle = getGetParameter("variableTitle");
				variable = getVariable(apartat, subapartat, variableTitle);
				if (variable === undefined || variable === "undefined") {
					//console.log(variable, any);
					loadDefaultVariable(any);
				}
			}

			loadInfoviz();
		}

		apartats.forEach(function(apartat, i) {
			//console.log(apartat.title);
			//$("#menu_apartats").append("<option value='"+apartat.title.trim()+"' data-i='"+i+"'>"+apartat.title.trim()+"</option>");

			var label = apartat.title.trim();
			var html = '<li><a class="dropdown-item dropdown-toggle" href="#">'+label+' <i class="fas fa-angle-right"></i></a>';
			html += '<ul class="dropdown-menu apartat apartat'+i+'"></ul>';
			html += '</li>';
			$('.eixos').append(html);

			loadSubapartats(label, i);
		});

		//console.log(searchArray, searchJson);

		if (callback) callback();

		//$("#menu .navbar-nav").append('<li class="nav-item search"><a class="nav-link"><span>Cercar</span> <i class="fas fa-search"></i></a></li>');
		$("#menu .navbar-nav .search").show();

		$(".nav-item.search").click(function() {

			if ($(this).find("#search").length == 0) {
				$(this).find("span").empty();
	            var html ='<input type="text" id="search" name="search" />';
	            $(this).find("span").append(html);

	            $("#search").focus();

				// search autocomplete
		        $("#search").autocomplete({
		        	minLength: 3,
		            source: function( request, response ) {
		                response( $.ui.autocomplete.filter(
		                    searchArray, extractLast( request.term ) ) );
		            },
		            focus: function(event, ui) {
		                $(this).val(ui.item.label);
		                return false;
		            },
		            select: function(event, ui) {
		            	var obj = searchJson[ui.item.label];
		                var value = obj.code;
		                var desc = obj.desc;

		                apartat = obj.apartat;
		                subapartat = obj.subapartat;
		                variable = value;
		                //var title = ui.item.label.split("-");
		                //variableTitle = title[title.length-1].trim();
		                variableTitle = ui.item.label;
		                varialbeDesc = desc;
		                
		                loadInfoviz();

		                //$("#search").val("");
		                $(".nav-item.search").find("span").empty();
		                $(".nav-item.search").find("span").append("Cercar");

		                return false;      
		            }
		        });
			}
		});

		$(".variable").click(function() {

			any = parseInt($(this).data("any"));
			apartat = $(this).data("apartat");
			subapartat = $(this).data("subapartat");
			variable = $(this).data("value");
			variableTitle = $(this).text();
			variableDesc = $(this).data("desc");

			loadInfoviz();

			// hide menu on click (turn off hover)
			$(".dropdown-li").hide();
			window.setTimeout(function(){ $(".dropdown-li").show(); }, 100);
			
            return false;
		});
	});
}

function loadInfoviz() {
	// ES5 for IE
	if (!variableTitle) variableTitle=null;
	if (!variableDesc) variableDesc=null;

	// get variable title and description if not passed
	if (!variableTitle || !variableDesc) {
		for (idApartat in apartats) {

			if (apartats[idApartat].title === apartat) {
				thisApartat = apartats[idApartat];

				for (idSubapartat in thisApartat.subapartats) {
					if (thisApartat.subapartats[idSubapartat].title === subapartat) {
						thisSubapartat = thisApartat.subapartats[idSubapartat];

						for (idVariable in thisSubapartat.variables) {
							if (thisSubapartat.variables[idVariable].code === variable) {
								thisVariable = thisSubapartat.variables[idVariable];

								//console.log(thisVariable);

								variableTitle = thisVariable.title;
								variableDesc = thisVariable.text;
								break;
							}
						}
						break;
					}
				}
				break;
			}
		}
	}

	console.log("loadInfoviz", any, apartat, subapartat, variable, variableTitle);

    /*$(".btco-hover-menu .collapse ul ul ul li:hover ul").css("display", "none");
	setTimeout(function() {
        $(".btco-hover-menu .collapse ul ul ul li:hover ul").css("display", "block");
    }, 1000);*/

    // select plot div
    $("#plotDiv").show();
    $("#plotDiv0").addClass("active");
    $("#plotDiv0 .grafic").addClass("active");

    // load infoviz
    draw(variable, variableTitle, variableDesc, any, apartat, subapartat);

    // show infoviz content area
    if (!$("#infoviz").hasClass("active")) {
        $(".nav-link").removeClass("active");
        $(this).addClass("active");
        $(".content").hide();
        $("#infoviz").show();
    }

    selectMenu($(".nav-link[data-id='infoviz']"));

    // change URL
    changeUrlParameters(any, apartat, subapartat, variable);

    // hide all buttons but SEXE for Genere
    if (variable == "genere") {
        $("#btn1").hide();
        $("#btn2").hide();
        $("#btn3").hide();
        $("#btn4").hide();
    }
}

function getVariable(apartat, subapartat, variableTitle) {

	//console.log(any, apartats);

	for (idApartat in apartats) {

		if (apartats[idApartat].title === apartat) {
			thisApartat = apartats[idApartat];

			for (idSubapartat in thisApartat.subapartats) {
				if (thisApartat.subapartats[idSubapartat].title === subapartat) {
					thisSubapartat = thisApartat.subapartats[idSubapartat];

					for (idVariable in thisSubapartat.variables) {
						if (thisSubapartat.variables[idVariable].title === variableTitle) {
							thisVariable = thisSubapartat.variables[idVariable];

							//console.log(thisVariable);
							variable = thisVariable.code;
							variableTitle = thisVariable.title;
							variableDesc = thisVariable.text;

							return variable;

							break;
						}
					}
					break;
				}
			}
			break;
		}
	}
}

function closeSearchIfActive() {
	if ($(".nav-item.search").find("#search").length !== 0) {
		// search active
		$(".nav-item.search").find("span").empty();
        $(".nav-item.search").find("span").append("Cercar");
	}
}

function loadSubapartats(apartat, pos) {

	var subapartats = apartats[pos].subapartats;
	subapartats.forEach(function(subapartat, i) {
		//$("#menu_subapartats").append("<option class='sub' value='"+subapartat.title.trim()+"' data-i='"+i+"' data-apartat='"+apartat.trim()+"' data-apartat-i='"+pos+"'>"+subapartat.title.trim()+"</option>");
		var label = subapartat.title.trim();
		var html = '<li><a class="dropdown-item dropdown-toggle" href="#">'+label+' <i class="fas fa-angle-right"></i></a>';
		html += '<ul class="dropdown-menu subapartat subapartat'+i+'"></ul>';
		html += '</li>';
		$('.apartat'+pos).append(html);

		loadVariables(apartat, pos, label, i);
	});
}

function loadVariables(apartat,pos,subapartat,pos2) {
	$("#gui").hide();

	var variables = apartats[pos].subapartats[pos2].variables;
	variables.forEach(function(variable) {

		//$("#menu_variables").append("<option class='sub' value='"+variable.code.trim()+"' data-desc='"+variable.text+"'>"+variable.title.trim()+"</option>");
		var label = variable.title.trim();
		var code = variable.code.trim();
		var desc = variable.text.trim();
		var html = '<li><a class="dropdown-item dropdown-toggle variable" href="#" data-value="'+code+'" data-desc="'+desc+'" data-any="'+any+'" data-apartat="'+apartat+'" data-subapartat="'+subapartat+'">'+label+'</a></li>';
		$('.apartat'+pos+' .subapartat'+pos2).append(html);

		// fill search array
		var text = apartat+" - "+subapartat+" - "+label;
		searchArray.push(text);
		var obj = {
			code: code,
			label: label,
			desc: desc,
			apartat: apartat,
			subapartat: subapartat
		};
		searchJson[text] = obj;
	});
}

function getGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
    .substr(1)
        .split("&")
        .forEach(function (item) {
        tmp = item.split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    });
    return result;
}

function extractLast( term ) {
    return split( term ).pop();
}

function split( val ) {
    return val.split( /,\s*/ );
}

function changeUrlParameters(any, apartat, subapartat, variable) {
	var url = window.location.origin+window.location.pathname;
    url += "?any="+any
        +"&apartat="+apartat
        +"&subapartat="+subapartat
        +"&variable="+variable;
	window.history.pushState({}, "FRESC", url);
}

function removeUrlParameters() {
	window.history.pushState({}, "FRESC", window.location.origin+window.location.pathname);
}