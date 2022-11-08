import math

def cheapest_dict(possible_items: list[dict], quantity: int):
    min_price = math.inf
    min_item = None
    for item in possible_items:
        if item['price'] < min_price:
            min_item = item
    if min_item is not None:
        min_item['price'] *= quantity
    return min_item, min_price

def cheapest_list(possible_lists: dict[list[dict]], quantity_map: dict[str, int]):
    min_list = []
    min_total = 0
    for item in possible_lists:
        min_item, min_price = cheapest_dict(possible_lists[item], quantity_map[item])
        min_list = min_list + [min_item]
        min_total += min_price
    return min_list, min_total