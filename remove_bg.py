from PIL import Image
import os

def remove_white_background(input_path, output_path, threshold=240):
    try:
        print(f"Processing {input_path}...")
        img = Image.open(input_path).convert("RGBA")
        datas = img.getdata()
        new_data = []
        for item in datas:
            # Check if r, g, b are all above threshold (whiteish)
            # Keeping it strict to avoid eating into the phone screen if it's white
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                new_data.append((255, 255, 255, 0)) # Transparent
            else:
                new_data.append(item)
        img.putdata(new_data)
        img.save(output_path, "PNG")
        print(f"Successfully saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

# Paths
input_file = r"C:\Users\ADITYA MAHESHWARI\.gemini\antigravity\brain\ae705692-f1c8-483e-b10a-6cf140e42eeb\survey_intro_bag_white_bg_1769684612902.png"
output_file = r"d:\CODING\GOOGLE FORM COMPETITOR\survey-intro-transparent.png"

remove_white_background(input_file, output_file, threshold=230) # Slightly stricter threshold for this one
