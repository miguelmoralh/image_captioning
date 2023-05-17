import os
import pandas as pd
import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from PIL import Image


# Class to generate the vocabulary for our LSTM
class Vocabulary:
    def __init__(self, freq_threshold: int):
        # Defining some needed tokens for Resnet model
        self.itos = {0:"<PAD>", 1:"<SOS>", 2:"<EOS>", 3:"<UNK>"}
        # Reversed ITOS dict
        self.stoi = {k:v for v,k in self.itos.items() }
        # Frequency threshold indicator, leading to ignore
        self.freq_threshold = freq_threshold
          
    def __len__(self):
        return len(self.itos)
    
    @staticmethod
    def vocab_tokenizer(text: str):
        return [token.lower() for token in word_tokenize(text)]
    
    def build_vocabulary(self, captions):
        frequencies = {}
        # Start idx 4 because of previous itos tokens
        idx = 4
        for caption in captions:
            for word in self.vocab_tokenizer(caption):
                if word not in frequencies:
                    frequencies[word] = 1
                else:
                    frequencies[word] += 1  
                if frequencies[word] == self.freq_threshold:
                    self.stoi[word] = idx
                    self.itos[idx] = word
                    idx += 1      
     
    def to_one_hot(self, text: str):
        tokenized_text = self.vocab_tokenizer(text)
        return [self.stoi[word] if word in self.stoi else self.stoi['<UNK>'] for word in tokenized_text]


# Class for our dataloader to access
class ImageCaptionDataset(Dataset):
    def __init__(self, data_dir, captions_file, transform=None, freq_threshold=5, train_set=True):
        # Data path
        self.data_dir = data_dir
        
        # Image captions dataframe
        df = pd.read_csv(captions_file)
        # Create train or test dataset
        unique = df['image'].unique()
        train_images, test_images = train_test_split(unique, test_size=0.2, random_state=42)
        if train_set:
            self.df = df[df['image'].isin(train_images)]
        else:
            self.df = df[df['image'].isin(test_images)]
            
        # Transform value
        self.transform = transform
        
        # Images and captions from DF
        self.images = self.df['image']
        self.captions = self.df['caption']
        
        # Build vocabulary
        self.vocab = Vocabulary(freq_threshold)
        self.vocab.build_vocabulary(self.captions.tolist())
        self.freq_threshold = freq_threshold

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx: int):
        caption = self.captions.iloc[idx]
        img_dir = self.images.iloc[idx]
        img = Image.open(os.path.join(self.data_dir, img_dir)).convert('RGB')
        
        if self.transform is not None:
            img = self.transform(img)
        
        one_hot_caption = [self.vocab.stoi['<SOS>']]
        one_hot_caption.extend(self.vocab.to_one_hot(caption))
        one_hot_caption.append(self.vocab.stoi['<EOS>'])
        
        return img, torch.tensor(one_hot_caption)
    
    
# Class to PAD our captions
class CollatePadding:
    def __init__(self, pad_idx):
        self.pad_idx = pad_idx
    
    # Work with each batch (Dataset.__getitem__)
    def __call__(self, batch):
        # convert a batch of tensors into a single tensor with an additional batch dimension representing batch size
        imgs = [ item[0].unsqueeze(0) for item in batch ]
        imgs = torch.cat(imgs, dim=0)
        targets = [ item[1] for item in batch ]
        targets = pad_sequence(targets, batch_first=False, padding_value=self.pad_idx)
        
        return imgs, targets
    
        
def get_loader(data_dir, captions_file, transform=None, train_set=True,
               batch_size=16, num_workers=2, shuffle=True, pin_memory=True):
    
    dataset = ImageCaptionDataset(data_dir=data_dir, captions_file=captions_file, transform=transform, train_set=train_set)
    
    pad_idx = dataset.vocab.stoi['<PAD>']
    
    data_loader  = DataLoader(dataset=dataset, batch_size=batch_size,
                         num_workers=num_workers, shuffle=shuffle,
                         pin_memory=pin_memory, collate_fn=CollatePadding(pad_idx=pad_idx)) 
    
    return data_loader, dataset