#!python3

import fileinput
import re
from collections import defaultdict
import sys

pattern = re.compile("(.*) \(contains (.*)\)")
recipes = []
for line in map(lambda x: x.strip(), fileinput.input()):
    ingredients, allergens = pattern.match(line).groups()
    ingredients = set(ingredients.split(" "))
    allergens = set(allergens.split(", "))
    print(ingredients, ":", allergens)
    recipes.append((ingredients, allergens))


all_allergen = set()
all_ingredients = set()
for ingredients, allergens in recipes:
    all_allergen = all_allergen.union(allergens)
    all_ingredients = all_ingredients.union(ingredients)

print("all_allergen", all_allergen)
print("all_ingredients", all_ingredients)

a_to_is = defaultdict(lambda: set(all_ingredients))
for ingredients, allergens in recipes:
    for allergen in allergens:
        a_to_is[allergen] = a_to_is[allergen].intersection(ingredients)

contains = {}
while a_to_is:
    print("posible match", a_to_is)
    allergen = None
    for allergen, ingredients in a_to_is.items():
        if len(ingredients) == 1:
            break
    if not allergen:
        raise ValueError("inconclusive")
    del a_to_is[allergen]
    ingredient = next(iter(ingredients))
    contains[ingredient] = allergen
    for ingredients in a_to_is.values():
        ingredients.discard(ingredient)

print("contains", contains)

nonallergen_ingredients = all_ingredients.difference(contains.keys())

print("nonallergen_ingredients", nonallergen_ingredients)

sum = 0
for ingredients, allergens in recipes:
    sum += len(ingredients.intersection(nonallergen_ingredients))

print(sum)
