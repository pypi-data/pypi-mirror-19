#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import print_function

import logging
import time

from . import astutils
from . import filters
from . import pattern

CLEAR = "\x1b[0m"
GREEN = "\x1b[1;32m"
YELLOW = "\x1b[1;33m"

LOG = logging.getLogger(__name__)


def _print(colour, text):
    print("{}{}{}".format(colour, text, CLEAR))


def display_result(filter_, file_path, node):
    source = filter_.get_source(file_path, node)
    print("{}{}{}:{}".format(YELLOW, node.lineno, CLEAR, source))


def print_file_path(file_path, first):
    if not first:
        print()
    _print(GREEN, file_path)


def search(args):

    start = time.time()

    ignore_dirs = [pattern.compile(i_d) for i_d in args.ignore_dir]
    ast_walker = astutils.ASTWalker(args.paths, ignore_dirs)
    files_with_matches = set()
    activated_filters = filters.get_active_filters(args)

    if len(activated_filters) == 0:
        LOG.info("No filters were provided. Using all filters")
        activated_filters = filters.get_all_filters()

    pat = pattern.matcher(args)

    node_count = 0

    for file_count, (file_path, nodes) in enumerate(ast_walker.walk()):
        for file_node_count, node in enumerate(nodes):
            for f in activated_filters:
                if f.match(node, pat):
                    if file_path not in files_with_matches:
                        files_with_matches.add(file_path)
                        if args.files_with_matches:
                            print(file_path)
                        else:
                            first = len(files_with_matches) == 1
                            print_file_path(file_path, first=first)

                    if not args.files_with_matches:
                        display_result(f, file_path, node)
        node_count += file_node_count

    if args.show_stats:
        seconds = round(time.time() - start, 2)
        print("**STATS**")
        print("Ran for {} seconds".format(seconds))
        print("Parsed {} Python files ({}/s)".format(
              file_count, round(file_count / seconds, 2)))
        print("Visited {} AST nodes ({}/s)".format(
              node_count, round(node_count / seconds, 2)))
        print("Ran {} regular expression matches ({}/s)".format(
              pat.count, round(pat.count / seconds, 2)))
