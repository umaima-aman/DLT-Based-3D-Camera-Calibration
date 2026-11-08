import cv2
import numpy as np
from scipy.linalg import rq  

# Load Image
image_path = r"" #add image path  
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(f"Error: Cannot open image at {image_path}")

# Display Full Image 
cv2.namedWindow("Click on 6 markers", cv2.WINDOW_NORMAL)  
cv2.imshow("Click on 6 markers", image)

# List to store pixel coordinates
pixel_coords = []

def get_pixel_coordinates(event, x, y, flags, param):
    # Capture 6 marker points when user clicks.
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(pixel_coords) < 6:  
            print(f"Clicked at: ({x}, {y})")
            pixel_coords.append((x, y))
        if len(pixel_coords) == 6:
            print("All 6 markers selected! Close the window.")
            cv2.destroyAllWindows()

cv2.setMouseCallback("Click on 6 markers", get_pixel_coordinates)

print("Click on all 6 markers (1 to 6) in the correct order... Press ESC when done.")
cv2.waitKey(0)
cv2.destroyAllWindows()

# Ensure exactly 6 points were selected
if len(pixel_coords) != 6:
    raise ValueError(f"Error: You selected {len(pixel_coords)} points instead of 6. Please retry.")

# Convert pixel coordinates to NumPy array
pixel_coords = np.array(pixel_coords, dtype=np.float32)
print("\nPixel Coordinates (u, v):", pixel_coords)

# Define 3D World Coordinates
inch_to_meter = 0.0254  

# Measured world coordinates (in meters)
world_coords = np.array([
    [0, 0.3048, 0],   # Right wall marker 1
    [0.2286, 0.3048, 0],  # Right wall marker 2 
    [0.1778, 0, 0.0762],  # Floor marker 3 
    [0.0762, 0, 0.0762],  # Floor marker 4 
    [0.2032, 0.3048, 0],  # Left wall marker 5 
    [0.127, 0, 0.2032]    # Left wall marker 6 
])

print("\nWorld Coordinates (X, Y, Z):", world_coords)

# DLT Algorithm to Compute Projection Matrix
def dlt_homography(world_points, image_points):
    # Compute camera projection matrix P using Direct Linear Transform (DLT).
    if len(world_points) != len(image_points):
        raise ValueError("Number of world points and image points must match!")

    A = []
    for i in range(len(world_points)):
        X, Y, Z = world_points[i]
        u, v = image_points[i]
        
        A.append([-X, -Y, -Z, -1, 0, 0, 0, 0, u*X, u*Y, u*Z, u])
        A.append([0, 0, 0, 0, -X, -Y, -Z, -1, v*X, v*Y, v*Z, v])
    
    A = np.array(A)
    _, _, Vh = np.linalg.svd(A)
    P = Vh[-1].reshape(3, 4)  
    return P

# Compute Projection Matrix
P = dlt_homography(world_coords, pixel_coords)
print("\nEstimated Camera Projection Matrix (P):\n", P)

# Decompose P into Intrinsic (K), Rotation (R), and Translation (t)
def decompose_projection_matrix(P):
    # Decompose P into intrinsic matrix K, rotation R, and translation t.
    M = P[:, :3]  # Extract first 3 columns
    K, R = rq(M)  # Use scipy RQ decomposition

    # Normalize K so that K[2,2] = 1
    K /= K[2, 2]

    # Ensure K has positive diagonal values
    T = np.diag(np.sign(np.diag(K)))
    K = K @ T
    R = T @ R

    # Ensure (det(R) = 1)
    if np.linalg.det(R) < 0:
        R = -R

    # Compute translation vector t
    t = np.linalg.inv(K) @ P[:, 3]

    return K, R, t

# Extract Camera Parameters
K, R, t = decompose_projection_matrix(P)
print("\nIntrinsic Matrix (K):\n", K)
print("\nRotation Matrix (R):\n", R)
print("\nTranslation Vector (t):\n", t)

# Compute Camera Position
camera_position = -np.linalg.inv(R) @ t
print("\nEstimated Camera Position (Cx, Cy, Cz):", camera_position)

# Compare with Physically Measured Camera Position
try:
    print("\nphysically measured camera position (in meters):")
    your_Cx = float(input("Cx: "))
    your_Cy = float(input("Cy: "))
    your_Cz = float(input("Cz: "))

    measured_position = np.array([your_Cx, your_Cy, your_Cz])
    error = np.abs(camera_position - measured_position)
    print("\nError between estimated and measured position:", error)
except ValueError:
    print("\nNo manual camera position entered. Skipping error calculation.")
