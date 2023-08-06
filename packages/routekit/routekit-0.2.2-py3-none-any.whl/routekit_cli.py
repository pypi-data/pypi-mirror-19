import consul
import click
import os
import platform

from colorama import Fore, Style

if platform.system() != 'Linux':
    click.secho('Sorry, routekit is Linux (netlink/iproute) only. :(', fg='red', err=True)
    exit(1)

from pyroute2 import iproute

import routekit
from routekit.helpers import *

rkconfig = routekit.config.RKConfig()
ipr = iproute.IPRoute()
cons = consul.Consul()
cfg = {}


@click.group()
@click.option('--debug/--no-debug', default=False, help='Enable debug mode for this invocation')
@click.option('-c', '--config', default='routekit.yml', help='The routekit config file')
@click.option('-d', '--directory', envvar='ROUTEKIT_CONF_DIR', help='Directory to search the config (-c) in')
def cli(debug, config, directory):
    """
    Welcome to RouteKit!

    This tool is made up of multiple modules.
    Please read the documentation below to get started.
    """

    global cfg

    rkconfig.debug = debug

    if directory is not None:
        config_paths = directory
    else:
        config_paths = os.curdir, \
                       os.path.expanduser("~/.config/routekit/"), \
                       "/etc/routekit/"

    # Configure RouteKit with the first found config in `config_paths`
    cfg, selected_config = routekit.config.first_found_config(config_paths, config)

    if cfg and selected_config:
        click_green('Using configuration at {}'.format(selected_config))
    elif cfg is None and selected_config:
        click_error('Found empty or invalid configuration at {}'.format(selected_config))
    elif cfg is None and selected_config is None:
        click_error('No {} found in any of the following paths: {}'.format(config, str(config_paths)))


@cli.group()
@click.pass_context
def routes(ctx):
    """Routing table manipulation"""

    # Set up RKConfig object with route configuration from disk
    try:
        rkconfig.tables = routekit.config.read_config_routes(cons, cfg)

        if rkconfig.debug:
            click_print(str(rkconfig))
            click_print('Learned the following table names from rt_tables(.d): {}'.format(routekit.router.rt_tables))

    except routekit.router.ConfigException as e:
        click_yellow('Warning: {}'.format(str(e)))
    except routekit.router.RouterException as e:
        click_error('Error parsing configuration: {}, exiting.'.format(str(e)))
        ctx.exit(code=1)


@cli.group()
def qos():
    """QoS policy management"""

    # TODO: Setup RKConfig with tc configuration from disk


@routes.group()
def list():
    """List routes available for manipulation"""


@list.command()
def system():
    """List routes active in the system"""
    if routekit.helpers.print_routes(routekit.config.read_system_routes(ipr)) is False:
        click_error('No routes found on the system.')


@list.command()
def configuration():
    """List routes specified in the configuration"""
    if routekit.helpers.print_routes(rkconfig.tables) is False:
        click_error('No routes found in configuration.')


@list.command()
def delta():
    """Show system <> config route delta"""
    deploy, delete = routekit.router.core.route_delta(routekit.config.read_system_routes(ipr), rkconfig.tables)

    click_bold('[ Route Delta ]')

    if len(deploy) == len(delete) is 0:
        click_dim('No differences detected')

    for ra in deploy:
        click_green("+ {}".format(ra))

    for ra in delete:
        click_red("- {}".format(ra))


@routes.command()
@click.option('--diff', is_flag=True, default=False, help='Display routing delta')
@click.pass_context
def apply(ctx, diff):
    """
    Apply config routes onto the system
    """

    # Re-use delta visualization call
    if diff:
        ctx.invoke(delta)

    click_bold('[ Apply Route Delta ]')

    deploy, delete = routekit.router.core.route_delta(routekit.config.read_system_routes(ipr), rkconfig.tables)

    # Quit the program if there is no work
    if len(deploy) == len(delete) is 0:
        click_dim('No differences detected, exiting.')
        ctx.exit()

    try:
        if routekit.config.apply_routes(ipr, deploy, delete) is True:
            click_green('Route application successful!')
        else:
            click_error('Error applying routes to the system')
    except Exception as e:
        click_error('Encountered unhandled exception while applying routes:')
        click_error(str(e))


if __name__ == '__main__':
    cli()
