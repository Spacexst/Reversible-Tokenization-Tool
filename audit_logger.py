import logging

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def log_action(token, action):
    logging.info(f"{action} - Token: {token}")
