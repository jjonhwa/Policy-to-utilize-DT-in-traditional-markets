# 전통시장 DT 활용 방안

## Project Flow
### 주제 선정
[넥스트노멀 시대 - 전통시장 DT 활용 방안](https://github.com/jjonhwa/Policy-to-utilize-DT-in-traditional-markets./blob/main/%EB%84%A5%EC%8A%A4%ED%8A%B8%EB%85%B8%EB%A9%80%20%EC%8B%9C%EB%8C%80%20-%20%EC%A0%84%ED%86%B5%EC%8B%9C%EC%9E%A5%20DT%20%ED%99%9C%EC%9A%A9%20%EB%B0%A9%EC%95%88.pdf) 참고

### 분석 데이터 선정
![전통시장](https://user-images.githubusercontent.com/53552847/142356042-f6e05621-fa81-435a-be3f-464f9ab7a453.jpg)
- 위의 데이터와 더불어, 통계청에서 제공하는 데이터를 추가적으로 활용(유동인구 Dataset)하였으며, 이는 공개 불가하며 이로 인한 PCA 과정에서 최종 발표자료와의 차이가 있음을 참고하자.

### Data Preprocessing
- 좌표계 변환
- 결측치 처리 및 보간
- 이상치 처리
- 데이터 정규화

### Feature Engineering
#### 차원 축소 (PCA & MCA)
- 많은 Feature 수로 인한, 다중공선성 문제 해결을 위하여 차원 축소 기법 적용
- PCA를 활용하여 연속형 변수의 다중공선성 문제 해결 및 파생 변수 생성
- MCA를 활용하여 명목형 변수의 다중공선성 문제 해결 및 파생 변수 생성

![전통시장1](https://user-images.githubusercontent.com/53552847/142358764-101fd579-5e04-4ca6-93e3-9682a24c7c4f.jpg)

#### Clustering (KMeans)
- DTC(Drive Througth Center) 위치 선정 문제 및 상품 추천을 적용하기 위한 운영위기 시장 군집을 클러스터링을 활용하여 선정
- KMeans, Hierarchical, DBSCAN, GMM 적용 후 실루엣 계수를 활용하여 최종 KMeans 기법 선택
- 실루엣 계수의 분산을 고려하여 KMeans의 3개의 군집 선정
![전통시장2](https://user-images.githubusercontent.com/53552847/142359351-021fea0d-da10-4d71-b241-9bdeddb17e8b.jpg)
- 3개의 군집 가운데 가장 위기 시장을 시각화 한 후 이를 바탕으로 최종 군집 선정

### Item
#### DTC 최적 입지 선정
- 공공시설을 DTC 후보군으로 선정 
- 선정된 공공시설 후보군 중 가장 좋은 입지를 선정하는 방법인 P-Median 알고리즘을 활용
- 추가적인 제약사항을 활용하여 P-Median을 Heuristic하게 적용.
- 유동인구와 편의점수의 강한 상관관계를 확인한 후, 유동인구 데이터를 편의점 수 데이터로 대체하여 활용
- P-Median: 입지 후보지 중 수요지와의 거리를 계산하여 P개의 최종 입지 선정.
- 이에 추가적으로 복수처리, 빈도수 제약을 추가하여 최종 3~4개의 후보군 선정.
- 최종 후보군에 추가 제약사항을 더하여 최종 입지를 선정.
![전통시장4](https://user-images.githubusercontent.com/53552847/142362059-049b28a2-2eb1-48e1-b9fc-139db10c4d08.jpg)

#### DTC 상품 품목 추천
- "온라인 인기 유통 상품 == DTC 상품 품목 추천 대상" 이라고 판단.
- 농산물, 수산물, 축산물에 대한 온라인 유통 상품을 인기순으로 데이터 크롤링
- 빈도수를 바탕으로 WordCloud를 통한 시각화 및 추천.
![전통시장3](https://user-images.githubusercontent.com/53552847/142362044-d44628f7-7529-4277-965c-ee4a7818acb1.jpg)


#### 기대효과
- 다양한 경제적 파급효과 창출
- 소비자들의 편의성 확대
- 전통시장의 디지털 전환에 대한 정부 정책의 가이드라인 제공

## Contributor
- [jjonhwa](https://github.com/jjonhwa)
- [Brady Kim](https://github.com/fenzhantw)
- [wjdghwo](https://github.com/wjdghwo)


