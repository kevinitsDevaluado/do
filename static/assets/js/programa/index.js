var $ =jQuery.noConflict();
function listadoPrograma(){
    $.ajax({
        url:"/indexadmin/listarprograma/",
        type: "get",
        dataType: "json",
        success: function(response){
            if($.fn.DataTable.isDataTable('#tabla_programa')){
                $('#tabla_programa').DataTable().destroy();
            }
            $('#tabla_programa tbody').html("");
            for(let i = 0; i < response.length; i++){
                let fila = '<tr>';
                fila += '<td>' + (i+1) + '</td>';//Concatenacion 
                fila += '<td>' + response[i]["fields"]["titulo_pro"] + '</td>';
                fila += '<td>' + response[i]["fields"]["fechacreacion_pro"] + '</td>';
                fila += '<td>' + response[i]["fields"]["descripcion_pro"] + '</td>';
                fila += '<td> <img src="/media/'+ response[i]["fields"]["imagen_pro"] +'" class="img-fluid d-block mx-auto" style="width: 50px; height: 50px;"><br> </td>';    
                fila += '<td>' + response[i]["fields"]["slug"] + '</td>';
                fila += '<td>'+response[i]["fields"]["estado_pro"]+'</td>';
                fila += '<td> <button class="status-tb-btn btn-primary"';
                fila += 'onclick="abrir_modal_edicion(\'/usuarios/editar_usuarios/'+response[i]['pk']+'/\');"><i class="fa-solid fa-arrows-rotate"></i></button>';
                fila += '<button class="status-tb-btn btn-danger"';
                fila += 'onclick="abrir_modal_eliminacion(\'/usuarios/eliminar_usuarios/'+response[i]['pk']+'/\');"><i class="fa-solid fa-trash"></i></button></td>';

                fila += '</tr>';
                $('#tabla_programa tbody').append(fila);  
            }
            $('#tabla_programa').DataTable({
                language:{
                    "decimal": "",
                    "emptyTable": "No hay información",
                    "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
                    "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                    "infoPostFix": "",
                    "thousands": ",",
                    "lengthMenu": "Mostrar _MENU_ Entradas",
                    "loadingRecords": "Cargando...",
                    "processing": "Procesando...",
                    "search": "Buscar:",
                    "zeroRecords": "Sin resultados encontrados",
                    "paginate": {
                        "first": "Primero",
                        "last": "Ultimo",
                        "next": "Siguiente",
                        "previous": "Anterior"
                    },
                },
                responsive: true
            });
             
        },
        error: function(error){
            console.log(error);
        }
    })
}

function registrar(){
    activarBoton();
    var data = new FormData($('#form_creacion').get(0));
    $.ajax({
        data: data,
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        cache : false, 
        contentType:false,
        processData: false,
        success: function(response){
            notificacionSuccess(response.mensaje);
            listadoPrograma();
            cerrar_modal_creacion();
        },
        error: function(error){
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion(error);
            activarBoton();
        }        
    });
}



$(document).ready(function (){
    listadoPrograma();
});




