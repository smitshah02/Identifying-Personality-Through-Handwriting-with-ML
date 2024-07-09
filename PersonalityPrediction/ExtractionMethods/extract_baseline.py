import cv2
import numpy as np

def pre_processing(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply adaptive thresholding to create a binary image
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return binary

def find_optimal_skew_angle(img, initial_rotation_angle=1, precision=0.1):
    def rotate_image(image, angle):
        M = cv2.getRotationMatrix2D((image.shape[1] // 2, image.shape[0] // 2), angle, 1)
        rotated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def calculate_horizontal_projection_sum(image):
        return np.sum(image, axis=1)

    img_binarized = pre_processing(img)

    best_angle = 0
    max_sum = calculate_horizontal_projection_sum(img_binarized).max()
    for direction in [-1, 1]:  # Try both clockwise and anticlockwise
        angle = 0
        while abs(angle) <= 40:
            angle += direction * initial_rotation_angle
            rotated = rotate_image(img_binarized, angle)
            horizontal_sum = calculate_horizontal_projection_sum(rotated).max()

            if horizontal_sum > max_sum:
                max_sum = horizontal_sum
                best_angle = angle

            # Increase precision after finding an approximate angle
            if direction * angle >= 10:
                initial_rotation_angle = precision

    return best_angle

def detect_and_correct_baseline(img):
    optimal_angle = find_optimal_skew_angle(img)
    M = cv2.getRotationMatrix2D((img.shape[1] // 2, img.shape[0] // 2), optimal_angle, 1)
    corrected_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return corrected_img, optimal_angle

# Usage example:
# img = cv2.imread('path_to_your_image.jpg')
# corrected_img, skew_angle = correct_baseline_skew(img)
# cv2.imshow('Corrected Image', corrected_img)
# cv2.waitKey(0)
