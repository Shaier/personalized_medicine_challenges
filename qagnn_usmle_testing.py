import subprocess
import os 
# import wget
# import sys
import shutil

# os.mkdir('saved_models')
# wget.download('https://nlp.stanford.edu/projects/myasu/QAGNN/models/medqa_usmle_model_hf3.4.0.pt', out='saved_models')

try:
    # Delete previous performance file
    os.remove('results/qagnn/qagnn_performance.txt')
    os.remove('results/qagnn/qagnn_predictions.txt')
except FileNotFoundError:
    pass

# create performance file
with open('results/qagnn/qagnn_performance.txt', 'a') as file:
    file.write('Performance:\n\n')

# iterate through the dataset files
folder_names = os.listdir('data/transformations/qagnn')
for folder in folder_names:
    for dataset_file in os.listdir(f'data/transformations/qagnn/{folder}'):

        print(f'Folder: {folder}, and dataset name: {dataset_file}\n')
        shutil.copyfile(f'data/transformations/qagnn/{folder}/{dataset_file}', 'qagnn/data/dataset_files/test.jsonl') # copying it to test.json
        
        # write dataset name
        with open('results/qagnn/qagnn_performance.txt', 'a') as file:
            file.write(f'Folder: {folder}, and dataset name: {dataset_file}\n')
        
        # write dataset name
        with open('results/qagnn/qagnn_predictions.txt', 'a') as file:
            file.write(f'Folder: {folder}, dataset_name: {dataset_file}\n')

        try:
            # delete folders and files for previous datasets
            shutil.rmtree('qagnn/data/medqa_usmle/statement')
            shutil.rmtree('qagnn/data/medqa_usmle/grounded')
            shutil.rmtree('qagnn/data/medqa_usmle/graph')
            os.remove('qagnn/data/ddb/ddb.graph')
            os.remove('qagnn/data/ddb/ent_emb.npy')
            os.remove('qagnn/data/ddb/ptrs.txt')
            os.remove('qagnn/data/ddb/vocab.txt')
            print('deleted previous datasets\' subgraphs')
        except FileNotFoundError:
            pass

        # create subgraphs
        subprocess.call(['python', 'preprocess_medqa_usmle.py']) # note that this is not the "qagnn/preprocess_medqa_usmle.py" file!

        # run eval (save results to performance file at qagnn.py)
        os.chdir('qagnn')
        subprocess.call(['./eval_qagnn__medqa_usmle.sh'])
        os.chdir('..')
