import os
import sys
import pandas as pd

from bs4 import BeautifulSoup
from langdetect import detect

from tags_generator.shared.preprocessing import preprocess_text

from tqdm import tqdm



def combine(input_dir='data/monthly_best_1000', output_file_path='data/monthly_best_1000_combined.csv'):
  first_file = os.listdir(input_dir)[0]
  df_columns = pd.read_csv(os.path.join(input_dir, first_file)).columns

  data = pd.DataFrame(columns=df_columns)
  
  for f in os.listdir(input_dir):
    temp = pd.read_csv(os.path.join(input_dir, f))
    data = pd.concat([data, temp],
                      axis=0,
                      ignore_index=True)

  data.to_csv(output_file_path, index=False)


def extract_code(text):
  soup = BeautifulSoup(text, 'lxml')
  code_blocks = soup.find_all('code')
  return '\n'.join(block.get_text() for block in code_blocks)


def is_english(text):
    try:
        return detect(text[0:100]) == 'en'
    except:
        return False

def filter_tokens(token):
  return token.pos_ in ["NOUN", "PROPN"] and token.text.lower() not in STOP_WORDS

def clean(input_file='data/monthly_best_1000_combined.csv', output_file='data/monthly_best_1000_cleaned.csv'):
  tqdm.pandas()

  data = pd.read_csv(input_file)

  data.set_index('Id', inplace=True)

  data = data.drop(columns=['Score', 'CreationDate', 'Rank'])

  print("Suppression des questions qui ne sont pas en anglais...")
  data = data[data['Body'].progress_apply(is_english)]

  print("Extraction du code...")
  data['Body'] = data['Body'].progress_apply(lambda x: BeautifulSoup(x, 'lxml').get_text())
  data['Body'] = data['Title'] + '. ' + data['Body']

  print("Prétraitement des données...")
  data['Body'] = data['Body'].progress_apply(preprocess_text).str.join(',')

  data['Tags'] = (data['Tags'].str.lstrip('<').str.rstrip('>').str.split('><')).str.join(',')
  data = data.drop(columns=['Title'])

  data.to_csv(output_file, sep=";")

if __name__ == '__main__':
    if len(sys.argv) > 2:
        # Si des arguments supplémentaires sont fournis, on les passe à la fonction
        globals()[sys.argv[1]](*sys.argv[2:])
    elif len(sys.argv) > 1:
        # Si seule la fonction est fournie, on l'appelle sans arguments
        globals()[sys.argv[1]]()
    else:
        print("Veuillez fournir le nom de la fonction à exécuter.")
