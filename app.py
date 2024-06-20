

import requests
from bs4 import BeautifulSoup

products_to_track = [
    {
        "product_url":  "https://www.amazon.in/dp/B0CS6JW9YQ/ref=syn_sd_onsite_desktop_0?ie=UTF8&pd_rd_plhdr=t&aref=PfNEU5HSMv&th=1",
        "name": "Samsung M31",
        "target_price": 1600000
    },
    {
        "product_url": "https://www.amazon.in/Test-Exclusive-668/dp/B07HGH88GL/ref=psdc_1805560031_t1_B07HGJKDQL",
        "name": "Samsung M21 6GB 128RAM",
        "target_price": 16000
    },
    {
        "product_url": "https://www.amazon.in/Test-Exclusive-553/dp/B0784D7NFQ/ref=sr_1_12?crid=2RE70JAZ07V4M&dchild=1&keywords=redmi+note+9&qid=1599449618&s=electronics&sprefix=redmi+%2Celectronics%2C-1&sr=1-12",
        "name": "Redmi Note 9 Pro",
        "target_price": 17000
    }
]

def give_product_price(URL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check different possible elements for the price
    selectors = [
        {"class": "a-price-whole"},
        {"id": "priceblock_ourprice"},
        {"id": "priceblock_dealprice"},
        {"class": "a-offscreen"}  # sometimes the price is in an offscreen span
    ]
    
    product_price = None
    for selector in selectors:
        if "class" in selector:
            product_price = soup.find("span", class_=selector["class"])
        elif "id" in selector:
            product_price = soup.find("span", id=selector["id"])
        
        if product_price:
            break

    if product_price is None:
        return None

    # Extract the text content of the price element
    price_text = product_price.get_text(strip=True)

    # Combine with any fractional part if present
    product_price_fraction = soup.find("span", class_="a-price-fraction")
    if product_price_fraction:
        price_text += product_price_fraction.get_text(strip=True)

    return price_text

result_file = open('my_result_file.txt', 'w')

try:
    for every_product in products_to_track:
        product_price_returned = give_product_price(every_product.get("product_url"))
        if product_price_returned is None:
            print(f"Price not found for {every_product.get('name')}")
            continue

        print(product_price_returned + " - " + every_product.get("name"))

        # Assuming the price returned is in the format '₹12,345.00'
        my_product_price = price_text.replace(',', '').replace('₹', '').strip()
        my_product_price = int(float(my_product_price))

        print(my_product_price)
        if my_product_price < every_product.get("target_price"):
            print("Available at your required price")
            result_file.write(every_product.get(
                "name") + ' -  \t' + ' Available at Target Price ' + ' Current Price - ' + str(my_product_price) + '\n')
        else:
            print("Still at current price")

finally:
    result_file.close()
