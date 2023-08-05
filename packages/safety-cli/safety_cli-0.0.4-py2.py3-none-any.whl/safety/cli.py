# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import click
from safety import __version__
from safety import safety
from safety.formatter import report
from safety.parser import parse
from safety import errors
from requests.exceptions import ConnectionError


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.option("--full-report/--short-report", default=False)
@click.option("--key", required=True)
@click.option("files", "--file", "-f", multiple=True, type=click.File())
def check(full_report, files, key):

    try:
        packages = []
        for f in files:
            for pkg in parse(f):
                packages.append(pkg)
        vulns = safety.check(packages=packages, key=key)
        click.secho(report(vulns=vulns, full=full_report))
        sys.exit(-1 if vulns else 0)
    except errors.ImproperlyConfigured as e:
        click.secho(e.__str__(), fg="red")
    except errors.LicenseKeyError as e:
        click.secho('Your license key {key} is no longer valid. Please visit https://safetydb.io '
                    'to get a new license key.'.format(key=key), fg='red')
    except errors.ServerError as e:
        click.secho('There was an error processing your request: {}'.format(e), fg='red')
    except ConnectionError as e:
        click.secho('There was an error connecting to the server.', fg='red')
    sys.exit(-1)

if __name__ == "__main__":
    cli()
