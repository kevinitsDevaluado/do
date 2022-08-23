var $ =jQuery.noConflict();
function ListadoVistaAsamblea() {
    $.ajax({
        url: "/indexadmin/listarcontadorvistaasamblea/",
        type: "get",
        dataType: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_contador_asamblea')) {
                $('#tabla_contador_asamblea').DataTable().destroy();
            }
            $('#tabla_contador_asamblea tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>'; 
                fila += '<td>' + response[i]["fields"]['fk_id_cont'] + '</td>';   
                fila += '<td>' + response[i]["fields"]['asamblea_cont'] + '</td>';   
                fila += '<td><button type = "button" class="status-tb-btn rounded-circle btn-danger" ';
                fila += 'onclick = "abrir_modal_eliminacion(\'/indexadmin/eliminarcontadorvistaasamblea/' + response[i]['pk'] + '/\');"><i class="fas fa-trash-alt"></i></buttton></td>';
                fila += '</tr>';
                $('#tabla_contador_asamblea tbody').append(fila);
            }
            $('#tabla_contador_asamblea').DataTable({
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
            ListadoVistaAsamblea();
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
        url: '/indexadmin/eliminarcontadorvistaasamblea/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            ListadoVistaAsamblea();
            cerrar_modal_eliminacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
        }
    });
}



$(document).ready(function () {
    ListadoVistaAsamblea();
   
});


