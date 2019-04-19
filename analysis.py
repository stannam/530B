import regex as re
from konlpy.tag import Komoran
import os
import pickle
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def directory_manager(foldername):
    path = './result/'+foldername
    filelist = os.listdir(path)
    filelist.remove('finished.txt')
    filelist.remove('log.txt')
    filelist.remove('tocollect.txt')
    sentences = []
    while len(filelist) > 0:
        filename = filelist.pop()
        sentences += corpus_opener(path+'/' + filename)
    return sentences


def corpus_opener(filename):
    if not bool(re.search(".txt", filename)):
        return directory_manager(foldername=filename)

    twit_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            twit_list += line.split('>!!>>!!>>!')
    list_sentences = []
    for sentence in twit_list:
        if not bool(re.search("[가-힣]", sentence)):
            continue
        sentence = re.sub("http[\S]* ?", "", sentence)   #removes hyperlinks
        if sentence != "":
            list_sentences.append(sentence)
    return list_sentences


def kor_tokenizer(list_sentences):
    komoran = Komoran(max_heap_size=1024)
    list_output = []
    for sentence in list_sentences:
        sentence = re.sub("[^가-힣\s]", "", sentence)
        tokenized_sentence = komoran.morphs(sentence)
        list_output.append(tokenized_sentence)
        with open('./result/tokens.pickle', 'wb') as f:
            pickle.dump(list_output, f, pickle.HIGHEST_PROTOCOL)
    return list_output


def kor_honorific(list_sentences, group):
    komoran = Komoran(max_heap_size=1024)
    honorific = [('습니다', 'EC'), ('ㅂ니다', 'EC'),
                 ('습니다', 'EF'), ('ㅂ니다', 'EF'),              # honorific formal declarative
                 ('습니까', 'EC'), ('ㅂ니까', 'EC'),
                 ('습니까', 'EF'), ('ㅂ니까', 'EF'),              # honorific formal interrogative
                 ('ㅂ시오', 'EC'), ('ㅂ시오', 'EF')]              # honorific formal imperative
    informal = [('어요', 'EC'), ('요', 'EC'), ('네요', 'EC'),
                ('어요', 'EF'), ('요', 'EF'), ('네요', 'EF')]     # honorific informal declarative/imperative/interrogative
    topics = r'(자유한국당)|(자한당)|(새누리당)|(이명박)|(박근혜)|(한미동맹)|(국방)|(안보)' \
             r'|(문재인)|(문재앙)|(민주당)|(세월호)|(인권)|(민주주의)'   # conservative and liberal topic keywords, respectively
    result_directory = './result/' + group + '/'
    if not os.path.isdir(result_directory):
        os.mkdir(result_directory)
        with open(result_directory+'list_sentences.txt', 'w', encoding='utf-8') as f:
            for item in list_sentences:
                f.write("%s\n" % item)
        df_output = pd.DataFrame(columns=['no.','group','mention','topic','honorific','formal'])
        df_output.to_csv(result_directory + group+'_dataframe.csv')
    list_sentences = []
    with open(result_directory+'list_sentences.txt', 'r', encoding='utf-8') as f:
        for line in f:
            list_sentences.append(line.strip())
    df_output = pd.read_csv(result_directory+group+'_dataframe.csv')
    todo = len(list_sentences) - len(df_output.index)
    list_sentences = list_sentences[:todo]
    while len(list_sentences) > 0:
        sentence = list_sentences.pop()
        clean_sentence = re.sub("[^가-힣\s]", "", sentence)
        clean_sentence = re.sub("\s{2,}", " ", clean_sentence)
        if (clean_sentence == ' ') or (clean_sentence == ''):
            continue
        pos_sentence = komoran.pos(clean_sentence, flatten=True)

        topic_search = re.findall(topics,sentence)
        current_topic = set([element for tupl in topic_search for element in tupl])
        current_topic = ' '.join(current_topic)
        this_dict={'group': group, 'mention': False, 'topic': current_topic,
                                      'honorific': False, 'formal': False}

        if bool(re.search("^@",sentence)):
            this_dict['mention'] = True

        if any(item in pos_sentence for item in honorific):
            this_dict['honorific'] = True
            this_dict['formal'] = True

        if any(item in pos_sentence for item in informal):
            this_dict['honorific'] = True
            this_dict['formal'] = False

        df_output = df_output.append(this_dict, ignore_index=True)
        df_this_dict = pd.DataFrame(this_dict, index=[len(df_output.index)])
        df_this_dict.to_csv(result_directory+group+'_dataframe.csv', mode='a', header=False)
    return df_output


def kor_nouns(list_sentences, group):
    komoran = Komoran(max_heap_size=1024)
    result_directory = './result/' + group + '/'

    # 150 highly frequent nouns in Korean (r_freq of 4%+) from Sejong Project
    stopwords = []
    with open('./references/stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f:
            stopwords.append(line.strip())

    if not os.path.isdir(result_directory):
        os.mkdir(result_directory)
        with open(result_directory+'list_sentences.txt', 'w', encoding='utf-8') as f:
            for item in list_sentences:
                f.write("%s\n" % item)
        dict_freq = {}
        pickle.dump(dict_freq, open(result_directory+'dict_freq.pickle','wb'))
    list_sentences = []
    with open(result_directory+'list_sentences.txt', 'r', encoding='utf-8') as f:
        for line in f:
            list_sentences.append(line.strip())
    dict_freq = pickle.load(open(result_directory+'dict_freq.pickle','rb'))

    while len(list_sentences) > 0:
        sentence = list_sentences.pop()
        clean_sentence = re.sub("[^가-힣\s]", "", sentence)
        clean_sentence = re.sub("\s{2,}", " ", clean_sentence)
        if (clean_sentence == ' ') or (clean_sentence == ''):
            continue
        nouns_sentence = komoran.nouns(clean_sentence)

        for word in nouns_sentence:
            if word not in stopwords:
                if word in dict_freq:
                    dict_freq[word] += 1
                else:
                    dict_freq[word] = 1
        pickle.dump(dict_freq, open(result_directory+'dict_freq.pickle', 'wb'))


def word_cloud(group, dict, freq_threshold):
    font_path = './references/D2Coding-Ver1.3.1-20180115.ttc'
    dict_wc = {key: val for key, val in dict.items() if (val > freq_threshold)}
    wc = WordCloud(font_path=font_path, background_color='white', width=800, height=600)
    cloud = wc.generate_from_frequencies(dict_wc)
    fig = plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()
    fig.savefig('./result/'+group+'_wordcloud.png')


def k_words(dict1, dict2):
    dict_freq1 = pickle.load(open('./result/' + dict1 + '/dict_freq.pickle', 'rb'))
    dict_freq2 = pickle.load(open('./result/' + dict2 + '/dict_freq.pickle', 'rb'))

    total_count_df1 = sum(dict_freq1.values())
    total_count_df2 = sum(dict_freq2.values())

    for key in dict_freq1:
        dict_freq1[key] = dict_freq1[key] / total_count_df1

    for key in dict_freq2:
        dict_freq2[key] = dict_freq2[key] / total_count_df2

    counter_df1 = Counter(dict_freq1)
    counter_df2 = Counter(dict_freq2)
    counter_df1.subtract(counter_df2)
    return counter_df1
