import git


def load_repository(path):
    return Repository(path)


class Repository(object):
    def __init__(self, path):
        self._gitrepo = git.Repo(path=path)
