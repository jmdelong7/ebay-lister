import change_me
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def scroll_to_element(element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(change_me.time_sleep)
    
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # This will suppress all logs except fatal errors.
driver = webdriver.Chrome(options=options)

driver.get("https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&ru=https%3A%2F%2Fwww.ebay.com%2F")
input("Press enter when logged in.")

df = pd.read_excel(change_me.excel_file_new)

def list_item(df, row):

    # Go to template page.
    driver.get("https://bulkedit.ebay.com/managetemplates")
    time.sleep(change_me.page_delay)

    # Create new listing from template.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "create-new-template")))

    table_template_name = driver.find_element(By.XPATH, '//table//tbody//tr//td[text()="{}"]'.format(df['category'][row]))
    scroll_to_element(table_template_name)
    create_listing_template_url = table_template_name.find_element(By.XPATH, "..//div//a[contains(@href, 'AddItem')]").get_attribute("href")
    time.sleep(change_me.time_sleep)
    driver.get(create_listing_template_url)

    # Wait for page to load.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Save for later']"))) 
    time.sleep(change_me.page_delay)

    # Upload photos
    item_photos_str = df.loc[row, "item_photos"]
    item_photos_list = json.loads(item_photos_str)
    driver.find_element(By.ID, "fehelix-uploader")

    for photo in item_photos_list:
        driver.find_element(By.ID, "fehelix-uploader").send_keys(photo)
        time.sleep(change_me.time_sleep)

    # Input title.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "title")))

    title = driver.find_element(By.NAME, "title")
    scroll_to_element(title)
    title.send_keys(df["title"][row])
    time.sleep(change_me.time_sleep)

    # Input sku.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "customLabel")))

    sku = driver.find_element(By.NAME, "customLabel")
    scroll_to_element(sku)
    sku.send_keys(df["sku"][row])
    time.sleep(change_me.time_sleep)

    # Select condition if necessary.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "condition")))

    item_condition_button = driver.find_element(By.NAME, "condition")
    scroll_to_element(item_condition_button)

    condition = df["condition"][row]

    if condition != "pre-owned":
        item_condition_button.click()
        time.sleep(change_me.time_sleep)
        
        conditions = driver.find_elements(By.XPATH, "//input[@type='radio']")
        
        if len(conditions) != 4:
            conditions[0].click()
            
        else:
            condition_values = {
                    "1000": "new with tags", "1500": "new without tags", "1750": "new with defects", "3000": "pre-owned"
                    }
            for c in conditions:
                if condition_values[c.get_attribute("value")] == condition:
                    c.click()
                    break
        time.sleep(change_me.time_sleep)

    # Input condition description if necessary.
    if condition == "new with tags":
        pass

    else:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "itemConditionDescription")))
        item_condition_description_field = driver.find_element(By.NAME, "itemConditionDescription")
        scroll_to_element(item_condition_description_field)
        
        item_condition_description_field.send_keys(df["condition_description"][row])
        time.sleep(change_me.time_sleep)

    # Input main description.
    html_btn = driver.find_element(By.NAME, "descriptionEditorMode")
    scroll_to_element(html_btn)
    html_btn.click()
    time.sleep(change_me.time_sleep)

    description = driver.find_element(By.NAME, "description")
    description.click()
    time.sleep(change_me.time_sleep)

    description.send_keys(df["html_description"][row])
    time.sleep(change_me.time_sleep)

    html_btn.click()
    time.sleep(change_me.time_sleep)

    # Input price.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "price")))

    price = driver.find_element(By.NAME, "price")
    scroll_to_element(price)
    price.send_keys((df["final_price"][row]))
    time.sleep(change_me.time_sleep)

    # Select shipping policy if necessary.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "shippingPolicyId")))

    if df["shipping_policy"][row] == "pre-owned":
        pass

    else:
        shipping_policy_dropdown = driver.find_element(By.NAME, "shippingPolicyId")
        scroll_to_element(shipping_policy_dropdown)
        shipping_policy_dropdown.click()
        time.sleep(change_me.time_sleep)
        
        shipping_policies = driver.find_elements(By.XPATH, "//div[@role='option']")
        for policy in shipping_policies:
            policy_text = policy.text.lower()
            if "listings" in policy_text:
                policy_text = policy_text.rsplit(" (", 1)[0]
                if policy_text == df["shipping_policy"][row]:
                    policy.click()
                    time.sleep(change_me.time_sleep)
                    break

    # Input weight.         
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "majorWeight")))

    lbs_input = driver.find_element(By.NAME, "majorWeight")
    ozs_input = driver.find_element(By.NAME, "minorWeight")

    scroll_to_element(lbs_input)

    # Convert weight to lbs and ozs.
    weight = int(df["weight"][row])
    if weight <= 16:
        lbs_ozs = [0, weight]
    else:
        lbs_ozs = [weight // 16, weight % 16]
        
    # Input the lbs and ozs, clears the inputs first just in case.
    lbs_input.clear()
    time.sleep(change_me.time_sleep)
    lbs_input.send_keys(lbs_ozs[0])
    time.sleep(change_me.time_sleep)

    ozs_input.clear()
    time.sleep(change_me.time_sleep)
    ozs_input.send_keys(lbs_ozs[1])
    time.sleep(change_me.time_sleep)

    # Input size.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "attributes.Size")))
    size_input = driver.find_element(By.NAME, "attributes.Size")
    scroll_to_element(size_input)

    size = df["size"][row]

    size_list = size.split(", ")
    first_size = size_list[0]

    size_input.click()
    time.sleep(change_me.time_sleep)
    driver.find_element(By.NAME, "search-box-attributesSize").clear()
    time.sleep(change_me.time_sleep)
    driver.find_element(By.NAME, "search-box-attributesSize").send_keys(first_size)
    time.sleep(change_me.time_sleep)

    searched_size = driver.find_elements(By.NAME, "searchedOptions-attributesSize")

    # Get the size buttons (search results) if the search results are found.
    if len(searched_size) > 0:
        searched_size_panel = searched_size[0].find_element(By.CSS_SELECTOR, "div")
        searched_size_buttons = searched_size_panel.find_elements(By.CSS_SELECTOR, "div")
        
        # Click the size if it is found in the search results.
        for size_element in searched_size_buttons:
            size_text = size_element.text.lower()
            if size_text == first_size.lower():
                size_element.click()
                time.sleep(change_me.time_sleep)
                break
                    
    # If there aren't any matches in the search results (or no search results) click "Add custom details" option.
    else:
        driver.find_element(By.XPATH, "//button[contains(@class, 'custom')]").click()
        time.sleep(change_me.time_sleep)

    # Input color.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "attributes.Color")))
    color_input = driver.find_element(By.NAME, "attributes.Color")
    scroll_to_element(color_input)

    color = df["color"][row]
            
    color_list = color.split(", ")
    first_color = color_list[0]

    color_input.click()
    time.sleep(change_me.time_sleep)
    driver.find_element(By.NAME, "search-box-attributesColor").clear()
    time.sleep(change_me.time_sleep)
    driver.find_element(By.NAME, "search-box-attributesColor").send_keys(first_color)
    time.sleep(change_me.time_sleep)
            
    searched_color = driver.find_elements(By.NAME, "searchedOptions-attributesColor")
            
    # Get the color buttons (search results) if the search results are found.
    if len(searched_color) > 0:
        searched_color_panel = searched_color[0].find_element(By.CSS_SELECTOR, "div")
        searched_color_buttons = searched_color_panel.find_elements(By.CSS_SELECTOR, "div")
        
        # Click the color if it is found in the search results.
        for color_element in searched_color_buttons:
            color_text = color_element.text.lower()
            if color_text == first_color.lower():
                color_element.click()
                time.sleep(change_me.time_sleep)
                break
                        
    # If there aren't any matches in the search results (or no search results) click "Add custom details" option.
    else:
        driver.find_element(By.XPATH, "//button[contains(@class, 'custom')]").click()
        time.sleep(change_me.time_sleep)

    # Input material.  
    material = df["material"][row]
    if material == "none":
        pass

    else:
        # Split the material into a list.
        material_list = material.split(", ")

        # Center the "Material" field.
        material_dropdown = driver.find_element(By.NAME, "attributes.Material")
        scroll_to_element(material_dropdown)

        # Click "Material" dropdown.
        material_dropdown.click()
        time.sleep(change_me.time_sleep)

        material_search_box = driver.find_element(By.NAME, "search-box-attributesMaterial")

        for material in material_list:
            material_search_box.clear()
            time.sleep(change_me.time_sleep)
            material_search_box.send_keys(material)
            time.sleep(change_me.time_sleep)

            # Get the search results.
            searched_material = driver.find_elements(By.NAME, "searchedOptions-attributesMaterial")

            # Get the material buttons (search results) if the materials searched for are found.
            if len(searched_material) > 0:
                searched_material_panel = searched_material[0].find_element(By.CSS_SELECTOR, "div")
                searched_material_results = searched_material_panel.find_elements(By.CSS_SELECTOR, "div")
                
                # Click the material if it is found in the search results.
                for material_element in searched_material_results:
                    material_text = material_element.text.lower()
                    if material_text == material.lower():
                        material_element.click()
                        time.sleep(change_me.time_sleep)
                        break

        material_dropdown.click()
        time.sleep(change_me.time_sleep)   

    # Save draft.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Save for later']")))
    save_for_later_button = driver.find_element(By.XPATH, "//button[@aria-label='Save for later']")
    scroll_to_element(save_for_later_button)

    save_for_later_button.click()

    # Wait for the URL to change
    WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
    time.sleep(change_me.time_sleep)
    
    print(f"Listing #{str(row + 1)} draft created.")

    
for row in range(0, len(df)):
    list_item(df, row)
    
print("Done creating drafts!")

