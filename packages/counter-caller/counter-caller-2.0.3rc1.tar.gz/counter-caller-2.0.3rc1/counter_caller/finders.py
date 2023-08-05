import os

def find_static_asset_dirname(search_paths, asset):
    for dirname in search_paths:
        path = os.path.join(dirname, asset)

        if os.path.exists(path):
            return dirname

    return ''
