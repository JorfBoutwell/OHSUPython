import numpy as np
from PIL import Image, ImageFilter

input_filename = "input.jpg"
output_filename = "output.jpg"
Image.MAX_IMAGE_PIXELS = None

def erode(cycles, image):
     for _ in range(cycles):
          image = image.filter(ImageFilter.MinFilter(3))
     return image

def dilate(cycles, image):
     for _ in range(cycles):
          image = image.filter(ImageFilter.MaxFilter(3))
     return image

def calculate_contrast(pixel, neighborhood_pixels):
    # Calculate the contrast of a pixel relative to its neighbors
    # For simplicity, let's just use the absolute difference between the pixel and the average of its neighbors
    average_neighbors = sum(neighborhood_pixels) / len(neighborhood_pixels)
    return abs(pixel - average_neighbors)

def calculate_mean_value(pixel, neighborhood_pixels):
    average = sum(neighborhood_pixels) / len(neighborhood_pixels)
    return average

def apply_contrast_filter(input_image, output_image_path, threshold=50, scale_factor=0.5):
    # Open the input image
    input_image = input_image.convert('L')  # Convert to grayscale
    
    # Scale down the input image
    scaled_width = int(input_image.width * scale_factor)
    scaled_height = int(input_image.height * scale_factor)
    input_image = input_image.resize((scaled_width, scaled_height))
    
    # Create a blank output image with the same dimensions as the scaled input image
    output_image = Image.new('L', input_image.size, color=255)  # Initialize with white
    
    # Iterate over each pixel in the input image
    for y in range(input_image.height):
        for x in range(input_image.width):
            pixel = input_image.getpixel((x, y))
            
            # Get the pixels in the neighborhood of the current pixel
            neighborhood_pixels = []
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < input_image.width and 0 <= ny < input_image.height:
                        neighborhood_pixels.append(input_image.getpixel((nx, ny)))
            
            # Calculate the contrast of the current pixel
            #pixel_contrast = calculate_contrast(pixel, neighborhood_pixels)
            pixel_mean_value = calculate_mean_value(pixel, neighborhood_pixels)
            
            # If the contrast is above the threshold, set the corresponding pixel in the output image to black
            if 46 < pixel_mean_value < 50 :
                output_image.putpixel((x, y), 0)
    
    #output_image = erode(2,output_image)
    #output_image = dilate(1, output_image)
    #output_image = erode(3, output_image)

    output_image.filter(ImageFilter.GaussianBlur(20))
    # Save the output image
    output_image.save(output_image_path)
    output_image.show()

# Example usage
print("open")
with Image.open(input_filename) as img:
    img.load()

    img = img.filter(ImageFilter.FIND_EDGES)
    img = img.filter(ImageFilter.GaussianBlur(10))
    #img = img.filter(ImageFilter.EDGE_ENHANCE)
    #1160 860
    print(img.getpixel((1160, 860)))
    apply_contrast_filter(img, output_filename, threshold=20, scale_factor=0.05)
    

print("close")