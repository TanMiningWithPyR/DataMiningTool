library(RODBC)
library(readxl)
tblSqlToSend <- read_excel("C:/Users/tanalan/Desktop/DataMiningTool/tblSqlToSend.xlsx")
ch <- odbcConnect("PostgreSQL35W")
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

