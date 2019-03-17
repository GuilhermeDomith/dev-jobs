$(document).ready(() => {

    var competencias = {}

    /*Troca de tags entre os quadros de competência */
    function closetag(e) {
        let tag = $(this).parent();
        if (tag.attr('data-add') == 0)
            adicionarCompetencia(tag)
        else
            removerCompetencia(tag)
    }

    $('.close').on('click', closetag)

    function adicionarCompetencia(element) {
        /*let tag = element.clone()
        tag.children('i').html('close')
        tag.children('i').on('click', closetag)
        tag.children('input').removeAttr('disabled')
        tag.attr('data-add', 1)*/
        let texto = element.attr('data-value')
        let tag = criarTag(texto, 1);

        element.remove()
        competencias[texto] = 0
        $('#competencias').append(tag);
    }

    function removerCompetencia(element) {
        /*let tag = element.clone()
        tag.children('i').html('check')
        tag.children('i').on('click', closetag)
        tag.children('input').attr('disabled', 'true')
        tag.attr('data-add', 0)*/
        let texto = element.attr('data-value')
        let tag = criarTag(texto, 0);

        element.remove()
        delete competencias[texto]
        $('#nao-competencias').append(tag);
    }

    /** Cria uma tag que descreve uma competência.
     * texto - A descrição da tag
     * iscomp - Deve ser 1 se é uma competência e 0 se não for
     */
    function criarTag(texto, iscomp){
        let element = $('<div class="chip" data-add="'+iscomp+'" data-value="'+texto+'">'
                        + texto
                        + '<i class="close material-icons">'+ ((iscomp)? 'close' : 'check') +'</i>'
                        + '<input '+ ((iscomp)? '' : 'disabled') +' type="hidden" name="comp" value="'+texto+'">'
                    +'</div>');

        element.children('i').on('click', closetag);
        return element;
    }

    /*Filtro das competências*/
    $('#filtro').on('keyup', function(e){
        this.value

        $.ajax({
            method: "POST",
            url: "filter-tag/",
            data: { filtro: this.value }
          })
          .done(function( msg ) {

            $('#nao-competencias').children().remove();
            console.log(competencias)
            msg['tags'].forEach(function(texto, i){
                if(competencias[texto] == undefined)
                    $('#nao-competencias').append(criarTag(texto, 0))
            });
            console.log(competencias)
        });
    });

});


