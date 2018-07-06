library(RODBC)
library(readxl)
library(ggplot2)
ch <- odbcConnect("PostgreSQL35W")
## function defination 
# Currying
SendSql <- function(ch,sSql){
  function(sSql) {
    tryCatch(
      sqlQuery(ch,sSql),error=function(e){cat("error :",conditionMessage(e),"\n")}
    )
  }
}
# fix channel of "ch"
SendSqlToPostgreSQL <- SendSql(ch)

str_eval <- function(str){
  eval(parse(text = str))
}

## start program
excel_path <-commandArgs(T)[1]
tblCallParameter <- read_excel(excel_path)

# get dataset
sqlReadTable <- tblCallParameter$Parameter[tblCallParameter$Parameter_Name == 'DataFrameSQL']
table <- SendSqlToPostgreSQL(sqlReadTable)
odbcClose(ch)

## start plot 
str_ggplot <- tblCallParameter$Parameter[tblCallParameter$Parameter_Name == 'ggplot_function']

# save ploting image
folder <- "C:\\Users\\tanalan\\Documents\\Establish Table\\Media\\Image\\"
filename <- paste(c(tblCallParameter$Parameter[tblCallParameter$Parameter_Name == 'ImageID'],"png"), collapse = ".")
filepath <- paste(c(folder, filename), collapse = "\\")
png(filepath,width = 1200,height = 880)
str_eval(str_ggplot)
dev.off()
# ggsave(filepath)
