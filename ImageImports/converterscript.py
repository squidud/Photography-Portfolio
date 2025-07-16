import cv2
import glob
import os

# Directory containing JPGs (this script's directory)
src_dir = os.path.dirname(os.path.abspath(__file__))
# Directory to save WEBP files (../Images from this script)
dst_dir = os.path.abspath(os.path.join(src_dir, '../Images'))
os.makedirs(dst_dir, exist_ok=True)

# Find all JPG and JPEGs in src_dir
jpg_images = glob.glob(os.path.join(src_dir, '*.jpg'))
jpeg_images = glob.glob(os.path.join(src_dir, '*.jpeg'))
newImages = jpg_images + jpeg_images
if not newImages:
    print("No JPG or JPEG images found to process.")
else:
    for image in newImages:
        print(f"Processing {os.path.basename(image)}...")
        jpg_file_path = image
        webp_file_name = os.path.splitext(os.path.basename(jpg_file_path))[0] + '.webp'
        webp_file_path = os.path.join(dst_dir, webp_file_name)

        jpg_img = cv2.imread(jpg_file_path)
        if jpg_img is None:
            print(f"Failed to read {jpg_file_path}, skipping.")
            continue
        cv2.imwrite(webp_file_path, jpg_img, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
        print(f"Converted {jpg_file_path} to {webp_file_path}")

    print("All images processed successfully.")
    print("Delete original JPG files? (y/n)")
    delete_choice = input().strip().lower()
    if delete_choice == 'y':
        for image in newImages:
            os.remove(image)
            print(f"Deleted original file: {image}")
    else:
        print("Original files retained.")

    print("Update site content now? (y/n)")
    update_choice = input().strip().lower()
    if update_choice == 'y':
        print("Site content update initiated.")
        xx
    else:
        print("Site content update skipped.")