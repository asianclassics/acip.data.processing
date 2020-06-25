import os
import pandas as pd
import textract


current_dir = os.getcwd()
translations_dir = os.path.join(current_dir, '../data/csv/translations/texts')

# translations_dir = '/Users/joel/PROJECTS/WORK/CURRENT/ACIP/apps/neo4j.model/data/csv/translations/texts'
translations = [
    {
        "type": ('doc', 'docx'),
        "input": 'acip_translations.csv',
        "output": 'acip_translations_with_headers.csv'
    },
    {
        "type": ('txt'),
        "input": 'aci_course_translations.csv',
        "output": 'aci_translations_with_headers.csv'
    }
]


def get_content(text):
    if text.endswith('txt'):
        f_input = open(os.path.join(translations_dir, text), "rb")  # open input file for reading
        t = f_input.read()
        f_input.close()
    else:
        t = textract.process(os.path.join(translations_dir, text))
    return t


def get_translation_group(translation):
    texts = [f for f in os.listdir(translations_dir) if f.endswith(translation['type'])]
    df = pd.read_csv(os.path.join(translations_dir, '..', translation['input']))
    for text in texts:
        text_content = get_content(text)
        df.loc[df['assetID'] == text.split('.', 1)[0], 'text'] = text_content

    return df[df['text'].notna()]


def collect_translations():
    for translation in translations:
        df = get_translation_group(translation)
        print(df.head)
        df.to_csv(os.path.join(translations_dir, '../..', translation['output']), sep='\t', encoding='utf-8')


if __name__ == "__main__":
    collect_translations()
