import subprocess
import pandas as pd
import json
import os 
import shutil
import pathlib 
from langdetect import detect , detect_langs 
from langdetect.lang_detect_exception import LangDetectException
import re


INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'
THRESHOLD = 0.9

def reset_dir (name):
    print('reset directory: ' + name)
    # clean the directory tweet
    if os.path.isdir(name):
        shutil.rmtree(name)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def probIsEnglish (langs):
    for x in langs:
        if(x.lang == "en"):
            return x.prob
    return 0


def print_removed(isEng, probs,cleaned,source):
    if(not isEng):
        print("        removed: ", probs)
        print("            cleaned: \"", cleaned ,"\"")
        print("            source: \"", source ,"\"")

def isEnglish (content):
    source_text = content["text"]
    cleaned_text = remove_url(remove_hash_tag(source_text))

    try:
      probs = detect_langs(cleaned_text)
      isEng = probIsEnglish(probs) > THRESHOLD
      print_removed(isEng,probs,cleaned_text, source_text)
      return isEng

    except LangDetectException as e:
      print("        removed empty:", e, cleaned_text)
      return False

def process_csv(name):

    input_path = os.path.join(INPUT_DIR,name) 
  #  print ("  start: ", input_path)

    csv = pd.read_csv(input_path)
    items_en = [content for _, content  in csv.iterrows() if isEnglish(content) ]

    csv_en = pd.DataFrame(items_en, columns=['ID','datetime','text','user_id','usernameTweet'])

    csv_en = csv_en.replace({'\n': ' '}, regex=True).replace({'\t': ' '}, regex=True).replace({'\r': ' '}, regex=True) 

  #  print("    end Process",name,"  sizes: ", csv.size, csv_en.size);
    
    output_path = os.path.join(OUTPUT_DIR,name) 
    csv_en.to_csv(output_path)
    print("    saved: " , output_path)


is_csv = re.compile('.*\.csv$')

def remove_url(text):
    text = re.sub(r'https?:\/\/(www\.)?[\s]*[\S]*', '', text)

    text = re.sub(r'(\.\.\. )?pic.twitter.com?[\s]*[\S]*', '', text)

    text = re.sub(r'[\S]*.html', '', text)

    text = re.sub(r'www\.[\s]*[\S]*', '', text)

    text = re.sub(r'twitter\.com[\S]*', '', text)

    return text.strip()

def remove_hash_tag(text):
    return re.sub(r'#[\S]*', '', text)

def get_csv_list (dir):
    return [
        str(file) 
        for file 
            in os.listdir(dir) 
            if is_csv.match(str(file))
    ]

def main ():
    print("start processing ...")
    reset_dir(OUTPUT_DIR)
    tasks = get_csv_list(INPUT_DIR)
    for src in tasks:
        process_csv(src)
    
    print("processed ", len(tasks))
    print("finished!")


main()