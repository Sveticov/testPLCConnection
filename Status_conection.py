def status_connection(*connection):
    for conn in connection:
        if not conn:
            return False
            break

    return True