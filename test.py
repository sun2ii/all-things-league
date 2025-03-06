
# image_path = "../public/summoner-map-1.png"  # Change this to your actual image file path

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the map image
image_path = "../public/summoner-map-1.png"  # Change this to your actual image file path
original_image = cv2.imread(image_path)
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)  # Convert to RGB for Matplotlib
image = original_image.copy()

# Define scale factor (Adjust based on known distances)
UNITS_PER_PIXEL = 20  # Example: 20 game units per pixel (adjust based on measurement)
MOVEMENT_SPEED = 325  # Default movement speed of a champion (units/sec)

# Store clicked points
clicked_points = []

def click_event(event, x, y, flags, param):
    """Handles mouse clicks to capture two points on the image."""
    global clicked_points, image
    
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        print(f"Point {len(clicked_points)}: ({x}, {y})")
        
        # Draw a dot where the user clicked
        cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
        
        # If two points are clicked, draw the path and calculate travel time
        if len(clicked_points) == 2:
            draw_path_and_calculate()

def draw_path_and_calculate():
    """Draws a line between two points, calculates distance and travel time, and overlays text."""
    global clicked_points, image, original_image
    
    # Get points
    (x1, y1), (x2, y2) = clicked_points
    
    # Reset the image to remove previous lines and texts
    image = original_image.copy()
    
    # Draw line between the points
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Calculate pixel distance
    pixel_distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Convert to in-game distance
    game_distance = pixel_distance * UNITS_PER_PIXEL
    
    # Compute travel time
    travel_time = game_distance / MOVEMENT_SPEED
    
    # Display travel time on the image
    midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)
    text = f"{travel_time:.1f}s"
    cv2.putText(image, text, midpoint, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Show the updated image with line and text
    cv2.imshow("Map", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
    print(f"Pixel Distance: {pixel_distance:.2f} pixels")
    print(f"In-game Distance: {game_distance:.2f} units")
    print(f"Estimated Travel Time: {travel_time:.2f} seconds")
    
    # Reset clicked points for the next selection
    clicked_points = []

# Show image and wait for clicks
cv2.imshow("Map", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
cv2.setMouseCallback("Map", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()