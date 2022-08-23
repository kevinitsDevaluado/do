var $ =jQuery.noConflict();
function listadoGaleria(){
    $.ajax({
        url:"/indexadmin/listargaleria/",
        type: "get",
        dataType: "json",
        success: function(response){
            if($.fn.DataTable.isDataTable('#tabla_galeria')){
                $('#tabla_galeria').DataTable().destroy();
            }
            $('#tabla_galeria tbody').html("");
            for(let i = 0; i < response.length; i++){
                let fila = '<tr>';
                fila += '<td>' + (i+1) + '</td>';//Concatenacion 
                fila += '<td>' + response[i]["fields"]["titulo_gal"] + '</td>';
                fila += '<td>' + response[i]["fields"]["descripcion_gal"] + '</td>';
                fila += '<td> <img src="/media/'+response[i]["fields"]["imagen_gal"]+'" class="img-fluid d-block mx-auto" style="width: 50px; height: 50px;"><br></td>';
                
                if (response[i]["fields"]["url_gal"] === null){
                    fila += '<td>No asignado</td>';
                }else{
                    fila += '<td>' + response[i]["fields"]["url_gal"] + '</td>';       
                } 

                if (response[i]["fields"]["estado_gal"] === true){
                    fila += '<td>Activo</td>';
                }else{
                    fila += '<td>Desactivado</td>';       
                } 

                fila += '<td> <button type = "button" class="status-tb-btn rounded-circle btn-primary me-4"';
                fila += 'onclick="abrir_modal_edicion(\'/indexadmin/editargaleria/'+response[i]['pk']+'/\');"><i class="fas fa-pencil"></i></button>';
                fila += '<button type = "button" class="status-tb-btn rounded-circle btn-danger" ';
                fila += 'onclick="abrir_modal_eliminacion(\'/indexadmin/eliminargaleria/'+response[i]['pk']+'/\');"><i class="fas fa-trash-alt"></i></button></td>';

                fila += '</tr>';
                $('#tabla_galeria tbody').append(fila);  
            }
            $('#tabla_galeria').DataTable({
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
            listadoGaleria();
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
            listadoGaleria();
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
        url: '/indexadmin/eliminargaleria/'+pk+'/',
        type: 'post',
        success: function(response){
            notificacionSuccess(response.mensaje);
            listadoGaleria();
            cerrar_modal_eliminacion();
        },
        error: function(error){
            notificacionError(error.responseJSON.mensaje);
        }        
    });
}

$(document).ready(function (){
    listadoGaleria();
});

