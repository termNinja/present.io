class DocumentData:
    """
    Represents a data object that is used to fill in the template.
    """

    def __init__(self, author, title, file_name, directory, bibliography):
        self.author = author
        self.title = title
        self.file_name = file_name
        self.directory = directory
        self.bibliography = bibliography

    def __repr__(self):
        return f"[document] author={self.author} title={self.title} file_name={self.file_name} directory={self.directory} bibliography={self.bibliography}"

    def __str__(self):
        return self.__repr__()