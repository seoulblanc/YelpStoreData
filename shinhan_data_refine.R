
setwd('c:/Rwork')
imsi <- read.csv('Shinhan_data_ya.csv', sep=',')
imsi
summary(imsi)

# NA 값이 있는 열 제거 
dataclean = imsi[,c(2:7,10:15,17:26,28,34,35)]
head(dataclean)
str(dataclean)

# 데이터셋을 3개로 나누어서 corr 검사

# 첫번째
dataclean1 = dataclean[,c(1:9)]
head(dataclean1)
cor_data<-cor(dataclean1)
cor_data
corrplot::corrplot(cor_data, method = 'number')

# 두번째 
dataclean2 = dataclean[,c(7,10:18)]
head(dataclean2)
cor_data<-cor(dataclean2)
cor_data
corrplot::corrplot(cor_data, method = 'number')

# 세번째 
dataclean3 = dataclean[,c(7,18:25)]
head(dataclean3)
cor_data<-cor(dataclean3)
cor_data
corrplot::corrplot(cor_data, method = 'number')

# 상관관계 높은 값들을 제거한 데이터 (총 16개 변수)
nocorr_data = dataclean[,c(1:4,7,10,11,13,16:19,22:25)]
head(nocorr_data)
str(nocorr_data)

cor_data<-cor(nocorr_data)
cor_data
corrplot::corrplot(cor_data, method = 'number')

#분산 0 확인
library(caret)
nearZeroVar(nocorr_data) 
# 결과 8, 11, 12, 13 (펀드주식, 부채잔액, 부채잔액_신용대출, 부채잔액_전세자금대출)

# 분산이 0인 값 제거 후 nonzero_data 생성 (총 12개 변수 )
nozero_data <- nocorr_data[,-nearZeroVar(nocorr_data)]
str(nozero_data)
summary(nozero_data)

# min에 0이 있는 값들 -> 범주형으로 전환 (총 4개 변수)
# (기타자산, 월저축액_저축성보험, 월저축액_청약, 노후자금융월저축액)

# 기타자산, 범주화하기 
plot(nozero_data$기타자산)
boxplot(nozero_data$기타자산)
hist(nozero_data$기타자산)
summary(nozero_data$기타자산)

gita1 <- nozero_data[nozero_data$기타자산<=6750,]
boxplot(gita1$기타자산)
summary(gita1$기타자산)

data_gita_category <- transform(nozero_data, 
    기타자산B = ifelse(기타자산 < 300, "0_300",
                      ifelse(기타자산 >= 300 & 기타자산< 1000, "300_1000", 
                      ifelse(기타자산 >= 1000 & 기타자산 <2500, "1000_2500",
                      ifelse(기타자산 >= 2500 & 기타자산 <6750, "2500_6750",
                      ifelse(기타자산 >= 6759, "6750_upper", "no"
                                 ))))))

category_data <- data_gita_category[c('기타자산', '기타자산B')]
head(category_data)

# 월저축액_저축성보험, 범주화하기
plot(nozero_data$월저축액_저축성보험)
boxplot(nozero_data$월저축액_저축성보험)
hist(nozero_data$월저축액_저축성보험)
summary(nozero_data$월저축액_저축성보험)

data_juchuk_category <- transform(data_gita_category, 
      월저축액_저축성보험B = ifelse(월저축액_저축성보험 == 0 , "No", "Yes"
      ))
head(data_juchuk_category)


# 월저축액_청약,범주화하기
plot(nozero_data$월저축액_청약)
boxplot(nozero_data$월저축액_청약)
hist(nozero_data$월저축액_청약)
summary(nozero_data$월저축액_청약)

data_jungyak_catetory <- transform(data_juchuk_category, 
        월저축액_청약B = ifelse(월저축액_청약 == 0 , "No", "Yes"
                          ))
head(data_jungyak_catetory)

# 노후자금융월저축액, 범주화하기
plot(nozero_data$노후자금융월저축액)
boxplot(nozero_data$노후자금융월저축액)
hist(nozero_data$노후자금융월저축액)
summary(nozero_data$노후자금융월저축액)

data_all_category <- transform(data_jungyak_catetory, 
      노후자금융월저축액B = ifelse(노후자금융월저축액 == 0 , "No", "Yes"
                                   ))

# 범주형 데이터로 변환 완료(4개의 카테고리 모두)
head(data_all_category)
str(data_all_category)

# 범주형 데이터로 본래 데이터 대체 (총 12개 카테고리)
data_all <- data_all_category[,c(1:5,7,11:16)]
str(data_all)

# factor로 전환해야 하는 카테고리
# 성별, 연령_10세단위, 직업구분, 지역구분
data_all$성별  <- as.factor(data_all$성별)
data_all$연령_10세단위  <- as.factor(data_all$연령_10세단위)
data_all$직업구분  <- as.factor(data_all$직업구분)
data_all$지역구분 <- as.factor(data_all$지역구분)
str(data_all)

# 정규성 검사해야하는 카테고리 : 총자산, 월총저축액, 월총소비금액, 월평균카드사용금액 

# 총자산 정규성 검사 후 로그
hist(data_all$총자산)
qqnorm(data_all$총자산)
qqline(data_all$총자산, col=2)

data_all$총자산 <- log(data_all$총자산)
qqnorm(data_all$총자산)
qqline(data_all$총자산, col=2)

# 월총저축액 정규섬 검사 후 로그 
hist(data_all$월총저축액)
data_all$월총저축액 <- log(data_all$월총저축액)
hist(data_all$월총저축액)
qqnorm(data_all$월총저축액)
qqline(data_all$월총저축액, col=2)

# 월총소비금액 정규섬 검사 후 로그 
hist(data_all$월총소비금액)
data_all$월총소비금액 <- log(data_all$월총소비금액)
hist(data_all$월총소비금액)
qqnorm(data_all$월총소비금액)
qqline(data_all$월총소비금액, col=2)

# 월평균카드사용금액 정규성 검사 -> 정규분포에 따르고 있음. 그대로 둠. 
hist(data_all$월평균카드사용금액)
qqnorm(data_all$월평균카드사용금)
qqline(data_all$월평균카드사용금, col=2)

# 데이터 정규화 및 범주화가 완료된 데이터 검사 및 저장 (12개 독립변수 선별)
head(data_all)
str(data_all)
write.csv(data_all, "C:/Rwork/refined_data_ya.csv")

# NA 값이 있는 레이블을 y로 잡고 회귀식 만들어야 함 

# 독립변수 다시 선택

# 회귀식 검증 및 정확도 테스트 



