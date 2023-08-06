# -*- coding: utf-8 -*-
'''
Created on 2017-01-11

@author: hustcc
'''

import click
import provider_win


@click.command()
@click.option('-p', '--platform', default='win',
              type=click.Choice(['win', 'ios']),
              help='The platform of device. Default: win')
def provider_entry(platform):
    if platform == 'win':
        click.echo('start to %s provider...' % platform)
        provider_win.main()
    else:
        click.echo('platform is not valid...')


def run():
    provider_entry()


if __name__ == '__main__':
    run()
