var $ =jQuery.noConflict();
function listadoAnioMesTransparencia() {
    $.ajax({
        url: "/indexadmin/listaraniomestransparencia/",
        type: "get",
        dataType: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_anio_mes_transparencia')) {
                $('#tabla_anio_mes_transparencia').DataTable().destroy();
            }
            $('#tabla_anio_mes_transparencia tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>';
                fila += '<td>' + response[i]["fields"]['fk_id_car'] + '</td>';       
                fila += '<td>' + response[i]["fields"]['fk_id_sub'] + '</td>';          
                fila += '<td><button type = "button" class = "status-tb-btn btn-primary me-4"';
                fila += ' onclick = "abrir_modal_edicion(\'/indexadmin/editaraniomestransparencia/' + response[i]['pk'] + '/\');"><i class="fa-solid fa-arrows-rotate"></i></button>';
                fila += '<button type = "button" class="status-tb-btn btn-danger" ';
                fila += 'onclick = "abrir_modal_eliminacion(\'/indexadmin/eliminaraniomestransparencia/' + response[i]['pk'] + '/\');"><i class="fa-solid fa-trash"></i></buttton></td>';
                fila += '</tr>';
                $('#tabla_anio_mes_transparencia tbody').append(fila);
            }
            $('#tabla_anio_mes_transparencia').DataTable({
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
            listadoAnioMesTransparencia();
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
            listadoAnioMesTransparencia();
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
        url: '/indexadmin/eliminaraniomestransparencia/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoAnioMesTransparencia();
            cerrar_modal_eliminacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
        }
    });
}


$(document).ready(function () {
    listadoAnioMesTransparencia();
});


