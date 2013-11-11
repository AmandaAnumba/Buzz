import string

def hashtags(text):
	htset = set(part for part in text.split() if part.startswith('#'))
	t = filter(lambda w: w not in htset,text.split())
	t = ' '.join(t)
	return htset,t

def removePunctuation(text):
	table = string.maketrans("","")
	return text.translate(table, string.punctuation)

def summonDictionary():
	eng_dict_file = open("eng_dict",'r')
	eng_dict = [w.replace('\n','').strip() for w in eng_dict_file.readlines()]
	eng_dict.append('i')
	eng_dict.append('son')
	eng_dict_file.close()
	return eng_dict

def removeDictionaryWords(text):
	eng_dict = summonDictionary()
	noDictWords = []
	for t in text.split():
		if t.strip().lower() in eng_dict:
			continue
		noDictWords.append(t)
	return ' '.join(noDictWords)
	
a = '#Fond #Skrillexasdf! #Fond #Fond #memories of a band I love! #mygoldmask postgig with Gretta and the gals 9.10.10\xe2\x80\xa6 #http://t.co/YtWZB3y8A8'
a = "My son carved his pumpkin lol http://t.co/9hIooX9lqR"
#a = removePunctuation(a)
t = removeDictionaryWords(a)
print a
#ht,a = hashtags(a)
#print ht
print t
	

