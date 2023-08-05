"""
This module contains the actions that are combined to perform dploy's sub
commands
"""

import dploy.utils as utils


class AbstractBaseAction():
    # pylint: disable=too-few-public-methods
    """
    An abstract base class that define the interface for actions
    """
    def __init__(self):
        pass

    def _logic(self):
        pass

    def execute(self):
        """
        function that executes _logic() of each derived action
        """
        self._logic()


class SymbolicLink(AbstractBaseAction):
    # pylint: disable=too-few-public-methods
    """
    Action to create a symbolic link relative to the source of the link
    """
    def __init__(self, subcmd, source, dest):
        super().__init__()
        self.source = source
        self.source_relative = utils.get_relative_path(source, dest.parent)
        self.subcmd = subcmd
        self.dest = dest

    def _logic(self):
        self.dest.symlink_to(self.source_relative)

    def __repr__(self):
        return "dploy {subcmd}: link {dest} => {source}".format(
            subcmd=self.subcmd, dest=self.dest, source=self.source_relative)


class AlreadyLinked(AbstractBaseAction):
    # pylint: disable=too-few-public-methods
    """
    Action to used to print an already linked message
    """
    def __init__(self, subcmd, source, dest):
        super().__init__()
        self.source = source
        self.source_relative = utils.get_relative_path(source, dest.parent)
        self.dest = dest
        self.subcmd = subcmd

    def _logic(self):
        pass

    def __repr__(self):
        return "dploy {subcmd}: already linked {dest} => {source}".format(
            subcmd=self.subcmd,
            source=self.source_relative,
            dest=self.dest)


class AlreadyUnlinked(AbstractBaseAction):
    # pylint: disable=too-few-public-methods
    """
    Action to used to print an already unlinked message
    """
    def __init__(self, subcmd, source, dest):
        super().__init__()
        self.source = source
        self.source_relative = utils.get_relative_path(source, dest.parent)
        self.dest = dest
        self.subcmd = subcmd

    def _logic(self):
        pass

    def __repr__(self):
        return "dploy {subcmd}: already unlinked {dest} => {source}".format(
            subcmd=self.subcmd,
            source=self.source_relative,
            dest=self.dest)


class UnLink(AbstractBaseAction):
    # pylint: disable=too-few-public-methods
    """
    Action to unlink a symbolic link
    """
    def __init__(self, subcmd, target):
        super().__init__()
        self.target = target
        self.subcmd = subcmd

    def _logic(self):
        if not self.target.is_symlink():
            #pylint: disable=line-too-long
            raise RuntimeError('dploy detected and aborted an attempt to unlink a non-symlink this is a bug and should be reported')
        self.target.unlink()

    def __repr__(self):
        source_relative = utils.get_relative_path(self.target.resolve(), self.target.parent)
        return "dploy {subcmd}: unlink {target} => {source}".format(
            subcmd=self.subcmd,
            target=self.target,
            source=source_relative)

class MakeDirectory(AbstractBaseAction):
    # pylint: disable=too-few-public-methods
    """
    Action to create a directory
    """
    def __init__(self, subcmd, target):
        super().__init__()
        self.target = target
        self.subcmd = subcmd

    def _logic(self):
        self.target.mkdir()

    def __repr__(self):
        return "dploy {subcmd}: make directory {target}".format(
            target=self.target,
            subcmd=self.subcmd)

class RemoveDirectory(AbstractBaseAction):
    # pylint: disable=too-few-public-methods
    """
    Action to remove a directory
    """
    def __init__(self, subcmd, target):
        super().__init__()
        self.target = target
        self.subcmd = subcmd

    def _logic(self):
        self.target.rmdir()

    def __repr__(self):
        msg = "dploy {subcmd}: remove directory {target}"
        return msg.format(target=self.target, subcmd=self.subcmd)
