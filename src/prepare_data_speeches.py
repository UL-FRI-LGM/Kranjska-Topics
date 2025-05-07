#
# SPDX-FileCopyrightText: © 2024 Alenka Kavčič <alenka.kavcic@fri.uni-lj.si>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


# This script prepares the source data for topic analysis with BERTopic.
#
# Input: TEI encoded XML documents from corpus Kranjska 1.0, without linguistic annotation (https://www.clarin.si/repository/xmlui/handle/11356/1824)
# Output: json file with all speeches with corresponding dates


from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import json


SOURCE_DIR = "../corpus/Kranjska-xml-text" # directory with source files
EXCLUDE = "Corpus-Kranjska" # skip this file
OUTPUT_FILE = "../data/bert_docs_time_stamps.json" # the name of the output data file (create data directory beforehand)


names = [join(SOURCE_DIR,f) for f in listdir(SOURCE_DIR) if isfile(join(SOURCE_DIR, f)) and not f.startswith(EXCLUDE)]
print(len(names))

ns = {"default": "http://www.tei-c.org/ns/1.0"}
documents = []

# documents is a list of pairs (time_stamp, string);
# each string is one speech, sentences within the speech are separated by \n; 
# time_stamp is the date of the document (meeting proceedings) with this speech

for i in range(len(names)):
    # parse the date of the meeting proceedings from the document name
    datum = names[i].split('/')[-1].split('-')[1]
    datum = f'{datum[:4]}-{datum[4:6]}-{datum[6:]}'

    # parse the content of the meeting proceedings
    tree = ET.parse(names[i])
    root = tree.getroot()
    for seg in root.findall(".//default:seg", ns):
        sentence_list = []
        for s in seg.findall(".//default:s", ns):
            if s.text is None:
                print("---> ERROR - sentence skipped: no text in sentence (s) in " + names[i])
                continue
            sentence_list.append(s.text)
        documents.append((datum, "\n".join(sentence_list)))


# save the prepared data
with open(OUTPUT_FILE, 'w', encoding='utf8') as out:
    json.dump(documents, out)
