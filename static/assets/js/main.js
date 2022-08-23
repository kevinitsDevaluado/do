//=================Sidebar parte izquierda

//sirve para hacer que la barra pequeña lateral del siebar cambie la clase de active a los demas <li>
$(document).on('click','#sidebar li', function(){
    $(this).addClass('active').siblings().removeClass('active')
});


//==============SIDEBAR MENU IZQUIERDO (LEFT) dp toggle==================================
//sirve para hacer la funcionalidad de menu desplegable con subitems
$('.sub-menu ul').hide();
$(".sub-menu a").click(function(){
    $(this).parent(".sub-menu").children("ul").slideToggle("100");
    $(this).find(".right").toggleClass("fa-caret-up fa-caret-down");
});

//==============SIDEBAR  toggle==================================
//sirve para hacer la funcionalidad de menu desplegable con subitems

$(document).ready(function(){
    $("#toogleSidebar").click(function(){
        $(".left-menu").toggleClass("hide");
        $(".content-wrapper").toggleClass("hide");
    });
});
