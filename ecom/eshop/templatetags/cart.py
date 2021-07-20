from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(x, carts):
    keys = carts.keys()
    for id in keys:
        if int(id) == x.id:
            return True
    return False;


@register.filter(name='cart_quantity')
def cart_quantity(x , carts):
    keys = carts.keys()
    for id in keys:
        if int(id) == x.id:
            return carts.get(id)
    return 0;


@register.filter(name='price_total')
def price_total(product  , cart):
    return product.price * cart_quantity(product , cart)


@register.filter(name='total_cart_price')
def total_cart_price(products , cart):
    sum = 0 ;
    for p in products:
        sum += price_total(p , cart)

    return sum
