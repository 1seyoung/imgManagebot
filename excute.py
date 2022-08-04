from config import TELEGRAM_API_KEY
from nftbot import NFTmanager

sm = NFTmanager(TELEGRAM_API_KEY)

sm.main()