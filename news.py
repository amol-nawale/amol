import pandas as pd
import streamlit as st


import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
from wordcloud import WordCloud, STOPWORDS

st.title('Stock News Sentiment Analysis')
side_bar=st.sidebar
side_bar.header('Input Space')


with st.container():

    now = dt.date.today()
    now = now.strftime('%m-%d-%Y')



    compnay=side_bar.text_input('Enter The Company Name')
    day=side_bar.number_input('Enter Number Of Days History From Current Date')
    button=side_bar.button('submit')

    if button:
    
        yesterday = dt.date.today() - dt.timedelta(days = day)
        yesterday = yesterday.strftime('%m-%d-%Y')

        nltk.download('punkt')
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 10

   

        

    
    # save the company name in a variable
        company_name = compnay
#As long as the company name is valid, not empty...
        if company_name != '':
            print(f'Searching for and analyzing {company_name}, Please be patient, it might take a while...')

        googlenews = GoogleNews(start=yesterday, end=now)
        googlenews.search(company_name)
        result = googlenews.result()
        df = pd.DataFrame(result)


        for i in range(0,int(day//3):
            googlenews.getpage(i)
            result = googlenews.result()
            df = df.append(result)
            df = pd.DataFrame(df)

        df = df.drop_duplicates(subset=['title'], keep='last')
        df.reset_index(drop=True, inplace=True)
        print(df)


try:
        list =[] #creating an empty list 
        for i in df.index:
            dict = {} #creating an empty dictionary to append an article in every single iteration
            article = Article(df['link'][i],config=config) #providing the link
            try:
              article.download() #downloading the article 
              article.parse() #parsing the article
              article.nlp() #performing natural language processing (nlp)
            except:
               pass 
            #storing results in our empty dictionary
            dict['Date']=df['date'][i] 
            dict['Media']=df['media'][i]
            dict['Title']=article.title
            dict['Article']=article.text
            dict['Summary']=article.summary
            dict['Key_words']=article.keywords
            list.append(dict)
        check_empty = not any(list)
    # print(check_empty)
        if check_empty == False:
          news_df=pd.DataFrame(list) #creating dataframe
          print(news_df)

except Exception as e:
    #exception handling
        print("exception occurred:" + str(e))
        print('Looks like, there is some error in retrieving the data, Please try again or try with a different ticker.' )

        # print(news_df)

    # 
            # st.dataframe(df)


       


        # for i in range(0,5):
        #     googlenews.getpage(i)
        #     result = googlenews.result()
        #     df = df.append(result)
        #     df = pd.DataFrame(df)

        # df = df.drop_duplicates(subset=['title'], keep='last')
        # df.reset_index(drop=True, inplace=True)
        # print(df)

   
   

        

    
        

with st.container():
    try:
    
        news_df['cleaned_summary']=0
        for i in range(len(news_df)):
            news_df['cleaned_summary'][i]=" ".join(news_df['Summary'][i].split())
        st.write('Extracted News Data')
        st.dataframe(news_df.head())
        st.write(f"Number of news extracted: {len(news_df)}")


        from textblob import TextBlob
        b=[]
        a=news_df['cleaned_summary']
        for elm in a:
            b.append(TextBlob(elm).sentiment.polarity)

        a=pd.DataFrame(a)
        a['polarity']=b

        d=[]
        for elm in a['polarity']:
            if elm>= 0.05:
                d.append(1)
            elif elm<= -0.05:
                d.append(-1)
            else:
                d.append(0)
        a['sentiment_value']=d


        x=[]
        for elm in a['sentiment_value']:
            if elm==0:
                x.append('neutral') 
            elif elm==-1:
                x.append('negative')
            else:
                x.append('positive')

        a['sentiment']=x


        positive=a['sentiment'].loc[(a['sentiment']=='positive')]
        negative=a['sentiment'].loc[(a['sentiment']=='negative')]
        neutral=a['sentiment'].loc[(a['sentiment']=='neutral')] 

        a=len(positive)
        print(f"total positive sentiments: {a} ")
        b=len(negative)
        print(f"total negative sentiments: {b} ")
        c=len(neutral)
        print(f"total neutral sentiments: {c} ")




        col1,col2=st.columns(2)

        with col1:

            labels = ['Positive','Negative','Neutral']
            sizes = [a,b,c]
            colors = ['green', 'red','grey']
            plt.pie(sizes,colors=colors,startangle=90,autopct='%1.0f%%')
            plt.style.use('default')
            plt.legend(labels,loc='upper right')
            plt.title("Sentiment Analysis Result" )
            plt.axis('equal')
            plt.show()

    
            fig, ax = plt.subplots()
            ax.pie(sizes,colors=colors,startangle=90,autopct='%1.0f%%',labels=['positive','negative','neutral'])
        
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
        # show counts
            dict={'positive_count':[a],'negative_count':[b],'neutral_count':[c],'Total_count':[a+b+c]}
            df2=pd.DataFrame(dict)

            st._legacy_bar_chart(df2[['positive_count','negative_count','neutral_count']])
    
    except Exception as e:
        print(e)


#show counts

try:
   dict={'positive_count':[a],'negative_count':[b],'neutral_count':[c],'Total_count':[a+b+c]}
   st.dataframe(dict)

except Exception as e:
    print(e)
        


    
    
 







    
    





    



    

    
    







    















   

