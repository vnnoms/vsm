import sys 
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

def preprocess(teks):
    lteks = teks.lower()
    words = word_tokenize(lteks)
    
    stopwordlist = set(stopwords.words('english'))
    punclist = set(string.punctuation)
    stemmer = PorterStemmer()
    
    cleanwords = []
    for word in words:
        if word not in stopwordlist and word not in punclist:
            wordbase = stemmer.stem(word)
            cleanwords.append(wordbase)
            
    return cleanwords

def tfidf(doclist):
    cleandocs = {}
    all_terms = set()
    
    for docname in doclist:
        try:
            with open(docname, 'r') as f:
                filetext = f.read()
                cleanwords = preprocess(filetext)
                cleandocs[docname] = cleanwords
                
                for word in cleanwords:
                    all_terms.add(word)
        except FileNotFoundError:
            print(f"Error: File {docname} tidak ditemukan saat hitung TF-IDF.")
            return None, None, None

    N = len(doclist)
    
    dfterm = {}
    for term in all_terms:
        n = 0
        for docname in doclist:
            if term in cleandocs[docname]:
                n += 1
        dfterm[term] = n

    idfterm = {}
    for term in all_terms:
        n = dfterm[term]
        idfterm[term] = math.log10(N / n)
    tfidfweight = {}
    invertedidx = {term: [] for term in all_terms}

    for docname in doclist:
        tfidfweight[docname] = {}
        wordl = cleandocs[docname]
        
        for term in all_terms:
            freq = wordl.count(term)
            if freq > 0:
                tf = 1 + math.log10(freq)
            else:
                tf = 0
            
            tfidfscore = tf * idfterm[term]
            if tfidfscore > 0:
                tfidfweight[docname][term] = tfidfscore
                invertedidx[term].append((docname, tfidfscore))
    return invertedidx, tfidfweight, idfterm

def qevaluation(queryfilename, tfidfweight, idfterm):
    try:
        with open(queryfilename, 'r') as f:
            qshow = f.read()
    except FileNotFoundError:
        print(f"Error: File query '{queryfilename}' tidak ditemukan.")
        return None
    cleanqword = preprocess(qshow)
    qweight = {}
    for term in set(cleanqword):
        if term in idfterm:
            freq = cleanqword.count(term)
            tf_query = 1 + math.log10(freq) if freq > 0 else 0
            qweight[term] = tf_query * idfterm[term]
    if not qweight:
        return {}
    qtotal = sum(b ** 2 for b in qweight.values())
    norm_query = math.sqrt(qtotal)

    scoresimilarity = {}
    for docname, docweight in tfidfweight.items():
        dotproduct = 0.0
        for term in qweight:
            if term in docweight:
                dotproduct += qweight[term] * docweight[term]
        doctotal = sum(b ** 2 for b in docweight.values())
        norm_doc = math.sqrt(doctotal)

        if norm_doc > 0 and norm_query > 0:
            simscore = dotproduct / (norm_doc * norm_query)
        else:
            simscore = 0.0

        if simscore > 0.001:
            scoresimilarity[docname] = simscore
    ranks = dict(sorted(scoresimilarity.items(), key=lambda item: item[1], reverse=True))
    return ranks

def main():
    if len(sys.argv) < 3:
        print("Error: Jalankan dengan format 'python vsm.py base.txt query.txt'")
        return

    filebasename = sys.argv[1]  
    queryfilebasename = sys.argv[2]  
    doclist = []
    
    try:
        with open(filebasename, 'r') as file:
            for baris in file:
                docname = baris.strip() 
                
                if docname: 
                    doclist.append(docname)
                    
        print("--- LOGIKA INPUT BERHASIL ---")
        print("Isi list daftar_dokumen:", doclist)
        print("File query:", queryfilebasename)

    except FileNotFoundError:
        print(f"Error: File '{filebasename}' tidak ditemukan di folder proyekmu.")
        return
    print("--- MEMULAI PERHITUNGAN MATEMATIKA VSM ---")
    invertedidx, tfidfweight, idfterm = tfidf(doclist)
    if invertedidx is None:
        return
    with open('index.txt', 'w') as fidx:
        for term in sorted(invertedidx.keys()):
            showlist = invertedidx[term]
            weighttxtlist = []
            for docname, weight in showlist:
                no_doc = docname.replace('doc', '').replace('.txt', '')
                weighttxtlist.append(f"{no_doc},{weight:.1f}")
            
            lineprint = " ".join(weighttxtlist)
            fidx.write(f"{term}: {lineprint}\n")
            
    print("-> Berhasil membuat file: index.txt")
    with open('weights.txt', 'w') as f_weights:
        for docname in doclist:
            f_weights.write(f"{docname}: ")
            weighttermlist = []
            for term, weight in tfidfweight[docname].items():
                weighttermlist.append(f"{term}, {weight:.4f}")
            f_weights.write(" ".join(weighttermlist) + "\n")
            
    print("-> Berhasil membuat file: weights.txt")

    ranktotal = qevaluation(queryfilebasename, tfidfweight, idfterm)
    
    if ranktotal is not None:
        with open('response.txt', 'w') as f_response:
            f_response.write(f"{len(ranktotal)}\n")
            for docname, score in ranktotal.items():
                f_response.write(f"{docname} {score:.4f}\n")
                
        print("-> Berhasil membuat file: response.txt")
        print("\n--- SEMUA PROSES SELESAI DENGAN SUKSES! ---")

if __name__ == "__main__":
    main()