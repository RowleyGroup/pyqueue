class CommandContainerInterface:
    def __str__(self):
        raise NotImplementedError("A command container should implement __str__ method")

    def get_name(self):
        raise NotImplementedError("A command container should implement get_name method")

    def get_header(self):
        return '# %s' % self.get_name()
