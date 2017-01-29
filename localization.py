import random
import configparser


class Language:
    def __init__(self, path):
        self.localization_path = path

        config = configparser.ConfigParser()
        config.read(self.localization_path + '/responses_user.loc')
        self.user_responses = {}
        user_response_hello = {'Answer01': config.get('Hello', 'Answer01')}
        user_response_add_task = {'Answer01': config.get('AddTask', 'Answer01'),
                                  'Answer02': config.get('AddTask', 'Answer02')}

        self.user_responses.update({'Hello': user_response_hello,
                                    'AddTask': user_response_add_task})

    def roll_bot_response(self, section):
        section = section.casefold()
        path = self.localization_path

        with open(f'{path}/responses_ai_{section}.loc', 'r') as f:
            # Should add a trim for \n symbols
            responses = f.read().split('---\n')[1:]

        random_index = random.randint(0, len(responses) - 1)
        return responses[random_index]

    def get_user_responses(self, section):
        return self.user_responses.get(section)