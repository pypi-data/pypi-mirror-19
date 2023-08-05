import pyfunk.combinators as _


def fid(a):
    """
    The id high-order function
    @sig fid :: a -> a
    """
    return a


@_.curry
def trace(tag, val):
    """
    Prints a piped value to the console during a
    composition
    @sig trace :: Show a => String -> a -> a
    """
    print(tag, val)
    return val


def T(*args):
    """
    Always returns true
    @sig T :: _ -> Bool
    """
    return True


def F(*args):
    """
    Always returns false
    @sig F :: _ -> Bool
    """
    return False
