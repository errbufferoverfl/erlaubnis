def authorise_client(**kwargs):
    client = client.get()
    if not client:
        return None
    else:
        # here is where we go through the motions of validating that the URL and scopes are right.
        pass
