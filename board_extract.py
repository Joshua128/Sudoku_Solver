import cv2
import numpy as np
from keras.models import load_model
def get_corners(contour):
    # approximate the contour
    epsilon = 0.1 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) == 4:
        return np.array([pt[0] for pt in approx], dtype='float32') #returns coordinats of points
    return None

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    rect[0] = pts[np.argmin(s)]     
    rect[2] = pts[np.argmax(s)]      
    rect[3] = pts[np.argmax(diff)]   
    rect[1] = pts[np.argmin(diff)]   

    return rect
def is_cell_empty(cell):
    return cv2.countNonZero(cell) < 345  




def get_board():
    image = cv2.imread("sudoku_board.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    edges = cv2.Canny(thresh, 50, 150)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)

    corner_array = get_corners(largest_contour)
    rect = order_points(corner_array)
    (tl, tr, br, bl) = rect
    width = height = 450
    dst = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(gray, M, (width, height))

    #now get each individual cell. Each cell must have a 450/9 x 450/9 size ie a 25x25 size
    #can get each cell in row major format by going along the rows (double loop with rows on outer)

    cell_size = width // 9
    cells = []
    for i in range(9):
        for j in range(9):
            x = j * cell_size
            y = i * cell_size
            cell = warped[y:y + cell_size, x:x + cell_size]
            cells.append(cell)



    
    processed_cells = []
    for cell in cells:
        thresh = cv2.adaptiveThreshold(cell, 255, 1, 1, 11, 2)
        if not is_cell_empty(thresh):
            digit = cv2.resize(thresh, (28, 28))  # for MNIST-like CNNs
            digit = digit.astype("float32") / 255.0
            processed_cells.append(digit)
        else:
            processed_cells.append(None)

    model = load_model("MNIST_keras_CNN.h5",compile=False)  

    board = []
    for cell in processed_cells:
        if cell is None:
            board.append(0)
        else:
            input = cell.reshape(1, 28, 28, 1)

            pred = np.argmax(model.predict(input))
        
            board.append(pred)

    # Convert to 9x9 grid
    sudoku_grid = np.array(board).reshape(9, 9)
    return sudoku_grid
