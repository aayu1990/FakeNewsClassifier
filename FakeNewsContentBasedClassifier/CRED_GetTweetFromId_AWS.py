
# This code creates the dataset from output.csv which is downloadable from the
# internet well known dataset which is labeled manually by hand. But for the text
# of tweets you need to fetch them with their IDs.
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
import numpy as np
import pandas as pd
import csv
import ast
import tweepy


access_token = "----------------------------------"
access_token_secret = "----------------------------------"
consumer_key = "----------------------------------"
consumer_key_secret = "----------------------------------"

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
data = api.rate_limit_status()

# This method creates the training set


def createTrainingSet(tweetIdFile, ratingsFile, targetResultFile):
    import csv
    import time

    counter = 0
    tempData = []
    tweetData = []
    ratings = {}

    # ------------------------------------------------------------------------------------------------------------------------
    #                                           Reading the file cred_event_TurkRatings.data
    # ------------------------------------------------------------------------------------------------------------------------
    with open(ratingsFile, 'r') as ratingsFileData:
        # read a single line
        line = ratingsFileData.readline()
        while line:
            if counter == 0:
                counter += 1
                line = ratingsFileData.readline()
                continue
            topic = line.split("[")
            key = ""
            val = ""
            temp_list = []
            for i, string in enumerate(topic):
                # print(i,string)
                if i == 0:
                    key = string
                    key = key.strip()
                    # print("KEY",key)
                if i == 2:
                    val = string[:-2]
                    val = val.split(", ")
                    # print("VALUE",val)
                    for i in val:
                        i = i.strip('"')
                        i = i.strip("'")
                        temp_list.append(int(i))

                        # print(temp_list)
                        if len(temp_list) != 0:
                            continue
                        # else:
                            # print(key,temp_list)

            # print(key,sum(temp_list)/len(temp_list))
            ratings[key] = sum(temp_list) / len(temp_list)
            line = ratingsFileData.readline()

    # close the pointer to that file
    ratingsFileData.close()

    # for i in ratings:
    #    print(i, ratings[i])

    # ------------------------------------------------------------------------------------------------------------------------
    #                                           Reading the file cred_event_SearchTweets.data
    # ------------------------------------------------------------------------------------------------------------------------

    tweetFilehandle = open(tweetIdFile, 'r')

    counter = 0

    while True:
        # read a single line
        line = tweetFilehandle.readline()
        if not line:
            break

        temp_val = line.split()[0]
        counter += 1
        list_ = line.split(')')
        # for i in list_:
        # print(i)
        if counter == 1:
            continue
        for i in list_:
            counter += 1
            start = i.find('=')
            end = i.find("'", start + 1)
            temp = i[start + 1:end]
            if temp == ']':
                continue
            # print(temp_val, counter, temp)
            tempData.append((temp_val, int(temp)))
            if counter == 101:
                # print("BREAKING")
                counter = 1
                break
        # if counter == 2:
        #    break
    # print("________")
    # close the pointer to that file
    tweetFilehandle.close()

    # print(tempData)

    for row in tempData:
        tweetData.append(
            {"tweet_id": row})
        #   {"tweet_id": row[], "label": row[1], "topic": row[0]})

    # print(tweetData)

    sleepTime = 1 / 100
    trainingDataSet = []

    for tweet in tweetData:
        # , tweet["tweet_id"][1])
        try:
            # print("_______")
            tweetFetched = api.get_status(tweet["tweet_id"][1])
            # print("1")
            tweet["text"] = tweetFetched.text
            # print("2")
            trainingDataSet.append(tweet)
            # time.sleep(sleepTime)
        except Exception as e:
            # print(tweet["tweet_id"][0], tweet["tweet_id"[1]],
            #      tweet["text"], ratings[tweet["tweet_id"][0]])
            if trainingDataSet:
                with open(targetResultFile, 'a') as csvfile:
                    linewriter = csv.writer(
                        csvfile, delimiter=',', quotechar="\"")
                    # linewriter = csv.writer(csvfile, delimiter=',', quotechar="\"")

                    for tweet in trainingDataSet:
                        if tweet["tweet_id"][0] in ratings:
                            # print(tweet)
                            # print(tweet["tweet_id"][0])
                            # print(tweet["tweet_id"][1])
                            # print(tweet["text"])
                            # print(ratings[tweet["tweet_id"][0]])
                            try:
                                print(".")
                                linewriter.writerow(
                                    [tweet["tweet_id"][0], tweet["tweet_id"][1], tweet["text"], ratings[tweet["tweet_id"][0]]])  # , ratings[tweet["tweet_id"]][0]])
                            #[temp_val, tweet["tweet_id"], tweet["text"], ratings[temp_val]])
                            except Exception as e:
                                print("ERROR2", e)
                csvfile.close()
            trainingDataSet = []
    # print(trainingDataSet)

    # with open(targetResultFile, 'w') as csvfile:

    if trainingDataSet:
        with open(targetResultFile, 'a') as csvfile:
            linewriter = csv.writer(csvfile, delimiter=',', quotechar="\"")
            if tweet["tweet_id"][0] in ratings:
                for tweet in trainingDataSet:
                    try:
                        linewriter.writerow([tweet["tweet_id"][0], tweet["tweet_id"[
                                            1]], tweet["text"], ratings[tweet["tweet_id"][0]]])
                        #[temp_val, tweet["tweet_id"], tweet["text"], ratings[temp_val]])
                    except Exception as e:
                        print(e)
        csvfile.close()

    return trainingDataSet


# Code starts here
# This is tweetData dataset
tweetIdFile = "DataSet/cred_event_SearchTweets.data"
ratingsFile = "DataSet/cred_event_TurkRatings.data"

# This is my target file
targetResultFile = "DataSet/output.csv"

# Call the method
print("Please Wait, creating the csv file")
resultFile = createTrainingSet(tweetIdFile, ratingsFile, targetResultFile)
