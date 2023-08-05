# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import copy
from sys import exit

from ..concurrency import WorkerPool
from ..plugins import PluginManager
from ..repo import Repository
from ..utils.cmdline import get_target_nodes
from ..utils.text import bold, green, mark_for_translation as _, red
from ..utils.ui import io


def bw_test(repo, args):
    if args['target']:
        pending_nodes = get_target_nodes(repo, args['target'], adhoc_nodes=args['adhoc_nodes'])
    else:
        pending_nodes = copy(list(repo.nodes))

    def tasks_available():
        return bool(pending_nodes)

    def next_task():
        node = pending_nodes.pop()
        return {
            'target': node.test,
            'task_id': node.name,
            'kwargs': {
                'ignore_missing_faults': args['ignore_missing_faults'],
                'workers': args['item_workers'],
            },
        }

    worker_pool = WorkerPool(
        tasks_available,
        next_task,
        pool_id="test",
        workers=args['node_workers'],
    )
    worker_pool.run()

    checked_groups = []
    for group in repo.groups:
        if group in checked_groups:
            continue
        with io.job(_("  {group}  checking for subgroup loops...").format(group=group.name)):
            checked_groups.extend(group.subgroups)  # the subgroups property has the check built in
        io.stdout(_("{x} {group}  has no subgroup loops").format(
            x=green("✓"),
            group=bold(group.name),
        ))

    # check for plugin inconsistencies
    if args['plugin_conflict_error']:
        pm = PluginManager(repo.path)
        for plugin, version in pm.list():
            local_changes = pm.local_modifications(plugin)
            if local_changes:
                io.stderr(_("{x} Plugin '{plugin}' has local modifications:").format(
                    plugin=plugin,
                    x=red("✘"),
                ))
                for path, actual_checksum, should_checksum in local_changes:
                    io.stderr(_("\t{path} ({actual_checksum}) should be {should_checksum}").format(
                        actual_checksum=actual_checksum,
                        path=path,
                        should_checksum=should_checksum,
                    ))
                exit(1)
            else:
                io.stdout(_("{x} Plugin '{plugin}' has no local modifications.").format(
                    plugin=plugin,
                    x=green("✓"),
                ))

    # generate metadata a couple of times for every node and see if
    # anything changes between iterations
    if args['determinism_metadata'] > 1:
        hashes = {}
        for i in range(args['determinism_metadata']):
            repo = Repository(repo.path)
            if args['target']:
                nodes = get_target_nodes(repo, args['target'], adhoc_nodes=args['adhoc_nodes'])
            else:
                nodes = repo.nodes
            for node in nodes:
                with io.job(_("  {node}  generating metadata ({i}/{n})... ").format(
                    i=i + 1,
                    n=args['determinism_metadata'],
                    node=node.name,
                )):
                    result = node.metadata_hash()
                hashes.setdefault(node.name, result)
                if hashes[node.name] != result:
                    io.stderr(_(
                        "{x} Metadata for node {node} changed when generated repeatedly "
                        "(use `bw hash -d {node}` to debug)"
                    ).format(node=node.name, x=red("✘")))
                    exit(1)
        io.stdout(_("{x} Metadata remained the same after being generated {n} times").format(
            n=args['determinism_metadata'],
            x=green("✓"),
        ))

    # generate configuration a couple of times for every node and see if
    # anything changes between iterations
    if args['determinism_config'] > 1:
        hashes = {}
        for i in range(args['determinism_config']):
            repo = Repository(repo.path)
            if args['target']:
                nodes = get_target_nodes(repo, args['target'], adhoc_nodes=args['adhoc_nodes'])
            else:
                nodes = repo.nodes
            for node in nodes:
                with io.job(_("  {node}  generating configuration ({i}/{n})...").format(
                    i=i + 1,
                    n=args['determinism_config'],
                    node=node.name,
                )):
                    result = node.hash()
                hashes.setdefault(node.name, result)
                if hashes[node.name] != result:
                    io.stderr(_(
                        "{x} Configuration for node {node} changed when generated repeatedly "
                        "(use `bw hash -d {node}` to debug)"
                    ).format(node=node.name, x=red("✘")))
                    exit(1)
        io.stdout(_("{x} Configuration remained the same after being generated {n} times").format(
            n=args['determinism_config'],
            x=green("✓"),
        ))

    if not args['target']:
        repo.hooks.test(repo)
