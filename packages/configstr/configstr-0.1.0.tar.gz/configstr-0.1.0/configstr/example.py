import logging
import configstr


def example_main():
    logging.basicConfig(level=logging.DEBUG)
    cfg = configstr.load_config()
    print(cfg)
