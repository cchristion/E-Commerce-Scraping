# 20220914
# Importing libraries.
import os
import re
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Todays Date
date = str(datetime.today().strftime("%Y%m%d"))
print(date)

# Main Flipkart link.
main_link = "https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&as-pos=2&as-type=RECENT&as-searchtext=l&requestId=51477943-7e38-4ad9-b2b0-60196e384224&suggestionId=laptop%7CLaptops&p%5B%5D=facets.price_range%255B%255D%3DRs.%2B20000%2B-%2BRs.%2B40000&p%5B%5D=facets.price_range%255B%255D%3DRs.%2B40000%2B-%2BRs.%2B50000&p%5B%5D=facets.price_range%255B%255D%3DRs.%2B50000%2B-%2BRs.%2B60000&p%5B%5D=facets.screen_size%255B%255D%3D15%2Binch%2B-%2B15.9%2Binch&p%5B%5D=facets.screen_size%255B%255D%3D16%2Binch%2B-%2B17.9%2Binch&p%5B%5D=facets.screen_size%255B%255D%3DAbove%2B20%2Binch&p%5B%5D=facets.screen_size%255B%255D%3D14%2Binch%2B-%2B14.9%2Binch&sort=price_asc&pageUID=1663050251437"

# Initizing variables.
i, total_page_no = 1, 1
df = pd.DataFrame(
    {
        "Link": [],
        "Name": [],
        "Original Price": [],
        "Discount": [],
        "Price": [],
        "Rating": [],
        "CPU": [],
        "GPU": [],
        "RAM": [],
        "HDD": [],
        "SSD": [],
        "Battery": [],
        "Screen Resolution": [],
        "Screen Type": [],
    }
)

# To find Total Number of Pages
while True:
    loop_link = main_link + "&page=" + str(total_page_no)
    link_data = requests.get(loop_link).text
    data = BeautifulSoup(link_data, "lxml")
    last_page_no = int(data.find_all("a", {"class": "ge-49M"})[-1].text)
    # last_page_no = data.find_all('a',{"class":"ge-49M"})
    print(last_page_no)
    print(f"Page found so far: {last_page_no}")
    if last_page_no > total_page_no:
        total_page_no = last_page_no
    else:
        print(f"Total of {total_page_no} pages found.\n")
        break

# Looping through each page.
for page_no in range(1, total_page_no + 1):

    page_no_link = main_link + "&page=" + str(page_no)
    data = requests.get(page_no_link).text
    page_no_data = BeautifulSoup(data, "lxml")

    # Looping through each Product.
    for invalid_link in page_no_data.find_all("a", {"class": "_1fQZEK"}):

        print(f"Going through {i} Product")
        link = "https://www.flipkart.com" + invalid_link.get("href")
        data = requests.get(link).text
        product_page_data = BeautifulSoup(data, "lxml")

        # Finding Name, Original Price, Discount, Price, Rating.
        name = product_page_data.find("span", {"class": "B_NuCI"})
        if name is None:
            continue

        original_price = product_page_data.find("div", {"class": "_3I9_wc _2p6lqe"})
        if original_price is None:
            continue
        else:
            original_price = int(re.sub(r"\D", "", original_price.text))

        discount = product_page_data.find("div", {"class": "_3Ay6Sb _31Dcoz"})
        if discount is None:
            continue
        else:
            discount = int(re.sub(r"\D", "", discount.text))

        price = product_page_data.find("div", {"class": "_30jeq3 _16Jk6d"})
        if price is None:
            continue
        else:
            price = int(re.sub(r"\D", "", price.text))

        rating = product_page_data.find("div", {"class": "_3LWZlK"})
        if rating is None:
            continue

        # Finding CPU, GPU, RAM, HDD, SSD, Battery, Screen Resolution, Screen Type.
        CPU, GPU, RAM, HDD, SSD, Battery, Screen_Resolution, Screen_Type = (
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )

        for table_data in product_page_data.find_all("tr", {"class": "_1s_Smc row"}):

            table_name = table_data.find("td", {"class": "_1hKmbr col col-3-12"}).text

            if table_name == "Processor Variant":
                CPU = table_data.find("li", {"class": "_21lJbe"}).text
                # print(f"Name: {table_name}\tValue: {Processor_Variant}")

            elif table_name == "Graphic Processor":
                GPU = table_data.find("li", {"class": "_21lJbe"}).text
                # print(f"Name: {table_name}\tValue: {Graphic_Processor}")

            elif table_name == "RAM":
                RAM = table_data.find("li", {"class": "_21lJbe"}).text
                # print(f"Name: {table_name}\tValue: {RAM}")

            elif table_name == "HDD Capacity":
                HDD = table_data.find("li", {"class": "_21lJbe"}).text
                # print(f"Name: {table_name}\tValue: {HDD}")

            elif table_name == "SSD Capacity":
                SSD = table_data.find("li", {"class": "_21lJbe"}).text
                # print(f"Name: {table_name}\tValue: {SSD}")

            elif table_name == "Battery Backup":
                Battery = table_data.find("li", {"class": "_21lJbe"}).text
                # print(f"Name: {table_name}\tValue: {Battery}")

            elif table_name == "Screen Resolution":
                Screen_Resolution = table_data.find("li", {"class": "_21lJbe"}).text
                # print(f"Name: {table_name}\tValue: {Screen_Resolution}")

            elif table_name == "Screen Type":
                Screen_Type = table_data.find("li", {"class": "_21lJbe"}).text
                # print(f"Name: {table_name}\tValue: {Screen_Type}")

        i += 1
        # Appending data to Dataframe.
        df.loc[len(df.index)] = [
            link,
            name.text,
            original_price,
            discount,
            price,
            rating.text,
            CPU,
            GPU,
            RAM,
            HDD,
            SSD,
            Battery,
            Screen_Resolution,
            Screen_Type,
        ]

        continue
    continue
# print(df)

# Writing DataFrame to xlsx sheet.
if os.path.exists(f"Laptop list - {date}.xlsx"):
    os.remove(f"Laptop list - {date}.xlsx")
df.to_excel(f"Laptop list - {date}.xlsx")
