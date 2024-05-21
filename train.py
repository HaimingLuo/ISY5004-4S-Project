import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from data_loader import load_data, create_pairs, HandGestureDataset
from model import SiameseNetwork, contrastive_loss

# 加载数据
print("Loading data...")
data, labels_encoded = load_data()
print("Data loaded successfully.")

# 创建数据对
print("Creating pairs...")
pairs, pairs_labels = create_pairs(data, labels_encoded)
print("Pairs created successfully.")

# 创建数据加载器
print("Creating data loader...")
dataset = HandGestureDataset(pairs, pairs_labels)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
print("Data loader created successfully.")

# 构建模型
print("Building model...")
model = SiameseNetwork()
optimizer = optim.Adam(model.parameters(), lr=0.001)
print("Model built successfully.")

# 训练模型
num_epochs = 50
print("Starting training...")
for epoch in range(num_epochs):
    print(f'Epoch [{epoch+1}/{num_epochs}]')
    for batch_idx, (data1, data2, label) in enumerate(train_loader):
        optimizer.zero_grad()
        output1, output2 = model(data1, data2)
        loss = contrastive_loss(output1, output2, label)
        loss.backward()
        optimizer.step()

        print(f'Batch [{batch_idx+1}/{len(train_loader)}]')
        print(f'Data1: {data1}')
        print(f'Data2: {data2}')
        print(f'Label: {label}')
        print(f'Output1: {output1}')
        print(f'Output2: {output2}')
        print(f'Loss: {loss.item():.4f}\n')

    print(f'End of Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}\n')

# 保存模型
print("Saving model...")
torch.save(model.state_dict(), 'siamese_model.pth')
print("Model saved successfully.")
