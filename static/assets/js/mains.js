 //============DATATABLES=========================
 $(document).ready( function () {
    $('#example').DataTable({
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
        responsive: true,

        
    });
} );

var $ =jQuery.noConflict();
function abrir_modal_eliminacion(url){
    $('#eliminar').load(url, function(){
        $(this).modal('show');
    });
}

function abrir_modal_creacion(url){
    $('#crear').load(url, function(){
        $(this).modal('show');
    });
}

function cerrar_modal_creacion(url){
    $('#crear').modal('hide');
}

function abrir_modal_edicion(url){
    $('#editar').load(url, function(){
        $(this).modal('show');
    });
}

function cerrar_modal_edicion(url){
    $('#editar').modal('hide');
}


function abrir_modal_eliminacion(url){
    $('#eliminar').load(url, function(){
        $(this).modal('show');
    });
}

function cerrar_modal_eliminacion(url){
    $('#eliminar').modal('hide');
}

function activarBoton(){
    if($('#boton_creacion').prop('disabled')){
        $('#boton_creacion').prop('disabled', false);

    }else{
        $('#boton_creacion').prop('disabled', true);
    }
}


function mostrarErroresCreacion(errores){
	//Limpiamos los errores
    
	$("div.alert").remove();

       //Mostramos los errores actualizados
	for(var error in errores.responseJSON.error){
       	$('#form_creacion #'+error).after('<div class="alert alert-danger alert-dismissible fade show mt-2 mb-2" role="alert"><strong>'+errores.responseJSON.error[error]+'</strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
	}


}

function mostrarErroresEdicion(errores){
    //Limpiamos los errores
    
	$("div.alert").remove();

    //Mostramos los errores actualizados
    for(var error in errores.responseJSON.error){
            $('#form_edicion #'+error).after('<div class="alert alert-danger alert-dismissible fade show mt-2 mb-2" role="alert"><strong>'+errores.responseJSON.error[error]+'</strong> <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
    }
}

function notificacionError(mensaje){
    Swal.fire({
        title: 'Error!',
        text: mensaje,
        icon: 'error',
        confirmButtonText: 'OK'
    })
}

function notificacionSuccess(mensaje){
    Swal.fire({
        title: 'Buen trabajo!',
        text: mensaje,
        icon: 'success',
        confirmButtonText: 'Genial!!'
    })


}








