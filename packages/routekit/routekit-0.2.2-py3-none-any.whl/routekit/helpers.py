import sys
import click
from colorama import Fore, Style


def click_print(string):
  """
  Helper to print normal text to stdout.
  """
  click.secho(string)


def click_bold(string):
  """
  Helper to print bold (bright) text to stdout.
  """
  click.secho(string, bold=True)


def click_dim(string):
  """
  Helper to print dim text to stdout.
  """
  click.secho(string, dim=True)


def click_error(string):
  """
  Helper to print to stderr with red foreground.
  """
  click.secho(string, fg='red', bold=True, err=True)


def click_red(string):
  """
  Helper to print to stdout with red foreground.
  """
  click.secho(string, fg='red')


def click_yellow(string):
  """
  Helper to print to stdout with yellow foreground.
  """
  click.secho(string, fg='yellow')


def click_green(string):
  """
  Helper to print to stdout with green foreground.
  """
  click.secho(string, fg='green')


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def print_routes(tables):

    try:
        for k, t in tables.items():
            print(t)
            for r in t.routes:
                print("\t{}".format(r))
    except AttributeError:
        print('Error printing Tables: argument is not a valid dict of Tables')
        return False
