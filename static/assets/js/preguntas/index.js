var $ =jQuery.noConflict();
function listadoPreguntas() {
    $.ajax({
        url: "/indexadmin/listarpreguntas/",
        type: "get",
        dataType: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_preguntas')) {
                $('#tabla_preguntas').DataTable().destroy();
            }
            $('#tabla_preguntas tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>'; 
                fila += '<td>' + response[i]["fields"]['pregunta'] + '</td>';
                fila += '<td>' + response[i]["fields"]['respuesta'] + '</td>';             
                fila += '<td><button type = "button" class="status-tb-btn rounded-circle btn-primary me-4"';
                fila += ' onclick = "abrir_modal_edicion(\'/indexadmin/actualizarpreguntas/' + response[i]['pk'] + '/\');"><i class="fas fa-pencil"></i></button>';
                fila += '<button type = "button" class="status-tb-btn rounded-circle btn-danger" ';
                fila += 'onclick = "abrir_modal_eliminacion(\'/indexadmin/eliminarpreguntas/' + response[i]['pk'] + '/\');"><i class="fas fa-trash-alt"></i></buttton></td>';
                fila += '</tr>';
                $('#tabla_preguntas tbody').append(fila);
            }
            $('#tabla_preguntas').DataTable({
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
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoPreguntas();
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
    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoPreguntas();
            cerrar_modal_edicion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBoton();
        }
    });
}




function eliminar(pk) {
    $.ajax({
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        url: '/indexadmin/eliminarpreguntas/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoPreguntas();
            cerrar_modal_eliminacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
        }
    });
}





$(document).ready(function () {
    listadoPreguntas();
    console.log(listadoPreguntas());
});

