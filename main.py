import boto3
import logging
import cv2
import sys # Import sys for exit
import os # Import os to access environment variables
from dotenv import load_dotenv # Import dotenv to load .env file

# Load environment variables from .env file
load_dotenv()

# --- Configuration and Initialization ---
# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("rekognition_app.log"),
                        logging.StreamHandler()
                    ])

# Retrieve AWS region from environment variables
REGION_NAME = os.getenv('AWS_REGION')
if not REGION_NAME:
    logging.error("AWS region (AWS_REGION) not found in environment variables or .env file.")
    sys.exit(1)


def initialize_rekognition():
    """Initializes and returns the AWS Rekognition client.

    Retrieves AWS credentials and region from environment variables.
    Exits the script if credentials or region are missing or if initialization fails.

    Returns:
        boto3.client: An initialized Rekognition client instance.
    """
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    if not aws_access_key_id or not aws_secret_access_key:
        logging.error("AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) not found.")
        sys.exit(1)

    try:
        rek_client = boto3.client('rekognition',
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name=REGION_NAME)
        logging.info(f"Successfully initialized Rekognition client in region '{REGION_NAME}'.")
        return rek_client
    except Exception as e:
        logging.error(f"Error initializing Rekognition client: {e}")
        sys.exit(1)

def open_camera(index=0):
    """Opens the specified camera device.

    Args:
        index (int): The index of the camera device to open (default is 0).

    Returns:
        cv2.VideoCapture: The camera capture object.

    Raises:
        RuntimeError: If the camera cannot be opened.
    """
    logging.info(f"Attempting to open camera at index {index}...")
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        logging.error(f"Cannot open camera at index {index}.")
        raise RuntimeError(f"Cannot open camera at index {index}")
    logging.info(f"Camera at index {index} opened successfully.")
    return cap

def draw_labels(frame, labels):
    """Draws detected labels onto the video frame.

    Args:
        frame (numpy.ndarray): The video frame to draw on.
        labels (list): A list of labels detected by Rekognition,
                       each label being a dictionary with 'Name' and 'Confidence'.
    """
    y0 = 30 # Initial y-coordinate for the first label
    dy = 20 # Vertical spacing between labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_thickness = 1
    text_color = (0, 255, 0) # Green
    bg_color = (0, 0, 0) # Black
    margin = 5 # Margin around text

    for label in labels:
        text = f"{label['Name']} ({label['Confidence']:.1f}%)"

        # Get text size to draw background rectangle
        (w, h), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)

        # Draw background rectangle
        cv2.rectangle(frame, (margin, y0 - h - margin), (margin + w + margin, y0 + baseline + margin), bg_color, cv2.FILLED)

        # Draw label text
        cv2.putText(frame, text, (margin + margin, y0 + baseline // 2), font, font_scale, text_color, font_thickness)

        # Update y-coordinate for the next label
        y0 += h + baseline + dy

    logging.debug("Labels overlaid on frame.")

def process_frames(cap, rek_client):
    """Reads frames from the camera, performs label detection, and displays results.

    Args:
        cap (cv2.VideoCapture): The camera capture object.
        rek_client (boto3.client): The initialized Rekognition client.
    """
    while True:
        logging.debug("Reading frame from camera...")
        ret, frame = cap.read()
        if not ret:
            logging.warning("Failed to retrieve frame from camera. Exiting loop.")
            break

        # --- Frame Processing and Rekognition ---
        logging.debug("Encoding frame to JPEG...")
        success, img_buffer = cv2.imencode('.jpg', frame)
        if not success:
            logging.warning("Failed to encode frame.")
            continue
        logging.debug("Frame encoded successfully.")

        try:
            logging.info("Calling Rekognition detect_labels API...")
            response = rek_client.detect_labels(
                Image={'Bytes': img_buffer.tobytes()},
                MaxLabels=10,
                MinConfidence=75
            )
            labels = response.get('Labels', [])
            logging.info(f"Rekognition detected {len(labels)} labels.")
            logging.debug(f"Rekognition response: {response}")
        except Exception as e:
            logging.error(f"Error calling Rekognition API: {e}")
            continue # Skip this frame if Rekognition fails

        # --- Displaying Results ---
        draw_labels(frame, labels)
        cv2.imshow('Live Labels', frame)
        logging.debug("Frame displayed.")

        # --- User Input for Exit ---
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            logging.info("'q' key pressed. Exiting loop.")
            break

def main():
    """Main function to run the Rekognition live label detection application."""
    rek_client = None
    cap = None
    try:
        # Initialize AWS Rekognition client
        rek_client = initialize_rekognition()

        # Open the camera
        cap = open_camera(index=0)

        # Start processing frames
        process_frames(cap, rek_client)

    except RuntimeError as e:
        logging.error(f"Runtime Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        # --- Cleanup --- 
        logging.info("Starting cleanup...")
        if cap:
            logging.info("Releasing camera resource...")
            cap.release()
        logging.info("Destroying OpenCV windows...")
        cv2.destroyAllWindows()
        logging.info("Application finished.")

# --- Script Execution --- 
if __name__ == "__main__":
    main()
