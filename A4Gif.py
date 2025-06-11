#Fabio Leandro Lapuinka 14:50 08/06/2025 
from PIL import Image
import os

def convert_images_to_gif(input_folder, output_filename, target_size=(720, 900), duration=75, loop=0, background_color=(0, 0, 0)):
    """
    Convert all image files (PNG/JPG/JPEG) in a folder to an animated GIF with fixed resolution.
    
    Parameters:
    - input_folder: Path to folder containing image files
    - output_filename: Name of the output GIF file
    - target_size: Tuple with target resolution (width, height)
    - duration: Time each frame is displayed (in milliseconds)
    - loop: Number of loops (0 means infinite loop)
    - background_color: Background color as RGB tuple (default is black)
    """
    # Get all image files in the input folder (PNG, JPG, JPEG)
    valid_extensions = ('.png', '.jpg', '.jpeg')
    image_files = [f for f in os.listdir(input_folder) 
                  if f.lower().endswith(valid_extensions)]
    
    # Sort the files alphabetically
    image_files.sort()
    
    if not image_files:
        print("No image files (PNG/JPG/JPEG) found in the specified directory.")
        return
    
    # Open and resize all images
    images = []
    for image_file in image_files:
        file_path = os.path.join(input_folder, image_file)
        try:
            img = Image.open(file_path)
            
            # Convert to RGB if image is in palette mode or has transparency
            if img.mode in ('P', 'RGBA', 'LA'):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
            
            # Redimensiona mantendo a proporção
            img.thumbnail(target_size, Image.LANCZOS)
            
            # Cria uma nova imagem com o tamanho exato e fundo sólido
            new_img = Image.new("RGB", target_size, background_color)
            
            # Cola a imagem redimensionada centralizada
            # Trata imagens com transparência (PNG com alpha channel)
            if img.mode == 'RGBA':
                new_img.paste(img, (
                    (target_size[0] - img.size[0]) // 2,  # Posição X
                    (target_size[1] - img.size[1]) // 2    # Posição Y
                ), img)
            else:
                new_img.paste(img, (
                    (target_size[0] - img.size[0]) // 2,
                    (target_size[1] - img.size[1]) // 2
                ))
            
            images.append(new_img)
        except Exception as e:
            print(f"Could not process {image_file}: {e}")
    
    if not images:
        print("No valid images could be processed.")
        return
    
    # Save as GIF
    images[0].save(
        output_filename,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=loop
    )
    
    print(f"Successfully created {output_filename} ({target_size[0]}x{target_size[1]}) with {len(images)} frames.")

# Example usage:
convert_images_to_gif('C:\\Users\\lapui\\OneDrive\\Documentos\\Prints\\', 'output.gif')


#Quem conversa com I.A são os DEVs
#Sudo ./darknet detector demo -i 0 cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights -dont_show /mnt/c/Users/lapui/OneDrive/Documentos/Prints/output.gif -out_filename data/video/output.mp4
