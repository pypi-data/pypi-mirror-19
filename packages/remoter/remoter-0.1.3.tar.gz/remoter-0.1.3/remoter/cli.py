#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: http://stackoverflow.com/questions/32501538/save-a-command-line-options-value-in-an-object-with-pythons-click-library

import click

from .config import Config


@click.group()
def tasks():
    '''Manage tasks defined in config'''


@click.command('run')
@click.pass_context
def tasks_run(ctx):
    '''Run a series of tasks defined in config'''
    conf = Config(ctx.obj['file'])
    out = conf.run()
    click.echo(out)

tasks.add_command(tasks_run)


@click.group()
@click.option('--file', default='remoter.yml', help='Specify an alternate config file (default: remoter.yml)')
@click.pass_context
def main(ctx, file):
    '''Python 3 compatible remote task runner'''
    ctx.obj = dict({'file': file})

main.add_command(tasks)


if __name__ == "__main__":
    main()
