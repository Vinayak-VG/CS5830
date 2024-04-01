import torch
import gc

def accuracy(y_pred, y):
    _, predicted = torch.max(y_pred.data, 1)
    total = y.size(0)
    correct = (predicted == y).sum().item()
    return correct/total

####################################################################################################################

def train_(model, dataset, optimizer, criterion, device):

    train_loss_batch = []
    accu_train_batch = []
    model.train()
    for idx,(images, labels) in enumerate(dataset):
        
        # Loading the Images and Labels
        images = images.to(device)
        labels = labels.to(device)
        
        # Forward Pass
        output = model(images)
        
        # Calculating Loss
        train_loss = criterion(output,labels)
        train_loss_batch.append(train_loss)
        
        # Calculating Accuracy
        acc = accuracy(output, labels)
        accu_train_batch.append(acc)

        # Backward Pass
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()
    
    return sum(train_loss_batch)/len(dataset), sum(accu_train_batch)/len(dataset)

def test_(model, dataset, criterion, device):

    test_loss_batch = []
    accu_test_batch = []
    model.eval()
    for idx,(images, labels) in enumerate(dataset):
        with torch.no_grad():
            images = images.to(device)
            labels = labels.to(device)
            #Forward Pass
            output = model(images)
            # Loss
            test_loss = criterion(output,labels)
            test_loss_batch.append(test_loss)
            acct = accuracy(output, labels)
            accu_test_batch.append(acct)
    
    return sum(test_loss_batch)/len(dataset), sum(accu_test_batch)/len(dataset)

# Main Trainer Function
def trainer(epochs, model, trainloader, testloader, criterion, optimizer, device):
    epoch_train_losses = []
    epoch_test_losses = []
    accu_train_epoch = []
    accu_test_epoch = []

    # Start Training
    for epoch in range(epochs):
        
        print(f"Epoch: {epoch + 1}")
        epoch_loss, epoch_acc = train_(model, trainloader, optimizer, criterion, device) # Training
        test_loss, test_acc = test_(model, testloader, criterion, device) # Testing
        
        # Logging the losses and accuracy in a list for plotting
        epoch_train_losses.append(epoch_loss)
        epoch_test_losses.append(test_loss)
        accu_train_epoch.append(epoch_acc)
        accu_test_epoch.append(test_acc)

        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.empty_cache()
        gc.collect()
        print(f"Train Loss - {epoch_loss}    Train Acc - {epoch_acc}")
        print(f"Test Loss - {test_loss}    Test Acc - {test_acc}")

    
    print("OVERALL TRAINING COMPLETE")
    
    return epoch_train_losses, epoch_test_losses, accu_train_epoch, accu_test_epoch