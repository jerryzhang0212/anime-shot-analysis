import cv2

def draw_rule_of_thirds_grid(input_path, output_path):
    img = cv2.imread(input_path)
    h, w, _ = img.shape

    # rule of thirds lines
    lines = [
        (0, h//3), (0, 2*h//3),  # horizontal
        (w//3, 0), (2*w//3, 0)   # vertical
    ]

    # draw
    img2 = img.copy()
    cv2.line(img2, (0, h//3), (w, h//3), (0,255,0), 2)
    cv2.line(img2, (0, 2*h//3), (w, 2*h//3), (0,255,0), 2)
    cv2.line(img2, (w//3, 0), (w//3, h), (0,255,0), 2)
    cv2.line(img2, (2*w//3, 0), (2*w//3, h), (0,255,0), 2)

    cv2.imwrite(output_path, img2)