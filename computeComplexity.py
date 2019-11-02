import nltk
from nltk.corpus import cmudict
d = cmudict.dict()
import textstat
from textstat.textstat import easy_word_set
import argparse
import re
import math

class DocumentComplexity:
    def __init__(self, doc):

        self.__doc = open(doc).read()
        self.__doc = self.preprocess(self.__doc)
        self.__docWords = self.getTotalWords(self.__doc)
        self.__totalWords = textstat.lexicon_count(self.__doc, removepunct=True)
        self.__totalCharacters = textstat.char_count(self.__doc, ignore_spaces=True)
        self.__totalSentences = self.getSentencesCount(self.__doc)
        self.__totalSyllables = self.getSyllablesCount(self.__docWords)
        # self.__totalSyllables = textstat.syllable_count(self.__doc)
        self.__polySyllableCount = self.getPolySyllableCount(self.__docWords)
        print("Syllables, Words, Sentences", self.__totalSyllables, self.__totalWords, self.__totalSentences)
        pass

    def getTotalWords(self, doc):
        """
        Returns total words of the document as list
        :param doc:
        :return:
        """
        totalWords = []
        for line in doc.splitlines():
            totalWords += line.split()
        return totalWords

    def getSentencesCount(self, doc):
            return max(1, len(re.sub(r'[^\.!?]', '', doc)))

    def getSyllablesCount(self, words):
        """
        Returns total syllables of the words array
        :param words:
        :return:
        """
        syllableCount = 0
        for word in words:
            syllableCount += self.getWordSyllable(word)
        return syllableCount

    def difficultWordsCount(self, words):
        """
        Returns difficult word counts
        difficult words are those with syllables >= 2
        easy_word_set is provide by Textstat as
        a list of common words
        :param words:
        :return:
        """
        diffWordsSet = set()

        for word in words:
            # syllableCount = textstat.syllable_count(word)
            syllableCount = self.getWordSyllable(word)
            if word not in easy_word_set and syllableCount >= 2:
                diffWordsSet.add(word)

        return len(diffWordsSet)

    def getWordSyllable(self, word):
        """
        Returns syllables count of the given word
        :param word:
        :return:
        """
        try:
            return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
        except KeyError:
            # if word not found in cmudict
            return self.syllables(word)

    def syllables(self, word):
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
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count += 1
        if count == 0:
            count += 1
        return count

    def getPolySyllableCount(self, words, gunning=False):
        count = 0
        ignore = False
        for word in words:
            if gunning:
                pos = self.getPosTag(word)
                if pos == 'NNP' or pos == 'NNPS' or pos == 'CC':
                    ignore = True
            if self.getWordSyllable(word) >= 3 and not ignore:
            # if textstat.syllable_count(word) >= 3:
                count += 1
        return count

    def getPosTag(self, word):
        word = nltk.word_tokenize(word)
        l1 = nltk.pos_tag(word)
        return l1[0][1]

    def preprocess(self, text):
        """
        Tokenization/string cleaning
        """
        text = re.sub(r'[,:;()\-]', ' ', text)  # Override commas, colons, etc to spaces/
        text = re.sub(r'[\.!?]', '.', text)  # Change all terminators like ! and ? to "."
        text = re.sub(r'^\s+', '', text)  # Remove whites pace
        text = re.sub(r'[ ]*(\n|\r\n|\r)[ ]*', ' ', text)  # Remove new lines
        text = re.sub(r'([\.])[\. ]+', '.', text)  # Change all ".." to "."
        text = re.sub(r'[ ]*([\.])', '. ', text)  # Normalize all "."`
        text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces
        text = re.sub(r'\s+$', '', text)  # Remove trailing spaces
        text = re.sub(r'\b[0-9]+\b', '', text)  # Remove digits
        return text.lower()

    def fleschReadingScore(self):
        """
        Returns Flesch Reading Ease Score
        Formula for calculation is :
        readingScore = 206.835 - 1.015 * (total words/total sentences) - 84.6 * (total syllables/total words)
        :return:
        """
        readingScore = 206.835 - (1.015 * (float(self.__totalWords)/self.__totalSentences))-(84.6*(self.__totalSyllables/float(self.__totalWords)))
        return readingScore

    def daleChallReadabilityScore(self):
        """
        Returns Dale Chall Readability Score
        Formula for calculation is :
        Raw score = 0.1579*(PDW) + 0.0496*(ASL) if the percentage of PDW is less than 5 %, otherwise compute
        Raw score = 0.1579*(PDW) + 0.0496*(ASL) + 3.6365
        Where PDW = Percentage of difficult words not on the Dale–Chall word list.
              ASL = Average sentence length
        :return:
        """
        pdw = (self.difficultWordsCount(self.__docWords) / float(self.__totalWords)) * 100
        asl = float(self.__totalWords)/self.__totalSentences
        rawScore = (0.1579 * pdw) + (0.0496 * asl)
        if rawScore > 5:
            rawScore += 3.6365
        return rawScore

    def gunningFogScore(self):
        """
        Returns Gunning Fog Score
        Grade level= 0.4 * ( (average sentence length) + (percentage of Hard Words) )
        :return:
        """
        polySyllableCount = self.getPolySyllableCount(self.__docWords, True)
        gradeLevel = 0.4*(self.__totalWords/float(self.__totalSentences)) + ((polySyllableCount /self.__totalWords) * 100)
        return gradeLevel

    def automatedReadabilityIndex(self):
        """
        Returns ARI of the document
        Formula for calculation :
        4.71*(characters/words)+0.5*(words/sentences)-21.43
        :return:
        """
        return (4.71 * (self.__totalCharacters/self.__totalWords)) + (0.5 * ( self.__totalWords/self.__totalSentences)) - 21.34


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputDoc', help='Input Document')
args = parser.parse_args()

docComplexityObj = DocumentComplexity(args.inputDoc)

############ Flesch Reading Ease Score ##################
fleschReadingEase = docComplexityObj.fleschReadingScore()
print("Flesch Reading Ease Score : ",fleschReadingEase)

if fleschReadingEase >= 90:
    print('5th grade or lower')
elif fleschReadingEase >=80 and fleschReadingEase < 90:
    print('6th grade')
elif fleschReadingEase >= 70 and fleschReadingEase < 80:
    print('7th grade')
elif fleschReadingEase >= 60 and fleschReadingEase < 70:
    print('8th and 9th grade')
elif fleschReadingEase >= 50 and fleschReadingEase < 60:
    print('10th to 12th grade')
elif fleschReadingEase >= 30 and fleschReadingEase < 50:
    print('College Student')
else:
    print('College graduate')


############ Dale Chall Reading Score ##################
daleChallReadingScore = docComplexityObj.daleChallReadabilityScore()
print("Dale Chall Reading Score : ", daleChallReadingScore)

if daleChallReadingScore >= 9:
    print('College Student')
elif daleChallReadingScore >=8 and daleChallReadingScore < 9:
    print('11th to 12th grade')
elif daleChallReadingScore >= 7 and daleChallReadingScore < 8:
    print('9th to 10th grade')
elif daleChallReadingScore >= 6 and daleChallReadingScore < 7:
    print('7th to 8th grade')
elif daleChallReadingScore >= 5 and daleChallReadingScore < 6:
    print('5th to 6th grade')
else:
    print('4th grade and lower')

############ Gunning Fog Score ###########################
fogScore = docComplexityObj.gunningFogScore()
print('Gunning Fog Score : ', fogScore)
if fogScore >= 17:
    print('College graduate')
elif fogScore >=13 and fogScore < 17:
    print('College student')
elif fogScore >= 9 and fogScore < 12:
    print('High School student')
elif fogScore >= 8 and fogScore < 9:
    print('8th grade')
elif fogScore >= 7 and fogScore < 8:
    print('7th grade')
else:
    print('6th grade and lower')


############ Automated Readbility Index #####################
automatedRI = docComplexityObj.automatedReadabilityIndex()
print('Automated Readability Index', automatedRI)
if automatedRI >= 14:
    print('Professor')
elif automatedRI >=13 and automatedRI < 14:
    print('College student')
elif automatedRI >=10  and automatedRI < 13:
    print('10th to 12th grade')
elif automatedRI >= 7 and automatedRI < 10:
    print('7th to 9th grade')
elif automatedRI >= 5 and automatedRI < 7:
    print('5th to 6th grade')
else:
    print('4th grade and lower')
