import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PlotPolygon
from matplotlib.collections import PatchCollection
import os
import random

def calculate_polygon_area(coords):
    """
    Calculate the area of a polygon using the Shoelace formula.
    
    Args:
        coords: List of (x, y) coordinate pairs
    
    Returns:
        Area of the polygon in square pixels
    """
    coords = np.array(coords)
    x = coords[:, 0]
    y = coords[:, 1]
    
    # Shoelace formula
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return area

def normalize_to_pixel_coords(normalized_coords, img_width, img_height):
    """
    Convert normalized coordinates to pixel coordinates.
    
    Args:
        normalized_coords: List of normalized (x, y) coordinate pairs
        img_width: Width of the image in pixels
        img_height: Height of the image in pixels
    
    Returns:
        List of (x, y) pixel coordinate pairs
    """
    pixel_coords = []
    for i in range(0, len(normalized_coords), 2):
        x = normalized_coords[i] * img_width
        y = normalized_coords[i+1] * img_height
        pixel_coords.append((x, y))
    return pixel_coords

def parse_yolo_polygon(line):
    """
    Parse a line from a YOLO polygon annotation file.
    
    Args:
        line: String containing class_id and coordinates
        
    Returns:
        class_id: Integer class ID
        coords: List of normalized coordinate values
    """
    values = list(map(float, line.strip().split()))
    class_id = int(values[0])
    coords = values[1:]
    return class_id, coords

def main():
    # Image dimensions
    img_width, img_height = 640, 480
    image_area = img_width * img_height
    
    # Complex YOLO polygon annotations for 5 different classes
    # Format: class_id x1 y1 x2 y2 x3 y3 ...
    complex_annotations = [
        # Class 0 - A complex shape with many vertices (e.g., a car)
        "0 0.12 0.15 0.11 0.16 0.10 0.18 0.08 0.20 0.07 0.23 0.06 0.27 0.05 0.32 0.05 0.37 0.06 0.42 0.07 0.46 0.09 0.49 0.12 0.50 0.15 0.50 0.19 0.49 0.22 0.47 0.24 0.45 0.25 0.40 0.25 0.35 0.24 0.30 0.23 0.25 0.20 0.20 0.17 0.17 0.15 0.15",
        
        # Class 1 - A complex polygon (e.g., a person)
        "1 0.65 0.10 0.67 0.12 0.68 0.15 0.70 0.20 0.71 0.25 0.70 0.30 0.69 0.35 0.68 0.40 0.67 0.45 0.66 0.50 0.65 0.55 0.64 0.60 0.63 0.65 0.62 0.60 0.61 0.55 0.60 0.50 0.59 0.45 0.58 0.40 0.60 0.35 0.61 0.30 0.62 0.25 0.63 0.20 0.64 0.15",
        
        # Class 2 - A plant-like shape with many curves
        "2 0.30 0.65 0.32 0.63 0.35 0.60 0.38 0.58 0.40 0.59 0.42 0.61 0.45 0.63 0.47 0.65 0.45 0.67 0.44 0.70 0.42 0.72 0.40 0.73 0.38 0.72 0.36 0.70 0.34 0.68 0.32 0.67 0.30 0.65",
        
        # Class 3 - A building-like shape with many edges
        "3 0.75 0.70 0.80 0.70 0.80 0.75 0.85 0.75 0.85 0.80 0.90 0.80 0.90 0.85 0.88 0.87 0.86 0.88 0.84 0.89 0.82 0.90 0.80 0.90 0.78 0.89 0.76 0.88 0.74 0.85 0.74 0.80 0.75 0.75 0.75 0.70",
        
        # Class 4 - A complex curved shape (e.g., a cloud)
        "4 0.10 0.85 0.15 0.83 0.20 0.82 0.25 0.81 0.30 0.82 0.35 0.83 0.38 0.85 0.38 0.88 0.35 0.90 0.30 0.91 0.25 0.91 0.20 0.90 0.15 0.89 0.10 0.88 0.10 0.85"
    ]
    
    # Class names and colors
    class_names = {
        0: "Car",
        1: "Person", 
        2: "Plant",
        3: "Building",
        4: "Cloud"
    }
    
    colors = {
        0: 'red',
        1: 'blue',
        2: 'green',
        3: 'orange',
        4: 'purple'
    }
    
    # Store results
    results = []
    polygons_for_plot = []
    polygon_colors = []
    
    # Process each annotation
    for annotation in complex_annotations:
        class_id, coords = parse_yolo_polygon(annotation)
        pixel_coords = normalize_to_pixel_coords(coords, img_width, img_height)
        
        # Calculate area and percentage
        area = calculate_polygon_area(pixel_coords)
        percentage = (area / image_area) * 100
        
        # Store results
        results.append({
            'class_id': class_id,
            'class_name': class_names[class_id],
            'area_pixels': area,
            'percentage': percentage,
            'pixel_coords': pixel_coords
        })
        
        # Prepare for plotting
        polygons_for_plot.append(PlotPolygon(pixel_coords, True))
        polygon_colors.append(colors[class_id])
    
    # Print results
    print(f"Image dimensions: {img_width}x{img_height} pixels")
    print(f"Total image area: {image_area} square pixels")
    print("\nCoverage Analysis:")
    print("-" * 70)
    print(f"{'Class ID':<10}{'Class Name':<15}{'Area (pixels)':<20}{'Coverage %':<15}{'Vertices':<10}")
    print("-" * 70)
    
    total_coverage = 0
    for r in results:
        print(f"{r['class_id']:<10}{r['class_name']:<15}{r['area_pixels']:<20.2f}{r['percentage']:<15.2f}%{len(r['pixel_coords']):<10}")
        total_coverage += r['percentage']
    
    print("-" * 70)
    print(f"{'TOTAL':<25}{sum(r['area_pixels'] for r in results):<20.2f}{total_coverage:<15.2f}%")
    
    # Create a mask visualization for each class
    fig, axs = plt.subplots(2, 3, figsize=(18, 12))
    axs = axs.flatten()
    
    # Create full visualization with all polygons
    ax = axs[0]
    ax.set_xlim(0, img_width)
    ax.set_ylim(img_height, 0)  # Invert y-axis to match image coordinates
    
    p = PatchCollection(polygons_for_plot, alpha=0.7)
    p.set_color(polygon_colors)
    ax.add_collection(p)
    
    # Add class labels
    for r, poly in zip(results, polygons_for_plot):
        centroid_x = sum(v[0] for v in poly.get_xy()) / len(poly.get_xy())
        centroid_y = sum(v[1] for v in poly.get_xy()) / len(poly.get_xy())
        ax.text(centroid_x, centroid_y, f"{r['class_name']}\n{r['percentage']:.2f}%", 
                ha='center', va='center', fontsize=9, color='white', fontweight='bold')
    
    ax.set_title(f'All Classes - Total Coverage: {total_coverage:.2f}%')
    ax.set_xlabel('X (pixels)')
    ax.set_ylabel('Y (pixels)')
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Create individual class visualizations
    for i, result in enumerate(results):
        ax = axs[i+1]
        ax.set_xlim(0, img_width)
        ax.set_ylim(img_height, 0)
        
        # Create a mask for this class
        poly = PlotPolygon(result['pixel_coords'], True)
        p = PatchCollection([poly], alpha=0.7)
        p.set_color(colors[result['class_id']])
        ax.add_collection(p)
        
        # Add class label and vertices
        ax.set_title(f"{result['class_name']} - {result['percentage']:.2f}% - {len(result['pixel_coords'])} vertices")
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Draw vertices for better visualization
        vertices = np.array(result['pixel_coords'])
        ax.scatter(vertices[:, 0], vertices[:, 1], color='yellow', s=20, zorder=3)
        
        # Number the vertices
        for j, (x, y) in enumerate(result['pixel_coords']):
            if j % 5 == 0:  # Number every 5th vertex to avoid clutter
                ax.text(x, y, str(j), fontsize=8, color='black', 
                        bbox=dict(facecolor='white', alpha=0.7, pad=1))
    
    plt.tight_layout()
    plt.savefig('complex_polygon_coverage_analysis.png', dpi=300)
    
    # Create a visualization function for a real-world example
    def visualize_real_example():
        # For a real example, you would load from a file
        # This is the sample you provided earlier
        real_annotation = "0 0.17166666666666666 0 0.17083333333333334 0.00375 0.15875 0.005625 0.14375 0.00375 0.12958333333333333 0.005625 0.11166666666666666 0.0025 0.09541666666666666 0.0025 0.08958333333333333 0.005 0.059583333333333335 0.00375 0.04833333333333333 0 0.04416666666666667 0.004375 0.04083333333333333 0.0025 0.014583333333333334 0.005 0.009166666666666667 0.003125 0.005416666666666667 0.00625 0 0.00375 0 0.99375 0.005 0.995625 0.034166666666666665 0.994375 0.06416666666666666 0.996875 0.20791666666666667 0.999375 0.9995833333333334 0.999375 0.9995833333333334 0.003125 0.9945833333333334 0 0.18916666666666668 0 0.185 0.005 0.17916666666666667 0.0025 0.17833333333333334 0 0.17166666666666666 0"
        
        # Parse the real annotation
        real_img_width, real_img_height = 360, 360
        class_id, coords = parse_yolo_polygon(real_annotation)
        pixel_coords = normalize_to_pixel_coords(coords, real_img_width, real_img_height)
        
        # Calculate area and percentage
        area = calculate_polygon_area(pixel_coords)
        percentage = (area / (real_img_width * real_img_height)) * 100
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, real_img_width)
        ax.set_ylim(real_img_height, 0)
        
        # Create a polygon for visualization
        poly = PlotPolygon(pixel_coords, True)
        p = PatchCollection([poly], alpha=0.7)
        p.set_color('blue')
        ax.add_collection(p)
        
        # Add class label
        ax.set_title(f"Real Example - Class {class_id} - Coverage: {percentage:.2f}% - Vertices: {len(pixel_coords)}")
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Draw vertices for better visualization
        vertices = np.array(pixel_coords)
        ax.scatter(vertices[:, 0], vertices[:, 1], color='yellow', s=20, zorder=3)
        
        # Number selected vertices to avoid clutter
        for j, (x, y) in enumerate(pixel_coords):
            if j % 5 == 0:  # Number every 5th vertex
                ax.text(x, y, str(j), fontsize=8, color='black',
                        bbox=dict(facecolor='white', alpha=0.7, pad=1))
        
        plt.tight_layout()
        plt.savefig('real_example_analysis.png', dpi=300)
        
        print("\nReal Example Analysis:")
        print("-" * 70)
        print(f"Image dimensions: {real_img_width}x{real_img_height} pixels")
        print(f"Total image area: {real_img_width * real_img_height} square pixels")
        print(f"Class ID: {class_id}")
        print(f"Number of vertices: {len(pixel_coords)}")
        print(f"Area: {area:.2f} square pixels")
        print(f"Coverage percentage: {percentage:.2f}%")
    
    # Run the real-world example analysis
    visualize_real_example()
    
    print("\nAnalysis complete. Visualizations saved as 'complex_polygon_coverage_analysis.png' and 'real_example_analysis.png'")

if __name__ == "__main__":
    main()