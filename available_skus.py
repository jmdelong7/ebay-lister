import pandas as pd
from datetime import date

def generate_available_skus(active_listings_report, upper_limit):
    # Create range of base SKUs
    base_skus = [*range(10001, upper_limit + 1)]

    # Add hyphen to base SKUs
    formatted_skus = [str(sku) + '-' for sku in base_skus]

    # Add 01-18 to each SKU
    all_skus = [sku + str(f"{suffix:02d}") for suffix in range(1, 19) for sku in formatted_skus]

    # Load active listing report CSV and create list of all active SKUs
    df_active = pd.read_csv(active_listings_report)
    active_skus = list(df_active["Custom label (SKU)"])
    
    # Create a set of active SKUs with the middle three digits stripped
    active_skus_stripped = set(sku.replace('-000-', '-') if '-000-' in sku else sku for sku in active_skus)

    # Compare all available SKUs list to active SKUs, put unused values into available_skus list
    available_skus = [sku for sku in all_skus if sku not in active_skus_stripped]
    
    # Sort the available SKUs from smallest to largest
    available_skus.sort()

    print("Total SKUs: ", len(all_skus))
    print("Active SKUs: ", len(active_skus))
    print("Available SKUs: ", len(available_skus))

    # Export available_skus list to a CSV file
    df_available = pd.DataFrame(available_skus)
    df_available.to_csv(r"G:\My Drive\eBay (Google Drive)\Misc\available skus {}.csv".format(date.today()), index=False, header=False)

# Call the function with the path to your active listings report
active_listings_file_name = "eBay-all-active-listings-report-2023-10-29-12135747194"
active_listings_csv = r"G:\My Drive\eBay (Google Drive)\Misc\{}.csv".format(active_listings_file_name)
generate_available_skus(active_listings_csv, 10380)