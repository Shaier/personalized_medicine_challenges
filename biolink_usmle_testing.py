from biolink_utils import *

# seed
set_seed(42)

try:
    # Delete previous performance file
    os.remove('biolinkbert_predictions.txt')
    os.remove('biolink_results.json')
except FileNotFoundError:
    pass

# performance dictionary to save results
performance_dictionary = {}

# iterate over all folders and in each, test each dataset
folder_names = os.listdir('data/transformations/biolinkbert')
for folder in folder_names:
    for dataset_file in os.listdir(f'data/transformations/biolinkbert/{folder}'):
        
        # Load preprocessed dataset
        datafiles = {}
        datafiles['validation'] = f'data/transformations/biolinkbert/{folder}/{dataset_file}'
        qa_dataset = load_dataset('json', data_files=datafiles)
        
        # Tokenize the dataset
        tokenized_qa = qa_dataset.map(preprocess_function, batched=True)
        
        # get model and tokenizer
        model, tokenizer = get_model_tokenizer()

        # Load trained model for testing
        model.eval() # put in testing mode (dropout modules are deactivated)
        
        # Predictions on the dataset
        predictions = trainer.predict(tokenized_qa["validation"])
        accuracy_score = predictions[2]['test_accuracy']

        # save predictions to file
        with open('results/biolink/biolinkbert_predictions.txt', 'a') as file:
            file.write(f'Folder: {folder}, dataset_name: {dataset_file}\n')
            file.write('total_preds: ' + str([chr((ord('A')+ out_item)) for out_item in np.argmax(predictions[0], axis=1)]) + '\n')
            file.write('total_labels: ' + str([chr((ord('A')+ out_item)) for out_item in predictions[1]]) + '\n\n')

        # save result to performance dictionary
        performance_dictionary[f'{folder}_{dataset_file}'] = accuracy_score

# saving results
with open('results/biolink/biolink_results.json', 'w') as fp:
    json.dump(performance_dictionary, fp)
