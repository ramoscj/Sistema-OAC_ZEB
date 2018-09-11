$(document).ready(function(){
	
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$('.item_div .delete').click(function(){
		
		var elem = $(this).closest('.item_div');
		//se captura el valor el id que tiene el div para conocer el elemento a eliminar
		var id = $(this).data("value");
		
		
		$.confirm({
			'title'		: 'Confirmacion para Eliminar',
			'message'	: 'Usted va a eliminar el elemento de la lista. <br />No podra desacer los cambios mas tarde! Desea Continuar?',
			'buttons'	: {
				'Yes'	: {
					'class'	: 'blue',
					'action': function(){
						
						$.ajax({

				          url: 'eliminar_caso/',
				          type: 'POST',
				          data:{ pk: id},
				          success: function(data) {
				          	// alert("todo ok");
				          	elem.slideUp();
				          	// se agrega la clase para  cambiar el estado del borde y la cabecera
				          	$('#lista-casos').addClass('box box-success box-solid');
				            $('#msjexitoso').css("display","inline");

				            
				            //Para hacer delay y quitar la clase y dejar la original
				            setTimeout(function(){

				            	$('#msjexitoso').css("display","none");
            					$('#lista-casos').removeClass('box-success box-solid');

      							},5000);

				          },
				          error: function(jqXHR, textStatus, error) {
				            // alert("todo mal");
				            // se agrega la clase para  cambiar el estado del borde y la cabecera
				            $('#lista-casos').addClass('box box-danger box-solid');
				            $('#msjerror').css("display","inline");

				            
				            //Para hacer delay y quitar la clase y dejar la original
				            setTimeout(function(){

				            	$('#msjerror').css("display","none");
            					$('#lista-casos').removeClass('box-danger box-solid');

      							},5000);
				            
				            // $('.box').delay("5000").removeClass('box box-success box-solid');
				          				            
				           }
				          
				        });
					}
				},
				'No'	: {
					'class'	: 'gray',
					'action': function(){}	// Nothing to do in this case. You can as well omit the action property.
				}
			}
		});
		
	});
});

function borrar_resp(id){



}