class DuplicateServerConfiguration(Exception):

    def __init__(self, section, server_name):
        super().__init__()
        self.section = section
        self.server_name = server_name

    def __str__(self):
        return 'Multiple {} configurations for server name "{}"'.format(
            self.section, self.server_name)
