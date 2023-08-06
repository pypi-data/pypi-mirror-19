"""
This is a comment.
"""
def proc(x, indent = False, level=0):
    """
    Just read the damn code to figure it out.
    """
    for i in x:
        if isinstance(i, list):
            proc(i, indent, level+1);
        else:
            if indent:
                for tab in range(level):
                    print("\t", end="");
            print(i);
