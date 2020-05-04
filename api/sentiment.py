import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions

import sqlite3
conn = sqlite3.connect("tweets.sqlite")
c = conn.cursor()
c.execute("SELECT * FROM tweets")
all_rows = c.fetchall()
data = []
added = {}
for row in all_rows:
    # filter out tweets from non florence areas
    if 'hurricane' not in row[4].lower() and 'florence' not in row[4].lower() :
        continue
    if row[1] in added:
        continue
    coords = row[3].split(',')
    if int(float(coords[0]))==33 and int(float(coords[1]))==-84:
        continue
    if float(coords[1])<-85.5 or float(coords[0])<30 or float(coords[1])>-67:
        continue
    if float(coords[1])<-82 and float(coords[0])<33:
        continue
    if float(coords[0])>41 and float(coords[1])<-82:
        continue

    data.append(row)
    added[row[1]] = 0


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    iam_apikey="",
    url="https://gateway-wdc.watsonplatform.net/natural-language-understanding/api"
)
i=0
for row in data:
    print(i)
    # if i>5:
    #     break
    i+=1
    id=row[0]

    try:
        if row[5] is not None:
            continue

        response = natural_language_understanding.analyze(
            text=row[4],
            features=Features(
                entities=EntitiesOptions(
                    # emotion=True,
                    sentiment=True,
                    limit=1
                    ),

            ))
        sentiment = response.result['entities'][0]['sentiment']['score']
        c.execute("UPDATE tweets SET sentiment=(?) WHERE id=(?)", (sentiment, id))
    except:
        pass

conn.commit()
conn.close()


# print(json.dumps(response, indent=2))
# print()
