def analyse_price(data_json):
    price_dict = {}
    total_price = 0
    highest_price = 0
    lowest_price = 9999999

    for product in data_json:

        if not product["Price"]:
            price = 0
        else:
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

analyse_price([{'Price': '', 'Product Type': 'Dress', 'Color': 'Black', 'url': 'https://www.lovebonito.com/sg/abilene-square-neck-knit-dress.html'}, {'Price': '', 'Product Type': 'Shirt Dress', 'Color': 'Lime', 'url': 'https://www.lovebonito.com/sg/anniston-puff-sleeve-shirt-dress.html'}, {'Price': '49.00', 'Product Type': 'Dress', 'Color': 'White', 'url': 'https://www.lovebonito.com/sg/dacia-drop-waist-ruffle-dress.html'}])