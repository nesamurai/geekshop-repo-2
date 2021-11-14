from django.forms import ModelForm

from orders.models import Order, OrderItem


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
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity']

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
