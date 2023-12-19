# personalized_medicine_challenges

Code for our paper: Emerging Challenges in Personalized Medicine: Assessing Demographic Effects on Biomedical Question Answering Systems:
http://www.afnlp.org/conferences/ijcnlp2023/proceedings/main-long/cdrom/pdf/2023.ijcnlp-long.36.pdf

# Data
In the "data" folder you can find 2 files: 

- "original_questions.jsonl": the 100 vignettes we use to generate the transformations. 
- "processed_questions.jsonl": the 100 vignettes we use to generate the transformations, but with slight gender modifications (e.g., "he" --> "[he]"), and also tokenized based on BioLinkBERT's tokenizer.

Feel free to add more vignettes or try this on your own data. Though note that if you do so you might want to go over the generate transformations to ensure that everything works correctly (as language has a lot of nuances we may have missed a few cases).

You will also find the folder "transformations", to which the transformations will be added. Note that BioLinkBERT and QAGNN require the questions to be in different formats (and also have different tokenizers), so there is a transformation folder for each. 

# To create the transformations
- python create_biolinkbert_transformations.py 
- python create_qagnn_transformations.py 

# Dependencies
QAGNN and BioLinkBERT have different dependencies so we need to create 2 environments based on their githubs

# QAGNN: https://github.com/michiyasunaga/qagnn
conda create -n qagnn python=3.7
conda activate qagnn
pip install torch==1.8.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html
pip install transformers==3.4.0
pip install nltk spacy==2.1.6
python -m spacy download en
pip install torch-scatter==2.0.7 -f https://pytorch-geometric.com/whl/torch-1.8.0+cu101.html
pip install torch-sparse==0.6.9 -f https://pytorch-geometric.com/whl/torch-1.8.0+cu101.html
pip install torch-geometric==1.7.0 -f https://pytorch-geometric.com/whl/torch-1.8.0+cu101.html
pip install protobuf==3.20.*

# BioLinkBERT: https://github.com/michiyasunaga/LinkBERT
conda create -n linkbert python=3.8
conda activate linkbert
pip install torch==1.10.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
pip install transformers==4.9.1 datasets==1.11.0 fairscale==0.4.0
pip install setuptools==59.5.0
pip install numpy

# To get BioLinkBERT results
conda activate linkbert
python biolink_usmle_testing.py
# To analyze results
analyze_answers_biolink.ipynb

# To get QAGNN results
## their script requires train, test, and dev files, each with at least one prompt. Since we only care about the dev set I placed 2 files in "qagnn/data/dataset_files" called "train.jsonl" and "test.jsonl" which have only 1 made up prompt. You can ignore their results. The process for testing is to replace each "dev.jsonl" file with each permuted dataset, then, following their script we create a graph using entity linking for each, followed by a transformer model (see their paper/script for more details).
conda activate qagnn 
git clone https://github.com/michiyasunaga/qagnn.git
cd qagnn
Download the pretrained model and place it in "qagnn/saved_models"
chmod +x download_preprocessed_data.sh
./download_preprocessed_data.sh
Add MedQA-USMLE: https://nlp.stanford.edu/projects/myasu/QAGNN/data_preprocessed_biomed.zip
Unzip it and put the "medqa_usmle" and "ddb" folders inside the qagnn/data/
python qagnn_usmle_testing.py
# To analyze results
analyze_answers_biolink.ipynb
