def pagination_params(skip: int=None, limit: int=None):
    return {
        'skip' : skip,
        'limit' : limit,
    }

def paginator_info(first: int=None, page: int=None):
    """
    pagination used in podchaser graphql api queries
    Args:
        first (int, optional): 
        page (int, optional): 

    """
    return {
        'first' : first,
        'page' : page,
    }