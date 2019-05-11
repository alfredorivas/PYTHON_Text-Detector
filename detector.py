# -*- coding: utf-8 -*-
"""
Translator: https://pypi.org/project/py-translator/
Idea: https://www.quora.com/How-do-you-solve-this-NLP-problem-detecting-and-correcting-incorrect-usage-of-English-articles-in-a-given-text
"""

# Esta es la rutina de traducción
def traductor(word):
    from py_translator import Translator
    try:
        text_new = Translator().translate(src='es', dest='en', text=word).text
        return text_new
    
    except ConnectionError as e:
        print ("Received error:", e.data)

# Esta es la rutina de procesamiento del texto
def estandarizador(word):
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    nltk.download('stopwords')
    
    try:
        text_ori = word_tokenize(word) # texto tokenizado
        text_no_stop = [x for x in text_ori if x not in stopwords.words('spanish')] # separo stopwords
        text_new = [x for x in text_no_stop if x.isalpha()] # palabras -> esto voy a traducir

        text_stop = [x for x in text_ori if x in stopwords.words('spanish')] # guardo stopwords -> esto sólo lo voy a mostrar
        alpha = [x for x in text_no_stop if not x.isalpha()] # no-palabras -> esto sólo lo voy a mostrar
        text_rest = text_stop + alpha
        
        return [text_new, text_rest]
    
    except:
        raise

# Esta es la rutina para leer el file de entrada
def read_file():
    try:
        f = open("input.txt", "r")
        text = f.read()        
        return text
        
    except:
        raise
    
    finally:
        f.close()

# Esta es la rutina para escribir el file de salida
def write_file(text_ok, text_bad, text_rest):
    try:
        f = open("output.csv", "w")
        
        f.write("TEXT|CLASS\n")
        write_temp = []
        
        if len(text_ok) > 0:
            for i in range(len(text_ok)):
                write_temp.append(text_ok[i])
                write_temp.append("|OK\n")
        
        if len(text_bad) > 0:
            for i in range(len(text_bad)):
                write_temp.append(text_bad[i])
                write_temp.append("|BAD\n")
        
        if len(text_rest) > 0:
            for i in range(len(text_rest)):
                write_temp.append(text_rest[i])
                write_temp.append("|REST\n")
        
        for i in write_temp:
            f.write(i)
        
    except:
        raise
    
    finally:
        f.close()

# Esta es la rutina de comparación
def main():
    # empiezo leyendo el texto que voy a verificar
    text = read_file()
    
    # estandarizo el texto
    text_filt = estandarizador(text)
    
    text_ok = []
    text_bad = []
    text_rest = text_filt[1]

    # genero las traducciones
    from tqdm import tqdm
    with tqdm(total=len(text_filt[0]), desc="Progress", ncols=50, bar_format='{l_bar}{bar}|') as pbar:
        for i in range(len(text_filt[0])):
            word = text_filt[0][i]
            word_eng = traductor(word)
            
            if not word_eng == word: # este es el concepto de la verificación
                text_ok.append(word)
                
            else:
                text_bad.append(word)            
            
            pbar.update(1)

    # escribo el archivo de salida y termino el programa 
    write_file(text_ok, text_bad, text_rest)
  
if __name__== "__main__":
    main()