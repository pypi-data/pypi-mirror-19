from os.path import dirname, realpath
from collections import Counter

directory = dirname(realpath(__file__))

language_to_code = {
"Arabic": "ar",
"English": "en",
"French": "fr",
"German": "de",
"Kurdish": "ku",
"Kurmanci": "ku-ku",
"Italian": "it",
"Portuguese": "pt",
"Sorani": "ku-so",
"Spanish": "es",
"Turkish": "tr",
"Vietnamese": "vi",
"Welsh": "cy"
}


char_language = []
with open(directory + "/prep/char_language.txt") as f:
    for line in f:
        if line:
            char, language, score = line.decode("utf-8").strip().split(u"\t")
            score = float(score)
            char_language.append((char, language, score))

def detect_language_text(text):
    if isinstance(text, str):
        text = text.decode("utf-8")

    # could make this more sophisticated with using TFIDF scores probably
    counts = Counter()
    for char, language, score in char_language:
        if char in text:
            #print "MATCHED", [char]
            counts[language] += score
    # basically return whichever language has most amount of special letters in there
    results = counts.most_common(1) 
    if results:
        return results[0][0]

# just returns the most common language of an iterable of string values
# an example of this can be a list of names
def detect_language_iterable(iterable):
    # may be able to speed this up with out using counter
    # hmmm nvm.. it's so freaking quick anyway, that probably don't worry about this now
    most_common = Counter([detect_language(iteration) for iteration in iterable]).most_common(2)
    if most_common[0][0]:
        return most_common[0][0]
    elif len(most_common) == 2:
        # know that not returning 1st one
        return most_common[1][0]
    # will return None if doesn't match any above

def detect_language(inpt, return_as_code=False):
    if isinstance(inpt, str) or isinstance(inpt, unicode):
        language = detect_language_text(inpt)
    elif isinstance(inpt, set) or isinstance(inpt, list):
        language = detect_language_iterable(inpt)
    if language:
        if return_as_code:
            if language in language_to_code:
                return language_to_code.get[language]
            else:
                return language
        else:
            return language


def isArabic(inpt):
    return detect_language(inpt) == "Arabic"

def isEnglish(inpt):
    return detect_language(inpt) == "English"
