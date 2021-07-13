class EquationError(Exception):

    def __init__(self, err_msg):
        self.error = err_msg

    def __str__(self):
        return self.error

    def __repr__(self):
        return self.error
