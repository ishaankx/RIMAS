from ultralytics import YOLO

# Load the YOLOv8 model - Start with a pre-trained 'small' model for better accuracy
model = YOLO('yolov8s.pt')  # Use 'yolov8n.pt' for nano or 'yolov8m.pt' for medium if needed

# Train the model on your custom dataset
model.train(
    data='F:/rimas/rimas/RIMAS.v2i.yolov8/data.yaml',  # Path to dataset YAML
    epochs=100,                # Increased epochs for more training
    imgsz=640,                 # Input image size
    batch=16,                  # Batch size (adjust based on your GPU memory)
    lr0=0.001,                 # Initial learning rate
    optimizer='AdamW',         # Use AdamW optimizer for better convergence
    patience=30,               # Early stopping if validation loss doesn't improve
    workers=4,                 # Number of data loader workers (adjust based on system)
    augment=True,              # Enable advanced augmentation
    perspective=0.01,          # Slight perspective adjustments
    flipud=0.5,                # Random vertical flip
    fliplr=0.5,                # Random horizontal flip
    mosaic=True,               # Mosaic augmentation for small object detection
    mixup=0.1,                 # Mixup augmentation for varied training data
    box=0.05,                  # Box loss gain
    cls=0.5,                   # Classification loss gain
    label_smoothing=0.1,       # Reduce overfitting by smoothing labels
    val=True                   # Evaluate on validation set after every epoch
)
