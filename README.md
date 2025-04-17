# Rekognition Live Label Detection

This Python application uses the AWS Rekognition service to detect and display labels in real-time video from a connected camera. It leverages the OpenCV library for video capture and display, and the boto3 library for interacting with the AWS Rekognition API.

## Introduction

The Rekognition Live Label Detection application is designed to provide a seamless experience for real-time object and scene detection using the powerful AWS Rekognition service. By leveraging the computer vision capabilities of Rekognition, this application can identify and label various objects, people, activities, and more in the live video feed from a connected camera.

The application continuously captures frames from the camera, sends them to the Rekognition service for label detection, and overlays the detected labels on the video display. This real-time labeling can be useful in various scenarios, such as security monitoring, object tracking, or educational purposes.

## Features

- Real-time label detection using AWS Rekognition
- Video capture and display using OpenCV
- Configurable label detection parameters (e.g., maximum labels, minimum confidence)
- Logging for monitoring and debugging
- Environment variable configuration for AWS credentials and region

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/rekognition-live-label-detection.git
```

2. Navigate to the project directory:

```bash
cd rekognition-live-label-detection
```

3. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Set up the required environment variables:

   - `AWS_ACCESS_KEY_ID`: Your AWS access key ID
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
   - `AWS_REGION`: The AWS region where you want to use the Rekognition service (e.g., `us-east-1`)

   You can either set these variables in your system's environment variables or create a `.env` file in the project directory with the following content:

   ```
   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   AWS_REGION=your_aws_region
   ```

## Usage

1. Ensure that you have a camera connected to your system.

2. Run the application:

```bash
python main.py
```

3. The application will initialize the Rekognition client, open the camera, and start processing frames. Detected labels will be overlaid on the video display.

4. Press the `q` key to exit the application.

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

When contributing, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and ensure that the code follows the project's coding style and conventions.
3. Write tests for your changes, if applicable.
4. Update the documentation (README.md, docstrings, etc.) if necessary.
5. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).