import os
import shutil
import glob
import sys

# Try to import icrawler
try:
    from icrawler.builtin import GoogleImageCrawler
except ImportError:
    print("Error: 'icrawler' library is not installed.")
    print("Please install it by running: pip install icrawler")
    sys.exit(1)

def clean_slug(slug):
    return slug.replace("-", " ")

def rename_images(folder_path):
    # Get all files in the folder
    files = glob.glob(os.path.join(folder_path, "*"))
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
    
    # Sort to ensure deterministic order if needed, though crawler order is usually fine
    image_files.sort()
    
    for i, file_path in enumerate(image_files):
        if i >= 4: # Keep only up to 4
            os.remove(file_path)
            continue
            
        ext = os.path.splitext(file_path)[1]
        new_name = f"{i+1}{ext}"
        new_path = os.path.join(folder_path, new_name)
        
        if file_path != new_path:
            # Handle case where target exists
            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(file_path, new_path)
            print(f"Renamed {os.path.basename(file_path)} to {new_name}")

def download_images_for_product(slug, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Check if we already have 4 images
    existing_images = [f for f in os.listdir(output_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if len(existing_images) >= 4:
        print(f"Skipping {slug}, already has {len(existing_images)} images.")
        return

    print(f"Downloading images for: {slug}")
    keyword = clean_slug(slug)
    
    # Configure crawler
    # Using BingImageCrawler as it is often more stable than Google for simple scraping
    from icrawler.builtin import BingImageCrawler
    bing_crawler = BingImageCrawler(
        feeder_threads=1,
        parser_threads=1,
        downloader_threads=4,
        storage={'root_dir': output_dir}
    )
    
    # Download
    bing_crawler.crawl(keyword=keyword, max_num=4)
    
    # Rename
    rename_images(output_dir)

    # Remove Watermarks
    for i in range(1, 5):
        # Check for common extensions
        for ext in ['.jpg', '.jpeg', '.png']:
            img_path = os.path.join(output_dir, f"{i}{ext}")
            if os.path.exists(img_path):
                remove_watermark(img_path)
                break

def remove_watermark(image_path):
    api_key = "d0cb217de5cc3f589c7beb950f4a1fab"
    url = "https://api.nanobanana.im/v1/remove-watermark"
    
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library is not installed. Skipping watermark removal.")
        return

    print(f"Removing watermark for {os.path.basename(image_path)}...")
    
    try:
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.post(url, files=files, headers=headers)
            
        if response.status_code == 200:
            # Save the processed image back to the same path
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Watermark removed successfully for {os.path.basename(image_path)}")
        else:
            print(f"Failed to remove watermark. Status: {response.status_code}, Response: {response.text}")
            
    except Exception as e:
        print(f"Error during watermark removal: {e}")

def main():
    base_folder = "products"
    keywords = []
    
    if not os.path.exists(base_folder):
        print(f"Error: Base folder '{base_folder}' does not exist.")
        return

    # Find target directories
    target_dirs = []
    for item in os.listdir(base_folder):
        item_path = os.path.join(base_folder, item)
        if os.path.isdir(item_path):
            # Add all directories
            target_dirs.append(item)

    print(f"Found {len(target_dirs)} product folders.")

    for slug in target_dirs:
        folder_path = os.path.join(base_folder, slug)
        try:
            download_images_for_product(slug, folder_path)
        except Exception as e:
            print(f"Failed to process {slug}: {e}")

if __name__ == "__main__":
    main()
