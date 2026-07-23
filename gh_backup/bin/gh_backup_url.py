#!/usr/bin/env python3
import os

def prepare_auth_url(git_url, auth_type, auth_value):
    if auth_type == 'none':
        return git_url
    elif auth_type == 'token':
        if not auth_value:
            return git_url
        token_path = os.path.expanduser(f"~/etc/{auth_value}")
        try:
            token = open(token_path, 'r', encoding='utf-8').read().strip()
        except Exception as e:
            token = auth_value
        if git_url.startswith('https://'):
            parts = git_url.split('://', 1)
            return f"{parts[0]}://{token}@{parts[1]}"
        return git_url
    elif auth_type == 'ssh':
        return git_url
    return git_url

