
function createOfferChooser(id, contentType) {
    var chooserElement = $('#' + id + '-chooser');
    var docTitle = chooserElement.find('.title');
    var input = $('#' + id);
    var editLink = chooserElement.find('.edit-link');

    $('.action-choose', chooserElement).click(function() {
        ModalWorkflow({
            url: window.chooserUrls.offerChooser,
            responses: {
                offerChosen: function(offerData) {
                    input.val(offerData.id);
                    docTitle.text(offerData.string);
                    chooserElement.removeClass('blank');
                    editLink.attr('href', offerData.edit_link);
                }
            }
        });
    });

    $('.action-clear', chooserElement).click(function() {
        input.val('');
        chooserElement.addClass('blank');
    });
}
