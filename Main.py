import commentClass
import NaverMovieInfo
from YTVideoReviewManager import YTVideoReviewManager
from apiclient.discovery import build
import pandas as pd
import os
import numpy as np
import re
import urllib.request
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"



print("Connecting to Youtube API...")
youtubeConnection = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

print("Model loading...\n")
vec=pd.read_csv("./data_for_model/data_all.csv")
tokenizer = Tokenizer(76712)
tokenizer.fit_on_texts(vec['x'])
loaded_model = load_model('./data_for_model/best_model2.h5')
print("Model loaded...\n")


movieName = input("Input movie name:")
movieInfo = input("movieinfo:")
#movieName ="어벤져스 엔드게임"
try:
    naverMovieInfo=NaverMovieInfo.NaverMovieInfo(movieName,movieInfo)
    print(naverMovieInfo.movieName)
except AttributeError as e:
    print(e)
    naverMovieInfo=None


YTVideoInfo = YTVideoReviewManager(movieName, youtubeConnection, naverMovieInfo)
print("\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
print("YT Video List:")
for result in  YTVideoInfo.YTVideoReviewList:
    print("video title: %s, video id: %s, reason for selection: %s"%(result.videoName, result.videoID, result.reasonForSelection))
print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")

commentCollectionbyVideo=[]
print("\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
for result in YTVideoInfo.YTVideoReviewList:
    commentCollectionbyVideo.append(commentClass.commentReviewManager(result, youtubeConnection,loaded_model,tokenizer))

movie_rate_list=[]
for i in commentCollectionbyVideo:
    if i.AVERAGE_RATE!=-1:
        movie_rate_list.append(i.AVERAGE_RATE)
print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

print("\n\n\n\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
print()
print(f"{movieName}의 평점은 {sum(movie_rate_list)/len(movie_rate_list)}입니다")
print()
print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")