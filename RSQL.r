library(RODBC)
library(readxl)
# get tblSqlToSend.xlsx from command  "RSQL.bat"
excel_path <-commandArgs(T)[1]
tblSqlToSend <- read_excel(excel_path)
ch <- odbcConnect("PostgreSQL_wechat")
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
lapply(tblSqlToSend$ToSend,SendSqlToPostgreSQL)
print("The Query is finished!")
odbcClose(ch)

