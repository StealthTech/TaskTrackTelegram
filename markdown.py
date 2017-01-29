import logging
import os


class Markdown:
    def __init__(self, path, title):
        self.path = '{path}/{title}.log'.format(path=path, title=title)
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write('[ Markdown Log File <{}> ]\n\n'.format(title))
        logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                            filename=self.path)

    @staticmethod
    def dump(message):
        logging.info(message)
        print('Markdown > {}'.format(message))
