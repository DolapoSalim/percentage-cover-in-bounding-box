###Calculate percentage coverage of an object using shoelace theorem

import numpy as np

# The normalized coordinates from the YOLO format (skipping the first class ID)
normalized_coords = [
    0.17166666666666666, 0,
    0.17083333333333334, 0.00375,
    0.15875, 0.005625,
    0.14375, 0.00375,
    0.12958333333333333, 0.005625,
    0.11166666666666666, 0.0025,
    0.09541666666666666, 0.0025,
    0.08958333333333333, 0.005,
    0.059583333333333335, 0.00375,
    0.04833333333333333, 0,
    0.04416666666666667, 0.004375,
    0.04083333333333333, 0.0025,
    0.014583333333333334, 0.005,
    0.009166666666666667, 0.003125,
    0.005416666666666667, 0.00625,
    0, 0.00375,
    0, 0.99375,
    0.005, 0.995625,
    0.034166666666666665, 0.994375,
    0.06416666666666666, 0.996875,
    0.20791666666666667, 0.999375,
    0.9995833333333334, 0.999375,
    0.9995833333333334, 0.003125,
    0.9945833333333334, 0,
    0.18916666666666668, 0,
    0.185, 0.005,
    0.17916666666666667, 0.0025,
    0.17833333333333334, 0,
    0.17166666666666666, 0
]

# Convert normalized coordinates to pixel coordinates
img_width = 360
img_height = 360
pixel_coords = []
for i in range(0, len(normalized_coords), 2):
    x = normalized_coords[i] * img_width
    y = normalized_coords[i+1] * img_height
    pixel_coords.append((x, y))

# Convert to numpy array for easier manipulation
coords = np.array(pixel_coords)

# Calculate area using the Shoelace formula
x = coords[:, 0]
y = coords[:, 1]
area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

# Calculate percentage of total image area
total_image_area = img_width * img_height
percentage = (area / total_image_area) * 100

print(f"Polygon coordinates (pixels):")
for x, y in pixel_coords:
    print(f"({x:.2f}, {y:.2f})")

print(f"\nPolygon area: {area:.2f} square pixels")
print(f"Image area: {total_image_area} square pixels")
print(f"Percentage coverage: {percentage:.2f}%")
