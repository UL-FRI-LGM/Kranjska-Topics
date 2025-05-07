#
# SPDX-FileCopyrightText: © 2024 Alenka Kavčič <alenka.kavcic@fri.uni-lj.si>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


# This script extracts lemmas as pairs (word, lemma) from the linguistically annotated XML documents.
# Only words with specific PoS tags are included. Stopwords are excluded. No duplicates.
#
# Input: TEI encoded XML documents from corpus Kranjska 1.0, with linguistic annotation (https://www.clarin.si/repository/xmlui/handle/11356/1824)
# Output: json file with a list of pairs (word, lemma)


from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import json


SOURCE_DIR = "../corpus/Kranjska-xml" # directory with source files
EXCLUDE = "Corpus-Kranjska" # skip this file
OUTPUT_FILE = "../data/word_lemmas.json" # the name of the output data file


stopwords_ger = ["aber", "als", "am", "an", "auch", "auf", "aus", "bei", "bin", "bis", "bist", "da", "dadurch", "daher", "darum", "das", "daß", "dass", "dein", "deine", "dem", "den", "der", "des", "dessen", "deshalb", "die", "dies", "dieser", "dieses", "doch", "dort", "du", "durch", "ein", "eine", "einem", "einen", "einer", "eines", "er", "es", "euer", "eure", "für", "hatte", "hatten", "hattest", "hattet", "hier", "hinter", "ich", "ihr", "ihre", "im", "in", "ist", "ja", "jede", "jedem", "jeden", "jeder", "jedes", "jener", "jenes", "jetzt", "kann", "kannst", "können", "könnt", "machen", "mein", "meine", "mit", "muß", "mußt", "musst", "müssen", "müßt", "nach", "nachdem", "nein", "nicht", "nun", "oder", "seid", "sein", "seine", "sich", "sie", "sind", "soll", "sollen", "sollst", "sollt", "sonst", "soweit", "sowie", "und", "unser", "unsere", "unter", "vom", "von", "vor", "wann", "warum", "was", "weiter", "weitere", "wenn", "wer", "werde", "werden", "werdet", "weshalb", "wie", "wieder", "wieso", "wir", "wird", "wirst", "wo", "woher", "wohin", "zu", "zum", "zur", "über"]

stopwords_slo = ["a", "ako", "ali", "b", "bi", "bil", "bila", "bile", "bili", "bilo", "biti", "blizu", "bo", "bodo", "bojo", "bolj", "bom", "bomo", "boste", "bova", "boš", "brez", "c", "cel", "cela", "celi", "celo", "d", "da", "daleč", "dan", "danes", "datum", "december", "deset", "deseta", "deseti", "deseto", "devet", "deveta", "deveti", "deveto", "do", "dober", "dobra", "dobri", "dobro", "dokler", "dol", "dolg", "dolga", "dolgi", "dovolj", "dr", "drug", "druga", "drugi", "drugo", "dva", "dve", "e", "eden", "en", "ena", "ene", "eni", "enkrat", "eno", "etc.", "f", "februar", "g", "g.", "ga", "ga.", "gor", "gospa", "gospod", "h", "halo", "i", "idr.", "ii", "iii", "in", "iv", "ix", "iz", "j", "januar", "jaz", "je", "ji", "jih", "jim", "jo", "julij", "junij", "jutri", "k", "kadarkoli", "kaj", "kajti", "kako", "kakor", "kamor", "kamorkoli", "kar", "karkoli", "kateri", "katerikoli", "kdaj", "kdo", "kdorkoli", "ker", "ki", "kje", "kjer", "kjerkoli", "ko", "koder", "koderkoli", "koga", "komu", "kot", "kratek", "kratka", "kratke", "kratki", "l", "lahka", "lahke", "lahki", "lahko", "le", "lep", "lepa", "lepe", "lepi", "lepo", "leto", "m", "maj", "majhen", "majhna", "majhni", "malce", "malo", "manj", "marec", "me", "med", "medtem", "mene", "mesec", "mi", "midva", "midve", "mnogo", "moj", "moja", "moje", "mora", "morajo", "moram", "moramo", "morate", "moraš", "morem", "mu", "n", "na", "nad", "naj", "najina", "najino", "najmanj", "naju", "največ", "nam", "narobe", "nas", "nato", "nazaj", "naš", "naša", "naše", "ne", "nedavno", "nedelja", "nek", "neka", "nekaj", "nekatere", "nekateri", "nekatero", "nekdo", "neke", "nekega", "neki", "nekje", "neko", "nekoga", "nekoč", "ni", "nikamor", "nikdar", "nikjer", "nikoli", "nič", "nje", "njega", "njegov", "njegova", "njegovo", "njej", "njemu", "njen", "njena", "njeno", "nji", "njih", "njihov", "njihova", "njihovo", "njiju", "njim", "njo", "njun", "njuna", "njuno", "no", "nocoj", "november", "npr.", "o", "ob", "oba", "obe", "oboje", "od", "odprt", "odprta", "odprti", "okoli", "oktober", "on", "onadva", "one", "oni", "onidve", "osem", "osma", "osmi", "osmo", "oz.", "p", "pa", "pet", "peta", "petek", "peti", "peto", "po", "pod", "pogosto", "poleg", "poln", "polna", "polni", "polno", "ponavadi", "ponedeljek", "ponovno", "potem", "povsod", "pozdravljen", "pozdravljeni", "prav", "prava", "prave", "pravi", "pravo", "prazen", "prazna", "prazno", "prbl.", "precej", "pred", "prej", "preko", "pri", "pribl.", "približno", "primer", "pripravljen", "pripravljena", "pripravljeni", "proti", "prva", "prvi", "prvo", "r", "ravno", "redko", "res", "reč", "s", "saj", "sam", "sama", "same", "sami", "samo", "se", "sebe", "sebi", "sedaj", "sedem", "sedma", "sedmi", "sedmo", "sem", "september", "seveda", "si", "sicer", "skoraj", "skozi", "slab", "smo", "so", "sobota", "spet", "sreda", "srednja", "srednji", "sta", "ste", "stran", "stvar", "sva", "svoj", "t", "ta", "tak", "taka", "take", "taki", "tako", "takoj", "tam", "te", "tebe", "tebi", "tega", "težak", "težka", "težki", "težko", "ti", "tista", "tiste", "tisti", "tisto", "tj.", "tja", "to", "toda", "torej", "torek", "tretja", "tretje", "tretji", "tri", "tu", "tudi", "tukaj", "tvoj", "tvoja", "tvoje", "u", "v", "vaju", "vam", "vas", "vaš", "vaša", "vaše", "ve", "vedno", "velik", "velika", "veliki", "veliko", "vendar", "ves", "več", "vi", "vidva", "vii", "viii", "visok", "visoka", "visoke", "visoki", "vsa", "vsaj", "vsak", "vsaka", "vsakdo", "vsake", "vsaki", "vsakomur", "vse", "vsega", "vsi", "vso", "včasih", "včeraj", "x", "z", "za", "zadaj", "zadnji", "zakaj", "zaprta", "zaprti", "zaprto", "zdaj", "zelo", "zunaj", "č", "če", "često", "četrta", "četrtek", "četrti", "četrto", "čez", "čigav", "š", "še", "šest", "šesta", "šesti", "šesto", "štiri", "ž", "že"]

# stopwords specific to these parliamentary debates
stopwords_parlament = ['baron', "beseda", 'dalje', 'dati', "deželen", 'dobiti', 'dovoliti', "finančen", 'glasovati', "glavar", "gld", "glede", "gospodje", 'gotovo', 'govoriti', 'hoteti', "imeti", 'iti', 'izvoliti', 'jako', "kr", 'misliti', "moči", "morati", 'nekoliko', "odbor", "odsek", 'ozir', 'popolnoma', 'poročevalec', "poročilo", "poslanec", "predlagati", "predlog", "priloga", 'priti', "prositi", "prošnja", 'reči', "red", "seja", 'skleniti', 'sklep', 'smeti', 'tedaj', 'točka', 'treba', 'vedeti', 'zaklada', "zbor", "zbornica", 'želeti'] + ["abgeordnete", "alle", 'allein', 'also', "ander", 'annehmen', "antrag", 'ausschuß', "beilage", 'bemerken', 'bereits', 'berichterstatter', 'beschließen', "bitten", 'bringen', 'dann', 'derselbe', "dieselbe", 'dr', 'eben', 'finanzausschuß', 'finden', "fl", "ganz", 'geben', "gemeinde", 'gesetz', "glauben", 'groß', 'gut', "haben", "herr", 'heute', "hoch", "jahr", 'jedoch', 'jen', "kein", "kommen", 'landesausschuß', "landtag", 'landtage', "man", 'mehr', 'nämlich', 'nehmen', "noch", "nur", 'sagen', 'schon', 'sehr', 'selbst', "sitzung", 'so', 'solch', "stellen", "um", "weil", "welch", "wollen", "wort", 'wünschen']


names = [join(SOURCE_DIR,f) for f in listdir(SOURCE_DIR) if isfile(join(SOURCE_DIR, f)) and not f.startswith(EXCLUDE)]
print(len(names))

ns = {"default": "http://www.tei-c.org/ns/1.0"}
stopwords = stopwords_ger + stopwords_slo + stopwords_parlament
relevant_upos_tags = ['ADJ', 'ADV', 'NOUN', 'PROPN', 'VERB', 'PRON']

# documents is a dictionary, keys are words, values are pairs (upos, lemma), all stopwords are omitted and
# only words with relevant upos tags ('ADJ', 'ADV', 'NOUN', 'PROPN', 'VERB', 'PRON') are included,
# no duplicated words (preferred lemmas are NOUN and PROPN, VERB, others)
documents = dict()
for i in range(len(names)):
    tree = ET.parse(names[i])
    root = tree.getroot()
    for w in root.findall(".//default:w", ns):
        lemma = w.get('lemma')
        lemma = lemma.lower().replace('.', '').replace(',', '')
        upos = w.get('msd').split('|')[0][len('UPosTag='):]
        if len(lemma) == 0:
            #print('ERROR: lemma for word <' + w.text + '> is an empty string')
            continue
        if lemma not in stopwords and lemma.isalpha() and upos in relevant_upos_tags:
            if w.text in documents.keys():
                value = documents.get(w.text)
                if upos in ['NOUN', 'PROPN'] and value[0] not in ['NOUN', 'PROPN']:
                    value = (upos, lemma)
                elif upos == 'VERB' and value[0] not in ['NOUN', 'PROPN', 'VERB']:
                    value = (upos, lemma)
                documents[w.text] = value
            else:
                documents[w.text] = (upos, lemma)

print("Dict of words prepared")
print(len(documents.keys()))
print("Prepare output data - list of pairs (word, lemma)")

# prepare a list of pairs (word, lemma)
processed_docs = list(map(lambda item: (item[0], item[1][1]), documents.items()))

# save the prepared data
with open(OUTPUT_FILE, 'w', encoding='utf8') as out:
    json.dump(processed_docs, out)
