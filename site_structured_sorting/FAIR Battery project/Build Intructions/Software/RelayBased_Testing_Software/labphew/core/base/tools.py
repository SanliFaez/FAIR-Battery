"""
Tools for base classes
======================

Functions used by the base classes

"""

def _check_method_presence(cls, base, method):
    """
    Test if a method is present in a class and whether it's inherited, overwritten, or "new".
    Table to explain return values:
    (cls, base)
    False, False    Neither child nor base has the method
    False, True     The child class inherits the method from the base class
    True,  False    The child has the method, the base doesn't
    True,  True     Both classes have the method, but the child has overwritten the one from the base

    :param cls: The child class
    :type cls: class
    :param base: The parent or base class from which the child inherits
    :type base: class
    :param method: name of the method to test
    :type method: str
    :return: uniquely present in cls, present in base
    :rtype: bool, bool
    """
    if not hasattr(cls, method):
        # Neither cls nor base has the method
        return False, False
    elif not hasattr(base, method):
        # Only cls has the method
        return True, False
    elif getattr(cls, method) is getattr(base, method):
        # Only base has the method and cls inherits the identical method
        return False, True
    else:
        # last option: cls has a different implementation of the method
        return True, True

def check_method_presence_and_warn(cls, required, recommended):
    """
    Test if required or recommended methods are present in the class and warns the user with print messages.
    Uses _check_method_presence() to check if the method is in the class itself or in the parent/base class and also
    warns when cls will fall back to parent/base class for recommended method.
    Will raise a NotImplementedError if a required method is missing from the class.

    :param cls: the (child) class to check
    :type cls: python class
    :param required: required method names
    :type required: list
    :param recommended: recommended method names
    :type recommended: list
    """
    base = cls.mro()[1]
    missing_required = []
    for method in required:
        if _check_method_presence(cls, base, method)[0] != True:
            print('MISSING required method [{}] in class [{}]'.format(method, cls.__name__))
            missing_required.append(method)
    for method in recommended:
        c, b = _check_method_presence(cls, base, method)
        if not c:
            if b:
                print('MISSING recommended method [{}] in class [{}], falling back on method in [{}] class'.format(method,
                                                                                                             cls.__name__, base.__name__))
            else:
                print('MISSING recommended method [{}] in class [{}], ALSO MISSING in [{}] class'.format(method,
                                                                                                      cls.__name__, base.__name__))
                missing_required.append(method)
    if missing_required:
        raise NotImplementedError(missing_required)
