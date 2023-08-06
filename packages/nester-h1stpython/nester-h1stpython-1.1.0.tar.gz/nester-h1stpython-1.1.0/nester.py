"""
This is a comment.
"""
def proc(x, level=0):
    """
    Just read the damn code to figure it out.
    """
    for i in x:
        if isinstance(i, list):
            proc(i, level+1);
        else:
            for tab in range(level):
                print("\t", end="");
            print(i);
