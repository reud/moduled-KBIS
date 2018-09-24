import os

# You need to set this enviromental-varience
KBIS_MINGEN = int(os.environ['KBIS_MINGEN'])  # 15
KBIS_MAXGEN = int(os.environ['KBIS_MAXGEN'])  # 21
USERLIST_DATA_DIRECTRY = os.environ['USERLIST_DATA_DIRECTRY']  # '../../KBIS_Workingplace/Twitter対応リスト.xlsx'
MANAGEBOOK_PLACE = os.environ['MANAGEBOOK_PLACE']  # '../Tools/237585_個人支払出納管理簿.xlsx'
USERLIST_DATA_SHEETNAME = os.environ['USERLIST_DATA_SHEETNAME']
MAXUSER_BY_GEN = int(os.environ['MAXUSER_BY_GEN'])  # G毎に分けた場合の最大人数　例えば　16Gが一番人多くて　30人なら　30を設定する。 最適解じゃないけど許して
MAX_EVENTS = int(os.environ['MAX_EVENTS'])  # 増減が書いてあるセルのもっとも右にある列の値　とりあえず100あればいいんじゃないかな？
START_EVENTS = int(os.environ['START_EVENTS'])  # 会計の始まりのセルの列　8で
OUTPUT_MODE = os.environ['OUTPUT_MODE']

LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

DATABASE_PLACE = os.environ['DATABASE_PLACE']

BUDGET_SHEETNAME = '予算'

TEAM_BUDGET_START_COLUMN = 12  # 3
TEAM_BUDGET_START_ROW = 9

RECEIPTS_AND_EXPENDITURE_SHEETNAME = '出納'
RECEIPTS_AND_EXPENDITURE_CELL = 'D3'

LINENOTIFY_TOKEN=os.environ['LINENOTIFY_TOKEN']
# エクセルのレイアウトいじると全部おじゃんなので注意
# 班の順番もいじらないでね！

# Optional
