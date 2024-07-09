import cv2
import numpy as np

def detect_slant_angle(pre_processed_image):
    rows, cols = pre_processed_image.shape
    optimal_shear = None
    max_projection = 0
    
    # Dynamic range based on empirical data or prior knowledge about the handwriting style
    shear_range = np.linspace(-0.5, 0.5, 100)  # More precise with 100 steps

    for shear in shear_range:
        M = np.float32([[1, shear, 0], [0, 1, 0]])
        sheared_image = cv2.warpAffine(pre_processed_image, M, (cols, rows))

        # Calculate the vertical projection
        vertical_projection = np.sum(sheared_image, axis=0)
        projection_sum = np.max(vertical_projection)

        # Update max projection and optimal shear factor
        if projection_sum > max_projection:
            max_projection = projection_sum
            optimal_shear = shear

    slant_angle = np.degrees(np.arctan(optimal_shear))
    return slant_angle

def extract_slant(pre_processed_lines):
    slant_angles = []

    for line in pre_processed_lines:
        slant_angle = detect_slant_angle(line)
        slant_angles.append(slant_angle)

    # Calculate the mean slant angle across all lines
    mean_slant_angle = np.mean(slant_angles)
    return mean_slant_angle

# Example usage:
# pre_processed_img = cv2.imread('path_to_your_pre_processed_image.jpg', cv2.IMREAD_GRAYSCALE)
# lines = [line1, line2, line3]  # Replace with actual segmented pre-processed lines
# mean_slant = extract_slant_from_lines(lines)
# print("Mean Slant Angle:", mean_slant)
