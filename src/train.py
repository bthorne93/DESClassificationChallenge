import torch 
import logging
from sklearn.metrics import roc_auc_score, precision_score, recall_score, det_curve
import wandb 
from .plotting import plot_mdr

def do_training(model, optimizer, metric, train, test, device, epochs):
    model.to(device)
    for epoch in range(epochs):
        logging.info(f"Epoch {epoch + 1} / {epochs}")
        model.train()
        running_loss = 0.

        for inputs, labels in train:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = metric(outputs.squeeze(), labels.squeeze())
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        train_epoch_loss = running_loss / len(train)

        model.eval()
        running_loss = 0.
        
        true_labels = []
        score = []
        for inputs, labels in test:
            inputs, labels = inputs.to(device), labels.to(device)
            with torch.no_grad():
                outputs = model(inputs)
                loss = metric(outputs.squeeze(), labels.squeeze())
            running_loss += loss.item()

            true_labels.extend(labels.squeeze())
            score.extend(outputs.squeeze())

        test_epoch_loss = running_loss / len(test)

        true_labels = torch.stack(true_labels).cpu().squeeze()
        score = torch.stack(score).cpu().squeeze()
        predicted_labels = torch.round(score)

        # This is required because wandb has weird requirements for argument ro ROC curve plot.
        per_class_score_for_wandb_roc_curve = torch.hstack(
            [(1 - score).unsqueeze(-1), 
            score.unsqueeze(-1)]
        )
        wandb.log({
            "MDR": plot_mdr(true_labels, score),
            "Epoch": epoch,
            "Train Loss": train_epoch_loss,
            "Test Loss": test_epoch_loss,
            "roc": wandb.plot.roc_curve(y_true=true_labels, y_probas=per_class_score_for_wandb_roc_curve),
            "Test AUC": roc_auc_score(true_labels, score),
            "Test Precision": precision_score(true_labels, predicted_labels),
            "Test Recall": recall_score(true_labels, predicted_labels),
        })

        torch.save(model.state_dict(), f"checkpoints/model_checkpoint_epoch_{epoch + 1}.pt")
        wandb.save(f"checkpoints/model_checkpoint_epoch_{epoch + 1}.pt")

    return model

