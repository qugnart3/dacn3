from SetModel import Model
from Tokenize import Tokenize
import os
import torch

# Lấy đường dẫn hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(current_dir, "DataSet")

# Load và xử lý dữ liệu
data_train_return = Tokenize(
    os.path.join(dataset_dir, "train", "sents.txt"),
    os.path.join(dataset_dir, "train", "sentiments.txt")
)
data_test_return = Tokenize(
    os.path.join(dataset_dir, "test", "sents.txt"),
    os.path.join(dataset_dir, "test", "sentiments.txt")
)

# Khởi tạo và train model
model = Model("wonrax/phobert-base-vietnamese-sentiment")
model.Train(
    data_train_return,
    data_test_return,
    learning_rate=5e-5,
    epoch=10,  # Tăng số epoch để model học tốt hơn
    save_model="NotProcess"
)

# Save model weights
model_save_path = os.path.join(current_dir, "SetModel", "NotProcess", "Model", "model.safetensors")
print(f"Model saved to: {model_save_path}")
