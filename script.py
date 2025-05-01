import cv2
import numpy as np

# Load the images
pattern_img = cv2.imread('pattern.jpg')
flag_img = cv2.imread('flag.png')

# Check if images are loaded correctly
if pattern_img is None or flag_img is None:
    print("Error: Image not found")
    exit()

# Get dimensions of the flag
flag_height, flag_width = flag_img.shape[:2]

# Define points on the pattern image
src_pts = np.array([[0, 0], [pattern_img.shape[1], 0], [pattern_img.shape[1], pattern_img.shape[0]], [0, pattern_img.shape[0]]], dtype='float32')

# Define corresponding destination points on the flag (adjust these based on your flag)
dst_pts = np.array([[100, 50], [flag_width - 100, 50], [flag_width - 100, flag_height - 50], [100, flag_height - 50]], dtype='float32')

# Compute the perspective transform matrix
matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

# Warp the pattern image to the flag's perspective
warped_pattern = cv2.warpPerspective(pattern_img, matrix, (flag_width, flag_height))

# Create a mask where the pattern will be applied
mask = np.zeros((flag_height, flag_width), dtype=np.uint8)

# Fill the mask in the region where the pattern should appear (inside the flag's fold region)
cv2.fillConvexPoly(mask, np.int32(dst_pts), (255))

# Apply the mask to the flag image (keep the background intact)
flag_masked = cv2.bitwise_and(flag_img, flag_img, mask=mask)

# Now blend the warped pattern only with the masked flag
pattern_masked = cv2.bitwise_and(warped_pattern, warped_pattern, mask=mask)

# Add the flag and the pattern together in the masked region
final_output = cv2.add(flag_masked, pattern_masked)

# Save the final output image
cv2.imwrite('Output.jpg', final_output)

# Display the result (optional)
cv2.imshow('Final Output', final_output)
cv2.waitKey(0)
cv2.destroyAllWindows()
