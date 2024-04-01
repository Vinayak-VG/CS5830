from PIL import Image
from torch.utils.data import Dataset
import os
from glob import glob
import torch
import torchvision
import torchvision.transforms as transforms
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data import random_split
from torch.utils.data.sampler import SubsetRandomSampler
from torchsummary import summary
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from dataset import MNIST
from model import Model
from trainer import train_, test_, trainer
from monitor_perf import monitor_perf

# Hyperparameters
batch_size = 32
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
epochs = 10
lr = 0.001

# Dataset Loading
trainset = MNIST(root_dir='mnist_png', mode='train', rotate_list=[''], perc_data=0.05)  # 0.05 is the amount of data required to achieve 95% acc on the monitor dataset
testset = MNIST(root_dir='mnist_png', mode ='test', rotate_list=[''], perc_data=1)

# Splitting the Testset into Monitorset for Monitoring purposes.
testset, monitorset = random_split(testset, [int(0.95*len(testset)), len(testset) - int(0.95*len(testset))])

trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=2)
testloader = DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=2)
monitorloader = DataLoader(monitorset, batch_size=batch_size, shuffle=False, num_workers=2)

# Loading the loss function, model and optimizer
criterion = nn.CrossEntropyLoss()
model = Model().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr)

# Entire Training
epoch_train_losses, epoch_test_losses, accu_train_epoch, accu_test_epoch = trainer(epochs, model, trainloader, testloader, criterion, optimizer, device)

# Plotting
plt.plot(accu_test_epoch, label='Testing Accuracy')
plt.legend()
plt.savefig("plot.png")

# Monitoring
flag, total_monitor_acc = monitor_perf(model, monitorloader, threshold=0.95, device=device)
if flag == 0:
    print(f"Drift observed from the model with Accuracy = {total_monitor_acc}")
else:
    print(f"Model is performing optimally with Accuracy = {total_monitor_acc}")
