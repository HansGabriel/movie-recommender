import pandas as pd
import os
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")

model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-emotion")


df = pd.read_csv('../input/9000-movies-dataset/mymoviedb.csv', lineterminator='\n')

index = 2022
movie_details = df.iloc[index]
movie_description = movie_details['Title'] + ' ' + movie_details['Genre'] + ' ' + movie_details['Overview']
print(movie_description)

# Encode the input text
input_text = movie_description
input_tokens = tokenizer.encode(input_text, return_tensors='pt')

# Generate the output tokens
output_tokens = model.generate(input_tokens)
output_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

print(f"Input text: {input_text}")
print(f"Output text: {output_text}")



df.to_csv('../working/movie_emotion.csv', index=False)

new_df = pd.read_csv('../working/movie_emotion.csv', lineterminator='\n')

start = 0
for i in range(start, len(new_df)):
    movie_details = new_df.iloc[i]
    movie_description = movie_details['Title'] + ' ' + movie_details['Genre'] + ' ' + movie_details['Overview']
    # Encode the input text
    input_text = movie_description
    input_tokens = tokenizer.encode(input_text, return_tensors='pt')

    # Generate the output tokens
    output_tokens = model.generate(input_tokens)
    output_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
    new_df.at[i, 'Emotion'] = output_text

    if i % 100 == 0 or i == len(new_df) - 1:
        print(i)

        new_df.to_csv('../working/movie_emotion.csv', index=False)



emotion_dict = {}
for i in range(len(new_df)):
    movie_details = new_df.iloc[i]
    emotion = movie_details['Emotion']
    if emotion in emotion_dict:

        emotion_dict[emotion].append({'title': movie_details['Title'], 'poster_url': movie_details['Poster_Url']})
    else:
        emotion_dict[emotion] = [{'title': movie_details['Title'], 'poster_url': movie_details['Poster_Url']}]

# save the emotion_dict to a json file
import json
with open('../working/emotion_dict.json', 'w') as fp:
    json.dump(emotion_dict, fp)