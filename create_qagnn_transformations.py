####################################
        # libraries
####################################
import json
import shutil

####################################
        # functions
####################################

# names for each ethnicity/gender
names_dict = {}
names_dict['black_male'] = ['Roosevelt', 'Jermaine', 'Darnell', 'Willie', 'Mattie', 'Reginald', 'Cedric', 'Sylvester', 'Tyrone', 'Errol']
names_dict['black_female'] = ['Latonya', 'Tamika', 'Ebony', 'Latasha', 'Keisha', 'Lillie', 'Minnie', 'Gwendolyn', 'Bessie', 'Marva']
names_dict['white_male'] = ['Bradley', 'Brett', 'Scott', 'Kurt', 'Todd', 'Chad', 'Matthew', 'Dustin', 'Shane', 'Douglas']
names_dict['white_female'] = ['Beth', 'Megan', 'Kristin', 'Jill', 'Erin', 'Colleen', 'Kathleen', 'Heather', 'Holly', 'Laurie']
names_dict['hispanic_male'] = ['Rigoberto', 'Santos', 'Javier', 'Efrain', 'Juan', 'Ramiro', 'Jesus', 'Humberto', 'Gonzalo', 'Hector']
names_dict['hispanic_female'] = ['Guadalupe', 'Marisela', 'Guillermina', 'Rocio', 'Yesenia', 'Blanca', 'Rosalba', 'Elvia', 'Alejandra', 'Mayra']
names_dict['asian_male'] = ['Viet', 'Thong', 'Qiang', 'Kwok', 'Hao', 'Yang', 'Nam', 'Huy', 'Yuan', 'Ho']
names_dict['asian_female'] = ['Zhen', 'Nga', 'Lien', 'Lam', 'Hui', 'Wing', 'Hoa', 'Wai', 'Min', 'Huong']
names_dict['black'] = names_dict['black_male'] + names_dict['black_female']
names_dict['white'] = names_dict['white_male'] + names_dict['white_female']
names_dict['asian'] = names_dict['asian_male'] + names_dict['asian_female']
names_dict['hispanic'] = names_dict['hispanic_male'] + names_dict['hispanic_female']

# to dimensionless 
def dimensionless_sentence(sentence):
    return sentence.replace(' he ', ' the patient ').replace(' He ', ' The patient ').replace(' she ', ' the patient ') \
    .replace(' She ', ' The patient ').replace(' man ', ' patient ').replace(' woman ', ' patient ').replace(' male ', ' patient ').replace(' female ', ' patient ') \
    .replace(' his ', ' their ').replace(' girl ', ' patient ').replace(' boy ', ' patient ').replace(' boy\'s ', ' patient ').replace(' girl\'s ', ' patient ').replace(' girl.', ' patient.').replace(' gentleman ', ' patient ')  \
    .replace(' His ', ' Their ').replace(' her ', ' their ').replace(' Her ', ' Their ')  \
    .replace('husband', 'partner').replace('wife', 'partner') \
    .replace('boyfriend', 'partner').replace('girlfriend', 'partner') \
    .replace(' has ', ' have ').replace(' [he] ', ' they ' ).replace(' [she] ', ' they ' ).replace('[her]','them') \
    .replace(' patient have ', ' patient has ').replace(' they resides ', ' they reside ') \
    .replace(' they states ', ' they state ').replace(' they is ', ' they are ') \
    .replace(' they does ', ' they do ').replace(' they describes ', ' they describe ') \
    .replace(' they replies ', ' they reply ').replace(' they feels ', ' they feel ') \
    .replace(' they goes ', ' they go ').replace(' they manages ', ' they manage ') \
    .replace(' It have ', ' It has ').replace(' they now produces ', ' they now produce ') \
    .replace(' it have ', ' it has ').replace(' they was ', ' they were ') \
    .replace(' This have ', ' This has ').replace(' they needs ', ' they need ') \
    .replace(' right eye have ', ' right eye has ').replace(' their breath have ', ' their breath has ') \
    .replace(' they usually produces ', ' they usually produce ').replace(' about 3 years ago and have ', ' about 3 years ago and has ') \
    .replace(' coughing pink sputum and have ', ' coughing pink sputum and has ').replace(' the patient appears uncomfortable and have ', ' the patient appears uncomfortable and has ') \
    .replace(' they frequently falls asleep while reading or watching television in the afternoons and feels ', ' they frequently fall asleep while reading or watching television in the afternoons and feel ').replace(' they sometimes hears ', ' they sometimes hear ') \
    .replace(' they falls ', ' they fall ').replace(' they laughs ', ' they laugh ') \
    .replace(' they drops whatever the patient is holding and feels ', ' they drop whatever the patient is holding and feel ').replace(' they requires ', ' they require ') \
    .replace(' they drinks multiple liters of water and soda daily and still feels ', ' they drink multiple liters of water and soda daily and still feel ').replace(' they struggles ', ' they struggle ') \
    .replace(' they lacks ', ' they lack ').replace(' they leaves ', ' they leave ') \
    .replace(' The patient works as an assistant for a nature camp organization but have ', ' The patient works as an assistant for a nature camp organization but has ').replace(' The patient feels fatigued but have ', ' The patient feels fatigued but has ') \
    .replace(' the patient has not slept within the past 24 hours and have ', ' the patient has not slept within the past 24 hours and has ').replace(' they attributes ', ' they attribute ') \
    .replace(' The patient has a chronic cough that have ', ' The patient has a chronic cough that has ').replace(' they leaves ', ' they leave ') \
    .replace(' The patient denies having any other friends and have ', ' The patient denies having any other friends and has ')

# to mask    
def mask_sentence(sentence):
    return sentence.replace(' he ', ' [PRONOUN-MASK] ').replace(' He ', ' [PRONOUN_CAP-MASK] ').replace(' she ', ' [PRONOUN-MASK] ') \
    .replace(' She ', ' [PRONOUN_CAP-MASK] ').replace(' man ', ' [GENDER-MASK] ').replace(' woman ', ' [GENDER-MASK] ').replace(' male ', ' [GENDER-MASK] ').replace(' female ', ' [GENDER-MASK] ') \
    .replace(' his ', ' [POSSESSIVE-MASK] ').replace(' girl ', ' [GENDER-MASK] ').replace(' boy ', ' [GENDER-MASK] ').replace(' boy\'s ', ' [GENDER-MASK] ').replace(' girl.', ' [GENDER-MASK].').replace(' girl\'s ', ' [GENDER-MASK] ').replace(' gentleman ', ' [GENDER-MASK] ')  \
    .replace(' His ', ' [POSSESSIVE_CAP-MASK] ').replace(' her ', ' [POSSESSIVE-MASK] ').replace(' Her ', ' [POSSESSIVE_CAP-MASK] ').replace(' patient ', ' [GENDER-MASK] ')  \
    .replace('year-old [GENDER-MASK] ', 'year-old [SEXUAL_ORIENTATION-MASK] [ETHNICITY-MASK] [GENDER-MASK] [NAME_MASK] ') \
    .replace('year-old imprisoned [GENDER-MASK] ', 'year-old [SEXUAL_ORIENTATION-MASK] imprisoned [ETHNICITY-MASK] [GENDER-MASK] [NAME_MASK] ') \
    .replace('year-old homeless [GENDER-MASK] ', 'year-old [SEXUAL_ORIENTATION-MASK] homeless [ETHNICITY-MASK] [GENDER-MASK] [NAME_MASK] ') \
    .replace('husband', 'partner').replace('wife', 'partner') \
    .replace('boyfriend', 'partner').replace('girlfriend', 'partner')

# to male 
def to_male(normalized_sentence):
    return normalized_sentence.replace(' [PRONOUN-MASK] ', ' he ').replace(' [PRONOUN_CAP-MASK] ', ' He ').replace(' [GENDER-MASK] ', ' male ') \
    .replace(' [POSSESSIVE-MASK] ', ' his ').replace(' [POSSESSIVE_CAP-MASK] ', ' His ').replace(' [he] ', ' he ' ).replace(' [she] ', ' he ' )

# to female
def to_female(normalized_sentence):
    return normalized_sentence.replace(' [PRONOUN-MASK] ', ' she ').replace(' [PRONOUN_CAP-MASK] ', ' She ').replace(' [GENDER-MASK] ', ' female ') \
    .replace(' [POSSESSIVE-MASK] ', ' her ').replace(' [POSSESSIVE_CAP-MASK] ', ' Her ') \
    .replace(' [POSSESSIVE-MASK] ', ' her ').replace(' [POSSESSIVE_CAP-MASK] ', ' Her ').replace(' [he] ', ' she ' ).replace(' [she] ', ' she ' )

# to genderless
def to_genderless(normalized_sentence):
    return normalized_sentence.replace(' [PRONOUN-MASK] ', ' the patient ').replace(' [PRONOUN_CAP-MASK] ', ' The patient ')\
    .replace(' [POSSESSIVE-MASK] ', ' their ').replace(' [POSSESSIVE_CAP-MASK] ', ' Their ') \
    .replace (' [GENDER-MASK] ', ' patient ').replace(' [he] ', ' they ' ).replace(' [she] ', ' they ' ).replace('[her]','them') \
    .replace(' patient have ', ' patient has ').replace(' they resides ', ' they reside ') \
    .replace(' they states ', ' they state ').replace(' they is ', ' they are ') \
    .replace(' they does ', ' they do ').replace(' they describes ', ' they describe ') \
    .replace(' they replies ', ' they reply ').replace(' they feels ', ' they feel ') \
    .replace(' they goes ', ' they go ').replace(' they manages ', ' they manage ') \
    .replace(' It have ', ' It has ').replace(' they now produces ', ' they now produce ') \
    .replace(' it have ', ' it has ').replace(' they was ', ' they were ') \
    .replace(' This have ', ' This has ').replace(' they needs ', ' they need ') \
    .replace(' right eye have ', ' right eye has ').replace(' their breath have ', ' their breath has ') \
    .replace(' they usually produces ', ' they usually produce ').replace(' about 3 years ago and have ', ' about 3 years ago and has ') \
    .replace(' coughing pink sputum and have ', ' coughing pink sputum and has ').replace(' the patient appears uncomfortable and have ', ' the patient appears uncomfortable and has ') \
    .replace(' they frequently falls asleep while reading or watching television in the afternoons and feels ', ' they frequently fall asleep while reading or watching television in the afternoons and feel ').replace(' they sometimes hears ', ' they sometimes hear ') \
    .replace(' they falls ', ' they fall ').replace(' they laughs ', ' they laugh ') \
    .replace(' they drops whatever the patient is holding and feels ', ' they drop whatever the patient is holding and feel ').replace(' they requires ', ' they require ') \
    .replace(' they drinks multiple liters of water and soda daily and still feels ', ' they drink multiple liters of water and soda daily and still feel ').replace(' they struggles ', ' they struggle ') \
    .replace(' they lacks ', ' they lack ').replace(' they leaves ', ' they leave ') \
    .replace(' The patient works as an assistant for a nature camp organization but have ', ' The patient works as an assistant for a nature camp organization but has ').replace(' The patient feels fatigued but have ', ' The patient feels fatigued but has ') \
    .replace(' the patient has not slept within the past 24 hours and have ', ' the patient has not slept within the past 24 hours and has ').replace(' they attributes ', ' they attribute ') \
    .replace(' The patient has a chronic cough that have ', ' The patient has a chronic cough that has ').replace(' they leaves ', ' they leave ') \
    .replace(' they also has ', ' they also have ').replace(' they has ', ' they have ') \
    .replace(' they usually produces ', ' they usually produce ').replace(' The patient also says they feel fatigued and has ', ' The patient also says they feel fatigued and have ') \
    .replace(' they drops ', ' they drop ').replace(' they was ', ' they were ') \
    .replace(' The patient denies having any other friends and have ', ' The patient denies having any other friends and has ')

# to name
def to_name(normalized_sentence, name):
    return normalized_sentence.replace(' [NAME_MASK] ', ' named '+name+' ')

# to sexual orientation
def to_sexual_orientation(normalized_sentence, sexual_orientation):
    return normalized_sentence.replace(' [SEXUAL_ORIENTATION-MASK] ', f' {sexual_orientation} ')

# to ethnicity (either or with names)
def to_ethnicity(normalized_sentence, ethnicity):
    return normalized_sentence.replace('[ETHNICITY-MASK]',f'{ethnicity}')


# to dimensions
def to_dimensions(sentence, dimensionless_option = False, gender_option = None, names_option = False, sexual_orientation_option = None, ethnicity_option = None):
    
    # check for dimensionless
    if dimensionless_option == True:
        return dimensionless_sentence(sentence)

    # mask first
    new_sentence = mask_sentence(sentence)

    # gender
    if gender_option == 'male':
        new_sentence = to_male(new_sentence)
    elif gender_option == 'female':
        new_sentence = to_female(new_sentence)
    else:
        new_sentence = to_genderless(new_sentence)

    # sexual orientation
    if sexual_orientation_option == 'heterosexual':
        new_sentence = to_sexual_orientation(new_sentence, 'heterosexual')
    if sexual_orientation_option == 'homosexual':
        new_sentence = to_sexual_orientation(new_sentence, 'homosexual')
    if sexual_orientation_option == 'bisexual':
        new_sentence = to_sexual_orientation(new_sentence, 'bisexual')
    
    # ethnicity
    if ethnicity_option == 'white':
        new_sentence = to_ethnicity(new_sentence,'white')
    if ethnicity_option == 'black':
        new_sentence = to_ethnicity(new_sentence,'black')
    if ethnicity_option == 'asian':
        new_sentence = to_ethnicity(new_sentence,'asian')
    if ethnicity_option == 'hispanic':
        new_sentence = to_ethnicity(new_sentence,'hispanic')
    if ethnicity_option == 'African-American':
        new_sentence = to_ethnicity(new_sentence,'African-American')

    # remove all unused dimensions
    split_sentence = new_sentence.split() 
    complete_sentence = " ".join([word for word in split_sentence if "-MASK" not in word]) # note that this doesnt remove the name masking (if names are needed you need to iterate over each name)

    if not names_option: # names are needed (default is false)
        split_sentence = complete_sentence.split() 
        complete_sentence = " ".join([word for word in split_sentence if "_MASK" not in word]) # remove names if not needed

    return complete_sentence

####################################
        # transformations
####################################
# load base questions
with open('data/processed_questions.jsonl', 'r') as json_file:
    processed_questions = list(json_file)       

questions_list = []
# convert biolink-processed questions (they are tokenized based on its tokenizer) to QAGNN format ({question, answer, options}) 
for qa_string in processed_questions:

    # load data
    qa = json.loads(qa_string)

    #parse data
    question = qa['sent1']
    option0 = qa['ending0']
    option1 = qa['ending1']
    option2 = qa['ending2']
    option3 = qa['ending3']
    all_options = [option0, option1, option2, option3]
    answer_idx = qa['label']  
    answer = all_options[answer_idx]
    
    # clean data (biolink has tokens)
    def clean_sentence(sentence):
        return sentence.replace('\u2019', '\'').replace('\u00b0', u'°').replace('\u2191', '↑')\
        .replace('\u201c', '"').replace('\u201d', '"').replace('\u2193', '↓').replace('\u2013', '–').replace('\u03b2','β').replace('\u03b11','α1')
    
    question = clean_sentence(question)
    option0 = clean_sentence(option0)
    option1 = clean_sentence(option1)
    option2 = clean_sentence(option2)
    option3 = clean_sentence(option3) 
    answer = clean_sentence(answer)

    # covert to format
    qagnn_ready_format = {}
    qagnn_ready_format['question'] = question
    qagnn_ready_format['options'] = {'A': option0, 'B': option1, 'C': option2, 'D': option3}
    qagnn_ready_format['answer'] = answer
    qagnn_ready_format['answer_idx'] = chr(ord('@')+answer_idx+1)
    questions_list.append(qagnn_ready_format)

# save to file
with open('data/qagnn_questions.jsonl', 'w') as f:
    for qa_dict in questions_list:
        json.dump(qa_dict, f, ensure_ascii=False)
        f.write('\n')    

# Dimensionless
with open('data/transformations/qagnn/dimensionless/dimensionless.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'])
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# Gender
# male
with open('data/transformations/qagnn/gender/male.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='male')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# female
with open('data/transformations/qagnn/gender/female.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='female')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# Ethnicity
# white
with open('data/transformations/qagnn/ethnicity/white.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], ethnicity_option='white')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# black
with open('data/transformations/qagnn/ethnicity/black.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], ethnicity_option='black')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# african-american
with open('data/transformations/qagnn/ethnicity/African-American.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], ethnicity_option='African-American')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# asian
with open('data/transformations/qagnn/ethnicity/asian.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], ethnicity_option='asian')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')


# hispanic
with open('data/transformations/qagnn/ethnicity/hispanic.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], ethnicity_option='hispanic')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')


# Names
# white
with open('data/transformations/qagnn/names/white.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['white']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')

# black
with open('data/transformations/qagnn/names/black.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['black']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')


# hispanic
with open('data/transformations/qagnn/names/hispanic.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['hispanic']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')

# asian
with open('data/transformations/qagnn/names/asian.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['asian']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')


# Gender + Ethnicity
# white male
with open('data/transformations/qagnn/gender_ethnicity/white_male.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='male', ethnicity_option = 'white')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# black male
with open('data/transformations/qagnn/gender_ethnicity/black_male.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='male', ethnicity_option = 'black')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')


# African-American male
with open('data/transformations/qagnn/gender_ethnicity/African-American_male.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='male', ethnicity_option = 'African-American')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')
            
# hispanic male
with open('data/transformations/qagnn/gender_ethnicity/hispanic_male.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='male', ethnicity_option = 'hispanic')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# asian male
with open('data/transformations/qagnn/gender_ethnicity/asian_male.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='male', ethnicity_option = 'asian')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')


# white female
with open('data/transformations/qagnn/gender_ethnicity/white_female.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='female', ethnicity_option = 'white')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# black female
with open('data/transformations/qagnn/gender_ethnicity/black_female.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='female', ethnicity_option = 'black')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')


# hispanic female
with open('data/transformations/qagnn/gender_ethnicity/hispanic_female.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='female', ethnicity_option = 'hispanic')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# asian female
with open('data/transformations/qagnn/gender_ethnicity/asian_female.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='female', ethnicity_option = 'asian')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')


# African-American female
with open('data/transformations/qagnn/gender_ethnicity/African-American_female.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='female', ethnicity_option = 'African-American')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f, ensure_ascii=False)
        f.write('\n')

# Gender, names, ethnicity
# white male
with open('data/transformations/qagnn/gender_names_ethnicity/white_male.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['white_male']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='male', ethnicity_option = 'white'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')

# black male
with open('data/transformations/qagnn/gender_names_ethnicity/black_male.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['black_male']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='male', ethnicity_option = 'black'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')


# African-American male
with open('data/transformations/qagnn/gender_names_ethnicity/African-American_male.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['black_male']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='male', ethnicity_option = 'African-American'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')
            
# hispanic male
with open('data/transformations/qagnn/gender_names_ethnicity/hispanic_male.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['hispanic_male']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='male', ethnicity_option = 'hispanic'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')

# asian male
with open('data/transformations/qagnn/gender_names_ethnicity/asian_male.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['asian_male']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='male', ethnicity_option = 'asian'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')


# white female
with open('data/transformations/qagnn/gender_names_ethnicity/white_female.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['white_female']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='female', ethnicity_option = 'white'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')

# black female
with open('data/transformations/qagnn/gender_names_ethnicity/black_female.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['black_female']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='female', ethnicity_option = 'black'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')


# hispanic female
with open('data/transformations/qagnn/gender_names_ethnicity/hispanic_female.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['hispanic_female']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='female', ethnicity_option = 'hispanic'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')

# asian female
with open('data/transformations/qagnn/gender_names_ethnicity/asian_female.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['asian_female']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='female', ethnicity_option = 'asian'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')


# African-American female
with open('data/transformations/qagnn/gender_names_ethnicity/African-American_female.jsonl', 'w') as f:
    for qa in questions_list:
        for name_example in names_dict['black_female']:
            dimensioned_sentence = to_name(to_dimensions(qa['question'], names_option=True, gender_option='female', ethnicity_option = 'African-American'),name = name_example)
            new_qa = qa.copy()
            new_qa['question'] = dimensioned_sentence
            new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
            json.dump(new_qa, f, ensure_ascii=False)
            f.write('\n')

# Sexual orientation + Gender
# white male
with open('data/transformations/qagnn/sexual_orientation_gender/bisexual_male.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='male', sexual_orientation_option = 'bisexual')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f)
        f.write('\n')

# black male
with open('data/transformations/qagnn/sexual_orientation_gender/heterosexual_male.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='male', sexual_orientation_option = 'heterosexual')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f)
        f.write('\n')


# African-American male
with open('data/transformations/qagnn/sexual_orientation_gender/homosexual_male.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='male', sexual_orientation_option = 'homosexual')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f)
        f.write('\n')
            
# hispanic male
with open('data/transformations/qagnn/sexual_orientation_gender/bisexual_female.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='female', sexual_orientation_option = 'bisexual')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f)
        f.write('\n')

# asian male
with open('data/transformations/qagnn/sexual_orientation_gender/heterosexual_female.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='female', sexual_orientation_option = 'heterosexual')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f)
        f.write('\n')


# white female
with open('data/transformations/qagnn/sexual_orientation_gender/homosexual_female.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], gender_option='female', sexual_orientation_option = 'homosexual')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f)
        f.write('\n')

# sexual orientation
# bisexual
with open('data/transformations/qagnn/sexual_orientation/bisexual.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], sexual_orientation_option = 'bisexual')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f)
        f.write('\n')

# heterosexual
with open('data/transformations/qagnn/sexual_orientation/heterosexual.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], sexual_orientation_option = 'heterosexual')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f)
        f.write('\n')


# homosexual
with open('data/transformations/qagnn/sexual_orientation/homosexual.jsonl', 'w') as f:
    for qa in questions_list:
        dimensioned_sentence = to_dimensions(qa['question'], sexual_orientation_option = 'homosexual')
        new_qa = qa.copy()
        new_qa['question'] = dimensioned_sentence
        new_qa['metamap_phrases'] = [] #remove just in case they use it because it has keywords (male, etc)
        json.dump(new_qa, f)
        f.write('\n')
            