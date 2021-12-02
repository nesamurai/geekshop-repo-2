from django.forms import ModelForm, CharField

from orders.models import Order, OrderItem
from products.models import Product


class OrderForm(ModelForm):
    class Meta:
        model = Order
        # fields = ['created', 'updated', 'status', 'is_active']
        exclude = ['user',]

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class OrderItemForm(ModelForm):
    price = CharField(label='цена', required=False)
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity']

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        # line from 5 lesson
        self.fields['product'].queryset = Product.get_items()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
