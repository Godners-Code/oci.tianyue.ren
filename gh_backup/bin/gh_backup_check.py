#!/usr/bin/env python3

def validate_config(config, config_path, logger):
    if not config:
        logger.error(f"Configuration Invalid: EMPTY - {config_path}")
        return False

    source = config.get('source')
    if not source or not isinstance(source, list) or len(source) != 1:
        logger.error(f"Configuration Invalid: Absence SOURCE or Wrong Format - {config_path}")
        return False

    destinations = config.get('destination')
    if not destinations or not isinstance(destinations, list) or len(destinations) == 0:
        logger.error(f"Configuration Invalid: Absence DESTINATIONS or Wrong Format - {config_path}")
        return False

    src = source[0]
    if not src.get('git_url'):
        logger.error(f"Configuration Invalid: Absense URL on SOURCE - {config_path}")
        return False

    for dest in destinations:
        if not dest.get('git_url'):
            logger.error(f"Configuration Invalid: Absense URL on DESTINATION {dest} - {config_path}")
            return False

    return True
