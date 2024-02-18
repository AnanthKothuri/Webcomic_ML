from image_link_scraping import scrape_image_links
from preprocessing_images import save_dataset2
import os


link_file = './image_links.txt'
dataset_path = '/Users/ananthkothuri/Desktop/Webcomic_Dataset/'

# create the image link file if it doesn't exist
if not os.path.exists(link_file):
    try:
        print("--- Scraping image links ---")
        scrape_image_links(link_file)
    except:
        raise Exception("Error scraping image links")
else:
    print(f"--- {link_file} already exists ---")
    
# create dataset if it doesn't exist
# if not os.path.exists(dataset_path):
#     try:
#         print("--- Saving dataset to disk ---")
#         save_dataset2(link_file, dataset_path)
#     except:
#         raise Exception("Error creating image dataset")
# else:
#     print(f"--- dataset already exists at {dataset_path} ---")
    
print("--- Saving dataset to disk ---")
save_dataset2(link_file, dataset_path)

print("--- FINISHED ---")