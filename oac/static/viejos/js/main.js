$(document).on('ready', main);

function main () {
	
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$('#clases').on('click','a', cargar_contenido_caso);

	//menu para cargar dinamicamente
	$('#nav-2').click(carga_crp);
	
	
}

function cargar_contenido_caso(data) {
	var id = $(data.currentTarget).data('id');
	$.get('cargar_contenido_caso/' + id, cargar_caso);
}

function cargar_caso(data){
	var contenido = $('#contenido-clase');
	var divedit = $('<div id="editar">');

	contenido.html('');

	$('<a class="regresar">').html('Regresar').appendTo(contenido);

	$('<button type="button" class="btn btn-default btn-lg">').html('').appendTo(divedit);
	divedit.appendTo(contenido);
	var btn = $('.btn');
	$('<span class="glyphicon glyphicon-search" aria-hidden="true">').html('').appendTo(btn);
	btn.appendTo("#editar");
	

	$('<h2>').html(data.nombres + ' ' + data.apellidos).appendTo(contenido);

	$('<p>').html(data.descripcion).appendTo(contenido);

	$('<p class="pk" data-id="' +data.id+ '">').html('').appendTo(contenido);

	//mover los article y hacer efecto de desplazamiento
	$('#clases').css('left', '-110%');
	contenido.css('left', '0');

	contenido.on('click', 'a', function(){
		contenido.css('left', '-110%');
		$('#clases').css('left', '0');
	});

	// Para responder el caso de no poseer respuesta
	var div = $('<div id="sitio_resp">');
	$('<span class="responder">').html('Responder').appendTo(div).on('click', responder_caso);
	div.appendTo(contenido);

	// se cargar la respuesta en caso de poseer una
	var id = $('p.pk').data('id');
	$.get('cargar_respuesta_contenido/'+ id, actualizar_respuestas_caso);

}

function responder_caso(data){

	var contenido = $('#contenido-clase');
	var div = $('<div id="resp_caso">');
	div.appendTo(contenido);

	//Se crea el textarea, se carga la siguiente funcion y se ocualta el boton
	$('<textarea placeholder="Escribe tu respuesta" name="txtarea" id="txtarea">').appendTo(div);
	$('<button>').html('Enviar Respuesta').appendTo(div).on('click', enviar_resp_caso);
	$('.responder').hide("low");
}

function test(){
	// var cntent = $('#resp_caso textarea');
	var id_caso = $('p.pk').data('id');
	// console.log(cntent.val());
	console.log(id_caso);

}

function enviar_resp_caso() {

	var respuesta = $('#resp_caso textarea');
	var id = $('p.pk').data('id');

	//se envia la respuesta y se refresca 
	if (respuesta.val() != ''){
		$.post('responder_caso/', 
			{ texto: respuesta.val(), idcaso: $('p.pk').data('id') },'');
		$.get('cargar_respuesta_contenido/'+ id, actualizar_respuestas_caso);
	}
}

function actualizar_respuestas_caso(data) {

	//se carga la respuesta en caso de existir
	if (data.texto != 'Sin Resultados'){

		$('.responder').hide();
		var div = $('<div>');
		var contenido = $('#sitio_resp');
		div.appendTo(contenido);

		$('<blockquote>').html(data.texto).appendTo(div);

		$('#resp_caso').hide();
	}
	else{

		console.log(data.texto)
	}
	
}

//#########################
// BLOQUE PARA OTRO article
//#########################


function carga_crp(){

	$('#libro').load('reporte_nuevo');

}