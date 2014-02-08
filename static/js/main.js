
var contenidos;
var host_user;
var activo = -1;

function patalla_ancho(){

	return window.innerWidth;
}

function cambiar_seccion() {

	var posicion_actual = $(window).scrollTop();

	var n = contenidos.length;

	var ant = 300;

	var max_franja = 500;

	if (patalla_ancho() < '768')
		max_franja = 100;

	for ( var i = 0; i < n; i++){

		if ( posicion_actual >= ant && posicion_actual < contenidos[i].pos && activo != i){

			var icono_actual = contenidos[i].elem.find('.icono');

			icono_actual.animate({ backgroundColor: "green"}, 500);

			var franja_actual = contenidos[i].elem.find('.franja');
			franja_actual.css('padding-bottom', '0.3em');
			franja_actual.css('width', 0);
			franja_actual.animate({width: '+=' + max_franja + '%'}, 500);

			if (activo != -1 ){

				var icono_anterior;
				icono_anterior = contenidos[activo].elem.find('.icono');
				icono_anterior.animate({ backgroundColor: "#ffa500"}, 500);

				var franja_anterior;
				franja_anterior = contenidos[activo].elem.find('.franja');
				franja_anterior.animate({paddingBottom: '0em'},300);

			}

			activo = i;

			break;


		}

		ant = contenidos[i].pos;

	}
}

function get_user(){

	var url_split = document.URL.split('/');
	var length = url_split.length;

	if (url_split[length-1] != window.location.host){
		return url_split[length-1];
	}else
		return '';
}

function show_notification(message){

	var notificator_el = document.getElementById("notificator");

	notificator_el.innerHTML = message;
	$(notificator_el).addClass("show");

	setTimeout(function(){
		$(notificator_el).removeClass("show");
	}, 3000);
}


$(document).ready(function(){

	contenidos = [];
	host_user = get_user();


	$(".tarjeta").each(function(i, e){

		contenidos[i] = {};
		contenidos[i].elem = $(e);
		contenidos[i].pos = $(e).offset().top;
	});


	cambiar_seccion();

	document.onscroll = function(event){

		cambiar_seccion();

	};

	$("#invite_doctor").click(function(){

		var doctor_info = {};

		var full_name_el = document.getElementById("full_name");
		var specialities_el = document.getElementById("specialities");
		var email_el = document.getElementById("email");

		doctor_info.full_name = full_name_el.value;
		doctor_info.specialities = specialities_el.value;
		doctor_info.email = email_el.value;
		doctor_info.invited_by = get_user();

		gapi.client.doctors.save(doctor_info).execute(function(response){
			full_name_el.value = "";
			specialities_el.value = "";
			email_el.value = "";

			show_notification("¡Recibido! Muchas gracias");
		});

	});

	$("#i_want_help").click(function(){

		gapi.client.doctors.poll_opened({email: host_user}).execute(function(){
			window.open("http://www.google.com", '_blank');
		});
	});
});

function init_endpoints(){
	//var ROOT = 'https://capicptest.appspot.com/_ah/api';
	var host = window.location.host;
	var ROOT = '//' + host + '/_ah/api';
	gapi.client.load('doctors', 'v1', function() {

	}, ROOT);
}