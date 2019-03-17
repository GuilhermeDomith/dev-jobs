$(document).ready(() => {
    $(window).resize(function(){
        alterar_botao();
    });

    alterar_botao();

    function alterar_botao(){
        let btn = $('.search-jobs + button');

        if ($(window).width() <= 600) {  
            btn.html('<i class="material-icons left">search</i>');
        }else{
            btn.html('<i class="material-icons left">search</i> Buscar');
        }     
    }
 
});
