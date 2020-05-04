import config
import sqlite3
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions


def get_sentiment(text):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=config.WATSON_API_VERSION,
        iam_apikey=config.WATSON_API_KEY,
        url=config.WATSON_API_URL
    )

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(
                # emotion=True,
                sentiment=True,
                limit=1),
        ))

    return response.result['entities'][0]['sentiment']['score']


def get_all_florence_tweets():
    conn = sqlite3.connect("tweets.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM tweets")
    all_rows = c.fetchall()
    data = []
    added = {}
    for row in all_rows:
        row = list(row)
        # filter out tweets from non florence areas
        if 'hurricane' not in row[4].lower() and 'florence' not in row[4].lower():
            continue
        if row[1] in added:
            continue
        coords = row[3].split(',')
        if int(float(coords[0])) == 33 and int(float(coords[1])) == -84:
            continue
        if float(coords[1]) < -85.5 or float(coords[0]) < 30 or float(coords[1]) > -67:
            continue
        if float(coords[1]) < -82 and float(coords[0]) < 33:
            continue
        if float(coords[0]) > 41 and float(coords[1]) < -82:
            continue
        # if row[5] is None or row[5] is "":
        #     continue
        # sentiment_ = float(row[5]) + 1.2
        # score = 1/sentiment_**3
        # row.append(score)
        if row[5] is not None and row[5] is not "":
            sentiment_ = float(row[5]) + 1.2
            score = 1/sentiment_**3
            row.append(score)
        else:
            row.append(1)
        added[row[1]] = 0
        data.append(row)
    conn.close()
    return data

