from io import BytesIO
from django.core.files import File
from PIL import Image as IMG
from PIL import ImageDraw, ImageFont
import os


def make_thumbnail(image, size=(500, 500)):
    """Makes thumbnails of given size from given image"""
    thumbnail = None
    # im = IMG.open(image)
    try:
        with IMG.open(image) as im:
            # --- UTILITY FUNCTION ---
            def get_adaptive_color(img, x, y, width, height):
                """Returns black or white depending on background brightness"""
                # Sample a small area around the text position
                sample_area = img.crop((x, y, x + width, y + height))
                # Convert to grayscale and get average brightness (0-255)
                grayscale = sample_area.convert('L')
                avg_brightness = sum(grayscale.getdata()) / (width * height)
                return (0, 0, 0, 64) if avg_brightness > 127 else (255, 255, 255, 64)
            
            if im.mode in ('RGBA', 'P'):
                im = im.convert('RGB') # convert mode

            # extension = image.name.split('.')[-1]
            image_name, image_ext = os.path.splitext(os.path.basename(image.name))
            
            # resize image            
            im.thumbnail(size) # resize image

            # Add watermark +++++
            watermark_text = "inex-design.com"
            
            # Create a drawing context
            draw = ImageDraw.Draw(im)
            
            # --- CENTER WATERMARK (large, 50% opacity) ---
            # center_font_size = int(min(im.size) * 0.25)  # 15% of smaller dimension             
            center_font_size = 18  # For 500x500 images
           
            
            try:
                center_font = ImageFont.truetype("arial.ttf", center_font_size)
            except:
                center_font = ImageFont.load_default(size=center_font_size)
            
            # Get text dimensions
            center_bbox = draw.textbbox((0, 0), watermark_text, font=center_font)
            center_width = center_bbox[2] - center_bbox[0]
            center_height = center_bbox[3] - center_bbox[1]
            
            # Calculate center position
            center_x = (im.size[0] - center_width) // 2
            center_y = (im.size[1] - center_height) // 2
            
            # Get center color adaptive
            # center_color =(255, 255, 255, 128) # (RGBA color with alpha=128 for 50% opacity)
            center_color = get_adaptive_color(im, center_x, center_y, center_width, center_height)
            # Draw center watermark 
            
            draw.text((center_x, center_y), watermark_text, font=center_font, fill=center_color)
            
            # print('center font size', center_font_size)
            # print('center color', center_color)
            
            # --- CORNER WATERMARK (smaller, same as before) ---
            # corner_font_size = int(min(im.size) * 0.05)  # 5% of smaller dimension
            corner_font_size = 12
            
            try:
                corner_font = ImageFont.truetype("arial.ttf", corner_font_size)
            except:
                corner_font = ImageFont.load_default(size=corner_font_size)
            
            corner_bbox = draw.textbbox((0, 0), watermark_text, font=corner_font)
            corner_width = corner_bbox[2] - corner_bbox[0]
            corner_height = corner_bbox[3] - corner_bbox[1]
            
            margin = 10
            corner_x = im.size[0] - corner_width - margin
            corner_y = im.size[1] - corner_height - margin
            
            # corner_color = (255, 255, 255, 128)
            corner_color = get_adaptive_color(im, corner_x, corner_y, corner_width, corner_height)
            draw.text((corner_x, corner_y), watermark_text, font=corner_font, fill=corner_color)
            
            # print('corner font size', corner_font_size)
            # print('corner color', corner_color)
            # Add watermark +++++
            
            thumb_io = BytesIO() # create a BytesIO object
            # we have problem with gif image so if the save method doesnot work we do not 
            # make any thumbnail
             # Save the thumbnail based on format
            if image_ext.lower() in ('.jpg', '.jpeg'):
                format = 'JPEG'
            elif image_ext.lower() == '.png':
                format = 'PNG'
            elif image_ext.lower() == '.webp':
                format = 'WEBP'
            else:
                # Default to JPEG for other formats
                format = 'JPEG'
                image_ext = '.jpg'
                    
            try:
                im.save(thumb_io, format, quality=85) #, quality=85 save image to BytesIO object
            except Exception as e:
                print(f"Error creating thumbnail: {e}")
                return thumbnail
            # image_name = image.name.split('/')[-1]
            thumbnail = File(thumb_io, name=f"{image_name}{image_ext}") # create a django friendly File object
    except Exception as e:
        print(f"Error creating thumbnail main: {e}")   
    return thumbnail
    