var $ =jQuery.noConflict();
function listadoDocumentos() {
    $.ajax({
        url: "/archivero/listardocumentos/",
        type: "get",
        dataType: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_documentos')) {
                $('#tabla_documentos').DataTable().destroy();
            }
            $('#tabla_documentos tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>';
                fila += '<td>' + response[i]["fields"]['fechacreacion_doc'] + '</td>'; 
                fila += '<td>' + response[i]["fields"]['fk_id_atem'] + '</td>';       
                fila += '<td> <a href="/media/'+ response[i]["fields"]['documento_doc']+'" class="text-dark text-center" target="_blank_">'+ response[i]["fields"]['documento_doc']+'</a>'+ '</td>';             
                fila += '<td  class="d-none">' + response[i]["fields"]['contenido_doc'] + '</td>'; 
                fila += '<td> <a href="/media/'+response[i]["fields"]['documento_doc']+'" class="status-tb-btn rounded-circle btn-primary me-4" target="_blank_"><i class="fas fa-eye"></i></a>';
                fila += '<button type = "button" class="status-tb-btn rounded-circle btn-primary me-4"';
                fila += ' onclick = "abrir_modal_edicion(\'/archivero/actualizardocumentos/' + response[i]['pk'] + '/\');"><i class="fas fa-pencil"></i></button>';
                fila += '<button type = "button" class="status-tb-btn rounded-circle btn-danger" ';
                fila += 'onclick = "abrir_modal_eliminacion(\'/archivero/eliminardocumentos/' + response[i]['pk'] + '/\');"><i class="fas fa-trash-alt"></i></buttton></td>';
                fila += '</tr>';
                $('#tabla_documentos tbody').append(fila);
            }
            $('#tabla_documentos').DataTable({
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
            listadoDocumentos();
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
            listadoDocumentos();
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
        url: '/archivero/eliminardocumentos/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoDocumentos();
            cerrar_modal_eliminacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
        }
    });
}

$(document).ready(function () {
    listadoDocumentos();
    console.log(listadoDocumentos());
  
});
