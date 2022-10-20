# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: nlp
#     language: python
#     name: nlp
# ---

# +
import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm_notebook
from eunjeon import Mecab

from gensim.models import Word2Vec
from gensim.scripts.glove2word2vec import glove2word2vec
import gensim

from sklearn.decomposition import PCA

import preprocess_kr

import warnings
warnings.filterwarnings('ignore')


# -

# # mecab 토큰화 및 불용어 제거

# +
def get_tokenized_data(df):
    """
    mecab 형태소 분석기를 이용하여 토큰화 및 불용어 제거하는 함수¶
    """
    
    # 불용어 생성
    stopwords = preprocess_kr.make_stop_words()

    # mecab 형태소 분석기 객체 생성 
    mecab = Mecab('C:/mecab/mecab-ko-dic')

    # 결과 리스트
    tokenized_data = []

    # 원래 진행하고자했던 반복문 for i in range(100)에서 'in' 뒤에 문장을 tqdm()으로 감싸주면 진행 상황이 bar로 표현된다.
    # tqdm_notebook 은 tqdm 의 Jupiter Notebook version, progress bar가 예쁘다.
    for sentence in tqdm_notebook(df['Review']):
        tokenized_sentence = mecab.morphs(sentence) # mecab 문장 토큰화

        stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거    
        stopwords_removed_sentence = [word for word in stopwords_removed_sentence if len(word) > 1] # 한글자 제거

        tokenized_data.append(stopwords_removed_sentence)
        
    return tokenized_data

def show_review_info(tokenized_data):
    """
    리뷰 길이 분포 확인 함수
    """
    print('리뷰의 최대 길이 :',max(len(review) for review in tokenized_data))
    print('리뷰의 평균 길이 :',sum(map(len, tokenized_data))/len(tokenized_data))
    plt.hist([len(review) for review in tokenized_data], bins=50)
    plt.xlabel('length of samples')
    plt.ylabel('number of samples')
    plt.show()
    
def get_model_wv(tokenized_data):
    """
    토큰화된 데이터를 Word2Vec 알고리즘을 학습시켜 모델을 반환하는 함수
    """
    # Word2Vec으로 토큰화된 tokenized_data를 학습
    from gensim.models import Word2Vec
    # gensim 4.2 vector_size
    # gensim 3.8.3 size
    model = Word2Vec(sentences = tokenized_data, size = 100, window = 5, min_count = 5, workers = 4, sg = 0)
    
    # Word2Vec 임베딩 행렬의 크기를 확인
    print("model.wv.vectors.shape: ",model.wv.vectors.shape)
    
    return model    

def print_most_similar_words(model, words_list): 
    """
    특정단어 리스트를 입력받아 유사도를 출력하는 함수
    """
    for keyword in words_list:        
        print('[', keyword, '] 와 관련있는 단어들 :' , model.wv.most_similar(keyword))
        print()
        
def get_similarity_btw_two_words(model, w1,w2):
    """
    단어간 유사도 확인 함수
    """
    
    # 모델로부터 단어벡터를 구한다.
    word_vectors = model.wv
    
    vocabs = word_vectors.vocab.keys()
    word_vectors_list = [word_vectors[v] for v in vocabs]

    # 단어간 유사도를 반환
    return word_vectors.similarity(w1, w2)
        
def get_similarity_df(keyword):
    """
    특정 키워드를 입력받아 관련있는 단어를 찾고 유사도를 구하는 함수
    """
    similar_word = model.wv.most_similar(keyword)
    similar_word_df = pd.DataFrame(similar_word)
    similar_word_df.columns=["유사단어","유사도"]
    similar_word_df
    return similar_word_df   

def plot_2d_graph(vocabs, xs, ys):
    """
    단어와 2차원 X축의 값, Y축의 값을 입력받아 2차원 그래프를 그리는 함수
    """
    plt.figure(figsize=(10,10))
    plt.scatter(xs, ys, marker = 'o')
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(xs[i], ys[i]))    
        
def reduce_dimension_PCA(word_vectors_list):
    """
    PCA를 이용하여 차원을 축소하는 함수
    """
    pca = PCA(n_components=2)
    xys = pca.fit_transform(word_vectors_list[:10])
    xs = xys[:,0]
    ys = xys[:,1]
    return xs, ys        

def set_evn():
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 1000)

    plt.rc('font', family='NanumGothic')
    plt.style.use('ggplot')
    plt.rc('font', size=15)

    gensim.__version__  # '3.8.3'
    
def show_similar_words(words_list):
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    import chart_studio.plotly as py
    import plotly
    import cufflinks as cf
    import pandas as pd
    import numpy as np

    for word in words_list:

        similar_word_df = get_similarity_df(word)
        fig = similar_word_df.iplot(kind='pie',labels = "유사단어", 
                                        values="유사도", textinfo="percent+label",
                                        title= word + ' 관련 단어 Top10', hole = 0.5, asFigure=True)
        filename = './data/'+ word + '.html'   
        plotly.offline.plot(fig,filename=filename)
        fig.show()


# -

if __name__=="__main__":
    
    # 환경 설정
    set_evn()
    
    # 전처리된 정제된 파일을 읽어온다.
    df = pd.read_table('./data/kr_전지적 독자 시점_episode_total_cleaned_list.txt', header =None)
    df.columns = ['Review']
    df.head()
    
    # 1. 토큰화
    tokenized_data = get_tokenized_data(df)
    
    # 2. 댓글 정보 확인
    show_review_info(tokenized_data)
    
    # 3. tokenized_data로 모델을 학습
    model = get_model_wv(tokenized_data)
    
    # 모델을 저장한다.
    # model.save('word2vec.model')

    # 저장한 모델을 읽어온다.
    # model = Word2Vec.load('word2vec.model') 
    
    # 4. 유사단어 검색
    words_list = ['독자', '소설', '작가', '그림', '연출', '주인공', '캐릭터', '원작', '작화', '스토리']
    print_most_similar_words(model, words_list)    
    
    #  5. 단어간 유사도 확인
#     get_similarity_btw_two_words(model, '독자','수영')

    # 6. 유사단어와 유사도를 데이터프레임으로 확인
    similar_word_df = get_similarity_df('스토리')
    similar_word_df
    
    # 7. 유사단어 시각화
    show_similar_words(words_list)
    
    # 8. PCA 차원 축소 및 유사도 시각화
#     xs, ys = reduce_dimension_PCA(word_vectors_list)
#     plot_2d_graph(vocabs, xs, ys)


