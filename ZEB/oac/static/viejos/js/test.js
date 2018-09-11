$(document).on('ready', main);

function main () {
	
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$('#contenido-caso').on('click', cargar_contenido_caso);
	$('#descripcion-caso').on('click', cargar_caso);

	
	
}

function cargar_contenido_caso () {
	
	$('#contenido-caso').load('test');
	$('#contenido-caso').addClass('descripcion-caso')
	// var contenido = $('#contenido-caso');
	// contenido.html('');

	// $('<a>').html("Holaa").appendTo(contenido);
	// console.log("hola estoy en la funcion");

	// $('#contenido-caso').css('right', '-110%');
	// contenido.css('right', '0');
	// $('#contenido-caso').hide();
	// contenido.on('click', 'a', function(){
	// 	contenido.css('right', '-110%');
	// 	$('#contenido-caso').css('right', '0');
	// 	$('#contenido-caso').show("low");
	// 	$('#descripcion-caso').remove();
	// });
	// var id = $(data.currentTarget).data('id');
	// $.get('cargar_contenido_caso/' + id, cargar_caso)
}

function cargar_caso () {
	
	console.log("hola");
	// $('#descripcion-caso').load('inicio');
}