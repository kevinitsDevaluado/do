var $ =jQuery.noConflict();
function listadoInstitucion(){

    $.ajax({
        url:"/indexadmin/listarinstitucion/",
        type: "get",
        dataType: "json",
        success: function(response){
            if($.fn.DataTable.isDataTable('#tabla_interfaz')){
                $('#tabla_interfaz').DataTable().destroy();
            }
            $('#tabla_interfaz tbody').html("");
            for(let i = 0; i < response.length; i++){
                let fila = '<tr>';
                fila += '<td>' + (i+1) + '</td>';//Concatenacion 
                fila += '<td>' + response[i]["fields"]["introduccion"] + '</td>';
                fila += '<td>' + response[i]["fields"]["mision"] + '</td>';
                fila += '<td>' + response[i]["fields"]["vision"] + '</td>';
                fila += '<td>' + response[i]["fields"]["resenia"] + '</td>';
                fila += '<td> <button type = "button" class="status-tb-btn rounded-circle btn-primary me-4"';
                fila += 'onclick="abrir_modal_edicion(\'/indexadmin/actualizarinstitucion/'+response[i]['pk']+'/\');"><i class="fas fa-pencil"></i></button></td>';

                fila += '</tr>';
                $('#tabla_interfaz tbody').append(fila);  
            }
            $('#tabla_interfaz').DataTable({
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
            listadoInstitucion();
            cerrar_modal_creacion();
            
            location.reload();
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
            listadoInstitucion();
            cerrar_modal_edicion();
        },
        error: function(error){
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBoton();
        }        
    });
}



$(document).ready(function (){
    listadoInstitucion();
});




