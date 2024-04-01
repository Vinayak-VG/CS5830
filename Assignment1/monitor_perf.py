import torch


def accuracy(y_pred, y):
    _, predicted = torch.max(y_pred.data, 1)
    total = y.size(0)
    correct = (predicted == y).sum().item()
    return correct/total

##### Task 4 ######

def monitor_perf(model, dataset, threshold, device):
    
    # I have done the Monitoring of Performance in terms of Accuracy and not loss since comparing loss is difficult in real-world situations 
    # and accuracy is an easier way to track and adjust.
    
    monitor_acc = []
    model.eval()
    for idx,(images, labels) in enumerate(dataset):
        with torch.no_grad():
            # Loading the Images and Labels
            images = images.to(device)
            labels = labels.to(device)
            
            # Prediction by our model
            output = model(images)
            
            # Calculating the Accuracy of our model
            acct = accuracy(output, labels)
            monitor_acc.append(acct)
    total_monitor_acc = sum(monitor_acc)/len(dataset)
    # Comparing the accuracy to the threshold and raising a flag accordingly. 
    if total_monitor_acc < threshold:
        return 0, total_monitor_acc
    else:
        return 1, total_monitor_acc
