# -*- coding: utf-8 -*-

import click


all_colors = 'black', 'red', 'green', 'yellow', 'blue', 'magenta', \
             'cyan', 'white'


@click.command()
def main(args=None):
    for color in all_colors:
        click.echo(click.style('I am colored %s' % color, fg=color))
    for color in all_colors:
        click.echo(click.style('I am colored %s and bold' % color,
                               fg=color, bold=True))
    for color in all_colors:
        click.echo(click.style('I am reverse colored %s' % color, fg=color,
                               reverse=True))

    click.echo(click.style('I am blinking', blink=True))
    click.echo(click.style('I am underlined', underline=True))


if __name__ == "__main__":
    main()
