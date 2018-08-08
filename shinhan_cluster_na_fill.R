library(dplyr)
g_number = c(111,112,121,122,131,132,211,212,221,222,223,231,232,311,312,313,321,322,323,331,332,333,341,342,343)
for(one_g_number in g_number) {

# 클러스터링 그룹 정보가 들어간 모든 데이터 
setwd('c:/Rwork')
data <- read.csv('filled_NA_data_ya.csv', sep=',')
str(data)
summary(data)

# 데이터 셋에서 특정 그룹(step123 구분에 따라서) 선택 
data_group <- data[data$step123==one_g_number,]
data_group <- data_group[order(data_group$금융자산),]
str(data_group)

# 하나의 column씩 선택해서결측치 추정 (총 6개) 
one_col = c('은퇴후필요자금')
#('금융상품잔액_적금','금융상품잔액_청약','금융상품잔액_펀드', '금융상품잔액_ELS.DLS.ETF', '금융상품잔액_정기예금','은퇴후필요자금')

data_one_column <- select( data_group, idx, one_col)
data_group_no_na <- na.omit(data_one_column)
new_table <- table(data_group_no_na[one_col])
Frame <- data.frame(new_table)

# NA 없는 값을 data_vector 벡터로 만든다 
data_vector <- Frame$Var1
# 값이 나올 확률을 prop_vecto 벡터에 담는다
prop_vector <- c(Frame$Freq /sum(Frame$Freq))
# 샘플로 몇개를 추출할 것인가? (NA 수와 일치)
howmany_na <- sum(is.na(data_one_column))
# 샘플 코드 실행 
new_samples <- sample(data_vector, howmany_na, prob = prop_vector, replace = TRUE)
new_samples <- sort(new_samples)
new_samples <- as.character(new_samples)
new_samples <- as.numeric(new_samples)

# NA 값을 샘플로 추출된 것들로 채운다
data_one_column[one_col][is.na(data_one_column[one_col])] <- sort(new_samples)

# 원본 데이터 셋을 결측치 채운 칼럼으로 바꾼다 
data <- left_join(data, data_one_column, by="idx") %>% 
  mutate(은퇴후필요자금 = ifelse(is.na(은퇴후필요자금.x),은퇴후필요자금.y, 은퇴후필요자금.x)) %>% 
  select(-은퇴후필요자금.y, -은퇴후필요자금.x)
str(data)

# 데이터를 저장한다
write.csv(data, "C:/Rwork/filled_NA_data_ya.csv")
}


