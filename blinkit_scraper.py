import requests
import pandas as pd
from tqdm import tqdm
import time

# Loaded the CSV files
locations_df = pd.read_csv("blinkit_locations.csv")
categories_df = pd.read_csv("blinkit_categories.csv")

# BlinkIt API Endpoint (discovered via browser inspection)
API_URL = "https://www.blinkit.com/api/v1/search/sub-category-products"

# a list to store scraped results
results = []

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

for _, loc in tqdm(locations_df.iterrows(), total=len(locations_df), desc="Locations"):
    lat, lng = loc["latitude"], loc["longitude"]

    for _, cat in categories_df.iterrows():
        l1_category, l2_category = cat["l1_category"], cat["l2_category"]
        l1_id, l2_id = cat["l1_category_id"], cat["l2_category_id"]

        params = {
            "lat": lat,
            "lng": lng,
            "sub_category_id": l2_id
        }

        try:
            response = requests.get(API_URL, params=params, headers=headers)
            if response.status_code != 200:
                continue

            data = response.json()
            store_id = data.get("store", {}).get("store_id", None)
            products = data.get("products", [])

            for product in products:
                results.append({
                    "date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "l1_category": l1_category,
                    "l1_category_id": l1_id,
                    "l2_category": l2_category,
                    "l2_category_id": l2_id,
                    "store_id": store_id,
                    "variant_id": product.get("id"),
                    "variant_name": product.get("name"),
                    "group_id": product.get("group_id"),
                    "selling_price": product.get("price", {}).get("value"),
                    "mrp": product.get("price", {}).get("mrp"),
                    "in_stock": product.get("in_stock"),
                    "inventory": product.get("inventory"),
                    "is_sponsored": product.get("is_sponsored"),
                    "image_url": product.get("image_url"),
                    "brand_id": product.get("brand", {}).get("id"),
                    "brand": product.get("brand", {}).get("name")
                })

            time.sleep(0.2)  # to avoid rate-limiting

        except Exception as e:
            print(f"Error scraping {l2_category_id} at ({lat}, {lng}):", e)

# saved to CSV
output_df = pd.DataFrame(results)
output_df.to_csv("blinkit_scraped_output.csv", index=False)
print("Scraping complete!")
