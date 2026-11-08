var blankHref = false;
var ajaxurl = '/wp-admin/admin-ajax.php';

function normalizeTableFilterValue(value) {
	var normalized = value.toLocaleLowerCase('cs-CZ');

	if (typeof normalized.normalize === 'function') {
		normalized = normalized.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
	}

	return normalized.trim();
}

function findNextFilterTable(filter, assignedTables) {
	var scope = filter.closest('.wysiwyg') || filter.parentElement;
	var tables = scope ? scope.querySelectorAll('table') : [];

	for (var i = 0; i < tables.length; i += 1) {
		var isAfterFilter = filter.compareDocumentPosition(tables[i]) & Node.DOCUMENT_POSITION_FOLLOWING;

		if (isAfterFilter && assignedTables.indexOf(tables[i]) === -1) {
			return tables[i];
		}
	}

	return null;
}

function getFilterableTableRows(table) {
	var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));

	if (!table.tHead && rows.length) {
		rows.shift();
	}

	return rows;
}

function initTableFilters() {
	var filters = document.querySelectorAll('[data-table-filter]');
	var assignedTables = [];

	Array.prototype.forEach.call(filters, function (filter) {
		var input = filter.querySelector('.table-filter__input');
		var status = filter.querySelector('.table-filter__status');
		var table = findNextFilterTable(filter, assignedTables);

		if (!input || !table) {
			return;
		}

		assignedTables.push(table);
		if (!table.id) {
			table.id = 'table-filter-target-' + assignedTables.length;
		}
		input.setAttribute('aria-controls', table.id);

		input.addEventListener('input', function () {
			var query = normalizeTableFilterValue(input.value);
			var rows = getFilterableTableRows(table);
			var visibleRows = 0;

			rows.forEach(function (row) {
				var firstCell = row.cells[0];
				var matches = firstCell && normalizeTableFilterValue(firstCell.textContent).indexOf(query) !== -1;

				row.hidden = !matches;
				if (matches) {
					visibleRows += 1;
				}
			});

			status.hidden = !query || visibleRows > 0;
			status.textContent = status.hidden ? '' : filter.getAttribute('data-no-results');
		});
	});
}

// locking of body
var $docEl = jQuery('html, body'),
$wrap = jQuery('.content'),
scrollTop;
function lockBody() {
	if (window.pageYOffset) {
		scrollTop = window.pageYOffset;
		$wrap.css({
			top: -(scrollTop) + jQuery("header").outerHeight(true)
		});
	}
	$docEl.css({
		height: "100%",
		overflow: "hidden"
	});
}

function unlockBody() {
	$docEl.css({
		height: "",
		overflow: ""
	});
	$wrap.css({
		top: ''
	});
	window.scrollTo(0, scrollTop);
	window.setTimeout(function () {
		scrollTop = null;
	}, 0);
}

function getUrlVars() {
	var vars = [], hash;
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	for(var i = 0; i < hashes.length; i++)
	{
		hash = hashes[i].split('=');
		vars.push(hash[0]);
		vars[hash[0]] = hash[1];
	}
	return vars;
}

jQuery(document).ready(function ($) {
	initTableFilters();

	/*fake-select-function*/
	$('.fake-select').each(function () {
		var select = $(this);
		select.find('.input-expand,.value-text').on('click',function () {
            select.toggleClass('active');
        })
		select.find('.value-text').html('').append(select.find('select option[selected="selected"]').html());
		select.find('option:not(:disabled)').each(function () {
			select.find('.options-wrapper').append('<span value="'+$(this).attr('value')+'" class="select-option">'+$(this).html()+'</span>');
        })
		select.find('.select-option').each(function () {
			$(this).on('click',function () {
				select.find('select').val($(this).attr('value'))
                select.find('.value-text').html('').append($(this).html());
                select.removeClass('active');

            })
        })
	});

	$('body').removeAttr('style');

	$('input[type="radio"], input[type="checkbox"]').change(function(){
		var state = $(this).prop('checked');
		if ($(this).parent().parent().attr('role') === 'radiogroup') {
			$(this).parent().parent().find('input').each(function(){
				$(this).parent('label').attr('aria-checked', 'false');
			});
		}
		if (state === true) {
			$(this).parent('label').attr('aria-checked', 'true');
		} else {
			$(this).parent('label').attr('aria-checked', 'false');
		}
	});

	$('.view-fake_select').each(function () {
		var select = $(this);
		select.find('.input-expand,.value-text').on('click',function () {
            select.toggleClass('view_focus');
			select.find('input').trigger('click');
			select.find('input').trigger('focus');
        })

    })
	/*fake-select-function*/

	if ($('#vymi_autoupdate').length) {
		setInterval(function() {
			$.ajax({
				type: "post",
				dataType: "json",
				url: ajaxurl,
				data: {
					action: "vymiUpdateHP",
					ajax: true
				},
				success: function(response) {
					$('#vymi_autoupdate').html(response.html);
				}
			});
		}, 60000);
	}

	if ($('#vymi_tab_1').length) {
		setInterval(function() {
			$.ajax({
				type: "post",
				dataType: "json",
				url: ajaxurl,
				data: {
					action: "vymiUpdatePage",
          			line: $(".block-main").data('line'),
          			stop: $(".block-main").data('stop'),
					typdopravy: $(".block-main").data('typdopravy'),
					ajax: true
				},
				success: function(response) {
					$('#vymi_tab_1').html(response.tab_1);
					$('#vymi_tab_1_arch').html(response.tab_1_arch);
					$('#vymi_tab_2').html(response.tab_2);
					$('#vymi_tab_2_arch').html(response.tab_2_arch);
					$('#vymi_tab_3').html(response.tab_3);
					$('#vymi_tab_3_arch').html(response.tab_3_arch);
					$('#vymi_tab_4').html(response.tab_4);
				}
			});
		}, 60000);
	}

	$(document).on('click', '[data-remove-stop]', function() {
		$(this).hide();
		$(this).next().show();
		$.ajax({
			type: "post",
			dataType: "json",
			url: ajaxurl,
			data: {
				action: "removeOrderLine",
				order_id: $(this).attr('data-remove-stop'),
				ajax: true
			},
			success: function(response) {
				if(response.success) {
				} else {
					$(this).hide();
					$(this).prev().show();
					alert(response.message);
				}
			}
		});
	});

	$(document).on('click', '[data-add-stop]', function() {
		$(this).hide();
		$(this).prev().show();
		var self = $(this);
		var line = $(this).data('line');
		var node = $(this).data('node');
		var stop = $(this).data('add-stop');
		var char = $(this).data('char');
		var sls = $(this).data('sls');
		var szjr = $(this).data('szjr');
		$.ajax({
			type: "post",
			dataType: "json",
			url: ajaxurl,
			data: {
				action: "orderLine",
				line: line,
				node: node,
				stop: stop,
				char: char,
				sls: sls,
				szjr: szjr,
				ajax: true
			},
			success: function(response) {
				if(response.success) {
          self.prev().attr('data-remove-stop', response.insert_id);
				} else {
					self.show();
					self.prev().hide();
					alert(response.message);
				}
			}
		});
	})

	$(document).on('click', '[data-popup]', function(){
		var w = 700;
		var h = 700;
		var left = (window.screen.width-(w+60))/2;
		var top = (window.screen.height-(h+80))/2;
		var strWindowFeatures = "height=" + h + ",width=" + w + ",left=" + left + ",top=" + top + ",location=no,menubar=no,status=no,toolbar=no,scrollbars=yes,resizable=yes,dialog=yes";
		var oWin = window.open("http://pid.bypixelfield.com/detail-spojeni/?route=9999", "route", strWindowFeatures);
		oWin.focus();
	});

	$(document).on('click', '.add-new-line-button', function() {
		var option = $(this).prev().find('option:selected');
		if (option) {
			window.location.href = window.location.origin + window.location.pathname + '?' + [
				['line', option.data('line')].join('='),
				['node', option.data('node')].join('='),
				['char', option.data('char')].join('='),
        ['stop', option.text()].join('='),
			].join('&');
		}
	});

	$(document).on('click', '.add-new-line-toggle', function() {
		$(this).parent().parent().find('.add-new-line').toggle();
	});
	$(document).on('click', '.changeview', function() {
		var type = $(this).attr('data-type');
		$('.changeview').removeClass('view-active');
		$('.changeview[data-type="'+type+'"]').addClass('view-active');
		if (type == "after") {
			$('.boxes').addClass('restview');
		} else {
			$('.boxes').removeClass('restview');
		}
	});

	$('tr[data-src] td').click(function() {
		var src = $(this).parent().data('src');
		if (src) {
			window.open(src, '_blank');
		}
	});

	$(".with-note[title]").click(function() {
		var half = $(window).width() / 2 - 10;
		$(".absolute-tooltip").remove();
		$("body").append('<span class="absolute-tooltip">' + $(this).attr("title") + '</span>');
		$(".absolute-tooltip").css('left', Math.min($(this).offset().left, half) + 'px').css('top', $(this).offset().top + 20 + 'px');
	});

	$(document).on("click", ".absolute-tooltip", function(){
		$(this).remove();
	});

	// wrap tables for mobile scrolling
	function wrapTables() {
		if ($("table").length) {
			$("*:not(.scroll-inside) > table").each(function () {
				$(this).wrap("<div class='scroll-inside'></div>");
			});
		}
	}
	wrapTables();

	$("[data-expand]").click(function(){
		var open = $(this).data("expand");
		$("[data-expandable='" + open + "']").slideToggle(250);
		if ($(this).hasClass('view-slider')) {
			$('.slider_new-search').toggleClass('view-opened');
		}
	});

	var rangeSlider = document.getElementById('range-slider');

	if (rangeSlider) {
		var dt = new Date();
		var secs = dt.getSeconds() + (60 * (dt.getMinutes() + (60 * dt.getHours())));
		noUiSlider.create(rangeSlider, {
			start: [ secs / 60 ],
			tooltips: [
				wNumb({
					decimals: 2,
					mark: ':',
					encoder: function(a) {
						var hours = Math.floor(a / 60),
							minutes = a - (hours * 60);
						minutes = minutes / 100;
						return hours + minutes;
					},
				})
			],
			range: {
				'min': [  0 ],
				'max': [ 1439 ]
			}
		});
	}

	var prevArrow = '<button class="slick-arrow slick-prev"><svg xmlns="http://www.w3.org/2000/svg"><use xlink:href="/wp-content/themes/pid/images/icons.svg#arrow-left"/></svg></button>',
		nextArrow = '<button class="slick-arrow slick-next"><svg xmlns="http://www.w3.org/2000/svg"><use xlink:href="/wp-content/themes/pid/images/icons.svg#arrow-right"/></svg></button>'

	$(".slider-imgs").slick({
		arrows: false,
		asNavFor: '.slider-cnt'
	});

	$(".slider-cnt").slick({
		prevArrow: prevArrow,
		nextArrow: nextArrow,
		appendArrows: $('.slider-cnt-arrows'),
		slide: ".slider-cnt-slide",
		dots: true,
		appendDots: $('.slider-cnt-dots'),
		asNavFor: '.slider-imgs'
	});

	$('.slider_new-imgs').on('init', function(event, slick){
		let calc2 = 1 / slick.slideCount * 100;
		$('.slider_new-cnt-progress').find('div').css('transition-duration', '5s').css('width', calc2+'%');
	});

	$(".slider_new-imgs").slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		appendArrows: $('.slider_new-arrows'),
		autoplay: true,
		draggable: false,
		swipe: false,
		pauseOnHover: false,
		pauseOnFocus: false,
		adaptiveHeight: true,
		autoplaySpeed: 5000,
	});

	$('.slider_new-imgs').on('beforeChange', function(event, slick, currentSlide, nextSlide){
		$('.slider_new-cnt-slide').removeClass('view-active');
		$('.slider_new-cnt-slide[data-id='+nextSlide+']').addClass('view-active');
		progressBar(nextSlide, slick.slideCount);
	});

	$('.slider_new-cnt-slide').click(function() {
		let _this = $(this);
		setTimeout(function() {
			let _count = $('.slider_new-cnt-slide').length;
			let index = parseInt(_this.attr('data-id'));
			if (!_this.hasClass('view-active')) {
				$('.slider_new-cnt-slide').removeClass('view-active');
				_this.addClass('view-active');
				$('.slider_new-imgs').slick('slickGoTo',index);
			}
		},0);
	});

	function progressBar(nextSlide, count){
		if (nextSlide == 0) {
			$('.slider_new-cnt-progress').find('div').removeAttr('style');
		}
		let calc2 = (nextSlide + 1) / count * 100;
		let calc1 = (nextSlide) / count * 100;
		$('.slider_new-cnt-progress').find('div').removeAttr('style');
		$('.slider_new-cnt-progress').find('div').addClass('notransition');
		$('.slider_new-cnt-progress').find('div').css('width', calc1+'%');
		setTimeout(function(){
			$('.slider_new-cnt-progress').find('div').removeClass('notransition');
		}, 100);
		setTimeout(function(){
			$('.slider_new-cnt-progress').find('div').css('transition-duration', '5s').css('width', calc2+'%');
		}, 300);
	}

	$(".block-main-slider").slick({
		prevArrow: prevArrow,
		nextArrow: nextArrow,
		appendArrows: $('.block-main-slider-arrows'),
		slide: '.block-main-slide',
	});

	$(".articles.view-slider").slick({
		slidesToShow: 3,
		slidesToScroll: 3,
		prevArrow: prevArrow,
		nextArrow: nextArrow,
		responsive: [
			{
				breakpoint: 720,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2,
				}
			},
			{
				breakpoint: 640,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1,
				}
			},
		]
	});

	$(".page-template-tpl-jr-stops-tablo #from").change(function() {
		$("#stanoviste option:contains('vše')").prop("selected", true);
	});

	$("body").on('change', "input[name='stanoviste']", function() {
		$("#open-tablo").submit();
	})

	$("#download-order,#download-type").change(function() {
		$("#download-form").submit();
	});

	$(".full_nav-group .title").click(function(){
		if ($(window).width() < 640) {
			$('.header-logo .menu_button').toggleClass('view-back');
			$(this).parent().toggleClass("view-active");
			$('.full_nav-cnt').scrollTop(0)
		}
	});

	$('.full_nav-group:not(.view-lines):not(.view-small_only) ul').height($('.full_nav-groups').height());


	$("[data-back]").click(function(){
		$(this).parent().parent().parent().toggleClass("view-active");
	});

	// smooth scroll
	$("body").on('click', 'a[href*="#"]', function (e) {
		var target = this.hash,
			$target = $(target);
		if ($target.length) {
			e.preventDefault();
			// unlockBody();
			$docEl.css({
				height: "",
				overflow: ""
			});
			$wrap.css({
				top: ''
			});

			var scrollHeight = $target.offset().top - $(".header").outerHeight() - 10;
			if ($(window).width() < 1300) {
				scrollHeight = $target.offset().top - $(".header").outerHeight() - 130;
			}
			$("body").removeClass("has-nav-open");
			$('html, body').stop().animate({
				'scrollTop': scrollHeight
			}, 500, 'swing', function () {
				if(history.pushState) {
					history.pushState(null, null, target);
				}
				else {
					location.hash = target;
				}
			});
		}
    });

	if (location.hash) {
		setTimeout(function() {
			window.scrollTo(0, 0);

			var target = window.location.hash,
				$target = $(target);
			var scrollHeight = $target.offset().top - $(".header").outerHeight() - 10;
			if ($(window).width() < 1300) {
				scrollHeight = $target.offset().top - $(".header").outerHeight() - 130;
			}
			if (target.length) {
				$('html, body').stop().animate({
					'scrollTop': scrollHeight
				}, 500, 'swing', function () {
					//window.location.hash = target;
					if(history.pushState) {
						history.pushState(null, null, target);
					}
					else {
						location.hash = target;
					}
				});
			}
		}, 1);
	}

	$('.box-subject, .box-cnt.is-flex').click(function () {
		$(this).parent().find('.box-cnt-column-full').toggleClass('is-open');
	});

	if($('.sidebar-menu .current-menu-item').length > 1) {
		//$('.sidebar-menu .current-menu-item').removeClass('current-menu-item');
		var target = window.location.hash,
				$target = $(target);
		$('.sidebar-menu li a').each(function (){
			var href = $(this).attr('href');
			if(href.indexOf(target)>0) {
				$(this).parent().addClass('current-menu-item');
			}
		});
	}
	$('.sidebar-menu li a').click(function (){
		$('.sidebar-menu .current-menu-item').removeClass('current-menu-item');
		$(this).parent().addClass('current-menu-item');
	})

	function setSearchPlaceholder() {
		if ($(window).width() >= 640) {
			$('.search_form.view-desktop .search_form-input').attr("placeholder", $('#form-placeholders .view-desktop').text());
		} else {
			$('.search_form.view-desktop .search_form-input').attr("placeholder", $('#form-placeholders .view-mobile').text());
		}
	}

	function setSidebarHeight() {
		var viewHeight = $(window).height() - $(".header").outerHeight(true),
			headerHeight = $(".header").outerHeight(true),
			sidebarCntHeight = $(".sidebar-fixed").outerHeight(true),
			sidebarCntHeightPlain = $(".sidebar-fixed").height(),
			sidebarPadding = (sidebarCntHeight - sidebarCntHeightPlain) / 2,
			windowScrolledAtBottom = $(window).scrollTop() + $(window).height(),
			footerOffsetTop = $(".footer").offset().top,
			footerHeight = $(".footer").outerHeight(true);
		$(".sidebar-fixed").width($(".sidebar").width() - 60);

		var offsetBottom = 25;
		if ($(window).width() < 1300) {
			offsetBottom = 160;
		}
		if($(this).scrollTop() > sidebarPadding - offsetBottom) {
			if(sidebarCntHeightPlain < viewHeight - offsetBottom - footerHeight) {
				$(".sidebar-fixed").css("position", "fixed");
				if (windowScrolledAtBottom > footerOffsetTop + offsetBottom) {
					$(".sidebar-fixed").css('top', -sidebarPadding - (windowScrolledAtBottom - footerOffsetTop - offsetBottom) + headerHeight + offsetBottom + 'px');
					$(".sidebar-fixed").css('bottom', 'auto');
				} else {
					$(".sidebar-fixed").css('top', -sidebarPadding + headerHeight + offsetBottom + 'px');
					$(".sidebar-fixed").css('bottom', 'auto');
				}
			} else {
				$(".sidebar-fixed").css("position", "static").css('top', 0 + 'px');
			}
		} else {
			$(".sidebar-fixed").css("position", "static").css('top', 'auto');
			$(".sidebar-fixed").css("position", "static").css('bottom', 'auto');
		}
	}
	setSidebarHeight();

	function setMapWidth() {
		if ($("#map").length && $(window).width() > 640) {
			if ($("#map").data("maptype") == "on_homepage") {
				var endMap = $(".block.view-map .map_control").offset().left,
					width = $("body").width() - ($("body").width() - endMap);
				$("#map").width(width);
			}
			if ($("#map").data("maptype") == "in_tab") {
				var width = $("body").width() - ($(".sidebar").offset().left + $(".sidebar").outerWidth()),
					marginLeft = $(".block-main").offset().left - ($(".sidebar").offset().left + $(".sidebar").outerWidth()),
					marginBottom = parseInt($(".block-main").css("padding-top")) * (-1);
				$("#map").width(width);
				$("#map").css("margin-left", - marginLeft);
				$("#map").css("margin-bottom", marginBottom);
			}
		} else {
			$("#map").css(" ");
		}
	}
	function setMapWidth2() {
		if ($("#mapa").length && $(window).width() > 640) {
			if ($("#mapa").data("maptype") == "on_homepage") {
				var offset = $(".block.view-map .map_control").offset();
				var endMap = (!!offset) ? offset.left : 0;
				var width = $("body").width() - ($("body").width() - endMap);

				if (!offset) {
					width = $("#mapa").parent().width();
					var height = $("#mapa").parent().height();
					$("#mapa").height(height);
					$("#mapa").css('maxHeight', 'none');
				}

				$("#mapa").width(width);
			}
			if ($("#mapa").data("maptype") == "in_tab") {
				var width = $("body").width() - ($(".sidebar").offset().left + $(".sidebar").outerWidth());
				var marginLeft = $(".block-main").offset().left - ($(".sidebar").offset().left + $(".sidebar").outerWidth());
				var marginBottom = parseInt($(".block-main").css("padding-top")) * (-1);

				$("#mapa").width(width);
				$("#mapa").css("margin-left", -marginLeft);
				$("#mapa").css("margin-bottom", marginBottom);
			}
		} else {
			$("#mapa").css({ width: "100%", height: "auto" });
		}
	}

	setSearchPlaceholder();

  var prevScrollpos = window.pageYOffset;
	function positionMobileSidebar() {
		var $sidebar = $("body:not(.page-template-tpl-search_connection) .sidebar");
		var $mainMenu = $("#menu-hlavni-menu");

		if ($(window).width() >= 840 || !$sidebar.length || !$mainMenu.length) {
			$sidebar.css("top", "");
			return;
		}

		$sidebar.css("top", $mainMenu[0].getBoundingClientRect().bottom);
	}

	$(window).scroll(function(){
		setSidebarHeight();
		if ($("body").hasClass("has-mobile-sidebar-open")) {
			return;
		}

    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
      $("#menu-hlavni-menu").css("top", "");
      $("#menu-hlavni-menu").css("z-index", "");

	  $("body:not(.page-template-tpl-search_connection) .sidebar").css("top", "");
	  $("body:not(.page-template-tpl-search_connection) .sidebar").css("z-index", "");

		positionMobileSidebar();
    } else {
		if (currentScrollPos > 45) {
			$("#menu-hlavni-menu").css("top", "-50px");
			$("#menu-hlavni-menu").css("z-index", "-1");

			if ($(window).width() < 840) {
				$("body:not(.page-template-tpl-search_connection) .sidebar").css("top", "-50px");
				$("body:not(.page-template-tpl-search_connection) .sidebar").css("z-index", "-1");
			}
		}
    }

    prevScrollpos = currentScrollPos;
	});
	$(window).resize(function(){
		setSidebarHeight();
		setSearchPlaceholder();

		if ($(window).width() >= 840) {
			$("body").removeClass("has-mobile-sidebar-open");
			$("#menu-hlavni-menu").css({ "top": "", "z-index": "" });
			$(".sidebar").removeClass("mobile-menu-open").css({ "top": "", "z-index": "" });
			$(".mobile-menu-badge").removeClass("has-nav-open").attr("aria-expanded", "false");
			$(".sidebar-fixed").removeClass("show");
		} else {
			positionMobileSidebar();
		}
	});

	function setTabsWidths() {
		$(".tabs.view-large li").each(function(){
			$(this).addClass("view-current");
			$(this).css("width", $(this).width());
			$(this).removeClass("view-current");
		});
		$(".tabs.view-large li:first-child").addClass("view-current");
	}
	setTabsWidths();


	$("[data-tab]").click(function(){
		var tab = $(this).data("tab");
		$("[data-tab]").each(function(){
			$(this).removeClass("view-current");
		});
		$("[data-tabcnt]").each(function(){
			$(this).hide();
		});
		$("[data-tabcnt='" + tab + "']").show();
		$(this).addClass("view-current");
		if ($("[data-tabcnt='" + tab + "'] #map").length) {
			//initMap();
			runStopMap();
		}
		if($('body').hasClass('page-template-tpl-jr-stops') || $('body').hasClass('page-template-tpl-jr-stops-tablo')) {
			stopTabClick($(this));
		}
		if($(".block-main-slider").length && $(this).parent().hasClass('is-fakse')) {
			$(".block-main-slider").slick({
				prevArrow: prevArrow,
				nextArrow: nextArrow,
				appendArrows: $('.block-main-slider-arrows'),
				slide: '.block-main-slide',
			});
		}

	});

	$("h2.expandable").click(function() {
		$(this).toggleClass("is-expanded");
		$(this).next(".expandable-content").slideToggle(150);
	});

	$("h3.expandable").click(function() {
		$(this).toggleClass("is-expanded");
		$(this).next(".expandable-content").slideToggle(150);
	});

	$("form[action='']").addClass("without-action");

	// nav opening
	$("[data-menu]").click(function(){
		if ($("body").hasClass("has-nav-open")) {
			var canClose = true;
			$('.full_nav-group').each(function() {
				if($(this).hasClass('view-active')) {
					canClose = false;
				}
			});
			$('.full_nav-cnt').attr('aria-hidden', 'true');
			if(canClose) {
				unlockBody();
				$("body").removeClass("has-nav-open");
			} else {
				$('.header-logo .menu_button').removeClass('view-back');
				$('.full_nav-group').removeClass('view-active');
			}

		} else {
			lockBody();
			$("body").addClass("has-nav-open");
			$('.full_nav-cnt').attr('aria-hidden', 'false');
		}
	});

	$('body').on('click', ".result-more", function(){
		$(this).parent().toggleClass("view-expanded");
	});

	$('body').on('click', ".result-info__station-additional-interstations.is-link", function(e){
		e.preventDefault();
		$(this).toggleClass("opened");
		if ($(this).parent().next().find('.result-info__station-additional-list-single').length > 1) {

			$(this).parent().next().toggle();
		} else {
			var url = window.location.origin + '/detail-spojeni/?handle=' + $(this).data('handle') + '&connid=' + $(this).data('conn') + '&index=' + $(this).data('index');
			var w = 700;
			var h = 700;
			var left = (window.screen.width-(w+60))/2;
			var top = (window.screen.height-(h+80))/2;
			var strWindowFeatures = "height=" + h + ",width=" + w + ",left=" + left + ",top=" + top + ",location=no,menubar=no,status=no,toolbar=no,scrollbars=yes,resizable=yes,dialog=yes";
			var oWin = window.open(url, "route", strWindowFeatures);
			oWin.focus();
		}

	});

	$('body').on('click', ".route-popup-link", function(e){
		e.preventDefault();

		var url = window.location.origin + '/detail-spojeni/?handle=' + $(this).data('handle') + '&connid=' + $(this).data('conn') + '&index=' + $(this).data('index');
		var w = 700;
		var h = 700;
		var left = (window.screen.width-(w+60))/2;
		var top = (window.screen.height-(h+80))/2;
		var strWindowFeatures = "height=" + h + ",width=" + w + ",left=" + left + ",top=" + top + ",location=no,menubar=no,status=no,toolbar=no,scrollbars=yes,resizable=yes,dialog=yes";
		var oWin = window.open(url, "route", strWindowFeatures);
		oWin.focus();
	});

	function switchUserView(action) {
		if ($("body").hasClass("has-user-open") && action == "close") {
			var href = window.location.href;
			if(href.indexOf('?open=')) {
			    var url = href.split('?open=')[0];
				history.pushState(null, null, url);

			}
			unlockBody();
			$("body").removeClass("has-user-open");
		} else {
			lockBody();
			$("body").addClass("has-user-open");
			if (action == "user") {
				history.pushState(null, null, "?open=user");
				$(".user").removeClass("view-notifications").addClass("view-user");
			} else {
				history.pushState(null, null, "?open=notifications");
				$(".user").removeClass("view-user").addClass("view-notifications");
			}
		}
		$("form.without-action").each(function(){
			$(this).attr("action", window.location.href)
		});
	}

    $("#removeUser").click(function (e){
        if (confirm('Opravdu chcete smazat Váš účet?')) {
			window.location.href = window.location.origin + '?smazat_ucet=1';
        }
    });

	$("[data-user]").click(function(){
		if ($('body').hasClass('has-user-open')) {
			switchUserView('close');
		} else {
			if ($(this).hasClass('header-control-notification')) {
				switchUserView($(this).data("user"));
				$.ajax({
					type: "post",
					dataType: "json",
					url: ajaxurl,
					data: {
						action: "unreadNotifications",
						ajax: true
					}
				});

			} else {
				switchUserView($(this).data("user"));
			}
		}
	});

	if (getUrlVars()["open"] == "user") {
		switchUserView("user");
	}

	if (getUrlVars()["open"] == "notifications") {
		switchUserView("notifications");
	}

	$("input").on("focus", function(){
		$(this).parent().addClass("view-focus");
	});

	$("input").on("focus", function(){
		$(this).parent().addClass("view-focus");
	});

	$("input").on("focusout", function(){
		$(this).parent().removeClass("view-focus");
	});

	$('.links-link a').click(function (){
		var lineid = $(this).data('lineid');
		$('.links-link a:not([data-lineid='+lineid+'])').each(function (){
			$(this).removeClass('is-active');
		});
		$(this).toggleClass('is-active');
		$('.links-detail:not([data-id='+lineid+'])').each(function (){
			$(this).removeClass('is-active');
		});
		$('.links-detail[data-id='+lineid+']').last().toggleClass('is-active');
	});

	$('table.infocentra td').on('click',function (){
		$('#places-popup .places-popup-content').html('');
		$('#places-popup .places-popup-replace').text('');
		$('body').addClass('is-locked');
		$('#places-popup').show();
		$('.places-popup-close.is-full').show();
		 var content = $(this).parent().find('.places-services').html();
		 var title = $(this).parent().find('.places-title').html();
		 $('#places-popup .places-popup-replace').html(title);
		 $('#places-popup .places-popup-content').html(content);
	});

	$('.places-popup-close').on('click',function () {
		$('body').removeClass('is-locked');
		$('#places-popup').hide();
		$('.places-popup-close.is-full').hide();
	});

	$('#places-filter select').on('change',function (){
		var val = $("#filter").val();
		if(!val) {
			$("#filter").prop('disabled', true);
		}
		$('#places-filter').submit();
	});

	function updateStopTablo() {
		if($(".page-template-tpl-jr-stops-tablo .boxes").length) {
			var mode = "",
				fails = 0;
			$.ajax({
				type: "post",
				dataType: "json",
				url: ajaxurl,
				data: {
					action: "updateStopTablo",
					type: $("[data-tabcnt=1]").data('type'),
					stop: $("[data-tabcnt=1]").data('stop'),
					stanoviste: $("[data-tabcnt=1]").data('stanoviste'),
					mode: mode,
					ajax: true
				},
				success: function(response) {
					if(response.success) {
						$("[data-tabcnt=1] .boxes").html(response.html);
						fails = 0;
					} else {
						fails++;
						if (fails == 6) {
							$("[data-tabcnt=1] .boxes").html("Chyba při načítání dat. Informace o provozu na webu www.ropid.cz nebo na infolince 234 704 560.");
						}
					}
				}
			});
		}
	}

	var updateStopTabloInterval = null;
	function setUpdateStopTabloInterval() {
		updateStopTablo();
		clearInterval(updateStopTabloInterval);
		updateStopTabloInterval = setInterval(function() {
			updateStopTablo();
		}, 20 * 1000);
		// }, 20 * 1000);
	}
	setUpdateStopTabloInterval();


	setTimeout(function(){
		if($(".password-sent-notice").length > 0) {
			$(".password-sent-notice").hide();
		}
	}, 5000);

	$("#chooseForm").on("change", function(){
		if($("#range11:checked").length > 0) {
			$("#additional-P-7").show();
		} else {
			$("#additional-P-7").hide();
		}
	});

	$('input[name="low"]').on('change', function(e){
		if($(this).is(':checked')) {
			$('input[name="handicap"]').prop('checked', true);
			$('input[name="handicap"]').prop('disabled', true);
		} else {
			$('input[name="handicap"]').prop('checked', false);
			$('input[name="handicap"]').prop('disabled', false);
		}
	});
	$(".switch-direction").on("click", function (){
		var inputFrom = $("#search-form input[name='from']");
		var inputTo = $("#search-form input[name='to']");

		var inputFromValue = inputFrom.val();
		var inputToValue = inputTo.val();

		inputFrom.val(inputToValue);
		inputTo.val(inputFromValue);
	});

	$(".mobile-menu-badge").on("click", function(){
		var $badge = $(this);
		var $sidebar = $badge.closest(".sidebar");
		var isOpen = !$badge.hasClass("has-nav-open");

		$badge.toggleClass("has-nav-open", isOpen).attr("aria-expanded", isOpen ? "true" : "false");
		$badge.next(".sidebar-fixed").toggleClass("show", isOpen);
		$sidebar.toggleClass("mobile-menu-open", isOpen);
		$("body").toggleClass("has-mobile-sidebar-open", isOpen);
	}).on("keydown", function(e){
		if (e.key === "Enter" || e.key === " ") {
			e.preventDefault();
			$(this).trigger("click");
		}
	});

	positionMobileSidebar();

	postColorboxInit();
	backToTopButton();

	if ($('.dynamicForm').length > 0) {
		$("#pidFormSelect").on("change", function(e){
			let value = $(this).val();

			$(".dynamicForm .pidForm").each(function () {
				let formId = $(this).attr('option-id');

				let visibility = 0;

				if (formId === value) {
					visibility = 1;
				}

				$(this).attr('visibility', visibility);
			})
		});
	}

	$.datetimepicker.setLocale('cs');

	const dtOpts = {
		format: 'd.m.Y H:i',
		step: 1,
		dayOfWeekStart: 1,
		scrollInput: false
	};

	function initPicker($el){
		const el = $el.get(0);
		if ($el.data('xd-init')) return;
		$el.datetimepicker(dtOpts);
		$el.data('xd-init', true);
	}

	if ($(".pidDatetime").length > 0) {
		$(".pidDatetime").each(function (e) {
			initPicker($(this));
		})
	}
});

function backToTopButton() {
	const windowHeight = jQuery(window).height();
	let isVisible = false;

	jQuery(window).on('scroll', function(){
		let scrollTop = jQuery(window).scrollTop();
		let windowHeight = jQuery(window).height();
		let buttonHeight = jQuery("#back-to-top-button").outerHeight();
		let footerTop = jQuery("footer").offset().top;
		let buttonBottomPos = scrollTop + windowHeight - buttonHeight;

		if (scrollTop > windowHeight && !isVisible) {
			jQuery("#back-to-top-button").fadeIn();
			isVisible = true;
		} else if (scrollTop <= windowHeight && isVisible) {
			jQuery("#back-to-top-button").fadeOut();
			isVisible = false;
		}

		if (isVisible && buttonBottomPos > footerTop) {
			let overlap = buttonBottomPos - footerTop;
			jQuery("#back-to-top-button").css("bottom", overlap + 70 + "px");
		} else {
			jQuery("#back-to-top-button").css("bottom", "50px");
		}
	});

	jQuery("#back-to-top-button").on('click', function(){
		jQuery("html, body").animate({ scrollTop: 0 }, 500);
	});
}

function stopTabClick(_this) {
	if(!blankHref) blankHref = window.location.href;
	var replace = false;
	var re = /tab=\d+/;
	var m;
	if((m = re.exec(blankHref)) !== null) {
		if(m.index === re.lastIndex) re.lastIndex++;
		replace = m[0];
	}
	var ch = (blankHref.indexOf("?") === -1) ? '?' : '&';

	var id = _this.attr('data-tab');

	if(jQuery('[data-tabcnt="'+id+'"]').data('empty') === true) {
		requestStopTab(jQuery('[data-tabcnt="'+id+'"]').data('char'), jQuery('[data-tabcnt="'+id+'"]').data('inprague'), id);
	}
	var addr = replace
		? blankHref.replace(replace, 'tab=' + id)
		: blankHref + ch + 'tab=' + id;
	window.history.pushState('tab', 'Tab', addr);

	if(jQuery("#stops-for-map").length && id === '3') {
		setTimeout(function() {
			runStopMap2();
		}, 10);
	}

}

if(jQuery("#stops-for-map").length && jQuery(".tabs_cnt-tab.active").attr('data-tabcnt') === '3') {
	setTimeout(function() {
		runStopMap2();
	}, 250);
}

if(jQuery("#stop-map-wrap").length) {
	setTimeout(function() {
		runStopMap2();
	}, 250);
}

function requestStopTab(char, inPrague, tabId) {
	jQuery.ajax({
		type: "post",
		dataType: "json",
		url: ajaxurl,
		data: {
			action: "getStopTab",
			char: char,
			in_prague: inPrague,
			ajax: true
		},
		success: function(response) {
			if(response.success === true) {
				jQuery('[data-tabcnt="'+tabId+'"]').html(response.html).attr('data-empty', false);
			}
		}
	});
}

function runStopMap2() {
	const stopsForMap = jQuery("#stops-for-map").val();
	let cntr = stopsForMap ? JSON.parse(stopsForMap) : [];

	let lat = 0, lng = 0, cnt = 0;
	for (let k = 0; k < cntr.length; k++) {
		if (cntr[k].lat && cntr[k].lng) {
			cnt++;
			lat += parseFloat(cntr[k].lat);
			lng += parseFloat(cntr[k].lng);
		}
	}

	const center = cnt ? [lat / cnt, lng / cnt] : [50.0755, 14.4378]; // Defaultní Praha
	const zoom = cnt ? 18 : 11;

	const map = L.map('mapaD').setView(center, zoom);

	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: '&copy; OpenStreetMap contributors',
		zoom: 8.5,
		maxZoom: 18,
		minZoom: 8.5,
		maxBounds: [
			[49.3, 13.2], // Jihozápadní roh
			[50.8, 15.8]  // Severovýchodní roh
		],
		maxBoundsViscosity: 0.8
	}).addTo(map);

	const markers = L.markerClusterGroup();

	jQuery.getJSON('/points.json', function(columns) {
		processColumns2(columns, markers);
	});

	map.addLayer(markers);
}

function closeBubbles() {
	for(var i = 0; i < bubbles.length; i++) {
		bubbles[i].close();
	}
}

function clearOverlays() {

	mc.clearMarkers();
	for(var i = 0; i < markers.length; i++) {
		markers[i].setMap(null);
	}
	markers.length = 0;
	closeBubbles();
	bubbles.length = 0;
}

function processColumns(columns) {
	var mapBounds = map.getBounds();
	for(var i = 0; i < columns.length; i++) {
		var marker = addMarker(columns[i], mapBounds);
		if(marker) {
			markers.push(marker);
			if(map.getZoom() < 15) {
				mc.addMarker(marker);
			}
		}
	}
}
function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
	var p = 0.017453292519943295;    // Math.PI / 180
  var c = Math.cos;
  var a = 0.5 - c((lat2 - lat1) * p)/2 +
          c(lat1 * p) * c(lat2 * p) *
          (1 - c((lon2 - lon1) * p))/2;

  return 12742 * Math.asin(Math.sqrt(a));
}

function deg2rad(deg) {
	return deg * (Math.PI/180)
}
function processColumns2(columns, markers) {
	for (let i = 0; i < columns.length; i++) {
		const col = columns[i];
		const position = [parseFloat(col.lat), parseFloat(col.lng)];

		let size = (col.sta.length >= 3) ? 'wide' : 'narrow';
		if (col.sta === 'vlak') size = 'vlak';
		const fSize = (size === 'wide') ? '48px' : '30px';

		if ((col.sta === "M1" || col.sta === "M2" || col.sta === "M3" || col.sta === "M4") && typeof col.lines[0] !== "undefined") {
			if (!!col.special) size += `-${col.special.replace(',', '')}`;
			else size += `-${col.lines[0].link_name}`;
		} else if (!!col.special) {
			size += `-${col.special}`;
		}

		const markerHtml = `
            <div style="cursor: pointer; position: absolute; width: ${fSize}; height: ${fSize};">
                <img src="/wp-content/themes/pid/images/markers/marker-${size}.png" style="width: ${fSize};">
                <div style="position: absolute; left: 0px; top: 6px; text-align: center; width: 100%; color: black; font-size: 13px;">
                    ${(col.sta === "M1" || col.sta === "M2" || col.sta === "M3" || col.sta === "M4" || col.sta === "vlak" || !!col.special) ? '' : col.sta}
                </div>
            </div>`;

		const markerIcon = L.divIcon({
			className: 'custom-marker',
			html: markerHtml,
			iconSize: [48, 48],
			iconAnchor: [24, 48],
		});

		const popupContent = generatePopupContent(col);
		const marker = L.marker(position, { icon: markerIcon }).bindPopup(popupContent);

		markers.addLayer(marker);
	}
}

function generatePopupContent(col) {
	const tableRows = col.lines.map(line => `<tr><td>${line.link_name}</td><td>${line.to_name}</td></tr>`).join('');

	const actualText = jQuery('#translated-texts .actual').text();
	const stopText = jQuery('#translated-texts .stop').text();
	const stanText = jQuery('#translated-texts .stan').text();
	const enterText = jQuery('#translated-texts .enter').text();
	const scheduleText = jQuery('#translated-texts .schedule').text();

	const station = (col.sta === "M1" || col.sta === "M2" || col.sta === "M3" || col.sta === "M4")
		? enterText
		: `${stanText} <strong>${col.sta}</strong>`;

	return `
        <div class="bubble-content" style="margin-bottom:-5px">
            <span style="padding-right:10px">${stopText} <strong>${col.name}</strong>, ${station}</span>
            <table class="noscroll">${tableRows}</table>
            <table class="bubble-content-links noscroll">
                <tr>
                    <td><a href="#" onclick="selectStay('${col.sta}','${col.name}');">${actualText}</a></td>
                    <td><a href="#" onclick="selectActual('${col.sta}','${col.name}');">${scheduleText}</a></td>
                </tr>
            </table>
        </div>`;
}


var bubbles = [];

function addMarker(col, bounds) {
	var bubble = true;
	if(map.getZoom() >= 15) {
		var position = new google.maps.LatLng({lat: parseFloat(col.lat), lng: parseFloat(col.lng)});
	} else {
		if(col.avg === false) {
			return false;
		}
		var position = new google.maps.LatLng({lat: parseFloat(col.avg.lat), lng: parseFloat(col.avg.lng)});
		bubble = false
	}
	if(!bounds.contains(position)) return false;
	if(col.indx == 7068 || col.sta === null) return false;

	var size = (col.sta.length >= 3) ? 'wide' : 'narrow';
	if(col.sta === 'vlak') size = 'vlak';
	var fSize = (size === 'wide') ? 48 : 30;
	var sSize = (size === 'wide') ? 24 : 15;
	if((col.sta === "M1" || col.sta === "M2" || col.sta === "M3" || col.sta === "M4") && typeof col.lines[0] !== "undefined") {
		if(!!col.special) size += '-' + col.special.replace(',', '');
		else size += '-' + col.lines[0].link_name;
	} else if(!!col.special) {
		size += '-' + col.special;
	}

	var icon = {
		url: '/wp-content/themes/pid/images/markers/marker-' + size + '.png',
		size: new google.maps.Size(fSize, 48),
		scaledSize: new google.maps.Size(fSize, 48),
		labelOrigin: new google.maps.Point(sSize, 14),
	}
	var dot = {
		url: '/wp-content/themes/pid/images/markers/dot.png',
		size: new google.maps.Size(32, 32),
		scaledSize: new google.maps.Size(16, 16),
		labelOrigin: new google.maps.Point(24, 14),
		anchor: new google.maps.Point(8, 8)
	}

	var marker = bubble ? new google.maps.Marker({
		position: position,
		label: (col.sta === "M1" || col.sta === "M2" || col.sta === "M3" || col.sta === "M4"
			|| col.sta === "vlak" || !!col.special) ? '' : col.sta,
		icon: icon,
		map: map
	}) : new google.maps.Marker({
		position: position,
		title: col.name,
		optimized: false,
		icon: dot,
		map: map
	});

	if(bubble) {
		var rows = {};
		var tableRows = '';
		col.lines.sort(function(a, b) {
			if(isNaN(parseInt(a.link_name)) || isNaN(parseInt(b.link_name)))
				return a.link_name - b.link_name;
			return parseInt(a.link_name) - parseInt(b.link_name)
		});
		for(var i = 0; i < col.lines.length; i++) {
			var line = col.lines[i];
			tableRows += '<tr><td>' + line.link_name + '</td><td>' + line.to_name + '</td></tr>';
		}

		var actualText = jQuery('#translated-texts .actual').text();
		var stopText = jQuery('#translated-texts .stop').text();
		var stanText = jQuery('#translated-texts .stan').text();
		var enterText = jQuery('#translated-texts .enter').text();
		var scheduleText = jQuery('#translated-texts .schedule').text();

		var station = (col.sta === "M1" || col.sta === "M2" || col.sta === "M3" || col.sta === "M4")
			? enterText
			: stanText+' <strong>' + col.sta + '</strong>';

		var departure = (col.sta === "M1" || col.sta === "M2" || col.sta === "M3" || col.sta === "M4")
			? 'Metro'
			: col.sta;

		var windowString =
			'<div class="bubble-content" style="margin-bottom:-5px"><span class="bubble-content-close" onclick="closeBubbles()"></span>' +
			'<span style="padding-right:10px">'+stopText+' <strong>' + col.name + '</strong>, ' + station + '</span>' +
			'<table class="noscroll">' +
			tableRows +
			'</table>' +
			'<table class="bubble-content-links noscroll">' +
			'<tr><td><a href="#" onclick="selectStay(\'' + departure + '\',\'' + col.name + '\');">'+actualText+'</a></td><td><a href="#" onclick="selectActual(\'' + col.sta + '\',\'' + col.name + '\');">'+scheduleText+'</a></td></tr>' +
			'</table>' +
			'</div>';

		var infoBubble = new InfoBubble({
			minWidth: 225,
			maxWidth: 225,
			content: windowString,
			shadowStyle: 1,
			padding: 0,
			borderRadius: 0,
			arrowSize: 0,
			borderWidth: 1,
			borderColor: 'black',
			disableAutoPan: true,
			hideCloseButton: true,
			arrowPosition: 30,
			backgroundClassName: 'phoney-' + col.indx,
			arrowStyle: 5
		});


		marker.addListener('click', function() {
			if (infoBubble.isOpen()) {
				infoBubble.close();
				activeMarker = false;
			} else {
				activeMarker = true;
				closeBubbles();
				infoBubble.open(map, marker)
				updateHeight(infoBubble, '.phoney-' + col.indx);
				changeBoundsSemaphore = false;
				setTimeout(function() {
					changeBoundsSemaphore = true;
				},600);
				map.panTo(marker.getPosition());

			}
		});
		bubbles.push(infoBubble);
	} else {
		marker.addListener('click', function() {
			map.setZoom(17);
			map.setCenter(position);
		});
	}
	return marker;
}

function updateHeight(infoBubble, elm) {
	setTimeout(function() {
		if(jQuery(elm).length && jQuery(elm).last().height() > 0) {
			var h = Math.min(jQuery(elm).last().height() + 10, 200);
			infoBubble.setMaxHeight(h);
			infoBubble.setMinHeight(h);
		}
	},100)
}

function selectActual(stan,stop) {
	var newhref = jQuery('#getpermalink').val()+'?stop='+stop+'&stanoviste='+stan+'&tab=2';
	window.location.href = newhref;
}

function selectStay(stan,stop) {
	var newhref = jQuery('#getpermalink').val()+'?stop='+stop+'&stanoviste='+stan;
	window.location.href = newhref;
}

function postColorboxInit() {
	if (jQuery('body').hasClass('single-post') || jQuery('body').hasClass('page-template-default')) {
		jQuery('.wysiwyg .gallery a').filter(function() {
			return jQuery(this).find('img').length > 0;
		}).each(function() {
			var $link = jQuery(this);
			var $img = $link.find('img');
			var imgSrc = $link.find('img').attr('src');
			var currentHref = $link.attr('href');

			var isImageLink = /\.(jpg|jpeg|png|gif|bmp|webp|svg)$/i.test(currentHref);

			if (!isImageLink) {
				$link.attr('href', imgSrc);
			}

			$link.data('caption', $img.data('caption'));
			$link.data('description', $img.data('description'));

			$link.attr('title', $img.data('description'));
		}).colorbox({
			rel: 'gal',
			maxWidth: '90%',
			maxHeight: '90%',
			current: "Obrázek {current} z {total}",
			title: function() {
				var caption = jQuery(this).data('caption') || '';
				var description = jQuery(this).data('description') || '';
				return '<strong>' + caption + '</strong> ' + description;
			}
		});

		jQuery(document).on('cbox_complete', function() {
			var $title = jQuery('#cboxTitle');
			var $content = jQuery('#cboxLoadedContent');

			let positionOffset = 3;

			if (jQuery(window).width() < 767) {
				positionOffset = 10;

				if ($title.outerHeight(true) > 30) {
					positionOffset = 33;
				}
			}

			if ($title.length && $content.length) {
				var titleHeight = $title.outerHeight(true) + positionOffset;
				$title.css({
					top: '-' + titleHeight + 'px',
				});
			}
		});

	}
}

document.addEventListener("DOMContentLoaded", function () {
	const links = document.querySelectorAll("a[href*='jrportal.dpp.cz']");

	links.forEach(link => {
		link.addEventListener("click", function () {
			fetch("/wp-json/pid/v1/log-click/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-WP-Nonce": PID_Settings.nonce
				},
				body: JSON.stringify({
					time: new Date().toISOString(),
					url: link.href
				})
			});
		});
	});
});
