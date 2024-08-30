# Text Normalization

<p align='justify'>Text normalization adalah proses untuk mengubah teks menjadi format yang lebih standar atau konsisten, sehingga dapat diproses lebih efektif oleh mesin dalam berbagai aplikasi, seperti pemrosesan bahasa alami (*Natural Language Processing*). Berikut adalah beberapa teknik utama dalam *text normalization*:</p>

## 1. Replace Slangword
<p align='justify'>Slangword atau kata gaul sering digunakan dalam percakapan sehari-hari, tetapi mungkin tidak diakui dalam bahasa formal atau kamus. Untuk membuat teks lebih standar, kita dapat mengganti slangword dengan kata yang lebih formal atau standar.</p>

### Contoh:
- "gak" menjadi "tidak"
- "btw" menjadi "by the way"
- "bgt" menjadi "banget"

## 2. Stemming
<p align='justify'>Stemming adalah proses mengubah kata menjadi bentuk dasarnya dengan menghapus akhiran-akhiran (suffixes). Berbeda dengan lemmatization, stemming seringkali lebih cepat dan tidak mempertimbangkan konteks kata, sehingga hasilnya bisa kurang akurat.</p>

### Contoh:
"running" menjadi "run"
"happiness" menjadi "happi"

## 3. Lemmatization
<p align='justify'>Lemmatization adalah proses mengubah kata menjadi bentuk dasarnya atau bentuk lema, dengan mempertimbangkan konteks dan bagian dari ucapan (misalnya, kata benda, kata kerja). Lemmatization biasanya lebih akurat dibandingkan stemming karena mempertimbangkan konteks morfologis dari kata.</p>

### Contoh:
"better" menjadi "good"
"running" menjadi "run"

## Kesimpulan
<p align='justify'>Proses text normalization seperti mengganti slangword, stemming, dan lemmatization sangat penting dalam mempersiapkan teks untuk analisis lebih lanjut dalam pemrosesan bahasa alami. Dengan menormalisasi teks, kita dapat memastikan bahwa data yang diproses lebih konsisten dan mudah dipahami oleh algoritma NLP.</p>