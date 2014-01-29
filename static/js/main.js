
var contenidos;
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

$(document).ready(function(){

	contenidos = [];

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

		doctor_info.full_name = document.getElementById("full_name").value;
		doctor_info.specialities = document.getElementById("specialities").value;
		doctor_info.email = document.getElementById("email").value;

		gapi.client.doctors.save(doctor_info).execute(function(response){
			console.log(response);
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