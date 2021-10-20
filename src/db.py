import os
import shutil
import simpleBDB as db


dbPath = os.path.join('db')


def clearLocks():
    if os.path.exists(dbPath):  # pragma: no cover
        for file in os.listdir(dbPath):
            if '__db.0' not in file:
                continue
            filePath = os.path.join(dbPath, file)
            print('deleting lock file', filePath)
            os.remove(filePath)


def openEnv():
    db.open_env()
    db.createEnvWithDir(dbPath)
    db.setLockDetect()


def openDBs():
    db.open_dbs()


def closeDBObjects():
    db.close_dbs()


def addExitRegister():
    import atexit

    atexit.register(closeDBObjects)

def closeDBs():
    db.close_env()


def doBackup():
    backupDir = os.path.join(cfg.jbrowsePath, cfg.dataPath, 'backup')

    if not os.path.exists(backupDir):
        os.makedirs(backupDir)

    currentBackupDir = os.path.join(backupDir, str(datetime.today().date()))

    if not os.path.exists(currentBackupDir):
        os.makedirs(currentBackupDir)

    db.doBackup(currentBackupDir)


def cleanLogs():
    filesToBackup = db.getLogArchive()

    logBackupDir = os.path.join('db_log_backup')

    if not os.path.exists(logBackupDir):
        os.makedirs(logBackupDir)

    if len(filesToBackup) != 0:
        for logFile in filesToBackup:
            logFilePath = os.path.join(dbPath, logFile)
            movePath = os.path.join(logBackupDir, logFile)

            shutil.move(logFilePath, movePath)


def getTxn(parent=None):
    if parent is not None:
        return db.getEnvTxn(parent=parent)
    return db.getEnvTxn()


class Guild(db.Resource):
    keys = ("GuildID", )

    def make_details(self):
        return {'queue': [], 'currentGames': [], 'teamSize': 5}

    pass
