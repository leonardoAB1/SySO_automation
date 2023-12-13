import os
import matplotlib.pyplot as plt
from matplotlib import image as mpimg

# Get the current working directory
folder_path = os.getcwd()

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter only image files (you might need to adjust this based on your file extensions)
image_files = [f for f in files if f.endswith('.jpeg')]

# Create a subplot with 2 rows and 6 columns
fig, axs = plt.subplots(4, 3, figsize=(4, 5))

# Flatten the 2D array of subplots for easier indexing
axs = axs.flatten()

# Loop through the image files and plot each one
for i, image_file in enumerate(image_files):
    # Create the full path to the image
    image_path = os.path.join(folder_path, image_file)

    # Read the image using matplotlib
    img = mpimg.imread(image_path)

    # Display the image in the subplot
    axs[i].imshow(img)
    axs[i].axis('off')  # Turn off axis labels

# Adjust layout to prevent clipping of axis labels
plt.tight_layout()

# Show the plot
plt.show()
