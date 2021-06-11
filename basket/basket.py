from decimal import Decimal

from django.conf import settings

from fresher.models import Recipe


class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, recipe, qty):
        """
        Adding and updating the users basket session data
        """
        recipe_id = str(recipe.id)

        if recipe_id in self.basket:
            self.basket[recipe_id]['qty'] = qty
        else:
            self.basket[recipe_id] = {'price': str(recipe.price), 'qty': qty}

        self.save()

    def __iter__(self):
        """
        Collect the recipe_id in the session data to query the database
        and return recipes
        """
        recipe_ids = self.basket.keys()
        recipes = Recipe.recipes.filter(id__in=recipe_ids)
        basket = self.basket.copy()

        for recipe in recipes:
            basket[str(recipe.id)]['recipe'] = recipe

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())

    def update(self, recipe, qty):
        """
        Update values in session data
        """
        recipe_id = str(recipe)
        if recipe_id in self.basket:
            self.basket[recipe_id]['qty'] = qty
        self.save()

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def get_total_price(self):

        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(3.00)

        total = subtotal + Decimal(shipping)
        return total

    def delete(self, recipe):
        """
        Delete item from session data
        """
        recipe_id = str(recipe)

        if recipe_id in self.basket:
            del self.basket[recipe_id]
            self.save()

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
