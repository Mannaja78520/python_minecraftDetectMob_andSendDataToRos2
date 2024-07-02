from ultralytics import YOLO

# Load the YOLO model
model = YOLO('runs/detect/train5/weights/best.pt')  # Use your custom model if you have one

# Load and preprocess the image
image = 'Screenshot from 2024-07-02 21-11-55.png'
# Run predictions
results = model.predict(image)

# Display results
results[0].save()