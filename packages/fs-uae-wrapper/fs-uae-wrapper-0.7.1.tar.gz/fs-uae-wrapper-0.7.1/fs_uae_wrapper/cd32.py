"""
Run CD32 games using fsuae

It will use compressed directories, and create 7z archive for save state dirs.
It is assumed, that filename of cue file (without extension) is the same as
archive with game assets, while using config name (without extension) will be
used as a base for save state (it will append '_save.7z' to the archive file
name.

"""
from fs_uae_wrapper import base


class CD32(base.ArchiveBase):
    """
    Class for performing extracting archive, copying emulator files, and
    cleaning it back again
    """

    def run(self):
        """
        Main function which accepts configuration file for FS-UAE
        It will do as follows:
            - set needed full path for asset files
            - extract archive file
            - copy configuration
            - [copy save if exists]
            - run the emulation
            - archive save state
        """
        super(CD32, self).run()
        if not self._validate_options():
            return False

        if not self._extract():
            return False

        for method in (self._copy_conf, self._load_save):
            if not method():
                return False

        kick_opts = self._kickstart_option()
        if kick_opts:
            self.fsuae_options.update(kick_opts)

        if not self._run_emulator(self.fsuae_options.list()):
            return False

        if self._get_saves_dir():
            return self._save_save()

        return True


def run(config_file, fsuae_options, configuration):
    """Run fs-uae with provided config file and options"""

    runner = CD32(config_file, fsuae_options, configuration)
    try:
        return runner.run()
    finally:
        runner.clean()
