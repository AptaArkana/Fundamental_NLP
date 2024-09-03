import re
import json
import emoji
import asyncio
from nlp_id.stopword import StopWord

import rootutils

ROOT = rootutils.autosetup() # mengatur root path

class TextProcessor:
    """
    Class TextProcessor digunakan untuk memproses teks dengan melakukan pembersihan teks, 
    mengganti kata-kata slang, menghapus stopwords, dan memproses teks.
    
    Atribut:
        stopword (StopWord): Objek untuk mengelola stopwords.
        slang_words (dict): Kamus berisi kata-kata slang dan pengganti mereka.
        kata_tambahan (list): Daftar kata tambahan yang ingin dihapus dari teks.
    """
    def __init__(self, kata_tambahan=None):
        """
        Inisialisasi objek TextProcessor.
        
        Args:
            kata_tambahan (list, optional): Daftar kata tambahan untuk dihapus. 
                                            Jika None, akan menggunakan daftar default.
        """
        self.stopword = StopWord() # list stoword
        self.slang_words = self.load_slang_words(str(ROOT /'dataset\combined_slang_words.txt')) # load slangword dalam bentuk json
        self.kata_tambahan = kata_tambahan if kata_tambahan else ["t", "n", " t", " n", " n ", "dengan", "yang", "dan"] # list kata kata tambahan untuk stop word

    def load_slang_words(self, file_path):
        """
        Memuat kata-kata slang dari file JSON.
        
        Args:
            file_path (str): Path ke file JSON yang berisi kata-kata slang.
        
        Returns:
            dict: Kamus berisi kata-kata slang dan pengganti mereka.
        """
        # untuk load file slangword dalam bentuk json
        with open(file_path, 'r') as f:
            return json.load(f)

    async def clean_text(self, text):
        """
        Membersihkan teks dari emoticon, URL, tag HTML, nama pengguna, RT, dan simbol lainnya.
        
        Args:
            text (str): Teks yang akan dibersihkan.
        
        Returns:
            str: Teks yang telah dibersihkan.
        """
        emoticon_byte_regex = r"\s*(?:\\x[A-Fa-f0-9]{2})+"  # untuk mendeteksi dan menghapus byte emoticon (karakter yang di-encode sebagai \xHH, di mana H adalah digit heksadesimal).
        url_regex = r"((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+)||(http\S+))" # ini digunakan untuk mendeteksi dan menghapus URL dari teks.

        text = re.sub(emoticon_byte_regex, "", text)  # menghapus byte emoticon
        text = re.sub(url_regex, "", text)  # menghapus setiap URL
        text = re.sub(r"<[^>]*>", "", text)  # menghapus tag HTML
        text = re.sub(r"@[A-Za-z0-9]+", "", text)  # menghapus nama pengguna Twitter
        text = re.sub(r"\n", " ", text)  # menghapus setiap baris baru '\n'
        text = re.sub("@[\w\-]+", "", text)  # menghapus mention
        text = re.sub("RT", "", text)  # menghapus simbol retweet
        text = re.sub("USER", "", text)  # menghapus setiap kata "USER"
        text = re.sub(" URL", " ", text)  # menghapus kata "URL"
        text = re.sub(" url", " ", text)  # menghapus kata "url"
        text = re.sub("\+", " ", text)  # menghapus backslash
        text = re.sub("\s+", " ", text)  # menghapus karakter khusus ekspresi reguler
        text = re.sub("[^0-9a-zA-Z]", " ", text)  # menghapus tanda baca
        text = re.sub("[^a-zA-Z]", " ", text)  # menghapus angka
        text = re.sub(" +", " ", text)  # menghapus spasi ekstra
        # Menghapus URL atau tautan
        text = re.sub(r'http\S+', '', text)
        # Menghapus hashtag (#)
        text = re.sub(r'#\w+', '', text)
        # Menghapus nama pengguna dan mention (@)
        text = re.sub(r'@\w+', '', text)
        # Menghapus retweet (RT)
        text = re.sub(r'RT', '', text)
        # Menghapus tanda baca, baris baru, angka, spasi kosong, dan emoji
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\d+', '', text)
        # Menghapus emoji (Anda dapat menambahkan pola emoji lainnya)
        text = emoji.demojize(text)
        # Menghapus spasi ekstra dan spasi di awal/akhir
        text = ' '.join(text.split())
        text = text.strip()
        await asyncio.sleep(2)
        return text

    async def replace_slang_words(self, text):
        """
        Mengganti kata-kata slang dalam teks dengan padanan formalnya.
        
        Args:
            text (str): Teks yang akan diproses.
        
        Returns:
            str: Teks dengan kata-kata slang yang telah diganti.
        """
        text = text.lower() # casefolding lower
        text = re.sub(r'\n', ' ', text) # menghapus new line 
        text = re.sub(r'\s+', ' ', text) # mengahapus spasi berlebih
        words = text.split() # memotong kalimat
        new_words = [] # variabel untuk menampung kata kata yang sudah dinormalisasikan
        for word in words: # looping untuk normalisasikan
            if word in self.slang_words: # pengecekan slangword
                new_words.append(self.slang_words[word])
            else:
                new_words.append(word)
        new_text = ' '.join(new_words) # menyatukan menjadi kalimat
        await asyncio.sleep(2)
        return new_text

    async def remove_sentence(self, caption):
        """
        Menghapus kalimat jika hanya terdiri dari satu kata atau kurang.
        
        Args:
            caption (str): Teks yang akan diproses.
        
        Returns:
            str: Teks setelah menghapus kalimat yang tidak diinginkan.
        """
        word = caption.split() # memotong kalimat
        wordCount = len(word) # pengecekan panjang kata
        if wordCount <= 1: # kondisi kata kurang dari samadengan 1
            caption = ''
        await asyncio.sleep(2)
        return caption

    async def remove_stopwords(self, caption):
        """
        Menghapus stopwords dari teks, termasuk kata tambahan yang ditentukan.
        
        Args:
            caption (str): Teks yang akan diproses.
        
        Returns:
            str: Teks setelah stopwords dihapus.
        """
        # Hapus kata-kata yang ada di self.kata_tambahan
        filtered_caption = ' '.join([word for word in caption.split() if word not in self.kata_tambahan])
        
        # Hapus stopwords menggunakan metode stopword remover dari self.stopword
        filtered_caption = self.stopword.remove_stopword(filtered_caption)
        await asyncio.sleep(2)
        return filtered_caption

    async def clean_data(self, text):
        """
        Menggabungkan proses pembersihan teks, penggantian kata slang, penghapusan kalimat, 
        dan penghapusan stopwords dalam satu fungsi.
        
        Args:
            text (str): Teks yang akan diproses.
        
        Returns:
            str: Teks yang telah melalui semua proses pembersihan.
        """
        cleaned_text = await self.clean_text(text) # memanggil fungsi text cleaning
        replaced_text = await self.replace_slang_words(cleaned_text) # memanggil fungsi menormalisasikan slangword
        without_sentence = await self.remove_sentence(replaced_text) # memanggil fungsi hapus sentence kurang samadengan 1
        without_stopwords = await self.remove_stopwords(without_sentence) # memanggil fungsi menghapus stopwords
        return without_stopwords
    
    async def process_texts(self, texts):
        """
        Memproses daftar teks secara asinkron untuk melakukan pembersihan teks.
        
        Args:
            texts (list): Daftar teks yang akan diproses.
        
        Returns:
            list: Daftar teks yang telah dibersihkan.
        """
        # Fungsi asinkron untuk memproses teks
        tasks = [self.clean_data(text) for text in texts]
        results = await asyncio.gather(*tasks)
        return results

    '''async def process_texts(self, texts):
        with ProcessPoolExecutor() as executor:
            tasks = [self.clean_data(text) for text in texts]
            results = await asyncio.gather(*tasks)
        return results'''