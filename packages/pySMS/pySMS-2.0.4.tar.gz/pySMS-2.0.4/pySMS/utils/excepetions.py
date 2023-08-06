class GenericError(Exception):
    """Basic Exception for modules"""
    def __init__(self, func, msg=None):
        if msg is None:
            print("An error occurred on the function: " + func)
        super(GenericError, self).__init__(msg)
        self.func = func


class NoRecordsFoundError(Exception):
    """No Record Found while parsing"""
    def __init__(self, location, msg=None):
        if msg is None:
            print("No Records Found: no records found while parsing: " + location)
        super(NoRecordsFoundError, self).__init__(msg)
        self.location = location


class ProductChooserError(Exception):
    """Called when there is an issue using Product Chooser"""
    def __init__(self, problem, msg=None):
        if msg is None:
            print("An error occurred with the product chooser: " + problem)
        super(ProductChooserError, self).__init__(msg)
        self.problem = problem


class ProductChooserAddError(Exception):
    """Called when there is an issue using Product Chooser"""
    def __init__(self, problem, msg=None):
        if msg is None:
            print("An error occurred with the product chooser" + problem)
        super(ProductChooserAddError, self).__init__(msg)
        self.problem = problem


class LogicError(Exception):
    """Basic Excpetion for Logic Module"""
    def __init__(self, func, msg=None):
        if msg is None:
            print("An error occurred on the function: " + func)
        super(LogicError, self).__init__(msg)
        self.func = func


class SelectionError(Exception):
    """Basic Selection Exception for modules"""
    def __init__(self, func, element, msg=None):
        if msg is None:
            print("Unable to interact with element:  " + element + " : " + func)
        super(SelectionError, self).__init__(msg)
        self.func = func
        self.element = element
