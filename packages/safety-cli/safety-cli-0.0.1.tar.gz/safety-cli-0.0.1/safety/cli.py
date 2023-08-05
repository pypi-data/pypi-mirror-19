# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import click
from safety import __version__
from safety import safety
from safety.formatter import report
from safety.parser import parse


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.option("--full-report/--short-report", default=False)
@click.option("--key")
@click.option("files", "--file", "-f", multiple=True, type=click.File())
def check(full_report, files, key):

    packages = []
    for f in files:
        for pkg in parse(f):
            packages.append(pkg)

    vulns = safety.check(packages=packages, key=key)
    click.secho(report(vulns=vulns, full=full_report))
    sys.exit(-1 if vulns else 0)


if __name__ == "__main__":
    cli()
