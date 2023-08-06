"""
Wrapper module with preserved save state in archive file.
"""
from fs_uae_wrapper import base


class SaveState(base.Base):
    """
    Preserve save state.
    """
    def __init__(self, conf_file, fsuae_options, configuration):
        """
        Params:
            conf_file:      a relative path to provided configuration file
            fsuae_options:  is an CmdOption object created out of command line
                            parameters
            configuration:  is config dictionary created out of config file
        """
        super(SaveState, self).__init__(conf_file, fsuae_options,
                                        configuration)
        self.arch_filepath = None
        self.all_options['wrapper_save_state'] = '1'

    def run(self):
        """
        Main function which accepts configuration file for FS-UAE
        It will do as follows:
            - set needed full path for asset files
            - copy configuration
            - optionally extract save state archive
            - run the emulation
            - optionally make archive save state
        """
        if not super(SaveState, self).run():
            return False

        self._load_save()

        if not self._copy_conf():
            return False

        kick_opts = self._kickstart_option()
        if kick_opts:
            self.fsuae_options.update(kick_opts)

        if not self._run_emulator(self.fsuae_options.list()):
            return False

        if self._get_saves_dir():
            if not self._save_save():
                return False

        return True


def run(config_file, fsuae_options, configuration):
    """Run fs-uae with provided config file and options"""

    runner = SaveState(config_file, fsuae_options, configuration)
    try:
        return runner.run()
    finally:
        runner.clean()
