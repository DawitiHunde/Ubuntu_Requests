import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """Extracts a filename from the URL or generates one using a hash."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    if not filename:
        # If URL has no filename, generate one using a hash
        filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
    
    return filename

def download_image(url, folder="Fetched_Images"):
    """Downloads a single image and saves it to the folder."""
    try:
        # Ensure directory exists
        os.makedirs(folder, exist_ok=True)
        
        # Fetch the image with a timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for bad HTTP codes
        
        # Check Content-Type to ensure it's an image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped: URL does not point to an image ({content_type})")
            return None
        
        # Extract filename and prevent duplicates
        filename = get_filename_from_url(url)
        filepath = os.path.join(folder, filename)
        
        # Prevent overwriting duplicate images
        if os.path.exists(filepath):
            print(f"✓ Skipped: Duplicate image {filename} already exists")
            return filepath
        
        # Save the image in binary mode
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        return filepath

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Allow multiple URLs separated by commas
    urls_input = input("Please enter the image URL(s), separated by commas: ")
    urls = [url.strip() for url in urls_input.split(",") if url.strip()]
    
    if not urls:
        print("✗ No URLs provided. Exiting.")
        return
    
    for url in urls:
        download_image(url)
    
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
