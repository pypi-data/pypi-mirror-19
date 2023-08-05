# coding: utf-8

from pyicao9303.translate import decode

import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('string')
def utils(string):
    if string:
        print(decode(string))
