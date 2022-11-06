def optimizer(store: dict, quantities: dict[str, float]) -> list:
    estimated_price = 0
    list_of_items = []
    for item in store:
        print(item)
        value = {}
        for each_item in store[item]:
            value[each_item['name']] = each_item['price'] * quantities[item] / 100
        x = [value[each['name']] for each in store[item]]
        r = min(x)
        for each in store[item]:
            if value[each['name']] == r:
                name = each['name']
        estimated_price += r
        list_of_items += [{'name':name, 'price':round(r,2)}]
    return  [estimated_price]+[list_of_items]
