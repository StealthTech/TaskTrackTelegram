import os
import configparser
import localization


class Deployer:
    def __init__(self):
        # List of working directories initialization for deployment
        root_log = 'logs'
        path_log = {'Root': root_log,
                    'System': f'{root_log}/system',
                    'Interactions': f'{root_log}/interactions'}

        root_locale = 'lang'
        path_locale = {'Root': root_locale,
                       'Russian': f'{root_locale}/ru',
                       'English': f'{root_locale}/en'}

        root_settings = 'settings'
        path_settings = {'Root': root_settings}

        self.PATH = {'Settings': path_settings,
                     'Logs': path_log,
                     'Locales': path_locale}
        print('< Local PATH >')
        print(self.PATH)

        self.markdown = None

    def set_markdown(self, markdown):
        self.markdown = markdown

    def deploy(self, forced=False):
        # Creating directories if not exist
        for section in self.PATH:
            for element in self.PATH.get(section):
                os.makedirs(self.PATH.get(section).get(element), exist_ok=True)

        # Checking 'Settings' block
        path_settings = self.PATH.get('Settings').get('Root')
        # Creating Access file with spaces for tokens
        path_access = path_settings + '/access.ini'
        if forced or os.path.exists(path_settings) and not os.path.exists(f'{path_settings}/access.ini'):
            with open(f'{path_access}', 'w') as f:
                f.write('[ TaskTrack Access File ]\n\n')
                f.write('[Access]\n')
                f.write('TelegramToken = \n')
                f.write('WitToken = \n')
            if self.markdown is not None:
                self.markdown.dump(f'Created an access file at \'{path_access}\'')

        # Creating localization templates
        for locale in self.PATH.get('Locales'):
            # Ignore the language root information
            if locale is 'Root':
                continue

            path_locales = self.PATH.get('Locales').get(locale)
            # Creating a file with spaces for user responses on buttons
            path_responses_user = path_locales + '/responses_user.loc'
            if forced or not os.path.exists(path_responses_user):
                with open(path_responses_user, 'w') as f:
                    f.write(f'[ TaskTrack Localization File ::: Locale < {locale} > ]\n')
                    f.write('[ Response Templates For Users ]\n\n')
                    f.write('[Hello]\n')

                    # Rewrite!!!
                    f.write('Answer01 = \n')
                    f.write('\n')

                    f.write('[AddTask]\n')
                    f.write('Answer01 = \n')
                    f.write('Answer02 = \n')
                    f.write('\n')
                if self.markdown is not None:
                    self.markdown.dump(f'Created a user responses file at \'{path_responses_user}\'')

            # Creating files with bot responses
            states = ['Generic', 'Hello', 'AddTask', 'DeleteTask']
            for state in states:
                path_responses_ai = f'{path_locales}/responses_ai_{state.casefold()}.loc'
                if forced or not os.path.exists(path_responses_ai):
                    with open(path_responses_ai, 'w') as f:
                        f.write(f'[ TaskTrack Localization File ::: Locale < {locale} > ]\n')
                        f.write('[ Response Templates For AI ]\n')
                        f.write('Hint: To add a new response, write it down and use a \'---\' splitter at the end.\n')
                        f.write('---\n')
                    if self.markdown is not None:
                        self.markdown.dump(f'Created a user responses file at \'{path_responses_ai}\'')

    def load_locales(self):
        self.markdown.dump('Loading localization files...')
        locales = {}
        for locale in self.PATH.get('Locales'):
            if locale == 'Root':
                self.markdown.dump('Root folder is \'{}\''.format(self.PATH.get('Locales').get('Root')))
                continue
            self.markdown.dump(f'Loading locale \'{locale}\'...')
            lang = localization.Language(self.PATH.get('Locales').get(locale))
            locales.update({locale: lang})
            self.markdown.dump(f'Locale \'{locale}\' loaded successfully')
        self.markdown.dump(f'Resulting dictionary: {locales}')
        return locales

    def pull(self, config_title, section, option):
        result = None
        try:
            config = configparser.ConfigParser()
            config.read('{path}/{title}'.format(path=self.PATH.get('Settings').get('Root'), title=config_title))
            result = config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            print('Error: Can\'t get a section [{0}] option [{1}] from file {2}'.format(section, option, config_title))
        return result
