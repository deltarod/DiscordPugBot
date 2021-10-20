import configparser

configFile = 'bot.cfg'

config = configparser.ConfigParser()
config.read(configFile)

configSections = config.sections()

save = False

# Setup a default config if doesn't exist
if 'general' not in configSections:
    config.add_section('general')
    config['general']['token'] = 'discord_token'

    save = True

# If a section was missing, save that to the config
if save:
    with open(configFile, 'w') as cfg:
        config.write(cfg)

token = config['general']['token']
