# Image Captioning - Group 2 - UAB Deep Learning Course
Our main proposal for this project is to be able to train an image captioning model based on the [Flickr 8k Dataset on Kaggle](https://www.kaggle.com/datasets/adityajn105/flickr8k), which contains 8,091 images and 5 captions for each image.

<br/>

<img src="docs/caption_example.png" width="1000">

*Image 1: Example of an image with its corresponding captions.*

<!-- *Click on Image to open Kaggle Dataset page:* 

[<img src="docs/site-logo.svg" width="120"/>](https://www.kaggle.com/datasets/adityajn105/flickr8k) -->

<br/>

## General Project Structure
Our project is composed by *Python* scripts and notebooks. We made this distinction to make it easy for everyone to diferentiate the already predefined models and methods with the different training runs we did, setting different hyperparameters in order to see differences in results. 

<br/>

## Model architecture
Our model architecture is a combination of an encoder CNN network with a decoder LSTM network of two layers. 

For our CNN encoder we have used the *PyTorch's* pretrained [ResNet-50 model](https://pytorch.org/vision/main/models/generated/torchvision.models.resnet50.html). The softmax from the last layer has been deleted and changed to a fully connected layer that runs through a linear function that feeds the embedding, that afterwards is ran through the first LSTM input.

For our embedding, we have used the 300 dimensions [GloVe pretrained embedding](https://nlp.stanford.edu/projects/glove/). Once the CNN output runs through the embedding, it is sent into the first LSTM cell. To feed the rest of the cells we have used a 100% of teacher forcing, concatenating the image features with the ground-truth words.

<br/>

## How to run the code

> To download and install this repository you can either download the **.zip** on the top of this page or you can install *git* on your PC and run the following command on the location you want the repository to be: `git clone https://github.com/DCC-UAB/dlnn-project_ia-group_2.git`. 

<br/>

In order to replicate the project you will need all the dependencies and libraries that were used to develop the model. On the *environment.yml* file you will find all libraries needed to imitate our model. 

> To install the environment on Anaconda use  `conda env create -f environment.yml`  on the directory where the file is located with the Anaconda console. Change the name of the file if you want to give another name to the environment.

> In order to use that environment, run `conda activate <environment_name>`.

*We will be using PyTorch as our Deep Learning framework, and we highly recommended to use CUDA platform to use the GPU potential in order to train the model.*

<br/>

As external files, you will need:

* The *data* folder, which contains the *Flickr8k* dataset, formed by a folder with 8,091 images, and a **.txt** with 5 captions for each image.
    * In order to run the last model we trained, you will also have to download the [*Flickr30k Dataset on Kaggle*](https://www.kaggle.com/datasets/adityajn105/flickr30k).
* The *GloVe Embedding* folder, which contains the **.pkl** files and the data files in order to train the LSTM decoder with a pretrained embedding.
    * It is recommended to download the data from [the GloVe official site](https://nlp.stanford.edu/projects/glove/). 
    * We will be using the 300 dimensions embedding: *Wikipedia 2014 + Gigaword 5 (6B tokens, 400K vocab, uncased, 50d, 100d, 200d, & 300d vectors, 822 MB):* [glove.6B.zip](https://nlp.stanford.edu/data/glove.6B.zip). 
    * In order to use the embedding, you will have to use the [generate_embedding_data.py](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/generate_embedding_data.py) script with the defined path to the unzipped folder.
    
<br/>

## Code Structure

### General files:
* The *README.md* is this file which explains the repository information.
* The *environment.yml* file contains all the python dependencies that are needed to replicate our model experiments and to execute all scripts.

### Folders:
* The *300dim_embedding* is a folder used for the pretrained embedding with all needed files *(.pkl, data folder...)* inside. It is generated by the [generate_embedding_data.py](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/generate_embedding_data.py), as mentioned before.

* The *8k_data* and *30k_data* folders will contain all the data needed. You should install these by yourself. Links shared before.  

* The [**model**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/tree/main/model) folder contains *model.py* and *model_dropout.py*, which are the described architecture for our CNN to LSTM model, but one contains Dropout, as for the different tests we did for training.

* The [**utils**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/tree/main/utils) folder contains all functions that we developed in order to complement our project. There we can find both metrics and data generative functions, for example.

### Main scripts:
* The [**get_loader.py**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/get_loader.py) script contains the *Vocabulary* and *Dataset* classes for our project, with some dependency functions that are used to handle the training. In order to handle some inconsistencies on the *Flickr30k* training, we created a slightly modified script, which is [**get_loader_30k.py**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/get_loader_30k.py).

* The [**test.py**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/test.py) script contains the testing function, which will be used to obtain each model's metrics and results.

* The [**train.py**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/train.py) script contains the training and validation functions that will be used to train and evaluate our model during the training phase, no pun intended. It also contains a training function that depicts some images from the training batch and shows the current epoch's caption prediction. 

* The [**train_val_test_split.py**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/train_test_val_split.py) script contains a function to split the dataset in train, validation and test.

* The [**generate_embedding_data.py**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/generate_embedding_data.py) script automatically creates the needed folder with the needed scripts inside to use the pretrained embedding. You only need to provide the downladed **.txt** and it will automatically generate the data folder.

* The [**training_baseline_model.ipynb**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/training_baseline_model.ipynb) notebook contains the training of our baseline model using the pretrained embedding, as described in *image 2*.

* The [**training_model_2.ipynb**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/training_model_2.ipynb) notebook contains the training of another model using the pretrained embedding, applying finetuning and using dropout, as described in *image 2*.

* The [**training_model_3.ipynb**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/training_model_3.ipynb) notebook contains the training of another model using the pretrained embedding, without finetuning and without dropout, as described in *image 2*.

* The [**training_model_4.ipynb**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/training_model_4.ipynb) notebook contains the training of another model without using the pretrained embedding and without dropout, as described in *image 2*.

* The [**training_model_5_30K.ipynb**](https://github.com/DCC-UAB/dlnn-project_ia-group_2/blob/main/training_model_5_30K.ipynb) notebook contains the training of another model, but in this case using another dataset, the [Flickr 30k](https://www.kaggle.com/datasets/adityajn105/flickr30k). This dataset is similar to the Flickr 8k but instead of having only 8k images we have 30k images. The model is trained using the pretrained embedding, without finetuning (since we observed that with the 8k dataset the qualitative results were better without finetuning) and without dropout, as described in *image 2*.

*The definition of each model is described in the following image:*

<img src="docs/different_models.png" width="1200">

*Image 2: Definition of different trained models.*

<br/>

## Why isn't there a main.py?
Since we wanted to run the same model trained with different parameters we decided to run all the training in different python notebooks. If you want to test whether you have installed all dependencies, run the first cells on any of the notebooks. Just remember to set the path to your data folders (such as the FlickrDataset and the GloVe embedding data).

<br/>

## Output examples retrieved from our 30k model trained

<img src="docs/example1.png" width="700">

<img src="docs/example2.png" width="600">

<img src="docs/example3.png" width="760">

<br/>

## Contributors
* **Miguel Moral Hernández - miguel.moral@autonoma.cat**
* **Àlex Sànchez Zurita - alex.sanchezz@autonoma.cat**
* **Pol Medina Arévalo - pol.medina@autonoma.cat**


### ***Neural Networks and Deep Learning Course***

### ***Artificial Intelligence Degree***

### ***UAB 2023***
