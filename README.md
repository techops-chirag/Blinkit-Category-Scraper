# Blinkit-Category-Scraper 🛒
A Python-based scraper that collects product data from BlinkIt using public APIs, based on user location and category inputs. Outputs a clean CSV file with all relevant product metadata for analysis or cataloging. Built for assessment purposes.

This project scrapes subcategory product data from the BlinkIt website using their public APIs. The script extracts structured product data based on user location and selected categories.

## 📁 Files

- `blinkit_scraper.py` – Main scraping script
- `blinkit_locations.csv` – Input file containing lat-long pairs
- `blinkit_categories.csv` – Input file containing L1 and L2 categories
- `blinkit_scraped_output.csv` – Final scraped data in CSV format

## 📌 Data Fields (as per schema)

- `date`
- `l1_category`, `l1_category_id`
- `l2_category`, `l2_category_id`
- `store_id`, `variant_id`, `variant_name`
- `group_id`, `selling_price`, `mrp`
- `in_stock`, `inventory`, `is_sponsored`
- `image_url`, `brand_id`, `brand`

## 🚀 How to Run

```bash
pip install requests pandas tqdm
python blinkit_scraper.py
