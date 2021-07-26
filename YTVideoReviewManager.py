import sqlite3
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import NaverMovieInfo

class YTVideoReview:
    def __init__(self,videoName,videoID,reasonForSelection):   
        self.videoName=videoName
        self.videoID=videoID
        self.reasonForSelection=reasonForSelection

class YTVideoReviewManager:
    
    def _isBannedVideo(self, search_result):
        for row in self.cur.execute("SELECT videoid from banned_videos where query=\'%s\'"%(self.movieNameQuery)):
            if row[0]==search_result["id"]["videoId"]:
                return True

        return False

    def _isYTReviewVideo(self,search_result):

        mandanTags=("소개","결말","포함","리뷰","스포")

        request = self.youtubeConnection.videos().list(
            part="snippet",
            id=search_result["id"]["videoId"]
        ).execute()

        result =request.get("items",[])[0]

        videoTitle = search_result["snippet"]["title"]
        videoDescription = result["snippet"]["description"]        
        
        #print(search_result["id"]["videoId"], videoTitle)

        if (self.movieNameQuery not in videoTitle and 
        self.movieNameQuery not in videoDescription and
        self.naverMovieInfo.movieName not in  videoTitle and
        self.naverMovieInfo.movieName not in videoDescription
        ):
            return False

        for tag in mandanTags:
            if tag in search_result["snippet"]["title"] or tag in result["snippet"]["description"]:
                return True

        return False


    def banYTVideoOnDB(self,search_result,banned_reason):
        try:
            self.con.execute("INSERT INTO banned_videos VALUES(\'%s\', \'%s\', \'%s\')"%(self.movieNameQuery, search_result.videoID,banned_reason))
            self.con.commit()   
        except sqlite3.IntegrityError as e:
            print("Error: ",e)
        

        #해당하는 비디오는 영화 리뷰라고 판단하지 않고 밴하기.


    def __init__(self, movieNameQuery, youtubeConnection, naverMovieInfo):

        self.movieNameQuery= movieNameQuery
        self.youtubeConnection = youtubeConnection
        self.naverMovieInfo = naverMovieInfo
        self.YTVideoReviewList=[]


        print("connecting to DB...")
        self.con=sqlite3.connect("YTVideoListManageDB.db")
        self.cur=self.con.cursor()


        movieNameQuery+=" 영화 리뷰" # making query searching for movie review

         # making query searching for movie review based on naver movie info
        
        search_response = youtubeConnection.search().list(
        q=movieNameQuery,
        part="id,snippet",
        maxResults=50,
        regionCode="KR",
        topicId="/m/02vxn", # Restrict search topic only about movies
        type="video"
        ).execute()

        trueCount=5
        falseCount=5

        

        for search_result in search_response.get("items", []):
            if self._isYTReviewVideo(search_result) and not(self._isBannedVideo(search_result)):
                self.YTVideoReviewList.append(
                    YTVideoReview(search_result["snippet"]["title"],search_result["id"]["videoId"],"random"
                    )
                )
                trueCount-=1
            else:
                falseCount-=1

            if trueCount<0 or falseCount<0:
                break
 
        self.YTVideoReviewList.sort(key=lambda YTVideoReview: YTVideoReview.videoID)#sort by videoID
    

#--------------------------------------------------------------------------------------



if __name__=="__main__":




    DEVELOPER_KEY = "AIzaSyCI3F57KsmaUA8F9I8RSkyQwqF06u0Knso"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"


    
    print("Connecting to Youtube API...")
    youtubeConnection = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)



    #movieName = input("Input movie name:")
    movieName ="어벤져스 엔드게임"
    try:
        naverMovieInfo=NaverMovieInfo.NaverMovieInfo(movieName)
        print(naverMovieInfo.movieName)
    except AttributeError as e:
        print(e)
        naverMovieInfo=None


    #print(naverMovieInfo.movieName)
    YTVideoInfo = YTVideoReviewManager(movieName, youtubeConnection, naverMovieInfo)
    YTVideoInfo.banYTVideoOnDB(YTVideoInfo.YTVideoReviewList[5],"not a revie video")
    for result in  YTVideoInfo.YTVideoReviewList:
        print("video title: %s, video id: %s, reason for selection: %s"%(result.videoName, result.videoID, result.reasonForSelection))
    
    
