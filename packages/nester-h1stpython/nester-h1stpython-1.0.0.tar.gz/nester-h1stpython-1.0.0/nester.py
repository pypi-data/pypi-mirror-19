"""
This is a comment.
"""
def proc(x):
    """
    Just read the damn code to figure it out.
    """
    for i in x:
        if isinstance(i, list):
            proc(i);
        else:
            print(i);
