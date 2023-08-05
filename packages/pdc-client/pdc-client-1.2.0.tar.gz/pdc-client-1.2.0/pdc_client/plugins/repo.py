# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from __future__ import print_function

import json


from pdc_client.plugin_helpers import (PDCClientPlugin,
                                       extract_arguments,
                                       add_create_update_args)


class RepoPlugin(PDCClientPlugin):
    def register(self):
        self.set_command('content-delivery-repo')

        list_parser = self.add_action('list', help='list all content delivery repos')
        filters = ('arch', 'content-category', 'content-format', 'name', 'release-id',
                   'repo-family', 'service', 'shadow', 'variant-uid', 'product-id')
        for arg in filters:
            list_parser.add_argument('--' + arg, dest='filter_' + arg.replace('-', '_'))
        list_parser.set_defaults(func=self.repo_list)

        info_parser = self.add_action('info', help='display details of an content delivery repo')
        info_parser.add_argument('repoid', metavar='ID')
        info_parser.set_defaults(func=self.repo_info)

        create_parser = self.add_action('create', help='create a new content delivery repo')
        self.add_repo_arguments(create_parser, required=True)
        create_parser.set_defaults(func=self.repo_create)

        clone_parser = self.add_action('clone', help='clone repos from one release to another',
                                       description='The include-* options are used to filter '
                                                   'which releases should be cloned. If any are '
                                                   'omitted, all values for that attribute will '
                                                   'be cloned.')
        self.add_clone_arguments(clone_parser)
        clone_parser.set_defaults(func=self.repo_clone)

        update_parser = self.add_action('update', help='update an existing content delivery repo')
        update_parser.add_argument('repoid', metavar='ID')
        self.add_repo_arguments(update_parser)
        update_parser.set_defaults(func=self.repo_update)

        delete_parser = self.add_action('delete', help='delete an existing content delivery repo')
        delete_parser.add_argument('repoid', metavar='ID')
        delete_parser.set_defaults(func=self.repo_delete)

    def add_repo_arguments(self, parser, required=False):
        required_args = {
            'arch': {},
            'content_category': {},
            'content_format': {},
            'name': {},
            'release_id': {},
            'repo_family': {},
            'service': {},
            'variant_uid': {}
        }
        optional_args = {'product_id': {'type': int},
                         'shadow': {'help': 'default is false when create a content delivery repo',
                                    'metavar': 'SHADOW_FLAG'}}

        add_create_update_args(parser, required_args, optional_args, required)

    def add_clone_arguments(self, parser):
        necessary_args = {
            'release_id_from': {'metavar': 'RELEASE_ID_FROM'},
            'release_id_to': {'metavar': 'RELEASE_ID_TO'},
        }
        optional_args = {
            'include_service': {'nargs': '*', 'metavar': 'SERVICE'},
            'include_repo_family': {'nargs': '*', 'metavar': 'REPO_FAMILY'},
            'include_content_format': {'nargs': '*', 'metavar': 'CONTENT_FORMAT'},
            'include_content_category': {'nargs': '*', 'metavar': 'CONTENT_CATEGORY'},
        }
        add_create_update_args(parser, necessary_args, optional_args, True)

        shadow_group = parser.add_mutually_exclusive_group()
        shadow_group.add_argument('--include-shadow', action='store_true')
        shadow_group.add_argument('--exclude-shadow', action='store_false', dest='include_shadow')

        optional_args = {
            'include_product_id': {'metavar': 'PRODUCT_ID', 'type': int},
        }
        add_create_update_args(parser, {}, optional_args, False)

    def repo_list(self, args, data=None):
        filters = extract_arguments(args, prefix='filter_')
        if not filters and not data:
            self.subparsers.choices.get('list').error('At least some filter must be used.')
        repos = data or self.client.get_paged(self.client['content-delivery-repos']._, **filters)
        if args.json:
            print(json.dumps(list(repos)))
            return

        start_line = True
        for repo in repos:
            if start_line:
                start_line = False
                print('{0:<10} {1:120} {2:20} {3}'.format('ID', 'Name', 'Content Format', 'Content Category'))
                print()
            print('{id:<10} {name:120} {content_format:20} {content_category}'.format(**repo))

    def repo_info(self, args, repo_id=None):
        response = self.client['content-delivery-repos'][repo_id or args.repoid]._()
        if args.json:
            print(json.dumps(response))
            return
        fmt = '{0:20} {1}'
        print(fmt.format('ID', response['id']))
        print(fmt.format('Name', response['name']))
        print(fmt.format('Content Format', response['content_format']))
        print(fmt.format('Content Category', response['content_category']))
        print(fmt.format('Release ID', response['release_id']))
        print(fmt.format('Arch', response['arch']))
        print(fmt.format('Repo Family', response['repo_family']))
        print(fmt.format('Service', response['service']))
        print(fmt.format('Variant UID', response['variant_uid']))
        print(fmt.format('Shadow', response['shadow']))
        print(fmt.format('Product ID', response['product_id'] or ''))

    def repo_create(self, args):
        data = extract_arguments(args)
        self.logger.debug('Creating content delivery repo with data %r', data)
        response = self.client['content-delivery-repos']._(data)
        self.repo_info(args, response['id'])

    def repo_clone(self, args):
        data = extract_arguments(args)
        self.logger.debug('Clone repos with data {0}'.format(data))
        response = self.client.rpc['content-delivery-repos'].clone._(data)
        self.repo_list(args, response)

    def repo_update(self, args):
        data = extract_arguments(args)
        if data:
            self.logger.debug('Updating ontent delivery repo %s with data %r', args.repoid, data)
            self.client['content-delivery-repos'][args.repoid]._ += data
        else:
            self.logger.debug('Empty data, skipping request')
        self.repo_info(args)

    def repo_delete(self, args):
        data = extract_arguments(args)
        self.logger.debug('Deleting content delivery repo: %s', args.repoid)
        self.client['content-delivery-repos'][args.repoid]._("DELETE", data)


PLUGIN_CLASSES = [RepoPlugin]
