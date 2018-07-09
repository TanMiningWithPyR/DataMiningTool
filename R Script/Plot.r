library(RODBC)
library(readxl)
library(ggplot2)
## read envirment parameter
global_excel_path <-commandArgs(T)[1]
tblGlobalVar <- read_excel(global_excel_path)
## connection channel
dsn <- tblGlobalVar$Var[tblGlobalVar$VarName == 'Rdsn']
ch <- odbcConnect(dsn) #"PostgreSQL35W"
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
Rworkdir_path = tblGlobalVar$Var[tblGlobalVar$VarName == 'RWorkDir']
R_CallParameter_excel_path <- paste(c(Rworkdir_path,'Parameter\\tblCallParameter.xlsx'), collapse="\\")
tblCallParameter <- read_excel(R_CallParameter_excel_path)

# get dataset
sqlReadTable <- tblCallParameter$Parameter[tblCallParameter$Parameter_Name == 'DataFrameSQL']
table <- SendSqlToPostgreSQL(sqlReadTable)
odbcClose(ch)

## start plot 
str_ggplot <- tblCallParameter$Parameter[tblCallParameter$Parameter_Name == 'ggplot_function']

# save ploting image
folder <- paste(c(Rworkdir_path,"Media\\Image"), collapse = "\\")
filename <- paste(c(tblCallParameter$Parameter[tblCallParameter$Parameter_Name == 'ImageID'],"png"), collapse = ".")
filepath <- paste(c(folder, filename), collapse = "\\")
png(filepath,width = 1200,height = 880)
str_eval(str_ggplot)
dev.off()
# ggsave(filepath)
