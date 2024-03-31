import change_me
import pandas as pd
from PIL import Image
import sys
import numpy as np
import os
import json

# Load data
df = pd.read_excel(change_me.excel_file)

# Makes all characters lowercase.
def lowercase_except_numbers(cell):
    if isinstance(cell, str):
        return ''.join(c.lower() if not c.isdigit() else c for c in cell)
    return cell

# Shortens titles to 80 characters and capitalizes words separated by spaces.
def shorten_and_capitalize_title(title):
    words = title.split()
    new_words = []
    length = 0

    for word in words:
        if length + len(word) > 80:
            break
        length += len(word) + 1 
        new_word = word[0].upper() + word[1:].lower()
        new_words.append(new_word)

    return ' '.join(new_words)

# Updates size formatting to match eBay's.
def update_size(size):
    size = str(size)
    size_list = size.split(", ")
    size_list = [size.strip() for size in size_list]
    
    US_size_dict = {"extra extra small": "XXS", "extra small": "XS", "small": "S", "medium": "M", "large": "L", "extra large": "XL", "extra extra large": "XXL"}
    updated_size_list = [US_size_dict.get(size.strip(), size) for size in size_list]
    
    return ", ".join(updated_size_list)

# Updates the condition description.
def update_condition_description(condition_description, condition):
    if condition_description == "none" and condition == "pre-owned":
        return change_me.default
 
    elif condition_description == "none" and "new" in condition:
        return condition.capitalize()

    elif condition_description != "none":
        return condition_description.capitalize()
    
    else:
        return condition_description

# Adds the shipping price.
def add_shipping_price(df, item_price_col, shipping_policy_col, weight_col, final_price_col='final_price', shipping_price_col='shipping_price'):
    def get_shipping_price(shipping, weight):
        if shipping == "ground":
            if weight <= 12:
                return 5.99
            elif 12 < weight <= 16:
                return 6.99
        elif shipping in ["envelope", "padded"]:
            return 8.99
        elif shipping == "priority":
            return 12.99
        else:
            sys.exit("Incorrect shipping policy detected.")

    df[shipping_price_col] = df.apply(lambda row: get_shipping_price(row[shipping_policy_col], row[weight_col]), axis=1)
    
    df[final_price_col] = df[item_price_col] + df[shipping_price_col]

# Formats main description in HTML using previous data.
def create_html_description(df, html_path, title_col, condition_description_col, size_col, material_col, color_col, sku_col, shipping_policy_col, html_description_col="html_description"):
    def format_html_description(html_path, title, condition_description, size, material, color, sku, shipping_policy):
        with open(html_path, "r") as f:
            html_template = f.read()
        return html_template.format(title=title, condition_description=condition_description, size=size, material=material, color=color, sku=sku, shipping_policy=shipping_policy)
    
    df[html_description_col] = df.apply(lambda row: format_html_description(
        html_path, row[title_col], row[condition_description_col], row[size_col], row[material_col], row[color_col], row[sku_col], row[shipping_policy_col]), axis=1)

# Checks if a photo is black.
def check_black_photo(image_path, intensity_threshold=10, percentage_threshold=95):
    image = Image.open(image_path)
    grayscale_image = image.convert('L')
    pixel_array = np.array(grayscale_image)
    
    black_pixel_count = np.sum(pixel_array <= intensity_threshold)
    total_pixels = pixel_array.size
    black_pixel_percentage = (black_pixel_count / total_pixels) * 100
    
    return black_pixel_percentage >= percentage_threshold

# Gets number of photos per item.
def assign_photo_paths(df, photos_folder, item_photos_col='item_photos', num_photos_col='num_photos'):
    black_photo_list = []
    item_photo_lists = []
    photo_count = []

    photos = os.listdir(photos_folder)
    
    for photo in photos:
        is_black = check_black_photo(os.path.join(photos_folder, photo))
        black_photo_list.append(is_black)

    item_photos = []
    num_photos_count = 0
    
    for i, is_black in enumerate(black_photo_list):
        if not is_black:
            # Ensure paths are stored with forward slashes
            item_photos.append(os.path.join(photos_folder, photos[i]).replace('\\', '/'))
            num_photos_count += 1
        else:
            if item_photos:  # Ensure we don't add empty lists
                # Convert the list to a JSON string before appending
                item_photo_lists.append(json.dumps(item_photos))
                photo_count.append(num_photos_count)
            num_photos_count = 0
            item_photos = []
    
    # Handle the last set of photos if the last photo isn't black
    if item_photos:
        # Convert the list to a JSON string before appending
        item_photo_lists.append(json.dumps(item_photos))
        photo_count.append(num_photos_count)
    
    # Ensure the series are of the same length as df before assigning them
    len_diff = len(df) - len(item_photo_lists)
    if len_diff > 0:
        # Extend the lists with None or appropriate defaults to match the DataFrame length
        item_photo_lists.extend([json.dumps([])] * len_diff)
        photo_count.extend([0] * len_diff)

    df[item_photos_col] = pd.Series(item_photo_lists)
    df[num_photos_col] = pd.Series(photo_count)
    
df = df.applymap(lowercase_except_numbers)    
df['title'] = df['title'].apply(shorten_and_capitalize_title)    
df['size'] = df['size'].apply(update_size)
df['condition_description'] = df.apply(lambda row: update_condition_description(row['condition_description'], row['condition']), axis=1)
add_shipping_price(df, 'item_price', 'shipping_policy', 'weight')
create_html_description(df, change_me.html_description_file, 'title', 'condition_description', 'size', 'material', 'color', 'sku', 'shipping_policy')
print("Getting photo paths and checking photos, this will take a bit depending on number of photos this session.")
assign_photo_paths(df, change_me.photos_folder)

df.to_excel(change_me.excel_file_new, index=False)
print("All done. New Excel file created. Ready to list.")
