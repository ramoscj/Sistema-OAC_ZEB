$(document).on('ready', main);

function main () {

  	$.ajaxSetup({
  		beforeSend: function(xhr, settings) {
  			if(settings.type == "POST"){
  				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
  			}
  		}
  	});

    cargar_respuesta();
    $('#btnrespuesta').click(guardar_respuesta);
    $('#message-text').keyup(validar_txtarea);
    $('#editar-resp').click(editar_respuesta);
  }

function cargar_respuesta(){

  if ( $('#estado').val() == 'Por atender'){
      $('#txtrespuesta').hide("slow");
    }
  else {
      $('#mostrarmodal').hide("slow");
      $.get('respuesta_caso/', contenido_respuesta)
    }
}

function refrescar_respuesta(){

  if ( $('#estado').val() != 'Por atender'){
      $('#mostrarmodal').hide("fast");
      $.get('respuesta_caso/', contenido_respuesta)
      $('#txtrespuesta').show("slow");
    }
  
}

function guardar_respuesta(){

    var id_user = $('#usuario').data("user");
  	var respuesta = $('#message-text').val();
    var resp_existe = $('#h4-resp').html();
    var urlrespuesta = '';

    if (resp_existe == ''){

      urlrespuesta = 'responder/'

    } else {

      urlrespuesta = 'editar_respuesta/'
    }

    validar_txtarea();

    if (validar_txtarea() == true) {
      
      $.ajax({

          url: urlrespuesta,
          type: 'POST',
          data:{ texto: respuesta, user: id_user },
          success: function(data) {
            // se oculta la modal
            $('#exampleModal').modal('hide');
            // se muestra la alerta
            $('#exitoso').delay("600").fadeIn();
            // se cambia de valor el estado (para que funciona la siguiente linea)
            $('#estado').val('Atendido');
            // se refreca para que se muestre la respuesta
            refrescar_respuesta();
            // se oculta la alerta
            $('#exitoso').delay("6000").fadeOut();
          },
          error: function(jqXHR, textStatus, error) {
            $('#exampleModal').modal('hide');
            $('#error').delay("400").fadeIn();
            $('#error').delay("5000").fadeOut();
            
          }
          
        });

    }

  }
function contenido_respuesta(data){

    console.log(data.respuesta);
    $('#h4-resp').html('');
    $('#h4-resp').html(data.respuesta);

}

function editar_respuesta(){

  var respuesta = $('#h4-resp').html();
  // alert(respuesta);
  $('#message-text').val(respuesta);

}

function validar_txtarea(){

  var respuesta = $('#message-text').val();

    if (respuesta == null || respuesta.length == 0 || /^\s+$/.test(respuesta)){

      $('#error-txt').addClass('has-error');
      $('#alert-error').fadeIn("slow");
      return false;
      
    } else {

      $('#error-txt').removeClass('has-error').addClass('has-success');
      $('#alert-error').fadeOut("fast");
      return true;

    }
}
