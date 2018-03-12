from collections import Counter
import numpy as np

class conllu_file(object):

    known_tags = ['I-PER', 'B-MISC', 'I-ORG', 'I-MISC', 'B-PER', 'B-ORG', 'B-LOC', 'O', 'I-LOC']
    
    def __init__(self, conllu_path):
        self.conllu_path = conllu_path
        self._word_count = None
        self._words = None

    def yield_sentences(self):
        sentence = []
        for line in open(conllu_dir, 'r', encoding = 'latin-1'):
            stripped_line = line.strip().split(' ')
            
            if line == '\n':
                yield sentence
                sentence = []
            else:
                sentence.append(stripped_line)
    @property
    def word_count(self):
        if not self._word_count:
            max_sentence_length = 0
            labels = set()
            counter = Counter()
            for sentence in self.yield_sentences():
                max_sentence_length = max(max_sentence_length, len(sentence))
                words = [w[0] for w in sentence]
                labels = labels.union([w[1] for w in sentence])
                counter.update(words)

            self._max_sentence_length = max_sentence_length
            self._labels = list(labels)
            self._word_count = counter
            return counter
        return self._word_count
    
    @property
    def max_sentence_length(self):
        if not self._word_count:
            self.word_count
        return self._max_sentence_length

    @property
    def words(self):
        return list(self.word_count.keys())
    
    @property
    def labels(self):
        if not self._word_count:
            self.word_count
        return self._labels

    def words_to_lower(self):
        lower_word_count = {}
        for k, v in self.word_count.items():
            word = k.lower()
            if word in lower_word_count:
                lower_word_count[word] += self.word_count[word]
            else:
                lower_word_count[word] = self.word_count[word]
        self._word_count = lower_word_count

class encoder():
    def __init__(self, elements):
        
        self._encoding_size = len(elements) + 2
        self._unknown_element_index = self._encoding_size - 1
        self._sequence_padding_index = self._encoding_size - 2

        # i.e. {"el1":1, "el2":2}
        self._element_indexer = {element: index for index, element in enumerate(elements)}

    # TODO: improve
    def encode_sequence(self, element_sequence, size):
        e = np.zeros((size, self._encoding_size))
        
        for i in range(size):            
            if i < len(element_sequence):
                if element_sequence[i] in self._element_indexer:
                    e[i][self._element_indexer[element_sequence[i]]] = 1
                else:
                    e[i][self._unknown_element_index] = 1
            else:
                e[i][self._sequence_padding_index] = 1
        return e        

class conllu_encoder():
    def __init__(self, conllu_file, words_dictionary = None, tags_dictionary = None, max_sentence_length = None, capitalized = False):
        self._conllu_file = conllu_file
        
        self._words_dictionary = words_dictionary if words_dictionary else self._conllu_file.words
        self._tags_dictionary = tags_dictionary if tags_dictionary else self._conllu_file.known_tags
        
        self._words_encoder = encoder(self._words_dictionary)
        self._tags_encoder = encoder(self._tags_dictionary)

    # def yield_encoded_sentences(self):
    #     if capitalized:
    #         return NotImplementedError

    #     encoder = 

    #     for sentence in self._conllu_file.yield_sentences():
    #         return encode_sequence

conllu_dir = "/home/daniel/Repositories/Models/conll2002/files/esp.testa"

cf = conllu_file(conllu_dir)
print(next(cf.yield_sentences()))
#print(cf.word_count)
print(cf.words[:10])
cf.words_to_lower()
#print(cf.word_count)
print(cf.words[:10])
print(cf.max_sentence_length)
print(cf.labels)

ce = conllu_encoder(cf)
print(ce._tags_encoder.encode_sequence(["Brasil","I-PER",".",'B-ORG', 'B-LOC', 'B-PER', 'I-PER', 'I-ORG', 'I-MISC', 'B-MISC', 'O', 'I-LOC'], 18))