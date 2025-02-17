import cv2
import pytesseract
import threading
from queue import Queue
from ultralytics import YOLO

model = YOLO('best.pt')
cap = cv2.VideoCapture(0)

# Queue to handle OCR results asynchronously
ocr_queue = Queue()

def ocr_worker():
    """Thread function for processing OCR in the background."""
    while True:
        roi, coords, frame = ocr_queue.get()
        if roi is None:  # Stop signal
            break
        
        # Convert to grayscale and apply thresholding
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Perform OCR
        text = pytesseract.image_to_string(thresh).strip()
        greeting_text = f"Hello {text}"  # Format message

        # Define overlay position
        overlay_x1, overlay_y1 = frame.shape[1] - 300, 10
        overlay_x2, overlay_y2 = frame.shape[1] - 10, 60

        # Draw the black rectangle background
        cv2.rectangle(frame, (overlay_x1, overlay_y1), (overlay_x2, overlay_y2), (0, 0, 0), -1)

        # Put the greeting text on the image
        cv2.putText(frame, greeting_text, (overlay_x1 + 10, overlay_y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        print("Detected Text:", greeting_text)

        ocr_queue.task_done()  # Mark task as completed

# Start the OCR worker thread
ocr_thread = threading.Thread(target=ocr_worker, daemon=True)
ocr_thread.start()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    for result in results:
        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box[:4])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Extract the region of interest (ROI) and send it to the OCR thread
            roi = frame[y1:y2, x1:x2].copy()
            ocr_queue.put((roi, (x1, y1, x2, y2), frame))

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
ocr_queue.put((None, None, None))  # Send stop signal to the OCR thread
ocr_thread.join()
cap.release()
cv2.destroyAllWindows()

