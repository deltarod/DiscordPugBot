from src import db, cfg
from src.bot import bot

db.addExitRegister()

db.openEnv()
db.openDBs()

bot.run(cfg.token)


