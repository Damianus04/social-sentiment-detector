# standard flask libraries
from flask import Flask, render_template, request
import pandas as pd
from joblib import load
import nltk

# MySQL Libraries
import requests
from mysql.connector import connect, cursor
from flask import jsonify

# my functions
from static.src.helpers import get_tweets, predict_sentiment
from static.src.helpers import text_preprocessing

# data
real_estate = pd.read_csv('./data/melb_data.csv')
model = load('model/rand_search_logreg_hyper_tfidf_sklearn24.joblib')

app = Flask(__name__)


# data - connection to mysql database
myDB = {
    'user': 'damianus',
    'password': '12345',
    'host': 'localhost',
    'database': 'twitter'
}
connection = connect(**myDB)
cursor = connection.cursor()


########## HTML ROUTE FUNCTION ##########
# Route to index.html
@app.route('/', methods=["GET", "POST"])
def index():
    # Dummy Melbourne Data
    table = real_estate.head(100)

    # MySQL Database
    url = 'http://localhost:5005/tweet'
    result = requests.get(url)
    result = result.json()
    result_in_df = pd.DataFrame(columns=["id", "tweet_id", "user_name", "screen_name", "profile_url",
                                         "created_at", "created_at_date", "created_at_day_name",
                                         "created_at_month", "created_at_year", "created_at_time1",
                                         "created_at_time2", "tweet_text", "location",
                                         "followers", "following", "listed_count", "profile_image",
                                         "profile_banner_image", "news_url_1", "news_url_2",
                                         "tweet_data_preprocessed", "sentiment", "sentiment_description"],
                                data=result)

    # Total Conversations & Average Mentions
    try:
        total_mentions = len(result_in_df)
        average_mentions = round(total_mentions/7)

        # conversation trends
        time1 = result_in_df[['created_at_time1', 'tweet_text']].groupby(
            ['created_at_time1'], as_index=False).count()
        time2 = result_in_df[['created_at_time2', 'tweet_text']].groupby(
            ['created_at_time2'], as_index=False).count()

        tweet_legend = "conversations"
        # choose whether to use time1 (day & hour) or time2 (hour)
        if len(time1.created_at_time1) > 1:
            tweet_time_label = list(time1.created_at_time1)
            tweet_count_values = list(time1.tweet_text)
        else:
            tweet_time_label = list(time2.created_at_time2)
            tweet_count_values = list(time2.tweet_text)

        # sentiment
        sentiment_chart = result_in_df[['sentiment_description', 'tweet_text']].groupby(
            ['sentiment_description'], as_index=False).count()
        tweet_sentiment_label = list(sentiment_chart.sentiment_description)
        tweet_sentiment_values = list(sentiment_chart.tweet_text)

        # potential reach data
        reach_data = result_in_df[['screen_name', 'followers']].head(
            10).sort_values(by='followers', ascending=False)
        reach_data_screen_name = list(reach_data.screen_name)
        reach_data_followers = list(reach_data.followers)

        # word distribution
        word_freq_dist_dict = []
        for i in result_in_df.tweet_data_preprocessed:
            word_freq_dist_dict.extend(i.split(' '))

        word_freq_dist = nltk.FreqDist(word_freq_dist_dict)
        top10words = word_freq_dist
        top10words = word_freq_dist.most_common(20)
        words = []
        words_frequency = []
        for i in top10words:
            words.append(i[0])
            words_frequency.append(i[1])

        # location distribution
        top10locations = pd.DataFrame(
            result_in_df['location'].value_counts())[:20]
        locations = top10locations.index
        locations_frequency = [i for i in top10locations.location]
    except:
        total_mentions
        average_mentions
        tweet_legend = "conversations"
        tweet_time_label = ['None']
        tweet_count_values = [0]
        tweet_sentiment_label = ['None']
        tweet_sentiment_values = [0]
        reach_data_screen_name = ['None']
        reach_data_followers = [0]
        words = ['None']
        words_frequency = [0]
        locations = ['None']
        locations_frequency = [0]

    return render_template('index.html', data=table, result=result, result_in_df=result_in_df,
                           total_mentions=total_mentions, average_mentions=average_mentions,
                           locations=locations, locations_frequency=locations_frequency,
                           tweet_time_label=tweet_time_label, tweet_count_values=tweet_count_values, tweet_legend=tweet_legend,
                           reach_data_screen_name=reach_data_screen_name, reach_data_followers=reach_data_followers,
                           words=words, words_frequency=words_frequency,
                           tweet_sentiment_label=tweet_sentiment_label, tweet_sentiment_values=tweet_sentiment_values)


@app.route('/', methods=["GET", "POST"])
def keyword_search():
    # Dummy Melbourne Data
    df = real_estate

    # MySQL Database
    url = 'http://localhost:5005/tweet'
    result = requests.get(url)
    result = result.json()
    result_in_df = pd.DataFrame(columns=["id", "tweet_id", "user_name", "screen_name", "profile_url",
                                         "created_at", "created_at_date", "created_at_day_name",
                                         "created_at_month", "created_at_year", "created_at_time1",
                                         "created_at_time2", "tweet_text", "location",
                                         "followers", "following", "listed_count", "profile_image",
                                         "profile_banner_image", "news_url_1", "news_url_2",
                                         "tweet_data_preprocessed", "sentiment", "sentiment_description"],
                                data=result)

    # Get Tweet
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        # Get Tweet
        text_query = request.form['text']
        tweet_data = get_tweets(text_query)

        # Total Conversations & Average Mentions
        total_mentions = len(result_in_df)
        if total_mentions == 0 or text_query == " ":
            average_mentions = 0
        else:
            average_mentions = round(total_mentions/7)

        try:
            # add detailed datetime features
            # tweet_data['date'] = tweet_data.created_at.apply(
            #     lambda x: x.date())
            # tweet_data['day'] = tweet_data.created_at.apply(
            #     lambda x: x.day_name())
            # tweet_data['month'] = tweet_data.created_at.apply(
            #     lambda x: x.month_name())
            # tweet_data['year'] = tweet_data.created_at.apply(
            #     lambda x: x.year)
            # tweet_data['time1'] = tweet_data.created_at.apply(
            #     lambda x: x.to_period('H').strftime('%d-%b-%y'))
            # tweet_data['time2'] = tweet_data.created_at.apply(
            #     lambda x: x.to_period('H').strftime('%d-%b-%y %H:%M'))

            # conversation trends
            time1 = result_in_df[['created_at_time1', 'tweet_text']].groupby(
                ['created_at_time1'], as_index=False).count()
            time2 = result_in_df[['created_at_time2', 'tweet_text']].groupby(
                ['created_at_time2'], as_index=False).count()

            tweet_legend = "conversations"
            # choose whether to use time1 (day & hour) or time2 (hour)
            if len(time1.created_at_time1) > 1:
                tweet_time_label = list(time1.created_at_time1)
                tweet_count_values = list(time1.tweet_text)
            else:
                tweet_time_label = list(time2.created_at_time2)
                tweet_count_values = list(time2.tweet_text)

            # location distribution
            top10locations = pd.DataFrame(
                result_in_df['location'].value_counts())[:20]
            locations = top10locations.index
            locations_frequency = [i for i in top10locations.location]

            # Preprocessing 'tweet_text'
            # tweet_data['tweet_data_preprocessed'] = tweet_data['tweet_text'].apply(
            #     lambda x: text_preprocessing(x)
            # )

            # Predict Twitter Text
            # colname = 'tweet_text_preprocessed'
            # prediction_list = predict_sentiment(
            #     model, tweet_data, colname)
            # tweet_data['sentiment'] = prediction_list

            # sentiment_chart = tweet_data[['sentiment', 'tweet_text']].groupby(
            #     ['sentiment'], as_index=False).count()
            # tweet_sentiment_label = list(sentiment_chart.sentiment)
            # tweet_sentiment_values = list(sentiment_chart.tweet_text)

            # potential reach data
            reach_data = result_in_df[['screen_name', 'followers']].head(
                10).sort_values(by='followers', ascending=False)
            reach_data_screen_name = list(reach_data.screen_name)
            reach_data_followers = list(reach_data.followers)

            # word distribution
            word_freq_dist_dict = []
            for i in result_in_df.tweet_data_preprocessed:
                word_freq_dist_dict.extend(i.split(' '))

            word_freq_dist = nltk.FreqDist(word_freq_dist_dict)
            top10words = word_freq_dist
            top10words = word_freq_dist.most_common(20)
            words = []
            words_frequency = []
            for i in top10words:
                words.append(i[0])
                words_frequency.append(i[1])

            # location distribution
            top10locations = pd.DataFrame(
                result_in_df['location'].value_counts())[:20]
            locations = top10locations.index
            locations_frequency = [i for i in top10locations.location]

        except:
            tweet_legend = "conversations"
            tweet_time_label = ['None']
            tweet_count_values = [0]
            tweet_sentiment_label = ['None']
            tweet_sentiment_values = [0]
            reach_data_screen_name = ['None']
            reach_data_followers = [0]
            words = ['None']
            words_frequency = [0]
            locations = ['None']
            locations_frequency = [0]

        # Melbourne Data
        df_Regionname = df[['Price', 'Regionname']].groupby(
            ['Regionname'], as_index=False).mean()
        legend = 'Average Price'
        labels = list(df_Regionname.Regionname)
        values = list(df_Regionname.Price)

        return render_template('index.html',
                               data=df, tweet_data=tweet_data, text_query=text_query,
                               total_mentions=total_mentions, average_mentions=average_mentions,
                               legend=legend, labels=labels, values=values,
                               tweet_time_label=tweet_time_label, tweet_count_values=tweet_count_values, tweet_legend=tweet_legend,
                               tweet_sentiment_label=tweet_sentiment_label, tweet_sentiment_values=tweet_sentiment_values,
                               reach_data_screen_name=reach_data_screen_name, reach_data_followers=reach_data_followers,
                               words=words, words_frequency=words_frequency, locations=locations, locations_frequency=locations_frequency,
                               # result from mysql from API http://localhost:5005/tweet
                               result=result, result_in_df=result_in_df
                               )


# @app.route('/bad-sentiment', methods=["GET", "POST"])
# def bad_sentiment():
#     # Dummy Melbourne Data
#     df = real_estate

#     # Get Tweet
#     if request.method == "GET":
#         return render_template('index.html')
#     elif request.method == "POST":
#         # Get Tweet
#         text_query = request.form['text']
#         tweet_data = get_tweets(text_query)

#         # add text tweet stats
#         total_mentions = len(tweet_data)
#         if total_mentions == 0 or text_query == " ":
#             average_mentions = 0
#         else:
#             average_mentions = round(total_mentions/7)

#         try:
#             # add detailed datetime features
#             tweet_data['date'] = tweet_data.created_at.apply(
#                 lambda x: x.date())
#             tweet_data['day'] = tweet_data.created_at.apply(
#                 lambda x: x.day_name())
#             tweet_data['month'] = tweet_data.created_at.apply(
#                 lambda x: x.month_name())
#             tweet_data['year'] = tweet_data.created_at.apply(
#                 lambda x: x.year)
#             tweet_data['time1'] = tweet_data.created_at.apply(
#                 lambda x: x.to_period('H').strftime('%d-%b-%y'))
#             tweet_data['time2'] = tweet_data.created_at.apply(
#                 lambda x: x.to_period('H').strftime('%d-%b-%y %H:%M'))

#             time1 = tweet_data[['time1', 'tweet_text']].groupby(
#                 ['time1'], as_index=False).count()
#             time2 = tweet_data[['time2', 'tweet_text']].groupby(
#                 ['time2'], as_index=False).count()

#             tweet_legend = "conversations"
#             # choose whether to use time1 (day & hour) or time2 (hour)
#             if len(time1.time1) > 1:
#                 tweet_time_label = list(time1.time1)
#                 tweet_count_values = list(time1.tweet_text)
#             else:
#                 tweet_time_label = list(time2.time2)
#                 tweet_count_values = list(time2.tweet_text)

#             # DEFINE ONLY BAD SENTIMENT
#             # tweet_data = tweet_data[tweet_data['sentiment'] == -1]

#             # Preprocessing 'tweet_text'
#             tweet_data['tweet_text_preprocessed'] = tweet_data['tweet_text'].apply(
#                 lambda x: text_preprocessing(x)
#             )

#             # Predict Twitter Text
#             prediction_list = predict_sentiment(
#                 model, tweet_data, colname='tweet_text_preprocessed')
#             tweet_data['sentiment'] = prediction_list

#             sentiment_chart = tweet_data[['sentiment', 'tweet_text']].groupby(
#                 ['sentiment'], as_index=False).count()
#             tweet_sentiment_label = list(sentiment_chart.sentiment)
#             tweet_sentiment_values = list(sentiment_chart.tweet_text)

#             # potential reach data
#             reach_data = tweet_data[['screen_name', 'followers']].head(
#                 10).sort_values(by='followers', ascending=False)
#             reach_data_screen_name = list(reach_data.screen_name)
#             reach_data_followers = list(reach_data.followers)

#             # word distribution
#             word_freq_dist_dict = []
#             for i in tweet_data.tweet_text_preprocessed:
#                 word_freq_dist_dict.extend(i.split(' '))

#             word_freq_dist = nltk.FreqDist(word_freq_dist_dict)
#             top10words = word_freq_dist
#             top10words = word_freq_dist.most_common(20)
#             words = []
#             words_frequency = []
#             for i in top10words:
#                 words.append(i[0])
#                 words_frequency.append(i[1])

#             # location distribution
#             top10locations = pd.DataFrame(
#                 tweet_data['location'].value_counts())[:20]
#             locations = top10locations.index
#             locations_frequency = [i for i in top10locations.location]

#         except:
#             tweet_legend = "conversations"
#             tweet_time_label = ['None']
#             tweet_count_values = [0]
#             tweet_sentiment_label = ['None']
#             tweet_sentiment_values = [0]
#             reach_data_screen_name = ['None']
#             reach_data_followers = [0]
#             words = ['None']
#             words_frequency = [0]
#             locations = ['None']
#             locations_frequency = [0]

#     # Melbourne Data
#     df_Regionname = df[['Price', 'Regionname']].groupby(
#         ['Regionname'], as_index=False).mean()
#     legend = 'Average Price'
#     labels = list(df_Regionname.Regionname)
#     values = list(df_Regionname.Price)

#     return render_template('bad-sentiment.html',
#                            tweet_data=tweet_data, text_query=text_query,
#                            total_mentions=total_mentions, average_mentions=average_mentions,
#                            legend=legend, labels=labels, values=values,
#                            tweet_time_label=tweet_time_label, tweet_count_values=tweet_count_values, tweet_legend=tweet_legend,
#                            tweet_sentiment_label=tweet_sentiment_label, tweet_sentiment_values=tweet_sentiment_values,
#                            reach_data_screen_name=reach_data_screen_name, reach_data_followers=reach_data_followers,
#                            words=words, words_frequency=words_frequency, locations=locations, locations_frequency=locations_frequency
#                            )


########## ROUTE TO MYSQL FUNCTION ##########
# ROUTE TO API
# get dan post method
@app.route('/tweet', methods=['GET', 'POST'])
def tweet_to_mysql():
    if request.method == 'GET':
        # query untuk digunakan
        sql_query = 'SELECT * FROM twitter_database'

        # membuka koneksi ke db
        cursor = connection.cursor()

        # eksekusi perintah sql
        cursor.execute(sql_query)

        # fetch all data from query result
        query_result = cursor.fetchall()

        # return query_result data to API
        return jsonify(query_result)

    elif request.method == 'POST':
        # post untuk melakukan post data/memasukkan data ke db
        # data yang dikirim saat request ada di requests.form
        # data tersebut diubah menjadi dictionary
        form = dict(request.form)

        # menyimpan data ke variable
        id = 0
        tweet_id = form['tweet_id']
        user_name = form['user_name']
        screen_name = form['screen_name']
        profile_url = form['profile_url']
        created_at = form['created_at']
        created_at_date = form['created_at_date']
        created_at_day_name = form['created_at_day_name']
        created_at_month = form['created_at_month']
        created_at_year = form['created_at_year']
        created_at_time1 = form['created_at_time1']
        created_at_time2 = form['created_at_time2']
        tweet_text = form['tweet_text']
        location = form['location']
        followers = form['followers']
        following = form['following']
        listed_count = form['listed_count']
        profile_image = form['profile_image']
        profile_banner_image = form['profile_banner_image']
        news_url_1 = form['news_url_1']
        news_url_2 = form['news_url_2']
        tweet_data_preprocessed = form['tweet_data_preprocessed']
        sentiment = form['sentiment']
        sentiment_description = form['sentiment_description']

        # membuat query untuk menyimpan data di atas
        sql_query = """INSERT INTO twitter_database
                        (id, tweet_id, user_name, screen_name, profile_url, 
                        created_at, created_at_date, created_at_day_name,
                        created_at_month, created_at_year, created_at_time1, 
                        created_at_time2, tweet_text, location,
                        followers, following, listed_count, profile_image,
                        profile_banner_image, news_url_1, news_url_2, 
                        tweet_data_preprocessed, sentiment, sentiment_description)
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        # data yang akan disimpan dimasukkan ke variabel
        data = (id, tweet_id, user_name, screen_name, profile_url,
                created_at, created_at_date, created_at_day_name,
                created_at_month, created_at_year, created_at_time1,
                created_at_time2, tweet_text, location,
                followers, following, listed_count, profile_image,
                profile_banner_image, news_url_1, news_url_2,
                tweet_data_preprocessed, sentiment, sentiment_description)

        # membuka koneksi ke mysql
        cursor = connection.cursor()

        # eksekusi perintah
        cursor.execute(sql_query, data)

        # commit input data ke DB agar tersimpan lalu close supaya
        # tidak banyak koneksi terbuka
        connection.commit()
        cursor.close()

        # mengubah data dictionary menjadi json untuk dikirim balik
        return jsonify({'message': f'insert succes, name: {user_name}'})

# Route PATCH, DELETE
# @app.route('/employee/<id>', methods=['PATCH', 'DELETE'])
# def employee_id(id):
#     if request.method == 'PATCH':
#         # ambil data dari form yang masuk
#         form = dict(request.form)

#         # menyimpan data ke variable
#         name = form['name']
#         gender = form['gender']
#         salary = form['salary']

#         # jika ingin mengubah menjadi boolean
#         # married = bool(form['married'])

#         # membuat query untuk mengubah data berdasarkan employee id
#         # menggunakan kutip 3 agar bisa newline

#         sql_query = f"""UPDATE employee SET
#                         name ='{name}',
#                         gender = '{gender}',
#                         salary = '{salary}'
#                         WHERE employeeID={id}"""

#         # membuka koneksi ke mysql
#         cursor = connection.cursor()

#         # eksekusi perintah
#         cursor.execute(sql_query)

#         # commit input data ke DB agar tersimpan lalu close supaya
#         # tidak banyak koneksi terbuka
#         connection.commit()
#         cursor.close()

#         # mengubah data dictionary menjadi json untuk dikirim balik
#         return jsonify({'message': f'update succes', 'user_id': id})

#     elif request.method == 'DELETE':

#         sql_query = f'DELETE FROM employee WHERE employeeID = {id}'
#         cursor = connection.cursor()
#         cursor.execute(sql_query)

#         connection.commit()
#         cursor.close()

#         return jsonify({'message': 'Delete success', 'user_id': id})

# check connection
# query = 'SHOW DATABASES'
# cursor.execute(query)
# for i in cursor:
#     print(i)


if __name__ == "__main__":
    app.run(debug=True)
