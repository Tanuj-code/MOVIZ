#import streamlit as st
#import streamlit.components.v1 as stc
import pandas as pd
import numpy as np



movies=pd.read_csv('imdb_top_1000.csv')
star={}
genre={}
rating={}
for i in movies.columns:
    if(i=='IMDB_Rating' or i=='Released_Year'  or i=='Meta_score' or i=='No_of_Votes' or i=='Gross'):
        continue
    movies[i]=movies[i].str.lower()
    
for i in movies.values:
    star[i[10]]=1
    star[i[11]]=1
    star[i[12]]=1
    star[i[13]]=1
    
    for j in i[5].split(','):
        j.strip()
        genre[j]=1
    
    rating[i[6]]=1
star=list(star.keys())
genre=list(genre.keys())
rating=list(rating.keys())

molist=list(movies['Series_Title'])
chart=pd.DataFrame(index=movies['Series_Title'], columns=genre)
ind=chart.index
chart=dict(chart)
for i in range(0, 1000):
    stp=movies.values[i][5].split(',')
    for j in stp:
        chart[j][ind[i]]=1
chart=pd.DataFrame(chart)
chart.fillna(0, inplace=True)

from sklearn.metrics.pairwise import cosine_similarity
score=cosine_similarity(chart)
chart1=pd.DataFrame(index=movies['Series_Title'], columns=star)
chart1.fillna(0, inplace=True)
chart1=dict(chart1)
for i in range(0, 1000):
    stp=[movies.values[i][10], movies.values[i][11], movies.values[i][12], movies.values[i][13]]
    for j in stp:
        chart1[j][ind[i]]=1
chart1=pd.DataFrame(chart1)
score1=cosine_similarity(chart1)
a=movies.iloc[:, [1, 5]]
b=movies.iloc[:, [1, 6]]
b=b.sort_values('IMDB_Rating', ascending=False)
movcol=chart1.columns
movcol=list(movcol)

def recc(name):
    name=name.lower()
    lst=[]
    if name not in chart.index:
        return lst
    index=np.where(chart.index==name)[0][0]
    similar_items = sorted(list(enumerate(score[index])),key=lambda x:x[1],reverse=True)[1:51]
    for j in similar_items:
        if(j[1]==0):
            break
        lst.append(chart.index[j[0]])
    return lst

def rec1(name):
    name=name.lower()
    lst=[]
    if name not in chart1.index:
        return lst
    index=np.where(chart1.index==name)[0][0]
    similar_items = sorted(list(enumerate(score1[index])),key=lambda x:x[1],reverse=True)
    for j in similar_items:
        if(j[1]==0):
            break
        lst.append(chart1.index[j[0]])
    return lst

def mofindbyactor(xx):
    xx=xx.lower()    
    
    lst=[]
    fin=[]
    for i in xx.split(','):
        lst.append(i.strip())
    
    for k in lst:
        if(k not in chart1.columns):
            return fin
    newl=chart1[lst]
    
    for j in range(0, 1000):
        if(sum(newl.values[j])==len(lst)):            
            fin.append(newl.index[j])   
    return fin



def func() :
    if len(book)==0:
            
                st.error("Please enter a value")
            
    else:
            
           
                
            if mode=="By cast":
                stt.empty()
                
                lst= mofindbyactor(book)
                if len(lst)==0:
                    st.write("No Suggestions")
                else:
                    for i in lst:
                            
                        st.write(i.capitalize())
                
            elif mode=="By Movie":
                stt.empty()
                
                lst=rec1(book)
                if len(lst)==0:
                    st.write("No Suggestions")
                else:
                    for i in lst:
                            
                        st.write(i.capitalize())

            else:
                lst=recc(book)
                if len(lst)==0:
                    st.write("No Suggestions")
                else:
                                           
                        for i in lst:
                            col1, col2= st.columns([1, 1])
                            with col1:
                                st.write(i.capitalize())
                            with col2:
                                st.markdown(f'''
                                <img src={movies.values[molist.index(i)][0]} style="border: 1px solid black"> 
                                ''', unsafe_allow_html=True)
                
                
if mode and len(book)>0:
    func()

