var $ =jQuery.noConflict();
function listadoAsamblea() {
    $.ajax({
        url: "/indexadmin/listarasamblea/",
        type: "get",
        dataType: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_asamblea')) {
                $('#tabla_asamblea').DataTable().destroy();
            }
            $('#tabla_asamblea tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>';
                if (response[i]["fields"]['fk_id_asa'] == ''){
                    fila += '<td>Desconocido</td>';
                }else{
                    fila += '<td>' + response[i]["fields"]['fk_id_asa'] + '</td>';       
                }  
                fila += '<td>' + response[i]["fields"]['nombre_asa'] + '</td>';
                fila += '<td>' + response[i]["fields"]['descripcion_asa'] + '</td>';
                fila += '<td>' + response[i]["fields"]['archivo_asa'] + '</td>';
                fila += '<td>' + response[i]["fields"]['fechacreacion_asa'] + '</td>';              
                fila += '<td><button type = "button" class="status-tb-btn btn-primary me-4"';
                fila += ' onclick = "abrir_modal_edicion(\'/indexadmin/editarasamblea/' + response[i]['pk'] + '/\');"><i class="fa-solid fa-arrows-rotate"></i></button>';
                fila += '<button type = "button" class="status-tb-btn btn-danger" ';
                fila += 'onclick = "abrir_modal_eliminacion(\'/indexadmin/eliminarasamblea/' + response[i]['pk'] + '/\');"><i class="fa-solid fa-trash"></i></buttton></td>';
                fila += '</tr>';
                $('#tabla_asamblea tbody').append(fila);
            }
            $('#tabla_asamblea').DataTable({
                language: {
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
        error: function (error) {
            console.log(error);
        }
    });
}


function registrar() {
    activarBoton();
    var data = new FormData($('#form_creacion').get(0));
    $.ajax({        
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'), 
        data: data,
        cache: false,
        processData: false,
        contentType: false, 
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoAsamblea();
            cerrar_modal_creacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion(error);
            activarBoton();
        }
    });
}

function editar() {
    activarBoton();
    var data = new FormData($('#form_edicion').get(0));
    $.ajax({        
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'), 
        data: data,
        cache: false,
        processData: false,
        contentType: false, 
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoAsamblea();
            cerrar_modal_edicion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBoton();
        },        
    });
}

function eliminar(pk) {
    $.ajax({
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        url: '/indexadmin/eliminarasamblea/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoAsamblea();
            cerrar_modal_eliminacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
        }
    });
}





$(document).ready(function () {
    listadoAsamblea();
  
});

