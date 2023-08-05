'''
PyRP is a module that implements various tie-breaking rules for
Swiss tournaments including Recursive Performance and Recursive Bucholz.
The class Tournament encapsulates the funtionality to calculate the
tie-breaking rules and to import from Swiss Manager outputs.
'''

import sys
from itertools import dropwhile, compress

if not __package__:
    from _RP import _Tournament, TournamentError, _FewRounds
else:
    from ._RP import _Tournament, TournamentError, _FewRounds


class Tournament(_Tournament):
    '''
    Defines a class that holds the data of a Swiss tournament and gives
    functionality to calculate some tie-breaking rules and print the
    results to a file. The objects are instantiated through the method
    Tournament.load.
    '''
    def _import_swiss_manager(self, file_name, elo_default, draw_character):
        with open(file_name) as file:
            file_iter, index_name, index_elo, index_points, index_rounds =\
                self._read_first_line(file)

            # Initialize lists
            self._number_of_rounds = len(index_rounds)
            self._names = []
            self._opponents = []
            self._number_of_opponents = []
            self._elos = []
            self._points = []
            self._played_points = []
            self._did_not_play = []

            # Iterate over the file and fill in information
            for line in file_iter:
                fields = line.split(';')
                opps = self._calculate_opponents(fields, index_rounds)
                if opps:
                    # Save only the relevant players
                    self._names.append(fields[index_name])
                    self._opponents.append(opps)
                    self._number_of_opponents.append(len(opps))
                    elo = self._calculate_elo(fields[index_elo], elo_default)
                    self._elos.append(elo)
                    points = self._calculate_points(
                        fields[index_points], draw_character)
                    self._points.append(points)
                    played_points = self._calculate_played_points(
                        fields, index_rounds, draw_character)
                    self._played_points.append(played_points)
                else:
                    self._did_not_play.append(fields[index_name])

    def _read_log(self):
        less_than_half = {
            name for name, number in zip(self._names, self._number_of_opponents)
            if number < self._number_of_rounds/2} - set(self._did_not_play)
        return _FewRounds(set(self._did_not_play), less_than_half)

    ################### Tie-breaking rules ####################
    def bucholz(self, **kwargs):
        ''' Calculates the Bucholz tie-breaking rule.'''
        return (
            sum(self._extract(self._points, opp)) for opp in self._opponents)

    def average_bucholz(self, **kwargs):
        ''' Calculates the average score of the opponents.'''
        return (
            sum(self._extract(self._points, opps))/num
            for num, opps in zip(self._number_of_opponents, self._opponents))

    def performance(self, **kwargs):
        ''' Calculates the performance of the players.'''
        average_elos = (
            sum(self._extract(self._elos, opps))/num
            for num, opps in zip(self._number_of_opponents, self._opponents))
        points_num = zip(self._played_points, self._number_of_opponents)
        factors = (
            self._performance_table[int(100*points/num + 0.5)]
            for points, num in points_num)
        elos_factors = zip(average_elos, factors)
        return (elos + factor for elos, factor in elos_factors)
  
    def _rp_coefficient(self):
        # Recursive Performance coefficient
        points_num = zip(self._played_points, self._number_of_opponents)
        c = [
            self._performance_table[int(100*points/num + 0.5)]
            for points, num in points_num]
        num_opps = sum(self._number_of_opponents)
        c_num = zip(c, self._number_of_opponents)
        inflation = (sum(ci*num for ci, num in c_num)/num_opps)
        return [ci - inflation for ci in c]

    def _rb_coefficient(self):
        # Recursive Bucholz coefficient
        points_num = zip(self._played_points, self._number_of_opponents)
        return [points/num - 0.5 for points, num in points_num]

    def _rb_first(self):
        # Return the first iterand for the recursive Bucholz
        points_num = zip(self._played_points, self._number_of_opponents)
        rounds = self._number_of_rounds
        return [rounds*points/num for points, num in points_num]

    def _recursive_method(self, method_name, c, p0):
        epsilon, max_iterations = self._epsilon, self._max_iterations
        # Iterative process
        for k in range(max_iterations):
            # Next iteration
            c_opps_num = zip(c, self._opponents, self._number_of_opponents)
            p = [
                sum(self._extract(p0, opps))/num + ci
                for ci, opps, num in c_opps_num]
            # Epsilon test
            num_p0_p = zip(self._number_of_opponents, p0, p)
            difference = sum(num * (pi-p0i)**2 for num, p0i, pi in num_p0_p)
            if difference < epsilon*epsilon:
                self._write_log_info(method_name, k, difference)
                return p
            else:
                # Update iterand and continue
                p0 = p
        else:
            # The method did not converge
            self._write_log_info(method_name, max_iterations, difference)
            text = 'The {} method did not converge'.format(method_name)
            raise TournamentError(text)

    def _rivals_average(self, strengths, worst=0, best=0):
        # Average strength of the opponents removing best and worst opponents
        return (
            self._rivals_average_each(strengths, opps, worst, best)
            for opps in self._opponents)

    def _rivals_average_each(self, strengths, opponents, worst, best):
        # Sort opponents strengths and take out worst and best opponents
        strengths = sorted(self._extract(strengths, opponents), reverse=True)
        rivals_strengths = strengths[best:self._number_of_rounds - worst]
        return (
            sum(rivals_strengths)/len(rivals_strengths)
            if rivals_strengths else float('nan'))
                   

###############################################################################
if __name__ == '__main__':
    from os.path import join
    t = Tournament.load(join('..', 'test', 'testing.txt'))
    t.run(
        methods_list=(
            {'method': 'Names'}, {'method': 'Points'},
            {'method': 'Elos'}, {'method': 'Average Bucholz'},
            {'method': 'Performance'}, {'method': 'RB'}, {'method': 'RP'},
            {'method': 'ARPO', 'worst': 1},
            {'method': 'ARPO', 'worst': 2},
            {'method': 'ARPO', 'worst': 1, 'best': 1}),
        #output_file=r'results.csv',
        sort_by=(
            {'method': 'Points'},
            {'method': 'ARPO', 'worst': 1, 'best': 1}))
