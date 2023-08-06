# -*- coding: utf-8 -*-
import os
import sys

import dulwich.repo


class CustomRepo(dulwich.repo.Repo):
    def __init__(self, root, controldir=dulwich.repo.CONTROLDIR):

        hidden_path = os.path.join(root, controldir)
        if os.path.isdir(os.path.join(hidden_path, dulwich.repo.OBJECTDIR)):
            self.bare = False
            self._controldir = hidden_path
        elif (os.path.isdir(os.path.join(root, dulwich.repo.OBJECTDIR)) and
                  os.path.isdir(os.path.join(root, dulwich.repo.REFSDIR))):
            self.bare = True
            self._controldir = root
        elif os.path.isfile(hidden_path):
            self.bare = False
            with open(hidden_path, 'r') as f:
                path = dulwich.repo.read_gitfile(f)
            self.bare = False
            self._controldir = os.path.join(root, path)
        else:
            raise dulwich.repo.NotGitRepository(
                "No git repository was found at %(path)s" % dict(path=root)
            )

        commondir = self.get_named_file(dulwich.repo.COMMONDIR)
        if commondir is not None:
            with commondir:
                self._commondir = os.path.join(
                    self.controldir(),
                    commondir.read().rstrip(b"\r\n").decode(sys.getfilesystemencoding()))
        else:
            self._commondir = self._controldir
        self.path = root
        object_store = dulwich.repo.DiskObjectStore(
            os.path.join(self.commondir(), dulwich.repo.OBJECTDIR))
        refs = dulwich.repo.DiskRefsContainer(self.commondir(), self._controldir)
        dulwich.repo.BaseRepo.__init__(self, object_store, refs)

        self._graftpoints = {}
        graft_file = self.get_named_file(os.path.join("info", "grafts"), basedir=self.commondir())
        if graft_file:
            with graft_file:
                self._graftpoints.update(dulwich.repo.parse_graftpoints(graft_file))
        graft_file = self.get_named_file("shallow", basedir=self.commondir())
        if graft_file:
            with graft_file:
                self._graftpoints.update(dulwich.repo.parse_graftpoints(graft_file))

        self.hooks['pre-commit'] = dulwich.repo.PreCommitShellHook(self.controldir())
        self.hooks['commit-msg'] = dulwich.repo.CommitMsgShellHook(self.controldir())
        self.hooks['post-commit'] = dulwich.repo.PostCommitShellHook(self.controldir())

    @classmethod
    def init(cls, root, controldir=dulwich.repo.CONTROLDIR, mkdir=False):
        """Create a new repository.

        :param root: Path in which to create the repository
        :param controldir: Repository control directory
        :param mkdir: Whether to create the directory
        :return: `Repo` instance
        """
        if mkdir:
            os.mkdir(root)
        hidden_path = os.path.join(root, controldir)
        os.mkdir(hidden_path)
        cls._init_maybe_bare(hidden_path, False)
        return cls(root, controldir)
