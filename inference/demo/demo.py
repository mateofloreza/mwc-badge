import cv2
import pytesseract
from ultralytics import YOLO
model = YOLO('best.pt')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    results = model(frame)
    for result in results:
        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box[:4])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Extract the region of interest (ROI) from the frame
            roi = frame[y1:y2, x1:x2]

            # Convert to grayscale for better OCR accuracy
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to clean up the text
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # Extract text using Tesseract
            text = pytesseract.image_to_string(thresh)

            print("Detected Text:", text)


            # Define the top-right rectangle parameters
            overlay_x1, overlay_y1 = frame.shape[1] - 250, 10  # Adjust the size/position as needed
            overlay_x2, overlay_y2 = frame.shape[1] - 10, 60

            # Draw the rectangle (background for text)
            cv2.rectangle(frame, (overlay_x1, overlay_y1), (overlay_x2, overlay_y2), (0, 0, 0), -1)  # Black filled rectangle

            # Put text inside the rectangle
            cv2.putText(frame, text.strip(), (overlay_x1 + 10, overlay_y1 + 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)



    cv2.imshow('Camera', frame)


    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
