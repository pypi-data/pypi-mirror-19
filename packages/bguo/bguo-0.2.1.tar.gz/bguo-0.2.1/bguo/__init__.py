import horetu
from . import parse, dump

def main():
    horetu.cli({'import': parse.parse, 'export': dump.dump}, name='bguo')
