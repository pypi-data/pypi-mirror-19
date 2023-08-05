'''
PyRP is a package that provides functionallity to calculate the ARPO
tie-breaking methods for Swiss tournaments.
Use PyRP.RP for calculating ARPO tie-breaking methods and displaying them in a
csv file or standard output.
Use PyRP.RPxlsx to display these results in xlsx format.
'''

from .RP import Tournament, TournamentError
