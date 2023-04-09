# ---------------------------------------------Project: Twitter Scraper------------------------------------------#
# Deployment project
# Deployment is the process by which the document types, model, and overall project definition are made available for use.

# Import pandas
import streamlit as st
import datetime
import time
from datetime import date, timedelta
import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import pymongo

###-----------------------------------------     G   U   I   -----------------------------------------###    

#---------------    Front  bar   ---------------#

#1 Heading
st.title('**:blue[Twitter Scraper]**')
st.subheader('Enter your requirements below')

#2 selection :-keyword or Hashtag...........
selection = st.selectbox('Select your option.',('Keyword.', 'Hashtag.',))
if selection == 'Keyword.':
    word = st.text_input('''You selected Keyword, (ex:-**Elon musk**), Don't use '# 'before the Keyword.''', 'India')
else:
    word = st.text_input('''You selected Hashtag, (ex:-**#elonmusk**), use '# '  before the Keyword.''', '#india')

#3 select from date and to date........
col1, col2, = st.columns(2)
with col1:
    startdate = st.date_input('Select the Start date.', date.today() - timedelta(days = 100))
with col2:
    enddate = st.date_input('Select the End date.',date.today())

#4 Select the count in number min=1 to max=1000....
count = st.number_input('Number of Twitts,  (note:-Minimum **1** to Maximum up to **1000**).',min_value=1, max_value=1000,step=10,)

#5   #Scrap button col1 below :    #show button col2 below :   # download csv col3 below :  #download json col4  below :
col1, col4,col5,col6, = st.columns(4)

# -------------------------------------------************--------------------------------------------------------#


#---------------    Front  bar frame work  (scrap program.) ---------------#

# scrap_data storage
tweets=[]

#Scrap button with program.
with col1:
    st.write('''Start Scrap to click below **:blue['Scrap']**.''')
    scrape_button = st.button('**Scrap**')

if "scrape_state" not in st.session_state:
    st.session_state.scrape_state = False

if scrape_button or st.session_state.scrape_state:
    st.session_state.scrape_state = True
    # st.write('scrape_button running')

    if word:
        try:
            if selection == 'Keyword.':
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} lang:en since:{startdate} until:{enddate}').get_items()):
                    if i>count-1:
                        break
                    data=[tweet.date,tweet.user.id,tweet.url,tweet.rawContent,tweet.user.username, tweet.replyCount,
                        tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount,]
                    tweets.append(data)
                # st.write('keyword running')
            else:
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} lang:en since:{startdate} until:{enddate}').get_items()):
                    if i>count-1:
                        break
                    data=[tweet.date,tweet.user.id,tweet.url,tweet.rawContent,tweet.user.username, tweet.replyCount,
                        tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount,]
                    tweets.append(data)
                # st.write('Hashtag running')
        except Exception as e:
            st.error('Server error (or) Check your internet connection (or) Please Try again after a few minutes', icon='🚨')
    else:
        st.warning(selection,' Must enter atleast one word', icon = "⚠️")
# progress bar
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    st.success('Done . . .')

# Convert the scraped data into Data frame, csv, json, dictionary
df = pd.DataFrame(tweets, columns=(['Date', 'User ID', 'URL', 'Tweet content', 'User Name','Reply count',
                                    'Retweet count','Language', 'Source', 'Like count',]))
csv = df.to_csv()
json = df.to_json(orient = 'records')
data_dict = df.to_dict(orient='records')
# st.write('Last conversion of data')

# show button
with col4:
    st.write('''You can view in to click below **:blue['Show']**.''')
    show_button = st.button('**Show**')

if "show_state" not in st.session_state:
    st.session_state.show_state = False

if show_button or st.session_state.show_state:
    st.session_state.show_state = True
    st.dataframe(df)
    # st.write('Show running')

# Download CSV file button
with col5:
    st.write('''Download CSV file click below **:blue['CSV']**.''')
    st.download_button (label = '**CSV**',data = csv, file_name = f'{word}.csv' ,mime = 'csv/text',)
    # st.write('CSV running')

# Download JSON file button
with col6:
    st.write('''Download JSON file click below **:blue['JSON']**.''')
    st.download_button (label = '**JSON**',data = json,file_name = f'{word}.json' ,mime = 'json/docx/docxtpl/application',)
    # st.write('JSON running')



#---------------  Side bar ----------------#

#6 Upload datas into MongoDB data base with data base name ,collection name 
with st.sidebar:
    st.title('Storage option')
    st.write('You can store your data in the **:green[MongoDB]** database.')
    mongodburl = st.text_input('Enter **:green[MongoDB URL]** link below.', 'mongodb://localhost:27017')
    st.write('Default Database name: **Twitter**.')
    collectionname = st.text_input('**Collection name.**',f'{word}')
    st.write('''Click the **:blue['Upload']** button to start uploading.''')
    upload_data = st.button('**Upload**')


#---------------    Side bar Frame work  (Upload data to Mongodb program.) ---------------#

if "upload_state" not in st.session_state:
    st.session_state.upload_state = False

if upload_data or st.session_state.show_state:
    st.session_state.show_state = True

    # connect mongo client
    client = pymongo.MongoClient(mongodburl)
    db = client['Twitter']
    col = db[collectionname]
    # Insert the datas to Mongodb 
    col.insert_many(data_dict)
    # close
    client.close()

    
# Stop all program
st.stop()