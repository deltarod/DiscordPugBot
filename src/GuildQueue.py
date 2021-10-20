from simpleBDB import retry, txnAbortOnError
from src import db


@retry
@txnAbortOnError
def join(ctx, txn=None):
    guildId = ctx.guild.id
    userId = ctx.author.id

    guildDb = db.Guild(guildId)
    guildInfo = guildDb.get(txn=txn, write=True)

    if userId in guildInfo['queue']:
        return 'Already in queue'

    for game in guildInfo['currentGames']:
        if userId in game:
            return 'Already in an ongoing game'

    guildInfo['queue'].append(userId)

    if len(guildInfo['queue']) >= guildInfo['teamSize'] * 2:
        users = guildInfo['queue']

        guildInfo['queue'] = []

        guildInfo['currentGames'].append(users)

        output = "Queue Popped:\n"

        for user in usersListFromId(ctx.guild, guildInfo['queue']):
            output += user.display_name + '\n'

    else:
        output = 'You have joined the queue, there are %i in queue' % len(guildInfo['queue'])

    guildDb.put(guildInfo, txn=txn)

    return output


@retry
@txnAbortOnError
def queue(ctx, txn=None):
    guildId = ctx.guild.id

    guildDb = db.Guild(guildId)
    guildInfo = guildDb.get(txn=txn)

    inQueue = usersListFromId(ctx.guild, guildInfo['queue'])

    output = 'Current Queue:\n'

    for user in inQueue:
        output += user.display_name + '\n'

    return output


@retry
@txnAbortOnError
def clear(ctx, txn=None):
    guildId = ctx.guild.id

    guildDb = db.Guild(guildId)
    guildInfo = guildDb.get(txn=txn, write=True)

    guildInfo['queue'] = []

    guildDb.put(guildInfo, txn=txn)

    return 'Queue Cleared'


@retry
@txnAbortOnError
def finish(ctx, txn=None):
    guildId = ctx.guild.id
    authorId = ctx.author.id

    guildDb = db.Guild(guildId)
    guildInfo = guildDb.get(txn=txn, write=True)

    newCurrentGames = []

    for game in guildInfo['currentGames']:
        if authorId in game:
            continue
        else:
            newCurrentGames.append(game)

    guildInfo['currentGames'] = newCurrentGames

    guildDb.put(guildInfo, txn=txn)

    return 'Game Finished'


def usersListFromId(guild, ids):
    members = []
    for user in ids:
        members.append(guild.get_member(user))

    return members

