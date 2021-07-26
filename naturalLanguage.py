# Imports the Google Cloud client library
from google.cloud import language_v1

# Instantiates a client
def googleSentimentAnalyze(text):
    print("Google Server Request...")
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    document = language_v1.Document(content=text, language='ko',type_=language_v1.Document.Type.PLAIN_TEXT)

    print("Assessting sentiment...")
    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    #print("Text: {}".format(text))
    #print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

    #print(document)
    return sentiment.score

if __name__=="__main__":
    text=input()
    print(googleSentimentAnalyze(text))