import os
import spacy
import pandas as pd
import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from tqdm.notebook import tqdm
from collections import Counter

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
        return [token.text.lower() for token in word_tokenize(text)]
    
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
    def __init__(self, data_dir: str, captions_file: str, transform=None, freq_threshold: int=5):
        # Data path
        self.data_dir = data_dir
        # Image captions dataframe
        self.df = pd.read_csv(captions_file)
        # Transform value
        self.transform = transform
        
        # Images and captions from DF
        self.images = self.df['image']
        self.captions = self.df['caption']
        
        # Build vocabulary
        self.vocab = Vocabulary(freq_threshold)
        self.vocab.build_vocabulary(self.captions.tolist())
        self.freq_threshold = freq_threshold
        self.max_caption_length = self.get_max_caption_length()
        
    def get_max_caption_length(self):
        max_length = 0
        for caption in self.captions:
            tokenized_caption = self.vocab.vocab_tokenizer(caption)
            max_length = max(max_length, len(tokenized_caption))
        
        return max_length 
    
    def padded_caption(self, caption):
        padded_caption = caption[:self.max_caption_length]
        padded_caption += [self.vocab.stoi["<PAD>"]] * (self.max_caption_length - len(caption))
        return padded_caption

    def __len__(self):
        return len(self.df)  
    
    def __getitem__(self, idx: int):
        caption = self.captions[idx]
        img_dir = self.images[idx]
        img = Image.open(os.path.join(self.data_dir, img_dir)).convert('RGB')
        
        if self.transform is not None:
            img = self.transform(img)
        
        one_hot_caption = [self.vocab.stoi['<SOS>']]
        one_hot_caption.extend(self.vocab.to_one_hot(caption))
        one_hot_caption.append(self.vocab.stoi['<EOS>'])
        
        padded_vector = self.padded_caption(one_hot_caption)

        
        return img, torch.tensor(padded_vector)

def get_loader(data_dir, captions_file, transform=None, 
               batch_size=16, num_workers=2, shuffle=True, pin_memory=True):
    
    dataset = ImageCaptionDataset(data_dir=data_dir, captions_file=captions_file, transform=transform)
    
    pad_idx = dataset.vocab.stoi['<PAD>']
    
    data_loader  = DataLoader(dataset=dataset, batch_size=batch_size,
                         num_workers=num_workers, shuffle=shuffle,
                         pin_memory=pin_memory) 
    
def main():
    img_dir = 'data/Images/'
    captions_file = 'data/captions.txt'
    
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ]
        
    )

    dataloader = get_loader(data_dir=img_dir, 
                            captions_file=captions_file,
                            transform=transform)

    for idx, (imgs, captions) in enumerate(dataloader):
        print(imgs.shape)
        print(captions.shape)

if __name__ == "__main__":
    main()
    