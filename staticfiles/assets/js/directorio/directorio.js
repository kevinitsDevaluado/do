var $ =jQuery.noConflict();
function listadoDirectorio() {
    $.ajax({
        url: "/indexadmin/listardirectorio/",
        type: "get",
        dataType: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_directorio')) {
                $('#tabla_directorio').DataTable().destroy();
            }
            $('#tabla_directorio tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>';
                fila += '<td>' + response[i]["fields"]['fk_id_dir'] + '</td>';       
                fila += '<td>' + response[i]["fields"]['nombre_dir'] + '</td>';
                fila += '<td>' + response[i]["fields"]['descripcion_dir'] + '</td>';
               
                fila += '<td> <a href="/media/'+response[i]["fields"]['archivo_dir']+'" class="text-dark text-center" target="_blank_">archivo  </a>'+ '</td>';
                fila += '<td>' + response[i]["fields"]['fechacreacion_dir'] + '</td>';              
                fila += '<td><button type = "button" class="status-tb-btn btn-primary me-4"';
                fila += ' onclick = "abrir_modal_edicion(\'/indexadmin/editardirectorio/' + response[i]['pk'] + '/\');"><i class="fa-solid fa-arrows-rotate"></i></button>';
                fila += '<button type = "button" class="status-tb-btn btn-danger" ';
                fila += 'onclick = "abrir_modal_eliminacion(\'/indexadmin/eliminardirectorio/' + response[i]['pk'] + '/\');"><i class="fa-solid fa-trash"></i></buttton></td>';
                fila += '</tr>';
                $('#tabla_directorio tbody').append(fila);
            }
            $('#tabla_directorio').DataTable({
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
            listadoDirectorio();
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
            listadoDirectorio();
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
        url: '/indexadmin/eliminardirectorio/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoDirectorio();
            cerrar_modal_eliminacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
        }
    });
}

$(document).ready(function () {
    listadoDirectorio();
  
});
