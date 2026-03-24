import logging

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def log_action(token, action):
    logging.info(f"{action} - Token: {token}")


def clear_audit_file():
    with open("audit.log", "w") as f:
        pass
    print("Audit log file cleared!")
