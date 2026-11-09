var deVorigeSpan = false;

$(document).ready(function(){setTimeout(function(){$('#legendatabel1 > tbody > tr:nth-child(14) > td:nth-child(3) > span').trigger('click');}, 1000);});

function doeLegendaItem(pSpan, pWaarde) {
	doeHerstel();
	var deLijnNummers;
	deFeatureGroups["1_laag_4"].eachLayer(function(pObject){deLijnNummers = pObject.label.toString().split(" - "); deLijnNummers[0].split(" | ").forEach(function(pLabel) {if ("0" + pLabel == pWaarde.toString()) {pObject.setStyle({color:"#FF0000"});}});});		
	deFeatureGroups["1_laag_6"].eachLayer(function(pObject){deLijnNummers = pObject.label.toString().split(" - "); deLijnNummers[0].split(" | ").forEach(function(pLabel) {if ("0" + pLabel == pWaarde.toString()) {pObject.setStyle({color:"#0051FF"});}});});
	deFeatureGroups["1_laag_3"].eachLayer(function(pObject){deLijnNummers = pObject.label.toString().split(" - "); deLijnNummers[0].split(" | ").forEach(function(pLabel) {if ("0" + pLabel == pWaarde.toString()) {pObject.setStyle({fillColor:"#FF0000"});}});});
	deFeatureGroups["1_laag_5"].eachLayer(function(pObject){deLijnNummers = pObject.label.toString().split(" - "); deLijnNummers[0].split(" | ").forEach(function(pLabel) {if ("0" + pLabel == pWaarde.toString()) {pObject.setStyle({fillColor:"#0051FF"});}});});
	if ($('#legendatabel1 > tbody > tr').index($(pSpan).parent().parent()) < 23) $(pSpan).css('color', '#FF0000');
	else $(pSpan).css('color', '#0051FF');
	$(pSpan).css('font', 'normal 16px/25px Maps_Bold, Arial');
	$(pSpan).addClass('actief');
	deVorigeSpan = pSpan;
}

function doeKlikObject(pLabel) {
	doeHerstel();
	var dePuntNummers = pLabel.toString().split(" - "), deLijnNummers;
	dePuntNummers[0].split(" | ").forEach(function(puntLabel) {
		deFeatureGroups["1_laag_4"].eachLayer(function(pObject){deLijnNummers = pObject.label.toString().split(" - "); deLijnNummers[0].split(" | ").forEach(function(lijnLabel) {if ("0"+puntLabel == "0"+lijnLabel) {pObject.setStyle({color:"#FF0000"});}});});	
		deFeatureGroups["1_laag_6"].eachLayer(function(pObject){deLijnNummers = pObject.label.toString().split(" - "); deLijnNummers[0].split(" | ").forEach(function(lijnLabel) {if ("0"+puntLabel == "0"+lijnLabel) {pObject.setStyle({color:"#0051FF"});}});});		
		deFeatureGroups["1_laag_3"].eachLayer(function(pObject){deLijnNummers = pObject.label.toString().split(" - "); deLijnNummers[0].split(" | ").forEach(function(lijnLabel) {if ("0"+puntLabel == "0"+lijnLabel) {pObject.setStyle({fillColor:"#FF0000"});}});});
		deFeatureGroups["1_laag_5"].eachLayer(function(pObject){deLijnNummers = pObject.label.toString().split(" - "); deLijnNummers[0].split(" | ").forEach(function(lijnLabel) {if ("0"+puntLabel == "0"+lijnLabel) {pObject.setStyle({fillColor:"#0051FF"});}});});			
	});
}

function doeHerstel() {
	if (deVorigeSpan) {$(deVorigeSpan).css('color', '#000000'); $(deVorigeSpan).css('font', 'normal 16px/25px Maps_Regular, Arial'); $(deVorigeSpan).removeClass('actief'); deVorigeSpan = false;};
	deFeatureGroups["1_laag_4"].eachLayer(function(pObject){pObject.setStyle({color:"#000000"});});		
	deFeatureGroups["1_laag_6"].eachLayer(function(pObject){pObject.setStyle({color:"#000000"});});	
	deFeatureGroups["1_laag_3"].eachLayer(function(pObject){pObject.setStyle({fillColor:"#000000"});});
	deFeatureGroups["1_laag_5"].eachLayer(function(pObject){pObject.setStyle({fillColor:"#000000"});});
}	
