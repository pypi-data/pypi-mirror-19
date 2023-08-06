function(modal) {
    modal.respond('offerChosen', {{ offer_json|safe }});
    modal.close();
}
