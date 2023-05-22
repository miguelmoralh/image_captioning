import torch
from get_loader_v2_train_val_test import show_image
import matplotlib.pyplot as plt
from torch.optim.lr_scheduler import ReduceLROnPlateau
import nltk
from utils.utils import best_bleu_cap


def validate(criterion, model, loader, device): # vocab tendria q ser train_vocab_df

    model.eval()
    total_loss = 0
    total_samples = 0

    with torch.no_grad():
        for images, captions in loader:
            images = images.to(device)
            captions = captions.to(device)
            batch_size = images.size(0)
            total_samples += batch_size

            outputs = model(images, captions)
            loss = criterion(outputs.view(-1, outputs.size(-1)), captions.view(-1))
            total_loss += loss.item() * batch_size

    average_loss = total_loss / total_samples
    print("Validation set: Average loss: {:.5f}".format(average_loss))
    return average_loss


def train(epoch, criterion, model, optimizer, loader, device):
    
    
    total_samples = 0
    total_loss = 0.0
    print_every = 250

    model.train()

    for batch_idx, (images, captions) in enumerate(loader):
        images = images.to(device)
        captions = captions.to(device)
        batch_size = images.size(0)
        total_samples += batch_size
        optimizer.zero_grad()

        outputs = model(images, captions)
        loss = criterion(outputs.view(-1, outputs.size(-1)), captions.view(-1))
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * batch_size

        if (batch_idx + 1) % print_every == 0:
            print("Train Epoch: {} Batch [{}/{}]\tLoss: {:.5f}".format(
                epoch, batch_idx + 1, len(loader), loss.item()
            ))

    average_loss = total_loss / total_samples
    print("Train Epoch: {} Average Loss: {:.5f}".format(epoch, average_loss))

    return average_loss
   

def val_visualize_captions(model, train_loader, val_loader, criterion, optimizer, device, vocab_size, vocab, epochs, vocab_val_df):
    print_every = 250
    model.train()
    for epoch in range(1, epochs+1):
        for idx, (image, captions) in enumerate(iter(train_loader)):
                image,captions = image.to(device),captions.to(device)
                
                # Zero the gradients.
                optimizer.zero_grad()

                # Feed forward
                outputs = model(image, captions)
                
                # Calculate the batch loss.
                loss = criterion(outputs.view(-1, vocab_size), captions.view(-1))

                # Backward pass.
                loss.backward()

                # Update the parameters in the optimizer.
                optimizer.step()
                if (idx+1)%print_every == 0:
                    print("Epoch: {} loss: {:.5f}".format(epoch,loss.item()))
                
                    #generate the caption
                    model.eval()
                    with torch.no_grad():
                        dataiter = iter(val_loader)
                        img,captions = next(dataiter)
                        caption = captions[0:1][0].tolist() 
                        s = [vocab_val_df[idx] for idx in caption if idx != 0] # if idx != 0 and idx != 1 and idx != 2 (to erase eos and sos if we want idx 1 and 2)
                        print("Original:", ' '.join(s))
                        features = model.encoder(img[0:1].to(device))
                        print(f"features shape - {features.shape}")
                        #print(f"True captions of the image:\n {true_caps}")
                        print("Predicted caption:")
                        caps = model.decoder.generate_caption(features.unsqueeze(0),vocab=vocab)
                        caption = ' '.join(caps)
                        print(caption)
                        show_image(img[0],title=caption)  
                    model.train()
                    


'''

from tqdm.auto import tqdm
import wandb

def train(model, loader, criterion, optimizer, config):
    # Tell wandb to watch what the model gets up to: gradients, weights, and more!
    wandb.watch(model, criterion, log="all", log_freq=10)

    # Run training and track with wandb
    total_batches = len(loader) * config.epochs
    example_ct = 0  # number of examples seen
    batch_ct = 0
    for epoch in tqdm(range(config.epochs)):
        for _, (images, labels) in enumerate(loader):

            loss = train_batch(images, labels, model, optimizer, criterion)
            example_ct +=  len(images)
            batch_ct += 1

            # Report metrics every 25th batch
            if ((batch_ct + 1) % 25) == 0:
                train_log(loss, example_ct, epoch)


def train_batch(images, labels, model, optimizer, criterion, device="cuda"):
    images, labels = images.to(device), labels.to(device)
    
    # Forward pass ➡
    outputs = model(images)
    loss = criterion(outputs, labels)
    
    # Backward pass ⬅
    optimizer.zero_grad()
    loss.backward()

    # Step with optimizer
    optimizer.step()

    return loss


def train_log(loss, example_ct, epoch):
    # Where the magic happens
    wandb.log({"epoch": epoch, "loss": loss}, step=example_ct)
    print(f"Loss after {str(example_ct).zfill(5)} examples: {loss:.3f}")
    
'''