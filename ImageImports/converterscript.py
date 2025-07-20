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
        
        # decrease resolution to 80% of original
        height, width = jpg_img.shape[:2]
        new_height = int(height * 0.80)
        new_width = int(width * 0.80)
        jpg_img = cv2.resize(jpg_img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(webp_file_path, jpg_img, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
        
        #save thumbnail version to Thumbs folder at 25% of original resolution
        thumb_dir = os.path.join(dst_dir, 'Thumbs')
        os.makedirs(thumb_dir, exist_ok=True)
        thumb_file_name = os.path.splitext(os.path.basename(jpg_file_path))[0] + '.webp'
        thumb_file_path = os.path.join(thumb_dir, thumb_file_name)
        thumb_img = cv2.resize(jpg_img, (new_width // 3, new_height // 3), interpolation=cv2.INTER_AREA)
        cv2.imwrite(thumb_file_path, thumb_img, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
        
        # print confirmation
        if os.path.exists(webp_file_path):
            print(f"Converted {jpg_file_path} to {webp_file_path} and saved thumbnail to {thumb_file_path}")
        else:
            print(f"Failed to convert {jpg_file_path} to {webp_file_path}")
            continue

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

    print("Run image order GUI to reorder images? (y/n)")
    update_choice = input().strip().lower()
    if update_choice == 'y':
        print("Site content update initiated.")
        os.system(f'python3 "{os.path.join(src_dir, "changeorder.py")}"')
    else:
        print("Site content update and order skipped. You can run the GUI later to reorder images.")