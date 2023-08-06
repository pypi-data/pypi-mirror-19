from signal import signal, SIGPIPE, SIG_DFL
import logging

import click
from prody import confProDy, LOGGER

from . import pass_context, make_cli_class
from ..version import version

from .util import config


def make_subcommand(package):
    @click.command(package, cls=make_cli_class(package))
    @pass_context
    def cli(ctx):
        pass
    return cli


@click.group('sblu')
@click.option('-v', '--verbose', count=True)
@click.version_option(version=version)
@pass_context
def cli(ctx, verbose):
    signal(SIGPIPE, SIG_DFL)

    ctx.verbosity = verbose
    level = logging.ERROR
    if verbose >= 1:
        level = logging.WARNING
    if verbose >= 2:
        level = logging.INFO
    if verbose >= 3:
        level = logging.DEBUG

    logging.basicConfig(level=level)
    LOGGER._setverbosity(confProDy('verbosity'))


for subcommand in ('pdb', 'docking', 'measure', 'cluspro'):
    sub_cli = make_subcommand(subcommand)
    cli.add_command(sub_cli)

cli.add_command(config)
