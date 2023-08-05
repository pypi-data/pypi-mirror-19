"""
A tool for managing ECS task definition files
including decryption via AWS KMS.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os

import boto3
import click

from ultra_config import UltraConfig
from ultra_config.extensions.aws import create_kms_decrypter, create_kms_encrypter, \
    load_task_definition_settings, dump_task_definition_settings


@click.group()
@click.argument('kms_key_alias')
@click.argument('task_definition')
@click.option('--container', type=int, default=0,
              help="The container index to update")
@click.pass_context
def config_setup(context, kms_key_alias, task_definition, container):
    """
    Helpful commands to read and write task definition files with
    KMS based encryption.
    """
    if not os.path.exists(task_definition):
        click.echo("Failed to find environment file {0}.  Please make sure it exists".format(task_definition))
        exit(1)
    with open(task_definition) as td:
        data = json.load(td)

    context.obj.task_definition = data
    context.obj.task_definition_file = task_definition
    kms_client = boto3.client('kms')
    encrypter = create_kms_encrypter(kms_client, kms_key_alias)
    decrypter = create_kms_decrypter(kms_client)
    loaders = [
        (load_task_definition_settings, [data], {'prefix': context.obj.config_prefix, 'container': container},)
    ]
    config = UltraConfig(loaders,
                         encrypter=encrypter,
                         decrypter=decrypter)

    config.load()
    config.decrypt()
    context.obj.config = config
    click.echo('Found task definition: {0}'.format(task_definition))


def _write_config(context):
    if context.obj.config.decrypted:
        context.obj.config.encrypt()
    task_definition_data = dump_task_definition_settings(
        context.obj.config, context.obj.task_definition, prefix=context.obj.config_prefix)
    with open(context.obj.task_definition_file, 'w') as outfile:
        outfile.write(task_definition_data)
    click.echo("Successfully updated configuration")


@config_setup.command('set-encrypted')
@click.option('-e', '--encrypt', nargs=2, multiple=True,
              help="A Key value pair.  The first should be"
                   " the key and the second the value to be encrypted")
@click.pass_context
def set_encrypted(context, encrypt):
    """
    Sets encrypted environment variable based
    settings in the task definition
    """
    config = context.obj.config
    for key, value in encrypt:
        config.set_encrypted(key, value)
    _write_config(context)


@config_setup.command('set')
@click.option('-v', '--value', nargs=2, multiple=True,
              help="A Key value pair.  The first is the key "
                   "and the second is the value")
@click.pass_context
def set_value(context, value):
    """
    Set a environment variable based setting in the task definition
    """
    for key, val in value:
        context.obj.config[key] = val
    _write_config(context)


@config_setup.command('read')
@click.pass_context
def read_task_definition(context):
    """
    Read the entirety of the decrypted task definition
    """
    task_definition = dump_task_definition_settings(
        context.obj.config, context.obj.task_definition, prefix=context.obj.config_prefix)
    click.echo(task_definition)


@config_setup.command('get')
@click.argument('config_value')
@click.pass_context
def get_config_value(context, config_value):
    """Get an individual config value"""
    try:
        click.echo(context.obj.config[config_value])
    except KeyError:
        click.echo("No configuration with key '{0}' found".format(config_value))


class _ContextObject(object):
    def __init__(self, config_prefix,
                 task_definition=None,
                 task_definition_file=None,
                 config=None):
        self.config_prefix = config_prefix
        self.task_definition = task_definition
        self.task_definition_file = task_definition_file
        self.config = config


def create_click_command(config_prefix):
    return config_setup(obj=_ContextObject(config_prefix))
