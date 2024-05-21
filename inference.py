
import torch
from model import HandGestureGCN
from torch_geometric.data import Data
import json

def load_landmarks(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        landmarks = data['pts']
        return landmarks

def inference(model, landmarks, device):
    # Create a Data object from the landmark points
    x = torch.tensor([[pt["x"], pt["y"]] for pt in landmarks.values()], dtype=torch.float)
    edge_index = torch.tensor([[i, j] for i in range(21) for j in range(21) if i != j], dtype=torch.long).t().contiguous()
    data = Data(x=x, edge_index=edge_index)
    
    # Move the data to the specified device (CPU or GPU)
    data = data.to(device)
    
    # Set the model to evaluation mode
    model.eval()
    
    # Perform forward pass
    with torch.no_grad():
        out = model(data)
        pred = out.argmax(dim=1)
    
    return pred.item()

def main():
    # Set the path to the trained model
    model_path = "models/model.pth"
    
    # Check if GPU is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load the trained model
    model = HandGestureGCN(num_features=2, num_classes=34)  # Update the number of classes to match the trained model
    model.load_state_dict(torch.load(model_path))
    model.to(device)
    
    # Set the path to the input JSON file
    json_file = "input_landmarks.json"
    
    # Load the landmark points from the JSON file
    landmarks = load_landmarks(json_file)
    
    # Perform inference using the trained model
    predicted_class = inference(model, landmarks, device)
    
    # Print the predicted class
    print(f"Predicted class: {predicted_class}")

if __name__ == "__main__":
    main()
