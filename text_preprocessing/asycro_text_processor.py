import re
import json
import emoji
from nlp_id.stopword import StopWord
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from concurrent.futures import ProcessPoolExecutor
import asyncio
import rootutils

ROOT = rootutils.autosetup()  # set root path

class TextProcessor:
    def __init__(self, kata_tambahan=None):
        self.stopword = StopWord()  # list of stopwords
        self.slang_words = self.load_slang_words(str(ROOT / 'dataset/combined_slang_words.txt'))  # load slang words from json
        self.kata_tambahan = kata_tambahan if kata_tambahan else ["t", "n", " t", " n", " n ", "dengan", "yang", "dan"]  # additional stop words

        # Initialize stemmer
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()

    def load_slang_words(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def clean_text_sync(self, text):
        emoticon_byte_regex = r"\s*(?:\\x[A-Fa-f0-9]{2})+"
        url_regex = r"((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+)||(http\S+))"
        
        text = re.sub(emoticon_byte_regex, "", text)
        text = re.sub(url_regex, "", text)
        text = re.sub(r"<[^>]*>", "", text)
        text = re.sub(r"@[A-Za-z0-9]+", "", text)
        text = re.sub(r"\n", " ", text)
        text = re.sub("@[\w\-]+", "", text)
        text = re.sub("RT", "", text)
        text = re.sub("USER", "", text)
        text = re.sub(" URL", " ", text)
        text = re.sub(" url", " ", text)
        text = re.sub("\+", " ", text)
        text = re.sub("\s+", " ", text)
        text = re.sub("[^0-9a-zA-Z]", " ", text)
        text = re.sub("[^a-zA-Z]", " ", text)
        text = re.sub(" +", " ", text)
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'RT', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = emoji.demojize(text)
        text = ' '.join(text.split())
        text = text.strip()
        return text

    def replace_slang_words_sync(self, text):
        text = text.lower()
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        words = text.split()
        new_words = [self.slang_words.get(word, word) for word in words]
        return ' '.join(new_words)

    def remove_stopwords_sync(self, caption):
        filtered_caption = ' '.join([word for word in caption.split() if word not in self.kata_tambahan])
        return self.stopword.remove_stopword(filtered_caption)

    def stem_text_sync(self, text):
        return self.stemmer.stem(text)

    def process_single_text_sync(self, text):
        # Combine all synchronous processing steps into one function
        text = self.clean_text_sync(text)
        text = self.replace_slang_words_sync(text)
        text = self.stem_text_sync(text)
        text = self.remove_stopwords_sync(text)
        return text

    async def process_texts(self, texts):
        # Use ProcessPoolExecutor for multiprocessing
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor() as executor:
            tasks = [loop.run_in_executor(executor, self.process_single_text_sync, text) for text in texts]
            results = await asyncio.gather(*tasks)
        return results

"""
import re
import json
import emoji
import asyncio
from nlp_id.stopword import StopWord
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

import rootutils

ROOT = rootutils.autosetup()  # mengatur root path

class TextProcessor:
    def __init__(self, kata_tambahan=None):
        self.stopword = StopWord()  # list stoword
        self.slang_words = self.load_slang_words(str(ROOT / 'dataset/combined_slang_words.txt'))  # load slangword dalam bentuk json
        self.kata_tambahan = kata_tambahan if kata_tambahan else ["t", "n", " t", " n", " n ", "dengan", "yang", "dan"]  # list kata kata tambahan untuk stop word

        # Inisialisasi stemmer
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()

    def load_slang_words(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    async def clean_text(self, text):
        emoticon_byte_regex = r"\s*(?:\\x[A-Fa-f0-9]{2})+"
        url_regex = r"((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+)||(http\S+))"
        
        text = re.sub(emoticon_byte_regex, "", text)
        text = re.sub(url_regex, "", text)
        text = re.sub(r"<[^>]*>", "", text)
        text = re.sub(r"@[A-Za-z0-9]+", "", text)
        text = re.sub(r"\n", " ", text)
        text = re.sub("@[\w\-]+", "", text)
        text = re.sub("RT", "", text)
        text = re.sub("USER", "", text)
        text = re.sub(" URL", " ", text)
        text = re.sub(" url", " ", text)
        text = re.sub("\+", " ", text)
        text = re.sub("\s+", " ", text)
        text = re.sub("[^0-9a-zA-Z]", " ", text)
        text = re.sub("[^a-zA-Z]", " ", text)
        text = re.sub(" +", " ", text)
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'RT', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = emoji.demojize(text)
        text = ' '.join(text.split())
        text = text.strip()
        await asyncio.sleep(2)
        return text

    async def replace_slang_words(self, text):
        text = text.lower()
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        words = text.split()
        new_words = []
        for word in words:
            if word in self.slang_words:
                new_words.append(self.slang_words[word])
            else:
                new_words.append(word)
        new_text = ' '.join(new_words)
        await asyncio.sleep(2)
        return new_text

    async def remove_sentence(self, caption):
        word = caption.split()
        wordCount = len(word)
        if wordCount <= 1:
            caption = ''
        await asyncio.sleep(2)
        return caption

    async def remove_stopwords(self, caption):
        filtered_caption = ' '.join([word for word in caption.split() if word not in self.kata_tambahan])
        filtered_caption = self.stopword.remove_stopword(filtered_caption)
        await asyncio.sleep(2)
        return filtered_caption

    async def stem_text(self, text):
        \"""
        Mengaplikasikan stemming pada teks menggunakan stemmer dari Sastrawi.
        
        Args:
            text (str): Teks yang akan distem.
        
        Returns:
            str: Teks yang telah distem.
        \"""
        stemmed_text = self.stemmer.stem(text)
        await asyncio.sleep(2)
        return stemmed_text

    async def clean_data(self, text):
        cleaned_text = await self.clean_text(text)
        replaced_text = await self.replace_slang_words(cleaned_text)
        stemmed_text = await self.stem_text(replaced_text)  # Menambahkan langkah stemming
        without_sentence = await self.remove_sentence(stemmed_text)
        without_stopwords = await self.remove_stopwords(without_sentence)
        return without_stopwords

    async def process_texts(self, texts):
        tasks = [self.clean_data(text) for text in texts]
        results = await asyncio.gather(*tasks)
        return results
"""