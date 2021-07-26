import xml.etree.ElementTree as ET
import urllib.request

class NaverMovieInfo:
    CLIENT_ID = "pu8qXcGXBhLD__SaDdSS"
    CLIENT_SECRET = "JAqZiBsAtl"
    NUM_OF_SEARCHING = 1

    #query is name of movie you want to find on NAVER search
    #var detail is string keyword able to specify the movie (ex. actor's name)
    def __init__(self, query, detail=""):

        encText = urllib.parse.quote(query+" "+detail)

        url = "https://openapi.naver.com/v1/search/movie.xml?query=%s&display=%d&sort=sim" %(encText,self.NUM_OF_SEARCHING) 
        

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.CLIENT_ID)
        request.add_header("X-Naver-Client-Secret",self.CLIENT_SECRET)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            response_xml_str = response_body.decode('utf-8')
            root = ET.fromstring(response_xml_str) #parsing XMLstring
            
            self.movieName = root.find("./channel/item/title").text
            self.movieName = self.movieName.replace("<b>","")
            self.movieName = self.movieName.replace("</b>","")
            #eliminating HTML Bold keyword by NAVER API

            self.rating = root.find("./channel/item/userRating").text

            self.link = root.find("./channel/item/link").text

        else:
            print("Error Code:" + rescode)

if __name__=="__main__":
    a = NaverMovieInfo("라이언 일병 구하기")
    print(a.movieName+" "+a.rating+" "+a.link)