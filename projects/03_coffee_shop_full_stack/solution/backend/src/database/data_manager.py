"""
    data_manager.py
    -------

    This module contains the :class:`DrinkDataManager` class which is
    responsible for getting, creating, updating and deleting drink data.
"""

__author__ = "Filipe Bezerra de Sousa"

import json

from jsonpatch import JsonPatch

from .models import Drink


class DrinkDataManager:
    """Contains static methods that manages the Drink data set."""

    @staticmethod
    def list_drinks(long_representation=True):
        """Retrieve a list of ``Drink`` from the database.

        :param long_representation: If True the Drink must show a long form
         representation, a short otherwise.
        :return: A list of Drink.
        """
        drinks = [
            drink.long() if long_representation else drink.short()
            for drink in Drink.query.all()
        ]
        return drinks

    @staticmethod
    def create_drink(drink_dict):
        """Insert the ``Drink`` to the database.

        :param drink_dict: The dict with Drink attributes.
        :return: A list containing only the short form representation of the
         new Drink created.
        """
        new_drink = Drink(
            title=drink_dict.get("title"),
            recipe=json.dumps(drink_dict.get("recipe")),
        )
        new_drink.insert()
        return new_drink.short()

    @staticmethod
    def update_drink(drink_id, updates_dict):
        """Apply the updates to an existing ``drink_id`` to the database.

        :param drink_id: The id of the Drink.
        :param updates_dict: The dict containing the updates to the existing
         Drink.
        :return: A short form representation of the Drink updated.
        """
        drink = Drink.query.get_or_404(drink_id)

        if "recipe" in updates_dict:
            updates_dict["recipe"] = json.dumps(updates_dict["recipe"])

        drink_dict = drink.asdict(exclude_pk=True)
        patch_instance = JsonPatch.from_diff(drink_dict, updates_dict)
        new_drink_dict = patch_instance.apply(drink_dict)
        drink.fromdict(new_drink_dict)
        drink.update()
        return drink.short()

    @staticmethod
    def delete_drink(drink_id):
        """Delete the ``Drink`` from the database.

        :param drink_id: The id of the Drink.
        """
        drink = Drink.query.get_or_404(drink_id)
        drink.delete()
