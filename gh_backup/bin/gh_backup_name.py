#!/usr/bin/env python3

def get_repo_name_from_url(git_url):
    name = git_url.rstrip('/').split('/')[-1]
    if name.endswith('.git'):
        name = name[:-4]
    return name

