# replaces content in images.html with all images in the Images folder as img tags, each contained in a div with class "image-container"
import glob 
import os
import sys

webp_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Images'))

#checks that webp_dir exists
if not os.path.exists(webp_dir):
    print(f"Directory {webp_dir} does not exist. Please check the path.")
    sys.exit(1)
#list of webp files in the Images directory
webp_images = glob.glob(os.path.join(webp_dir, '*.webp'))

# variable to store HTML content
html_content = ""

for image in webp_images:
    html_content += f'<div class="image-container">\n'
    html_content += f'    <img src="{os.path.basename(image)}" alt="{os.path.basename(image)}">\n'
    html_content += f'</div>\n'

# store template HTML in variable
with open('template.html', 'r') as template_file:
    template_html = template_file.read()

# represents the final HTML to be written to gallery.html
gallery_html = template_html.replace('<!--PLACEHOLDER-->', html_content)

# write the final HTML to gallery.html
with open('gallery.html', 'w') as gallery_file:
    gallery_file.write(gallery_html)