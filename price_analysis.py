def analyse_price(data_json):
    price_dict = {}
    total_price = 0
    highest_price = 0
    lowest_price = 9999999

    for product in data_json:

        price = float(product["Price"])

        total_price += price

        if price > highest_price:
            highest_price = price

        if price < lowest_price:
            lowest_price = price

    average_price = total_price / len(data_json)

    price_dict["Average Price"] = f"{round(average_price, 2):.2f}"
    price_dict["Highest Price"] = f"{round(highest_price, 2):.2f}"
    price_dict["Lowest Price"] = f"{round(lowest_price, 2):.2f}"

    print(price_dict)
    return price_dict
