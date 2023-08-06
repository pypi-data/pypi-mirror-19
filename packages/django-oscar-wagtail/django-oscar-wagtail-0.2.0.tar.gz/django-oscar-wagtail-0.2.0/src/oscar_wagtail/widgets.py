import json

from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_model
from wagtail.wagtailadmin.widgets import AdminChooser


class AdminProductChooser(AdminChooser):
    target_content_type = None
    choose_one_text = _('Choose a product')
    choose_another_text = _('Choose another product')
    link_to_chosen_text = _('Edit this product')

    def __init__(self, **kwargs):
        super(AdminProductChooser, self).__init__(**kwargs)
        Product = get_model('catalogue', 'Product')
        self.target_content_type = ContentType.objects.get_for_model(Product)

    def render_html(self, name, value, attrs):
        model_class = self.target_content_type.model_class()
        instance, value = self.get_instance_and_id(model_class, value)

        original_field_html = super(AdminProductChooser, self).render_html(
            name, value, attrs)

        return render_to_string("oscar_wagtail/widgets/product_chooser.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'product': instance,
        })

    def render_js_init(self, id_, name, value):
        return "createProductChooser({id});".format(id=json.dumps(id_))


class AdminOfferChooser(AdminChooser):
    target_content_type = None
    choose_one_text = _('Choose an offer')
    choose_another_text = _('Choose another offer')
    link_to_chosen_text = _('Edit this offer')

    def __init__(self, **kwargs):
        super(AdminOfferChooser, self).__init__(**kwargs)
        Offer = get_model('offer', 'ConditionalOffer')
        self.target_content_type = ContentType.objects.get_for_model(Offer)

    def render_html(self, name, value, attrs):
        model_class = self.target_content_type.model_class()
        instance, value = self.get_instance_and_id(model_class, value)

        original_field_html = super(AdminOfferChooser, self).render_html(
            name, value, attrs)

        return render_to_string("oscar_wagtail/widgets/offer_chooser.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'offer': instance,
        })

    def render_js_init(self, id_, name, value):
        return "createOfferChooser({id});".format(id=json.dumps(id_))
