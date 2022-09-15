#!/usr/bin/env python
# coding: utf-8

# ## Week 1 Reflection

# ### Der Dunkelgraf - Ludwig Bechstein
Working with the two example codes, either with example data such as the book downloaded from Gutenberg in the examples or with text data of particular interest to you, please answer the following questions briefly.1, What data did you use? If it is a book from Gutenberg, which one? 

   I have chosen die Verwandelung von Franz Kafka from Gutenberg.
   URL: https://www.gutenberg.org/cache/epub/22367/pg22367.txt2, Can you estimate how many sentences it contains? What can you do to compute this (conceptually, in Python and / or in R)?
# In[1]:


target = 22367 # Ebook number
import gutenbergpy.textget
raw = gutenbergpy.textget.get_text_by_id(target)
book= gutenbergpy.textget.strip_headers(raw)
count = 50 #number of charaters will be displayed


# In[2]:


# book head
book[:count]


# In[3]:


# book tail 
book[-count:]


# In[ ]:





# In[4]:


s = book.decode("utf-8") # get a string from the byte sequence
startmarker = '1917'
endmarker = 'Tochter als erste sich erhob und ihren jungen Körper dehnte.'
startPosition = s.index(startmarker) + len(startmarker)
endPosition = s.index(endmarker)+len(endmarker)
content = s[startPosition:endPosition]
print(content[:count]) # start
print(content[-count:]) # end


# In[ ]:





# In[208]:


import re
# extract Roman Numerals and replace them with 'ROMAN' by using Regular Expression
text = re.sub(r'(?=\b[MCDXLVI]{1,6}\b)M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})', 'ROMAN', content)
#print(text)


# In[177]:


# count the number of sections
sections = text.count('ROMAN')
print(sections, 'potential sections')


# In[176]:


# removing the sections headers
print('No digits:', sections)
clean = re.compile(r'\s+') # also combine any kind of repeated whitespace into a single space
ok = clean.sub(' ', text)
print('Cleaned:', ok[:count])
potential = ok.split('ROMAN')
stripped = [ candidate.strip().lstrip() for candidate in potential ] # remove leading and trailing space 
real = [ s for s in stripped if len(s) > 0 ] # keep only the ones with content
print(len(real), 'real chapters')
print(real[0][:count])


# In[8]:


# convert list to a string
real_text = ' '
for x in real:
    real_text += ' ' + x


# In[9]:


# sentence count
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

number_of_sentences = sent_tokenize(real_text)

print('There are ' + str(len(number_of_sentences)) + ' sentences in this book.')

3, How about paragraphs? Can you estimate how many there are? What can you do to
compute this (conceptually, in Python and/or in R)?
# In[10]:


# count paragraphs 
print ('There are ' + str(content.count("\n\n")) + ' paragraphs in the book.')

4, How many names (of places and people) are mentioned in the text? What did you do to
compute this (conceptually, in Python and/or in R)?
# In[18]:


new_string = re.sub(r'[^\w\s]', '', real_text)


# In[197]:


from HanTa import HanoverTagger as ht
tagger = ht.HanoverTagger('morphmodel_ger.pgz')
words = nltk.word_tokenize(new_string)
#print(tagger.tag_sent(words) )
tokens=[word for (word,x,pos) in tagger.tag_sent(words,taglevel= 1) if pos == 'NN']


# In[112]:


from collections import Counter
counts = Counter(tag for word,word,tag in tagger.tag_sent(words))


# In[109]:


print('There are ' +  str(counts['NN'])+ ' Nouns in this book.')


# In[118]:


noun = Counter(i for i in tokens)
noun.most_common(20)

5. What are the ten most frequent words in the text that you consider to clearly be stop
words?
# In[66]:


import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
skip = stopwords.words('german')


# In[81]:


stopwords_book = []
for w in new_string.split():
    if w in skip:
        stopwords_book.append(w)


# In[99]:


# Top 10 stop words 
num_stopwords = Counter(i for i in stopwords_book if i in new_string.split())
sort_num_stopwords = sorted(num_stopwords.items(), key=lambda pair: pair[1], reverse=True)
sort_num_stopwords[:10]

6. What are the ten most frequent words in the text that you consider to not be stop words?
# In[103]:


wordsFiltered = []
for w in new_string.split():
    if w not in skip:
        wordsFiltered.append(w)


# In[104]:


Counter(wordsFiltered).most_common(10)

7. How would you go about automatically identifying potential stop words for documents
written in a language you do not speak?As a Linguist 
1, Look for words that are repeated the most
2, Spot a noun, and see if this nous precedes a word, and if this word is repeaded many times in a text, then it might be a article, which is also a stop word
3, Look for prepositions in a sentence. Prepositions are indeclinable words, or words that have only one possible form, that establish the relationship between words in a sentence. In German, words follows a preposition must take the right grammatical form because they are operated by cases. 

As a Data Scientist
1, A good way to mathematically define stop words for corpora form different domains is to compute the inverse document frequency (IDF) of a word, but this method is subject domain specific, it differs from text to text. 
2, Compute word frequency in a text. Most frequent words in a text are ususaly stop words. 
3, Analyse words per 'document'. In a text, stopwords can be detected by finding words that exist in a large number of documents.
4, Employ Zipf's Law. It is a term based method, that observes the term's rank-frequency distribution can be fitted very closely by the relation F(r) = C/r^𝛼, where 𝛼 ≈ 1 and C ≈ 0.1. Each collection is indexed, stemmed but no tokens are removed. It allows one to determine the best possible stopworkd list for a given collection. 
5, Use the Kullback-Leibler divergence measure, it determines the amount of information a word contains. The less information a word has, the more likely it is going to be a stopword. 8.Looking at a histogram of the word frequencies (like the horizontal bar chart in the R
example code), what can be said about the shape of the distribution?
# In[231]:


# convert list to a string
f = ' '
for x in wordsFiltered:
    f += ' ' + x


# In[233]:


import nltk

def graph():
    tokens = nltk.tokenize.word_tokenize(f)
    fd = nltk.FreqDist(tokens)
    fd.plot(30,cumulative=False)

graph()

Looking at the graph above, it is very skewed. Between the highest word count and the lowerest word count, one can say that the spread of data is quite large. 9. Please show an example of a word cloud you created from your text along with a code
snippet of how you did it.
# In[223]:


import operator
for chapter in real:
    freq = { w : chapter.count(w) for w in chapter.split() } # build a dictionary
    top = max(freq.items(), key = operator.itemgetter(1))[0] # the most frequent word
    longest = max(freq.keys(), key = len) # the longest word
    print(top, longest)


# In[184]:


from string import punctuation
for chapter in real:
    nopunct = chapter.translate(str.maketrans(punctuation, ' ' * len(punctuation))) # substitute with space
    ok = clean.sub(' ', nopunct) # in case we made repeated spaces
    words = ok.split()
    freq = { w : words.count(w) for w in words if w.lower() not in skip } # build a dictionary of the non-stopwords
    top = max(freq.items(), key = operator.itemgetter(1))[0] # the most frequent word
    longest = max(freq.keys(), key = len) # the longest word
    print(top, longest)


# In[185]:


skip +=['Gregor']
from string import printable # this does not contain mdash & those angled quotes 
print('OK:', printable)
nonprint = f'[^{re.escape(printable)}]'


# In[186]:


for chapter in real:
    nopunct = chapter.translate(str.maketrans(punctuation, ' '*len(punctuation)))
    better = re.sub(nonprint, ' ', nopunct)
    ok = clean.sub(' ', better) # in case we made repeated spaces
    words = ok.split()
    freq = { w : words.count(w) for w in words if w.lower() not in skip } # now with ours on the skip list
    top = max(freq.items(), key = operator.itemgetter(1))[0] 
    longest = max(freq.keys(), key = len) 
    shortest = min(freq.keys(), key = len) 
    print(top, longest, shortest)


# In[189]:


words = set() # let's collect all the words
for chapter in real:
    nopunct = chapter.translate(str.maketrans(punctuation, ' '*len(punctuation)))
    better = re.sub(nonprint, ' ', nopunct)
    ok = clean.sub(' ', better) # in case we made repeated spaces
    words.update(set(better.split())) # include these new words in the set

names = set()
regular = set()
for w in words:
    if len(w) < 3:
        continue # too short for our taste
    u = w.upper() # all uppercase version
    l = w.lower() # all lowercase version
    if w == u: # the word WAS all uppercase
        w = l.capitalize() # just a capital initial, then
    if l in skip or u in skip or w in skip:
        continue # ignore stop words
    if l in words: # not a name since it also appears in lowercase
        regular.add(l) # only keep the lowercase version
    else:
        names.add(w)
print(names)


# In[224]:


top = 20
for chapter in real:
    nopunct = chapter.translate(str.maketrans(punctuation, ' ' * len(punctuation)))
    better = re.sub(nonprint, ' ', nopunct)
    ok = clean.sub(' ', better) 
    words = better.split()
    freq = { w.lower() : words.count(w) for w in words if w not in skip and w not in names and len(w) > 2 } # skip names, too, and make these lowercase
    highest = sorted(freq, key = freq.get, reverse = True)[:top]
    print(highest)


# In[225]:


from wordcloud import WordCloud, ImageColorGenerator

import matplotlib.pyplot as plt


# print(f'Plotting just the last chapter')
# chapter = real[-1]
nopunct = real_text.translate(str.maketrans(punctuation, ' ' * len(punctuation)))
better = re.sub(nonprint, ' ', nopunct)
ok = clean.sub(' ', better) 
words = better.split()
draw = ' '.join([ w.lower() for w in words if w not in skip and w not in names and len(w) > 2 ])
cloud = WordCloud().generate(draw)
plt.imshow(cloud)
plt.axis('off')
plt.show()

