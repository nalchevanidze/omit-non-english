import subprocess
import pandas as pd
import json
import os 
import shutil
import pathlib 
from langdetect import detect
import re

INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

def reset_dir (name):
    print('reset directory: ' + name)
    # clean the directory tweet
    if os.path.isdir(name):
        shutil.rmtree(name)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def isEnglish (content):
    lang = detect(content["text"])
    en = (lang == 'en')
    if(not en):
        print("        removed:", lang, content["text"]);
    return en;

def process_csv(name):

    input_path = os.path.join(INPUT_DIR,name) 
    print ("  start: ", input_path)

    csv = pd.read_csv(input_path)
    items_en = [content for _, content  in csv.iterrows() if isEnglish(content) ]

    csv_en = pd.DataFrame(items_en, columns=['ID','datetime','text','user_id','usernameTweet'])

    csv_en = csv_en.replace({'\n': ' '}, regex=True).replace({'\t': ' '}, regex=True).replace({'\r': ' '}, regex=True) 

    print("    end Process",name,"  sizes: ", csv.size, csv_en.size);
    
    output_path = os.path.join(OUTPUT_DIR,name) 
    csv_en.to_csv(output_path)
    print("    saved: " , output_path)


is_csv = re.compile('.*\.csv$')

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
    tasks = get_csv_list('./src')
    for src in tasks:
        process_csv(src)
    
    print("processed ", len(tasks))
    print("finished!")


main()