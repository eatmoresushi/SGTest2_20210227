import re

product_count_text = "381 Products found"
product_count_int = int(re.sub("[^0-9]", "", product_count_text))
