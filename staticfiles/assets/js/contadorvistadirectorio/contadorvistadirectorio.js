var $ =jQuery.noConflict();
function ListadoVistaDirectorio() {
    $.ajax({
        url: "/indexadmin/listarcontadorvistadirectorio/",
        type: "get",
        dataType: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_contador_directorio')) {
                $('#tabla_contador_directorio').DataTable().destroy();
            }
            $('#tabla_contador_directorio tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>'; 
                fila += '<td>' + response[i]["fields"]['fk_id_con'] + '</td>';   
                fila += '<td>' + response[i]["fields"]['directorio_con'] + '</td>';   
                fila += '<td><button type = "button" class="status-tb-btn btn-danger" ';
                fila += 'onclick = "abrir_modal_eliminacion(\'/indexadmin/eliminarcontadorvistadirectorio/' + response[i]['pk'] + '/\');"><i class="fa-solid fa-trash"></i></buttton></td>';
                fila += '</tr>';
                $('#tabla_contador_directorio tbody').append(fila);
            }
            $('#tabla_contador_directorio').DataTable({
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
            ListadoVistaDirectorio();
            cerrar_modal_creacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion(error);
            activarBoton();
        }
    });
}




function eliminar(pk) {
    $.ajax({
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        url: '/indexadmin/eliminarcontadorvistadirectorio/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            ListadoVistaDirectorio();
            cerrar_modal_eliminacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
        }
    });
}

$(document).ready(function () {
    ListadoVistaDirectorio();
   
});

