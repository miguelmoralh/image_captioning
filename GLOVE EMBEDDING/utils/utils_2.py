import wandb
import torch
import torch.nn 
import torchvision
import torchvision.transforms as transforms
import numpy as np
from model.model import *
import nltk

def best_bleu_cap(list_original_caps, pred_cap):
    reference_captions = list_original_caps  # Lista de leyendas originales
    generated_caption = pred_cap  # Leyenda generada por el modelo

    best_bleu_score = 0.0
    best_caption = ""

    for reference_caption in reference_captions:
        # Tokenizar las leyendas de referencia y la leyenda generada
        reference_tokens = nltk.word_tokenize(reference_caption)
        generated_tokens = nltk.word_tokenize(generated_caption)
        
        # Calcular el puntaje BLEU
        bleu_score = nltk.translate.bleu_score.sentence_bleu([reference_tokens], generated_tokens)
        
        # Actualizar la mejor puntuación BLEU y la mejor leyenda
        if bleu_score > best_bleu_score:
            best_bleu_score = bleu_score
            best_caption = reference_caption
    
    return best_caption, best_bleu_score


def weights_matrix(vocab, emb_dim, glove_embedding):
    """
    Input:
        - Vocabulary of dataset format -> {idx : word}
        - Embedding dimension
        
    Function returns a matrix with weight values that reresent the pretrained embedding.
    """
    matrix_len = len(vocab)
    weights_matrix = np.zeros((matrix_len, 50))
    words_found = 0

    for i, word in enumerate(vocab):
        try: 
            weights_matrix[i] = glove_embedding[word]
            words_found += 1
        except KeyError:
            weights_matrix[i] = np.random.normal(scale=0.6, size=(emb_dim, ))
    
    return weights_matrix