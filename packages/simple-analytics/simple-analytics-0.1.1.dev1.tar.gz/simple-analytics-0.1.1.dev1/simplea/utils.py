def add_suffix(txt, suffix):
    """add the given to every element in given comma separated list.
    adds suffix before -.
    
    Example:
    add_suffix("hello,john", "ga:") -> "ga:hello,ga:john"
    """

    if txt is None:
        return None

    elements = txt.split(",")
    elements = ["-" + suffix + e[1:] if e[0] == "-" 
            else suffix + e for e in elements]
    
    return ",".join(elements)
