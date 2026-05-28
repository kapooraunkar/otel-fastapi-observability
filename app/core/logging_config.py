import logging

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(name)s "
        "%(message)s "

    )
)

logger = logging.getLogger(__name__)

#creates a centralized logger system which records what happened, why and when. 
#example log output: 2026-06-01 INFO user_service Fetching users