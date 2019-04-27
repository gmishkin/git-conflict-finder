import datetime
import os
import re

import git
import yaml


def load_repository(path, base_branch_name, age_cutoff_duration):
    return Repository(path, base_branch_name, age_cutoff_duration)


class Repository(object):
    def __init__(self, path, base_branch_name, old_cutoff_duration):
        self._gitrepo = git.Repo(path=path)
        self._base_branch = self._gitrepo.heads[base_branch_name]
        self._age_cutoff = datetime.datetime.now(datetime.timezone.utc) - old_cutoff_duration

        # Config file in target repo
        rcpath = os.path.join(path, '.cxfinderrc')
        if os.path.exists(rcpath):
            with open(rcpath) as rcfile:
                rc = yaml.safe_load(rcfile)

        # Patterns of branches to exclude
        self._excluded_branches = []
        if rc is not None and 'exclude_branches' in rc:
            for exclude_rule in rc['exclude_branches']:
                self._excluded_branches.append(re.compile(exclude_rule))

    def filter_branches(self):
        branches_ok_by_name = []
        excluded_branches = []
        for branch in self._gitrepo.heads:
            if branch.name == self._base_branch.name:
                continue

            if branch.commit.committed_datetime < self._age_cutoff:
                continue

            if self._exclude_branch_by_patterns(branch):
                excluded_branches.append(branch)
                continue

            branches_ok_by_name.append(branch)

        # Exclude branches that appear to be branched off an excluded branch
        if len(excluded_branches) > 0:
            branches_ok_by_base = []
            for branch in branches_ok_by_name:
                if not self._exclude_branch_by_base_lca(branch, excluded_branches):
                    branches_ok_by_base.append(branch)
        else:
            branches_ok_by_base = branches_ok_by_name

        return branches_ok_by_base

    def _exclude_branch_by_patterns(self, branch):
        """Exclude branches that match a pattern excluded in the target repo config"""
        include = True
        for exclude_rule in self._excluded_branches:
            if exclude_rule.match(branch.name):
                include = False
                break

        return not include

    def _exclude_branch_by_base_lca(self, branch, excluded_branches):
        """Exclude branches that appear to be branched off an excluded branch"""
        include = True
        print(branch.name)

        lca_base = self._gitrepo.merge_base(branch, self._base_branch)[0]
        for excluded_branch in excluded_branches:
            lca_exclude = self._gitrepo.merge_base(branch, excluded_branch)[0]
            if lca_exclude.committed_datetime > lca_base.committed_datetime:
                include = False
                break

        return not include
