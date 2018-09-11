$(document).on('ready', main);

function main () {

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if(settings.type == "POST"){
          xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
        }
      }
    });

  // pos = document.getElementById("id_departamento").selectedIndex;
  // var v1 = document.getElementById("id_departamento");
  // var dep = v1.options[v1.selectedIndex].text;
  var v2 = document.getElementById("select2");
  var caso = v2.options[v2.selectedIndex].text;

  $("#select2").change(function(){

      var tipo = v2.options[v2.selectedIndex].text;
      $('#requisitos').html('')

      if (caso != ''){
        url = '../../../casos/registro_caso/requisitos/'
      }else{
        url = 'requisitos/'
      }
      $.get(url+ tipo, requisitos);
        
    });

  // if (pos != 0){
  //   cargarSelect2(dep)
  //   }
}

function cargarSelect2(valor)
{
    /**
     * Este array contiene los valores sel segundo select
     * Los valores del mismo son:
     *  - hace referencia al value del primer select. Es para saber que valores
     *  mostrar una vez se haya seleccionado una opcion del primer select
     *  - value que se asignara
     *  - testo que se asignara
     */
    var arrayValores=new Array(
        new Array("Despacho","Renuncias","Renuncias"),
        new Array("Personal","Ingresos","Ingresos"),
        new Array("Personal","Traslados","Traslados"),
        new Array("Juridica","Permisos por Grado","Permisos por Grado"),
        new Array("Juridica","Permisos por Defensa de Tesis","Permisos por Defensa de Tesis"),
        new Array("Eponimo","Creación de Código Administrativo","Creación de Código Administrativo"),
        new Array("Pago Directo","Pagos Indebidos","Pagos Indebidos"),
        new Array("Jubilacion","Jubilación del Personal","Jubilación del Personal"),
        new Array("Jubilacion","Pensión del Personal","Pensión del Personal"),
        new Array("Comunidades Educativas","Solicitud de Canaimas","Solicitud de Canaimas"),
        new Array("Notas","Notas Certificadas para Apostillamiento","Notas Certificadas para Apostillamiento"),
        new Array("Inicial","NADA","NADA"),
        new Array("Especial","NADA","NADA"),
        new Array("Primaria","NADA","NADA"),
        new Array("Media General","NADA","NADA"),
        new Array("Educ. para Adultos","NADA","NADA"),
        new Array("H.C.M","Reembolso por Gastos Médicos","Reembolso por Gastos Médicos")
    );
    if(valor==0)
    {

        // desactivamos el segundo select
        document.getElementById("select2").disabled=true;
        // document.getElementById("select2").options.length=1;
    }else{
        // eliminamos todos los posibles valores que contenga el select2
        document.getElementById("select2").options.length=0;
 
        // añadimos los nuevos valores al select2
        document.getElementById("select2").options[0]=new Option("Selecciona una opcion", "0");
        for(i=0;i<arrayValores.length;i++)
        {
            // unicamente añadimos las opciones que pertenecen al id seleccionado
            // del primer select
            if(arrayValores[i][0]==valor)
            {
                document.getElementById("select2").options[document.getElementById("select2").options.length]=new Option(arrayValores[i][2], arrayValores[i][1]);
            }
        }
 
        // habilitamos el segundo select
        document.getElementById("select2").disabled=false;
    }
}
 
/**
 * Una vez selecciona una valor del segundo selecte, obtenemos la información
 * y mostramos los requisitos y preguntas frecuentes
 */

function requisitos(data){

  if (data.requisitos != ''){
    if ((dep = data.departamento) && (caso = data.caso)) {
      $('#requisitos').html(data.requisitos)
      $('#id_preguntas').html(data.preguntas)
      console.log(data.requisitos)
    };
  };

}