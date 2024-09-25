import random
import pickle
import re

wordnet = {}
with open("wordnet.pickle", "rb") as f:
	wordnet = pickle.load(f)

# 한글, 알파벳, 공백만 남기고 나머지는 모두 제거.
def get_only_hangul(line):
	parseText= re.compile('[^가-힣\s]').sub('',line)

	return parseText

# 한글, 알파벳, 공백만 남기고 나머지는 모두 제거.
def get_only_character(line):
	parseText= re.compile('[^가-힣a-zA-Z\s]').sub('',line)

	return parseText

def get_words(sentence):
	return list(filter(lambda x:x!='',sentence.split(' ')))


########################################################################
# Synonym replacement
# Replace n words in the sentence with synonyms from wordnet
########################################################################
def synonym_replacement(words, n):
	new_words = words.copy()
	random_word_list = list(set([word for word in words]))
	random.shuffle(random_word_list)
	num_replaced = 0
	for random_word in random_word_list:
		synonyms = get_synonyms(random_word)
		if len(synonyms) >= 1:
			synonym = random.choice(list(synonyms))
			new_words = [synonym if word == random_word else word for word in new_words]
			num_replaced += 1
		if num_replaced >= n:
			break

	if len(new_words) != 0:
		sentence = ' '.join(new_words)
		new_words = sentence.split(" ")

	else:
		new_words = ""

	return new_words


def get_synonyms(word):
	synomyms = []

	try:
		for syn in wordnet[word]:
			for s in syn:
				synomyms.append(s)
	except:
		pass

	return synomyms

########################################################################
# Random deletion
# Randomly delete words from the sentence with probability p
########################################################################
def random_deletion(words, p):
	if len(words) == 1:
		return words

	new_words = []
	for word in words:
		r = random.uniform(0, 1)
		if r > p:
			new_words.append(word)

	if len(new_words) == 0:
		rand_int = random.randint(0, len(words)-1)
		return [words[rand_int]]

	return new_words

########################################################################
# Random swap
# Randomly swap two words in the sentence n times
########################################################################
def random_swap(words, n):
	new_words = words.copy()
	for _ in range(n):
		new_words = swap_word(new_words)

	return new_words

def swap_word(new_words):
	random_idx_1 = random.randint(0, len(new_words)-1)
	random_idx_2 = random_idx_1
	counter = 0

	while random_idx_2 == random_idx_1:
		random_idx_2 = random.randint(0, len(new_words)-1)
		counter += 1
		if counter > 3:
			return new_words

	new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
	return new_words

########################################################################
# Random insertion
# Randomly insert n words into the sentence
########################################################################
def random_insertion(words, n):
	new_words = words.copy()
	for _ in range(n):
		add_word(new_words)
	
	return new_words


def add_word(new_words):
	synonyms = []
	counter = 0
	while len(synonyms) < 1:
		if len(new_words) >= 1:
			random_word = new_words[random.randint(0, len(new_words)-1)]
			synonyms = get_synonyms(random_word)
			counter += 1
		else:
			random_word = ""

		if counter >= 10:
			return
		
	random_synonym = synonyms[0]
	random_idx = random.randint(0, len(new_words)-1)
	new_words.insert(random_idx, random_synonym)



def EDA(sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=9):
	"""
	:param sentence: 한 문장
	:param alpha_sr/ri/rs: num_words 중 sr/ri/rs 을 적욜할 단어의 개수 비율을 설정
	:param p_rd: num_words 중 rd를 적용할 비율을 설정
	:param num_aug: EDA로 증강할 문장 개수
	:return: List[증강된 문장들]
	"""
	sentence = get_only_character(sentence)
	words = sentence.split(' ')
	words = [word for word in words if word != ""]
	num_words = len(words) # 한 문장의 총 단어 개수

	augmented_sentences = []
	num_new_per_technique = int(num_aug/4) + 1

	n_sr = max(1, int(alpha_sr*num_words))
	n_ri = max(1, int(alpha_ri*num_words))
	n_rs = max(1, int(alpha_rs*num_words))

	# sr
	for _ in range(num_new_per_technique):
		a_words = synonym_replacement(words, n_sr)
		augmented_sentences.append(' '.join(a_words))

	# ri
	for _ in range(num_new_per_technique):
		a_words = random_insertion(words, n_ri)
		augmented_sentences.append(' '.join(a_words))

	# rs
	for _ in range(num_new_per_technique):
		a_words = random_swap(words, n_rs)
		augmented_sentences.append(" ".join(a_words))

	# rd
	for _ in range(num_new_per_technique):
		a_words = random_deletion(words, p_rd)
		augmented_sentences.append(" ".join(a_words))

	augmented_sentences = [get_only_hangul(sentence) for sentence in augmented_sentences]
	random.shuffle(augmented_sentences)

	if num_aug >= 1:
		augmented_sentences = augmented_sentences[:num_aug]
	else:
		keep_prob = num_aug / len(augmented_sentences)
		augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

	augmented_sentences.append(sentence)

	return augmented_sentences


def EDA_paragraph(paragraph, sentence_sep='.', alpha_sent=0.7, methods=['all'], method_alphas=[0.1, 0.1, 0.1, 0.1], num_aug=3):
	"""
	:param paragraph: List[str] - 문장은 sentence_sep로 구분되어야 한다.
	:param alpha_sent: 한 문단에서 EDA를 적용할 문장의 비율
	:param methods:
		['all'] : sr,ri,rs,rd 모두 사용
		['sr','ri'] 처럼 지정 시 : 해당 EDA method만 사용
	:param method_alphas: methods에 전달한 EDA 기법에 대응하는 alpha값과 p값을 설정
	:param num_aug: EDA로 증강할 문단 개수
	:return: List[증강된 문단]
	"""
	# 줄바꿈 기호 제거
	paragraph = re.compile('[\n\r]').sub('',paragraph)
	# 문장 구분 + 한글만 남기기
	sentences = list(filter(lambda x:len(x)>0,map(get_only_character,paragraph.split(sentence_sep))))
	sentences_index = list(range(sentences.__len__()))
	# EDA를 적용할 문장 선택
	random_index = random.sample(range(sentences.__len__()), int(sentences.__len__()*alpha_sent))
	# random_index 문장에 랜덤하게 EDA 적용
	if methods[0] == 'all':
		methods = ['sr','ri','rs','rd']
	# method와 method_alphas는 개수가 같아야 한다.
	assert methods.__len__() == method_alphas.__len__()

	augmented_paragraphs = set()

	while 1:
		for i in random_index:
			random_method_index = random.randint(0, methods.__len__()-1) # 적용할 EDA 방식 랜덤 선택
			method_func = get_method_function(methods[random_method_index])
			# 문장 >> words list
			sent = get_only_character(sentences[i])
			words = get_words(sentences[i])
			if methods[random_method_index] != 'rd':
				n_changes = max(1, int(method_alphas[random_method_index]*words.__len__()))
			else:
				n_changes = method_alphas[random_method_index]
			a_words = method_func(words, n_changes)
			# 기존 문장을 증강된 문장으로 대체
			sentences[i] = ' '.join(a_words)
		# 문장들을 다시 합치고 문장 끝에 마침표를 붙여서 문단으로 반환
		augmented_paragraphs.add('. '.join(sentences))
		if len(augmented_paragraphs) == num_aug: 
			# 증강 문단들을 집합에 저장함으로써 중복을 피함 -> num_aug에 도달했을 때 증강 중단.
			break
	return list(augmented_paragraphs)	


def get_method_function(method):
	if method == 'sr':
		return synonym_replacement
	if method == 'ri':
		return random_insertion
	if method == 'rs':
		return random_swap
	if method == 'rd':
		return random_deletion