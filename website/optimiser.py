import math
def optimizer(store: dict, quantities: dict[str, float]) -> list:
    estimated_price = 0
     list_of_items = []
        for item in store:
            value = {}
            for each_item in store[item]:
                for t, q in each_item:
                    if t == "unit" and q == "price":
                        value[each_item] = each_item[q] * quantities[item] / each_item[t]
                        break
            x = [value[each] for each in store[item]]
            r = min(x)
            for each in store[item]:
                if value[each] == r:
                    for y in each:
                        if y =="Name":
                            name = each[y]
            estimated_price += r
            list_of_items += [{'name':name, 'price':math.round(r,2)}]
             return  [estimated_price]+list_of_items
