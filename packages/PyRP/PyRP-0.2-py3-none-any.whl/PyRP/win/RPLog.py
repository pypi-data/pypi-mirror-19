'''
A module that writes and reads log information for the RPWin module.
'''

from os.path import dirname, join, normpath, realpath
import pickle
from collections import UserDict
from datetime import datetime
from locale import setlocale, LC_ALL
from io import StringIO


class RPLog(UserDict):
    '''
    RPLog represent the information that is logged on file from the PyRP
    tie-break methods.  It also saves GUI information that is used to run the
    GUI application next time.
    '''
    #Default values
    DEFAULT = {
        'options': {
            'file_name': '', 'sort': True,
            'default_elo': 1400, 'headings': True},
        'algorithm': {
            'draw_character': 'x', 'epsilon': 1.0e-10,
            'iterations': 500, 'comma_separator': 'default',
            'output_mode': 'csv'},
        'methods': [{'method': 'ARPO', 'worst': 1, 'best':1}],
        'last_run': None,
        'log_info': None}
    _LOG_FILE = normpath(join(dirname(realpath(__file__)), 'rp.log'))
    
    def __init__(self, **kwargs):
        # Make sure that the default values are always saved
        self.data = {'options': {}, 'algorithm': {}, 'methods': []}
        for key in self.DEFAULT['options']:
            options = kwargs.get('options', {})
            self.data['options'][key] = options.get(
                key, self.DEFAULT['options'][key])
        for key in self.DEFAULT['algorithm']:
            algorithm = kwargs.get('algorithm', {})
            self.data['algorithm'][key] = algorithm.get(
                key, self.DEFAULT['algorithm'][key])
        self.data['methods'] = list(
            kwargs.get('methods', self.DEFAULT['methods']))
        self.data['last_run'] = kwargs.get('last_run', self.DEFAULT['last_run'])
        log_info = self.DEFAULT.get('log_info') or {}
        self.data['log_info'] = kwargs.get('log_info', log_info)

    @classmethod
    def load(cls):
        '''
        Unpickles the log data from a file and returns the corresponding
        RPLog object.
        '''
        try:
            with open(cls._LOG_FILE, 'rb') as log_file:
                return cls(**pickle.load(log_file))
        except (OSError, EOFError):
            return cls()

    @classmethod
    def save(cls, dct):
        '''
        Pickles a dictionary to a file.  Argument dct must be a dictionary
        with the same estructure as in RPLog.DEFAULT.
        '''
        try:
            with open(cls._LOG_FILE, 'wb') as log_file:
                # take only the keys that are relevant
                options = {
                    key: dct['options'].get(key, value)
                    for key, value in cls.DEFAULT['options'].items()}
                algorithm = {
                    key: dct['algorithm'].get(key, value)
                    for key, value in cls.DEFAULT['algorithm'].items()}
                pickle.dump(
                    {'options': options,
                     'algorithm': algorithm,
                     'methods': list(dct['methods']),
                     'last_run': datetime.now(),
                     'log_info': dict(dct['log_info'])},
                    log_file)
        except OSError:
            # Ignore, if file can't be saved
            pass

    def __str__(self):
        '''
        Prints the log info in human readable form.
        '''
        result = StringIO()
        line_break = '-'*60
        setlocale(LC_ALL, '')
        if self['last_run'] is None:
            date = 'unknown'
        else:
            date = self['last_run'].strftime('%c')
        result.write('{}\nLast run: {}'.format(line_break, date))
        result.write('\n{}\nMethods: {}'.format(
            line_break, len(self['methods'])))
        for method in self['methods']:
            result.write(
                '\n  Method: {method},  # Worst: {worst},  '
                '# Best: {best}'.format(**method))
        result.write('\n{}\nAlgorithm options:'.format(line_break))
        for key, value in self['algorithm'].items():
            result.write('\n  {}: {}'.format(self._to_sentence(key), value))
        result.write('\n{}\nOptions:'.format(line_break))
        for key, value in self['options'].items():
            result.write('\n  {}: {}'.format(self._to_sentence(key), value))
        result.write('\n{}\nMethod execution:'.format(line_break))
        for key, value in self['log_info'].items():
            result.write('\n  {}: {}'.format(
                self._to_sentence(key), self._to_list(value)))
        result.write('\n{}'.format(line_break))
        return result.getvalue()

    @staticmethod
    def _to_sentence(string):
        return string.replace('_', ' ').title()

    @staticmethod
    def _to_list(value):
        if not isinstance(value, set):
            return value
        elif not value:
            return 'none'
        else:
            result = '\n    '.join(item for item in value)
            return '\n    ' + result

###############################################################################
if __name__ == '__main__':
    log = RPLog.load()
    print(log)
