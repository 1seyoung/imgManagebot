from config import TELEGRAM_API_KEY,GOOGLE_SERVICE_KEY,GOOGLE_SPREAD_SHEET
from nftbot import NFTmanager
sm = NFTmanager(TELEGRAM_API_KEY)

sm.main()
print("check")