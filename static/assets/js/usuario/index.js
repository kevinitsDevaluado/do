var $ =jQuery.noConflict();
function listadoUsuarios(){
    $.ajax({
        url:"/usuarios/listar_usuarios/",
        type: "get",
        dataType: "json",
        success: function(response){
            if($.fn.DataTable.isDataTable('#tabla_usuarios')){
                $('#tabla_usuarios').DataTable().destroy();
            }
            $('#tabla_usuarios tbody').html("");
            for(let i = 0; i < response.length; i++){
                let fila = '<tr>';
                fila += '<td>' + (i+1) + '</td>';//Concatenacion 
                fila += '<td>' + response[i]["fields"]["username"] + '</td>';
                fila += '<td>' + response[i]["fields"]["nombres"] + '</td>';
                fila += '<td>' + response[i]["fields"]["apellidos"] + '</td>';
                fila += '<td>' + response[i]["fields"]["email"] + '</td>';
                fila += '<td> <button type = "button" class="status-tb-btn rounded-circle btn-primary me-4"';
                fila += 'onclick="abrir_modal_edicion(\'/usuarios/editar_usuarios/'+response[i]['pk']+'/\');"><i class="fas fa-pencil"></i></button>';
                fila += '<button type = "button" class="status-tb-btn rounded-circle btn-danger" ';
                fila += 'onclick="abrir_modal_eliminacion(\'/usuarios/eliminar_usuarios/'+response[i]['pk']+'/\');"><i class="fas fa-trash-alt"></i></button></td>';

                fila += '</tr>';
                $('#tabla_usuarios tbody').append(fila);  
            }
            $('#tabla_usuarios').DataTable({
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
            listadoUsuarios();
            cerrar_modal_creacion();
        },
        error: function(error){
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion(error);
            activarBoton();
        }        
    });
}

function editar(){
    activarBoton();
    var data = new FormData($('#form_edicion').get(0));
    $.ajax({
        data: data,
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        cache : false, 
        contentType:false,
        processData: false,
        success: function(response){
            notificacionSuccess(response.mensaje);
            listadoUsuarios();
            cerrar_modal_edicion();
        },
        error: function(error){
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBoton();
        }        
    });
}

function eliminar(pk){
    
    $.ajax({
        data:{
            csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
        },
        url: '/usuarios/eliminar_usuarios/'+pk+'/',
        type: 'post',
        success: function(response){
            notificacionSuccess(response.mensaje);
            listadoUsuarios();
            cerrar_modal_eliminacion();
        },
        error: function(error){
            notificacionError(error.responseJSON.mensaje);
        }        
    });
}

$(document).ready(function (){
    listadoUsuarios();
});



