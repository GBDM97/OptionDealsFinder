def is_number(s):
    try:
        float(s)  # Try converting the string to a float
        return True  # If successful, it's a valid number
    except ValueError:
        return False  # If ValueError is raised, it's not a valid number