'''
_PyRP implements the common methods for PyRP and NumPyRP.
'''

import sys
from itertools import dropwhile
from functools import partial
from collections import namedtuple
from contextlib import contextmanager
from math import sqrt
import csv
import locale

# Use locale settings for decimal separator
locale.setlocale(locale.LC_ALL, '')


# A named tuple that saves the information of the first line of a Swiss
# Manager file
_FirstLine = namedtuple(
    '_FirstLine',
    ['file_iter', 'index_name', 'index_elo', 'index_points', 'index_rounds'])
# A named tuple for players that did not play many rounds
_FewRounds = namedtuple('_FewRounds', ['did_not_play', 'less_than_half'])


@contextmanager
def _open_file(output_file):
    ''' Opens a file for writing or gives stdout. '''
    if output_file is None:
        file = sys.stdout
    else:
        file = open(output_file, mode='w', newline='')
    yield file
    if output_file is not None:
        file.close()


class _Tournament:
    # Character used for drawn matches
    _DRAW = 'x'
    # Minimum Elo
    _MINIMUM_ELO = 1400
    # Default value for epsilon test
    _EPSILON = 1.e-10
    # Default value for the maximum number of iterations
    _MAX_ITERATIONS = 500
    # Approximately -400*log10(1/percentage-1)
    _performance_table = [
        -800, -677, -589, -538, -501, -470, -444, -422, -401, -383,
        -366, -351, -336, -322, -309, -296, -284, -273, -262, -251,
        -240, -230, -220, -211, -202, -193, -184, -175, -166, -158,
        -149, -141, -133, -125, -117, -110, -102, -95, -87, -80, -72,
        -65, -57, -50, -43, -36, -29, -21, -14, -7, 0, 7, 14, 21, 29,
        36, 43, 50, 57, 65, 72, 80, 87, 95, 102, 110, 117, 125, 133,
        141, 149, 158, 166, 175, 184, 193, 202, 211, 220, 230, 240,
        251, 262, 273, 284, 296, 309, 322, 336, 351, 366, 383, 401,
        422, 444, 470, 501, 538, 589, 677, 800]
    # Common string for file errors
    _FILE_ERROR = (
        'Error writing file {}\n'
        'Make sure that the file is not being used by another application')

    def __init__(self, *args, **kwargs):
        raise TournamentError(
            'Direct creation of instances is not allowed. Use Tournament.load.')

    @classmethod
    def load(
        cls, file_name, elo_default=_MINIMUM_ELO, draw_character=_DRAW,
        epsilon=_EPSILON, max_iterations=_MAX_ITERATIONS):
        '''
        Tournament.load(file_name) returns a Tournament object loaded from
        a Swiss Manager file called file_name.
        The optional arguments epsilon and max_iterations can be given to
        determine stopping conditions of the recursive algorithms.
        '''
        # Initialize private variables
        t = cls.__new__(cls)
        t.log_info = {}
        t._recursive_performances = None
        t._recursive_bucholzs = None
        t._epsilon = float(epsilon)
        t._max_iterations = int(max_iterations)
        # Load information from the file
        try:
            t._import_swiss_manager(file_name, elo_default, draw_character)
        except Exception as error:
            text = '{} could not be processed.'.format(file_name)
            raise TournamentError(text) from error
        else:
            # Get some log information
            log = t.log_info
            log['Did not play'], log['Less than half'] = t._read_log()
            return t

    def run(
        self, methods_list, output_file=None, sort_by=None,
        reverse_order=True, heading=True, comma_separator='default'):
        '''
        Tournament.run(
            [{'method' : 'method name 1'},...], output_file, 
            sort_by = [{'method' : 'method name i'},...], reverse_order = True)
        prints to output_file the results of the various methods given as a
        dictionary.
        If sort_by is given the output is sorted according to the methods given.
        Possible methods are:
        'Names': names of the players.
        'Elos': Elo of each player as obtained from the input.
        'Points': number of points of a player as obtained from the input.
        'Played points': points obtained by each player in actual matches.
        'Bucholz': Bucholz of each player.
        'Average Bucholz': Bucholz divided by the number of opponents.
        'Performance': performance of the players using FIDE's table.
        'Recursive Performance' or 'RP': gives an approximation of the
            recursive performance of a player.
        'Average Recursive Performance of Opponents' or 'ARPO': calculates the
            average recursive performance of the opponents of each player.
        'Recursive Bucholz' or 'RB': gives an approximation of the
            recursive Bucholz of a player.
        'Average Recursive Bucholz of Opponents' or 'ARBO': calculates the
            average recursive Bucholz of the opponents of each player.

        The modifications 'Worst' and 'Best' can be given to 'ARPO' and 'ARBO'
        to remove a number of worst or best opponents of a player.
        '''
        # Comma separators
        if comma_separator == 'default':
            decimal = locale.localeconv()['decimal_point']
            comma_separator = ';' if decimal==',' else ','
        try:
            with _open_file(output_file) as file:
                csv_file = csv.writer(file, delimiter=comma_separator)
                self._put_results(
                    csv_file, methods_list, sort_by, reverse_order, heading)
        except OSError as error:
            text = self._FILE_ERROR.format(str(output_file))
            raise TournamentError(text) from error

    def results_list(self, methods_list, sort_by=None, reverse_order=True):
        '''
        tournament.results_list(
            [{'method' : 'method name 1'},...],
            sort_by = [{'method' : 'method name i'},...], reverse_order = True)
        returns a list of the results obtained by the various methods given.
        See the Tournament.run method for information on the possible
        tie-breaks.
        '''
        try:
            # Create the list with the information
            info = list(zip(*(
                self._select_method(**method) for method in methods_list)))
            # Sort the results
            if sort_by:
                sort_indices=[methods_list.index(each) for each in sort_by]
                info.sort(
                    key=lambda lst: tuple(self._extract(lst, sort_indices)),
                    reverse=reverse_order)
            # Finally add the players that did not play any round
            info.extend(
                self._did_not_play_methods(each, methods_list)
                for each in self._did_not_play)
            return info
        except KeyError as error:
            raise TournamentError('Invalid method.') from error
        except TypeError as error:
            text = 'Method list\n{}\nis not valid.'.format(methods_list)
            raise TournamentError(text) from error
        except ValueError as error:
            text = 'Invalid sorting method'.format(error)
            raise TournamentError(text) from error

    def _read_first_line(self, file, convert=False):
        # Determine if we use str ot bytes
        if convert:
            type1 = partial(bytes, encoding='utf-8')
            type2 = partial(str, encoding='utf-8')
        else:
            type1, type2 = str, str
            
        file_iter = dropwhile(lambda line: type1('1.Rd.') not in line, file)
        try:
            # The first line is the heading line
            line = next(file_iter)
        except StopIteration:
            text = '{} is not a correct Swiss Manager file.'.format(file_name)
            raise TournamentError(text)
        
        # Determine the position of the information needed         
        fields = type2(line).strip().split(';')
        index_name = fields.index('Name')
        index_elo = fields.index('Rtg')
        index_points = fields.index('Pts')
        index_rounds = [
            i for i, field in enumerate(fields) if field.endswith('.Rd.')]
        return _FirstLine(
            file_iter, index_name, index_elo, index_points, index_rounds)

    @staticmethod
    def _calculate_elo(elo, elo_default):
        # Calculate the Elo from Swiss Manager
        return float(elo_default if not elo or int(elo)==0 else elo)
        
    @staticmethod
    def _calculate_points(value, draw_character):
        return float(value.replace(draw_character, '.5'))

    @classmethod
    def _calculate_played_points(cls, line, index_rounds, draw_character):
        # Calculate played points of a player from Swiss Manager
        return sum(
            cls._player_played_points(line, index, draw_character)
            for index in index_rounds)

    @staticmethod
    def _player_played_points(line, index, draw_character):
        return (
            float(line[index+2].replace(draw_character, '.5'))
            if line[index+1]=='w' or line[index+1]=='b' else 0.0)

    @staticmethod
    def _calculate_opponents(line, index_rounds):
        return [
            int(line[index])-1 for index in index_rounds if line[index+1]!='-']

    def _put_results(self, file, methods_list, sort_by, reverse_order, heading):
        info = self.results_list(methods_list, sort_by, reverse_order)
        if heading:
            titles = [self._str_heading(**method) for method in methods_list]
            file.writerow(titles)
        to_string = self._to_string
        for line in info:
            info = tuple(to_string(field) for field in line)
            file.writerow(info)

    @staticmethod
    def _to_string(expr):
        # Convert data applying locale characteristics
        return locale.str(expr) if isinstance(expr, float) else str(expr)

    @classmethod
    def _str_heading(cls, *, method='Name', worst=0, best=0):
        # Print headings using the methods dictionary
        if method in (
            'ARPO', 'ARBO', 'Average Recursive Performance of Opponents', 
            'Average Recursive Bucholz of Opponents'):
            return '{}({}-{})'.format(method, worst, best)
        else:
            return method

    def _did_not_play_methods(self, name, methods_list):
        # Just return empty information except for the name
        return tuple(
            name if method['method']=='Names' else '' for method in methods_list)

    def __getattr__(self, attrname):
        return lambda *args, **kwargs: getattr(self, '_{}'.format(attrname))

    def _select_method(self, method='Name', **kwargs):
        try:
            attr = method.lower().replace(' ', '_')
            yield from getattr(self, attr)(**kwargs)
        except AttributeError:
            text = 'String {} is not a valid method.'.format(method)
            raise TournamentError(text)

    def _write_log_info(self, method_name, iterations, difference, sqrt=sqrt):
        # Writes log information about the convergence of the method
        log = self.log_info
        log['{} iterations'.format(method_name)] = iterations
        log['{} epsilon'.format(method_name)] = sqrt(difference)

    @staticmethod        
    def _extract(target_list, indices):
        # Auxiliary function for extracting parts of lists
        return (target_list[each_index] for each_index in indices)

    def recursive_performance(self, **kwargs):
        ''' Calculates the Recursive Performance tie-breaking rule.'''
        if self._recursive_performances is None:
            self._recursive_performances = self._recursive_method(
                'RP', self._rp_coefficient(), self._elos)
        return self._recursive_performances
    rp = recursive_performance

    def arpo(self, worst=0, best=0, **kwargs):
        ''' Calculates the average recursive performance of the opponents.'''
        rp = self.recursive_performance()
        return self._rivals_average(rp, worst=worst, best=best)
    average_recursive_performance_of_opponents = arpo
        
    def recursive_bucholz(self, **kwargs):
        ''' Calculates the Recursive Bucholz tie-breaking rule.'''
        if self._recursive_bucholzs is None:
            # First iteration is vector of points rescaled
            # to the number of rounds
            b0 = self._rb_first()
            self._recursive_bucholzs = self._recursive_method(
                'RB', self._rb_coefficient(), b0)
        return self._recursive_bucholzs
    rb = recursive_bucholz

    def arbo(
        self, epsilon=_EPSILON, max_iterations=_MAX_ITERATIONS,
        worst=0, best=0, **kwargs):
        ''' Calculates the average recursive Bucholz of the opponents.'''
        rb = self._recursive_bucholz()
        return self._rivals_average(rb, worst=worst, best=best)
    average_recursive_bucholz_of_opponents = arbo


class TournamentError(Exception):
    '''
    A class that captures the errors produced by the Tournament class.
    '''
    def __init__(self, info):
        self.info = info

