"""
The logic and workings behind the stow and unstow sub-commands
"""

from collections import defaultdict
from collections import Counter
import pathlib
import sys
import dploy.actions as actions
import dploy.utils as utils
import dploy.errors as errors


class AbstractBaseSubCommand():
    """
    An abstract class to unify shared functionality in stow commands
    """

    # pylint: disable=too-many-arguments
    def __init__(self, subcmd, sources, dest, is_silent, is_dry_run, ignore_patterns):
        self.subcmd = subcmd
        self.actions = []
        self.exceptions = []
        self.is_silent = is_silent
        self.is_dry_run = is_dry_run

        dest_input = pathlib.Path(dest)

        for source in sources:
            source_input = pathlib.Path(source)
            self.ignore = Ignore(ignore_patterns,
                                 source_input.parent / pathlib.Path('.dploystowignore'))

            if self.ignore.should_ignore(source_input):
                self.ignore.ignore(source_input)
                continue
            if self.is_valid_input(source_input, dest_input):
                self.collect_actions(source_input, dest_input)

        self.check_for_other_actions()
        self.execute_actions()

    def check_for_other_actions(self):
        """
        Abstract method for examine the existing action to see if more actions
        need to be added or if some actions need to be removed.
        """
        pass

    def is_valid_input(self, source, dest):
        """
        Abstract method to check if the input to a sub-command is valid
        """
        pass

    def collect_actions(self, source, dest):
        """
        Abstract method that collects the actions required to complete a
        sub-command.
        """
        pass

    def execute_actions(self):
        """
        Either executes collected actions by a sub command or raises collected
        exceptions.
        """
        if len(self.exceptions) > 0:
            if not self.is_silent:
                for exception in self.exceptions:
                    print(exception, file=sys.stderr)
            raise self.exceptions[0]
        else:
            for action in self.actions:
                if not self.is_silent:
                    print(action)
                if not self.is_dry_run:
                    action.execute()

    def add_exception(self, exception):
        """
        Add an exception to to be handled later
        """
        self.exceptions.append(exception.exception)



class AbstractBaseStow(AbstractBaseSubCommand):
    """
    Abstract Base class that contains the shared logic for all of the stow
    commands
    """
    # pylint: disable=too-many-arguments
    def __init__(self, subcmd, source, dest, is_silent, is_dry_run, ignore_patterns):
        self.is_unfolding = False
        super().__init__(subcmd, source, dest, is_silent, is_dry_run, ignore_patterns)


    def is_valid_input(self, source, dest):
        """
        Check to see if the input is valid
        """
        result = True

        if not self.valid_source(source):
            result = False

        if not self.valid_dest(dest):
            result = False

        return result

    def valid_dest(self, dest):
        """
        Check if the dest argument is valid
        """
        result = True

        if not dest.is_dir():
            self.add_exception(errors.NoSuchDirectoryToSubcmdInto(self.subcmd, dest))
            result = False
        else:
            if not utils.is_directory_writable(dest):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
                result = False

            if not utils.is_directory_readable(dest):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
                result = False

            if not utils.is_directory_executable(dest):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
                result = False

        return result

    def valid_source(self, source):
        """
        Check if the source argument is valid
        """
        result = True

        if not source.is_dir():
            self.add_exception(errors.NoSuchDirectory(self.subcmd, source))
            result = False
        else:
            if not utils.is_directory_readable(source):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdFrom(self.subcmd, source))
                result = False

            if not utils.is_directory_executable(source):
                self.add_exception(
                    errors.InsufficientPermissionsToSubcmdFrom(self.subcmd, source))
                result = False

        return result

    def get_directory_contents(self, directory):
        """
        Get the contents of a directory while handling errors that may occur
        """
        contents = []

        try:
            contents = utils.get_directory_contents(directory)
        except PermissionError:
            self.add_exception(errors.PermissionDenied(self.subcmd, directory))
        except FileNotFoundError:
            self.add_exception(errors.NoSuchFileOrDirectory(self.subcmd, directory))
        except NotADirectoryError:
            self.add_exception(errors.NoSuchDirectory(self.subcmd, directory))

        return contents

    def are_same_file(self, source, dest):
        """
        Abstract method that handles the case when the source and dest are the
        same file when collecting actions
        """
        pass

    def are_directories(self, source, dest):
        """
        Abstract method that handles the case when the source and dest are directories
        same file when collecting actions
        """
        pass

    def are_other(self, source, dest):
        """
        Abstract method that handles all other cases what to do if no particular
        condition is true cases are found
        """
        pass

    def is_valid_collection_input(self, source, dest):
        """
        Helper to validate the source and dest parameters passed to
        collect_actions()
        """
        result = True
        if not self.valid_source(source):
            result = False

        if dest.exists():
            if not self.valid_dest(dest):
                result = False
        return result

    def collect_actions_existing_dest(self, source, dest):
        """
        collect_actions() helper to collect required actions to perform a stow
        command when the destination already exists
        """
        if utils.is_same_file(dest, source):
            if dest.is_symlink() or self.is_unfolding:
                self.are_same_file(source, dest)
            else:
                self.add_exception(errors.SourceIsSameAsDest(self.subcmd, dest.parent))

        elif dest.is_dir() and source.is_dir:
            self.are_directories(source, dest)
        else:
            self.add_exception(
                errors.ConflictsWithExistingFile(self.subcmd, source, dest))

    def collect_actions(self, source, dest):
        """
        Concrete method to collect required actions to perform a stow
        sub-command
        """

        if self.ignore.should_ignore(source):
            self.ignore.ignore(source)
            return

        if not self.is_valid_collection_input(source, dest):
            return

        sources = self.get_directory_contents(source)

        for source in sources:
            if self.ignore.should_ignore(source):
                self.ignore.ignore(source)
                continue

            dest_path = dest / pathlib.Path(source.name)

            does_dest_path_exist = False
            try:
                does_dest_path_exist = dest_path.exists()
            except PermissionError:
                self.add_exception(errors.PermissionDenied(self.subcmd, dest_path))
                return

            if does_dest_path_exist:
                self.collect_actions_existing_dest(source, dest_path)
            elif dest_path.is_symlink():
                self.add_exception(
                    errors.ConflictsWithExistingLink(self.subcmd, source, dest_path))
            elif not dest_path.parent.exists() and not self.is_unfolding:
                self.add_exception(errors.NoSuchDirectory(self.subcmd, dest_path.parent))
            else:
                self.are_other(source, dest_path)


class UnStow(AbstractBaseStow):
    """
    Concrete class implementation of the unstow sub-command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
        super().__init__("unstow", source, dest, is_silent, is_dry_run, ignore_patterns)

    def are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        self.actions.append(actions.UnLink(self.subcmd, dest))

    def are_directories(self, source, dest):
        self.collect_actions(source, dest)

    def are_other(self, source, dest):
        self.actions.append(actions.AlreadyUnlinked(self.subcmd, source, dest))

    def check_for_other_actions(self):
        self.collect_folding_actions()

    def get_unlink_actions(self):
        """
        get the current Unlink() actions from the self.actions
        """
        return [a for a in self.actions if isinstance(a, actions.UnLink)]

    def get_unlink_actions_target_parents(self):
        """
        Get list of the parents for the current Unlink() actions from
        self.actions
        """
        unlink_actions = self.get_unlink_actions()
        # sort for deterministic output
        return sorted(set([a.target.parent for a in unlink_actions]))

    def get_unlink_actions_targets(self):
        """
        Get list of the targets for the current Unlink() actions from
        self.actions
        """
        unlink_actions = self.get_unlink_actions()
        return [a.target for a in unlink_actions]

    def collect_folding_actions(self):
        """
        find candidates for folding i.e. when a directory contains symlinks to
        files that all share the same parent directory
        """
        unlink_actions_targets = self.get_unlink_actions_targets()
        unlink_actions_targets_parents = self.get_unlink_actions_target_parents()


        for parent in unlink_actions_targets_parents:
            items = utils.get_directory_contents(parent)
            other_links_parents = []
            other_links = []
            source_parent = None
            is_normal_files_detected = False

            for item in items:
                if item not in unlink_actions_targets:
                    does_item_exist = False
                    try:
                        does_item_exist = item.exists()
                    except PermissionError:
                        self.add_exception(errors.PermissionDenied(self.subcmd, item))
                        return

                    if does_item_exist and item.is_symlink():
                        source_parent = item.resolve().parent
                        other_links_parents.append(item.resolve().parent)
                        other_links.append(item)
                    else:
                        is_normal_files_detected = True
                        break

            if not is_normal_files_detected:
                other_links_parent_count = len(Counter(other_links_parents))

                if other_links_parent_count == 1:
                    assert source_parent != None
                    if utils.is_same_files(utils.get_directory_contents(source_parent),
                                           other_links):
                        self.fold(source_parent, parent)

                elif other_links_parent_count == 0:
                    self.actions.append(actions.RemoveDirectory(self.subcmd, parent))

    def fold(self, source, dest):
        """
        add the required actions for folding
        """
        self.collect_actions(source, dest)
        self.actions.append(actions.RemoveDirectory(self.subcmd, dest))
        self.actions.append(actions.SymbolicLink(self.subcmd, source, dest))


class Link(AbstractBaseSubCommand):
    """
    Concrete class implementation of the link sub-command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
        super().__init__("link", [source], dest, is_silent, is_dry_run, ignore_patterns)

    def is_valid_input(self, source, dest):
        """
        Check to see if the input is valid
        """
        if not source.exists():
            self.add_exception(errors.NoSuchFileOrDirectory(self.subcmd, source))
            return False

        elif not dest.parent.exists():
            self.add_exception(errors.NoSuchFileOrDirectory(self.subcmd, dest.parent))
            return False

        elif (not utils.is_file_readable(source)
              or not utils.is_directory_readable(source)):
            self.add_exception(errors.InsufficientPermissions(self.subcmd, source))
            return False

        elif (not utils.is_file_writable(dest.parent)
              or not utils.is_directory_writable(dest.parent)):
            self.add_exception(
                errors.InsufficientPermissionsToSubcmdTo(self.subcmd, dest))
            return False

        else:
            return True

    def collect_actions(self, source, dest):
        """
        Concrete method to collect required actions to perform a link
        sub-command
        """

        if dest.exists():
            if utils.is_same_file(dest, source):
                self.actions.append(actions.AlreadyLinked(self.subcmd,
                                                          source,
                                                          dest))
            else:
                self.add_exception(
                    errors.ConflictsWithExistingFile(self.subcmd, source, dest))
        elif dest.is_symlink():
            self.add_exception(
                errors.ConflictsWithExistingLink(self.subcmd, source, dest))

        elif not dest.parent.exists():
            self.add_exception(
                errors.NoSuchDirectoryToSubcmdInto(self.subcmd, dest.parent))

        else:
            self.actions.append(actions.SymbolicLink(self.subcmd, source, dest))


class Stow(AbstractBaseStow):
    """
    Concrete class implementation of the stow sub-command
    """
    # pylint: disable=too-many-arguments
    def __init__(self, source, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
        super().__init__("stow", source, dest, is_silent, is_dry_run, ignore_patterns)

    def unfold(self, source, dest):
        """
        Method unfold a destination directory
        """
        self.is_unfolding = True
        self.actions.append(actions.UnLink(self.subcmd, dest))
        self.actions.append(actions.MakeDirectory(self.subcmd, dest))
        self.collect_actions(source, dest)
        self.is_unfolding = False

    def get_duplicate_actions(self):
        """
        return a tuple containing tuples with the following structure
        (link destination, [indices of duplicates])
        """
        tally = defaultdict(list)
        for index, action in enumerate(self.actions):
            if isinstance(action, actions.SymbolicLink):
                tally[action.dest].append(index)
        # sort for deterministic output
        return sorted([indices for _, indices in tally.items() if len(indices) > 1])

    def handle_duplicate_actions(self):
        """
        check for symbolic link actions that would cause conflicting symbolic
        links to the same destination. Also check for actions that conflict but
        are candidates for unfolding instead.
        """
        has_conflicts = False
        dupes = self.get_duplicate_actions()

        if len(dupes) == 0:
            return

        for indices in dupes:
            first_action = self.actions[indices[0]]
            remaining_actions = [self.actions[i] for i in indices[1:]]

            if first_action.source.is_dir():
                self.unfold(first_action.source, first_action.dest)

                for action in remaining_actions:
                    self.is_unfolding = True
                    self.collect_actions(action.source, action.dest)
                    self.is_unfolding = False
            else:
                duplicate_action_sources = [str(self.actions[i].source) for i in indices]
                self.add_exception(
                    errors.ConflictsWithAnotherSource(self.subcmd, duplicate_action_sources))
                has_conflicts = True

        if has_conflicts:
            return

        # remove duplicates
        for indices in dupes:
            for index in reversed(indices[1:]):
                del self.actions[index]

        self.handle_duplicate_actions()

    def check_for_other_actions(self):
        self.handle_duplicate_actions()

    def are_same_file(self, source, dest):
        """
        what to do if source and dest are the same files
        """
        if self.is_unfolding:
            self.actions.append(
                actions.SymbolicLink(self.subcmd, source, dest))
        else:
            self.actions.append(
                actions.AlreadyLinked(self.subcmd, source, dest))

    def are_directories(self, source, dest):
        if dest.is_symlink():
            self.unfold(dest.resolve(), dest)
        self.collect_actions(source, dest)

    def are_other(self, source, dest):
        self.actions.append(
            actions.SymbolicLink(self.subcmd, source, dest))

class Ignore():
    """
    Handles ignoring of files via glob patterns either passed in directly in or
    in a specified ignore file.
    """
    def __init__(self, patterns, file):
        if patterns is None:
            input_patterns = []
        else:
            input_patterns = patterns
        self.ignored_files = []

        self.patterns = [str(file.name)] # ignore the ignore file
        self.patterns.extend(input_patterns)
        self._read_ignore_file_patterns(file)

    def _read_ignore_file_patterns(self, file):
        """
        read ignore patterns from a specified file
        """
        try:
            with open(str(file)) as afile:
                file_patterns = afile.read().splitlines()
                self.patterns.extend(file_patterns)
        except FileNotFoundError:
            pass

    def should_ignore(self, source):
        """
        check if a source should be ignored, based on the ignore patterns in
        self.patterns

        This checks if the ignore patterns match either the file exactly or
        its parents
        """
        for pattern in self.patterns:
            try:
                files = sorted(source.parent.glob(pattern))
            except IndexError: # the glob result was empty
                continue

            for file in files:
                if utils.is_same_file(file, source) or source in file.parents:
                    return True
        return False

    def ignore(self, file):
        """
        add a file to be ignored
        """
        self.ignored_files.append(file)

    def get_ignored_files(self):
        """
        get a list of the files that have been ignored
        """
        return self.ignored_files
