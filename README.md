# openSWMovieRatingProject
오픈소스SW프로젝트 과제용 git

신뢰성있는 영화 평점을 위해 유튜브 영화 리뷰 영상의 댓글을

크롤링 한 후 알고리즘을 이용해 신뢰성 있는 댓글들을 선별한 후

LSTM으로 이뤄진 영화 평점 예측 모델을 사용하여 평점을 도출합니다

Main.py로 작동합니다
원하는 영화를 정확히 입력한 후
영화에 관한 추가적인 정보를 입력합니다(optional)

영화 리뷰와 그에 달린 영화 리뷰 댓글을 알고리즘 으로 선별하고
모델을 이용하여 평점을 예측합니다

모든 리뷰 댓글의 평점을 평균내어 영화의 평점을 도출합니다
각 댓글들은 comment폴더 내 csv(유투브 영상id로 분류)파일로 저장됩니다




model_predict.py:
  영화평점 예측을 위한 LSTM
  
  
YTVideoReviewManager.py:
  영화 클래스 파일
  
  
commentClass.py:
  댓글 클래스 파일
  
  
youtube_env.yaml:
  아나콘다 가상환경파일
  
  
전처리.ipynb:
  평점 예측 모델을 위한 훈련데이터 전처리 파일

## 실행시 주의사항
  1. Konlpy, Keras, Anaconda 가상환경, Tensorflow 시스템이 구축되어 있어야 사용이 가능합니다.
  2. openSWMovieRatingProject\data_for_model 파일의 용량이 커서 압축되어있기 때문에 해당 파일을 압축 해제해야 사용이 가능합니다.
