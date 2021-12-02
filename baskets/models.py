from django.db import models
from django.utils.functional import cached_property

from products.models import Product
from users.models import User


# class added in lesson4
class BasketQuerySet(models.QuerySet):

    def delete(self):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    # line added in lesson4
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    @property
    def baskets(self):
        return Basket.objects.filter(user=self.user)

    def total_sum(self):
        return sum(basket.sum() for basket in self.baskets)

    def total_quantity(self):
        return sum(basket.quantity for basket in self.baskets)

    # method from 7 lesson
    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    # method from 3 lesson on level 2
    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    # method added in lesson4
    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(Basket, self).delete()

    # method added in lesson4
    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(Basket, self).save(*args, **kwargs)

    # methods added in lesson7
    @property
    def product_cost(self):
        return self.product.price * self.quantity
    
    def get_total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))
