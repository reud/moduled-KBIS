import os

#You need to set this enviromental-varience
KBIS_MINGEN=os.environ['KBIS_MINGEN']#15
KBIS_MAXGEN=os.environ['KBIS_MAXGEN']#22
USERLIST_DATA_DIRECTRY=os.environ['USERLIST_DATA_DIRECTRY']#'../../KBIS_Workingplace/Twitter対応リスト.xlsx'
MANAGEBOOK_PLACE=os.environ['MANAGEBOOK_PLACE'] #'../Tools/237585_個人支払出納管理簿.xlsx'
USERLIST_DATA_SHEETNAME=os.environ['USERLIST_DATA_SHEETNAME']
MAXUSER_BY_GEN=os.environ['MAXUSER_BY_GEN']# G毎に分けた場合の最大人数　例えば　16Gが一番人多くて　30人なら　30を設定する。 最適解じゃないけど許して
MAX_EVENTS=os.environ['MAX_EVENTS']  # 増減が書いてあるセルのもっとも右にある列の値　とりあえず100あればいいんじゃないかな？
START_EVENTS=os.environ['START_EVENTS']  # 会計の始まりのセルの列　8で
OUTPUT_MODE=os.environ['OUTPUT_MODE']
#Optional
