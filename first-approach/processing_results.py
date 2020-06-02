import os
import sys
import csv
import matplotlib.pyplot as plt
import string
import enchant
import numpy as np

'''
CREATE CSV FILES



filepath = "C:\\Users\\gabri\\Documents\\UFF\\TCC\\HR_CNNRNN\\SimpleHTR-master\\src\\"
filename = "inference_brdb_model1_checkdict.csv"
filename_beam = "inference_brdb_model1_checkdict_beamsearch.csv"

file = filepath+filename_beam
keys = ['filename', 'recognition', 'probability', 'hasMatch', 'match']


def readFile(file):
    data = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        for row in csv_reader:
            line = []
            for col in row:
                line.append(col)
            data.append(line)
    return data

def wordsFreq(data, key=1):
    words = []
    unique = []
    resp = []

    #get all words
    print("including words")
    for row in data:
        words.append(row[key])

    #calculates frequency
    print("checking uniques")
    u = 0
    for w in words:
        if(not w in unique):
            unique.append(w)
            u += 1
            print(u)
            resp.append([w, words.count(w)])
        else:
            print("tem")

    return resp

data = readFile(file)
freq = wordsFreq(data, 1)
with open('words_frequency_beam-search.txt', 'w') as freq_file:
    for f in freq:
        output = str(f[0])+";"+str(f[1])+"\n"
        freq_file.write(output)
print(len(freq))'''

#__GET WORDS FROM ORIGINAL TEXT 
def listKnownWords(filepath):
    file = open(filepath, 'r')
    text = file.read().split(" ")
    known_words = []
    #print("Palavras no texto: ", len(text))
    for word in text:
        if not word in known_words:
            #print(word)
            known_words.append(word)
    #print("Palavras no dicionário: ", len(known_words))
    return known_words

#__GET THE MOST FREQUENT WORDS FROM FILELINES LIKE "word;frequency"
def getMostFrequents(filepath, range):      #range=None to get all the words
    if os.path.isfile(filepath):
        data = []
        count = 0
        with open(filepath, 'r') as file:
            line = 1
            for row in file:
                row = row.split(";")
                if(len(row) == 2):
                    data.append([row[0], float(row[1])])
                    count += float(row[1])
                else:
                    print("Linha ", line, ": ", row)
                line += 1
        data.sort(key=lambda x: x[1], reverse=True)     #sort by the most frequent word to less
        if range == None: range = len(data)
        print("Num reconhecidas: ", count)
        return data[:range], count
    else:
        return None

#__HIDE WORDS FROM ORIGINAL TEXT ON THE LIST OF RECOGNIZED WORDS
def getKnownWords(data, dict, filename, exclude):       #filename=None to not saving unknown words, exclude=1 to get unknown words
    unknown_words = []
    count = 0
    if filename != None:
        file = open(filename, 'w')
    #file_resp = open("words_infer-unknown-twochars.txt", 'w')
    for word, freq in data:
        if not word in dict:
            if exclude == 1:
           #if freq > 1 and len(word) > 2:
                unknown_words.append([word, freq])
                output = word + ";" + str(freq) + "\n"
                if filename != None:
                    file.write(output)
           #else:
                #output = word+"\n"
                #file_resp.write(output)
        else:
            count += freq
            if exclude == 0:
                unknown_words.append([word, freq])
                output = word+";"+str(freq)+"\n"
                if filename != None:
                    file.write(output)
    print("Num corretas: ", count)
    return unknown_words, count

#__HIDE PUNCTUATION FROM LIST OF RECOGNIZED WORDS
def hidePunctuation(data):
    just_words = []
    count = 0
    for word, freq in data:
        if not word in string.punctuation:
            just_words.append([word, freq])
        else:
            count += freq
    print("Num punct: ", count)
    return just_words, count

def hideNumbers(data):
    no_numbers = []
    just_numbers = []
    count = 0
    for word, freq in data:
        if not word.isnumeric():
            no_numbers.append([word, freq])
        else:
            count += freq
            just_numbers.append([word, freq])
    with open("words_frequency_infer-just_numbers.txt", 'w') as file_num:
        for num, freq in just_numbers:
            output = str(num)+";"+str(freq)+"\n"
            file_num.write(output)
    print("Num numbers: ", count)
    return no_numbers, count

#__HIDE PORTUGUESE STOP WORDS FROM LIST OF RECOGNIZED WORDS
def hideStopWords(data, stop_file):
    orig_words = []
    count = 0
    if os.path.isfile(stop_file):
        stop_words = []
        
        with open(stop_file, 'r') as file:
            for row in file:
                row = row.split("\n")[0].split(" ")[0]
                stop_words.append(row)
        for word, freq in data:
            if not word in stop_words:
                orig_words.append([word, freq])
            else:
                count += freq
    print("Num stop: ", count)
    return orig_words, count

def getEnglishWords(data, exclude, filename): #exclude = 1 to hide english words, filename = None to not write english words
    d = enchant.Dict("en_US")
    no_eng = []
    count = 0
    if(filename != None):
        eng_words = open(filename, 'w')
    for word, freq in data:
        if not d.check(word):
            if(exclude == 1):
                no_eng.append([word, freq])
        else:
            count += freq
            if exclude == 0:
                no_eng.append([word, freq])
            if(filename != None):
                output = word+";"+str(freq)+"\n"
                eng_words.write(output)
    print("Num eng: ", count)
    return no_eng, count

#__PLOT MOST FREQUENT WORDS FROM LIST LIKE (list[0]: word, list[1]: frequency) AND SAVE
def plotFrequentWords(data, title, filename, color, yinit):       #filename=None to not saving plot figure
    words = []
    frequency = []
    for d in data:
        #--SET TO WORDS
        #words.append(d[0])

        #--SET TO WRITERS
        words.append(str(d[0]))
        frequency.append(d[1])

    fig, ax = plt.subplots()
    fig.set_size_inches(12.5, 6.5)
    plt.bar(words, frequency, color=color)
    ax.tick_params(axis='x', labelsize=8, rotation=90)
    '''
    #--SET TO WORDS
    plt.yticks(np.arange(0, max(frequency), 200))
    
    ax.set_xlabel('Palavras')
    ax.set_ylabel('Frequencias')
    #ax.set_yticks(y)
    #ax.set_yticklabels(x)
    #ax.invert_yaxis()
    '''
    #--SET TO WRITERS--
    plt.yticks(np.arange(yinit, max(frequency), 20))
    ax.set_ylim(bottom=yinit)
    #plt.xticks(np.arange(min(words), max(words), 1))
    #plt.subplots_adjust(wspace=1)
    ax.set_xlabel('Escritores (id)')
    ax.set_ylabel('Quantidade de Palavras')
    ax.set_title(title)
    if filename != None:
        plt.savefig(filename, dpi=1200)
    plt.show()

#__CREATE PIE CHART WITH GROUPS OF WORDS RECOGNIZED (stop, punct, etc...)
def plotRecognizedGroups(data, total, filename):
    labels = []
    sizes = []
    explodes = []
    for group, count in data:
        labels.append(group)
        sizes.append(count/100 * total)
        if group == "Texto original":
            explodes.append(0.1)
        else:
            explodes.append(0)

    fig1, ax1 = plt.subplots()
    patches, texts, autotexts = ax1.pie(sizes, explode=explodes, labels=labels, autopct='%1.2f%%', shadow=False, startangle=110)#, textprops={'fontsize': 5})
    ax1.axis('equal')
    for t in autotexts:
        t.set_fontsize(8)
    plt.title("Palavras geradas pela inferência")
    if filename != None:
        plt.savefig(filename, dpi=1200)
    plt.show()

#__CREATE DICT WITH WRITERS' INFOS EXTRACTED FROM INFERENCE RESULTS
def makeDictWithWriters(filename):
    if os.path.isfile(filename):
        writes_info = {}
        
        with open(filename, 'r') as file:
            for row in file:
                infos = row.split(";")
                writes_info[infos[0]] = {
                    "words_recognized": infos[1],
                    "unique_rocgnized:": infos[2],
                    "total_recognized": infos[3],
                    "total_cropped": infos[4].split("\n")[0]}
        return writes_info
    else:
        return "File not found."


def getNumWordsByWriters(dict, key, filename):
    words_recog = []
    id = 1
    for writer in dict:
        words_recog.append([id, int(dict[writer][key]), writer])
        id += 1
    words_recog.sort(key=lambda x: x[1], reverse=False)
    words_recog = words_recog[:50]
    file_w = "words_matchingdict-bywriter_50less-"+key+".txt"
    with open(file_w, 'w') as file_writers:
        for id, freq, writer in words_recog:
            print(writer, " ", freq)
            output = writer+";"+str(freq)+"\n"
            file_writers.write(output)
    words_recog.sort(key=lambda x: x[0], reverse=False)
    return words_recog

        
current_dir = "C:\\Users\\gabri\\Documents\\UFF\\TCC\\HandTran\\infer_task_SIMPLEHTR\\BFL_case\\"
'''
#__PROCESSING WORDS FILE
title = "Palavras encontradas"
num_words = 100
#TODO: join didn't work
#os.path.join(current_dir, "\\results\\best_path\\words_frequency_infer-forall.txt")
text_file = current_dir+"original_text_BFL.txt"
freq_file = current_dir+"results\\best_path\\words_frequency_infer-forall.txt"
stop_file = current_dir+"stopwords.txt"
known_file = current_dir+"results\\best_path\\words_frequency_infer-known_words.txt"

data, total = getMostFrequents(freq_file, None) #range=None to get all words

if (data != None):
    pie_groups = []
    title = "Total"
    print(title, " ", total)
    print()
    #pie_groups.append([title, total])

    known_words = listKnownWords(text_file)
    unknown, known_num = getKnownWords(data, known_words, None, 1)
    title = "Texto original"
    print(title, " ", known_num)
    print()
    pie_groups.append([title, known_num])
    
    just_words, punc_num = hidePunctuation(unknown)
    title = "Pontuação"
    print(title, " ", punc_num)
    print()
    pie_groups.append([title, punc_num])

    no_nums, num_num = hideNumbers(just_words)
    title = "Números"
    print(title, " ", num_num)
    print()
    pie_groups.append([title, num_num])

    no_stop, stop_num = hideStopWords(no_nums, stop_file)
    title = "Stop words"
    print(title, " ", stop_num)
    print()
    pie_groups.append([title, stop_num])

    no_eng, eng_num = getEnglishWords(no_stop, 1, None)
    title = "Palavras em inglês"
    print(title, " ", eng_num)
    print()
    pie_groups.append([title, eng_num])

    unrec_num = total - known_num - punc_num - stop_num - eng_num
    title = "Desconhecidas"
    print(title, " ", unrec_num)
    pie_groups.append([title, unrec_num])

    #plotFrequentWords(no_eng[:num_words], "Palavras reconhecidas do texto original", None, (1, 0, 0, 1))#"words_frequency_infer-known_words.png", (0.2, 0.6, 0.4, 0.7))
    plotRecognizedGroups(pie_groups, total, "words_frequency_infer-group_types.png")
    #plotFrequentWords(data, title, None) #just plot dont save
        
else:
    print("File not found.")

'''
#__PROCESSING WRITERS FILES
writers_file = current_dir+"results\\best_path\\words_matchingdict-bywriter.txt"
writers_dict = makeDictWithWriters(writers_file)
words_recog_bywriter = getNumWordsByWriters(writers_dict, "total_recognized", None)
#print(words_recog_bywriter)
#plotFrequentWords(words_recog_bywriter, "50 escritores com mais palavras reconhecidas", "words_frequency_infer-bywriter_10most.png", (0.8, 0.7, 0, 0.8), 50)
words_cropped_bywriter = getNumWordsByWriters(writers_dict, "total_cropped", None)
#plotFrequentWords(words_cropped_bywriter, "50 escritores com mais palavras recortadas", "words_frequency_crop-bywriter_10most.png", (0, 0.7, 0.8, 0.8), 400)
