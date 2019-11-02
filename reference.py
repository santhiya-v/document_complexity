import re
from nltk.corpus import cmudict
d = cmudict.dict()

def clean_str(self, string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!.?\'\`\r\n]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " ", string)
    string = re.sub(r"!", " ", string)
    string = re.sub(r"\(", " ", string)
    string = re.sub(r"\)", " ", string)
    string = re.sub(r"\?", " ", string)
    string = re.sub(r"[^\S\r\n]", " ", string)
    string = re.sub(r'\b[0-9]+\b', '', string)

    finalString = ''
    paragraph = ''

    for line in string.splitlines():
        if not re.match(r"^(\d|\s)+$", line):  # filters out lines which has only numbers
            if line == '':  # if there is empty line, write the paragraphs to finalString
                if paragraph:
                    finalString += paragraph + "\n"
                    paragraph = ''
            elif len(re.findall(r'\w+', line)) > 1:
                paragraph += line + ' '
    if paragraph:
        finalString += paragraph + "\n"
    finalString = re.sub(' +', ' ', finalString).strip()
    return finalString.strip().lower()


def getTotalWords(doc):
    totalWords = []
    for line in doc.splitlines():
        totalWords += line.split()
    return totalWords

def getWordSyllabel(word):
    """
    Returns syllables count of the given word
    :param word:
    :return:
    """
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
    except KeyError:
        # if word not found in cmudict
        return syllables(word)

def syllables(word):
    """
    Returns syllables count of the given word
    Custom implementation for the words which are not in nltk dictionary
    :param word:
    :return:
    """
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count

    def smogScore(self):
        """
        SMOG grading = 3 + √polysyllable count.
        :return:
        """
        smogScore = 3 + math.sqrt(self.__polySyllableCount)
        return smogScore
# print('readier', textstat.syllable_count('readier'))
# print('karate', textstat.syllable_count('karate'))
# print('insouciance', textstat.syllable_count('insouciance'))
# print('Siberia', textstat.syllable_count('Siberia'))