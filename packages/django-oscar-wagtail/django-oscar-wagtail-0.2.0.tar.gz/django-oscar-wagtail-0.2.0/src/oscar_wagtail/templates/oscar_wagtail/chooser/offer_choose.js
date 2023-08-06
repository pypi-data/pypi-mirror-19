function initModal(modal) {

    var listingUrl = $('#offer-chooser-list', modal.body).data('url');

    function ajaxifyLinks(context) {
        $('a.offer-choice', modal.body).click(function() {
            modal.loadUrl(this.href);
            return false;
        });

        $('.pagination a', context).click(function() {
            var page = this.getAttribute('data-page');
            var q = $('form.offer-search input[name=q]', modal.body).val();
            setPage(page, q);
            return false;
        });
    }


    function search() {
        $.ajax({
            url: $('form.offer-search', modal.body).attr('action'),
            data: {q: $('#id_q').val()},
            dataType: 'html',
            success: function(data, status, xhr) {
                var response = eval('(' + data + ')');
                $(modal.body).html(response.html);
                if (response.onload) {
                    response.onload(self);
                }
                ajaxifyLinks($('#offer-results'));
            }
        });
        return false;
    }

    function setPage(page, q) {

        $.ajax({
            url: listingUrl,
            data: { p: page, q: q },
            dataType: 'html',
            success: function(data, status, xhr) {
                var response = eval('(' + data + ')');
                $(modal.body).html(response.html);

                if (response.onload) {
                    response.onload(self);
                }

                ajaxifyLinks($('#offer-chooser-list'));
            }
        });

        return false;
    }

    ajaxifyLinks(modal.body);

    $('form.offer-search', modal.body).submit(search);

}
