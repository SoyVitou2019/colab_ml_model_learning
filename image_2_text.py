import os
import pandas as pd
from openpyxl import Workbook
import easyocr

def extract_text(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    text = " "
    for (bbox, text_s, prob) in result:
        text += text_s
    return text

# Define the directory containing the images
CATEGORIESDIR = "D:/Github/Activity.tracking_model/dataset"

# Initialize an empty list to store tuples of text and label
data = []

# Iterate over subdirectories in the main directory
for label in os.listdir(CATEGORIESDIR):
    subdir_path = os.path.join(CATEGORIESDIR, label)
    if os.path.isdir(subdir_path):
        # Iterate over image files in the subdirectory
        for image_file in os.listdir(subdir_path):
            if image_file.endswith(".jpg") or image_file.endswith(".png"):  # Add more extensions if needed
                image_path = os.path.join(subdir_path, image_file)
                # Extract text from the image
                text = extract_text(image_path)
                # Append the extracted text and label to the list
                data.append((text, label))

# Create a DataFrame from the list of tuples
df = pd.DataFrame(data, columns=["text", "label"])

# Write DataFrame to Excel file
output_excel = "text_from_image.xlsx"
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    writer.book = Workbook()
    df.to_excel(writer, sheet_name='Sheet1', index=False)

print("Data has been written to", output_excel)