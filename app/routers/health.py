from fastapi import APIRouter


# router object
router = APIRouter()


# -----------------------------
# HEALTH CHECK
# -----------------------------

@router.get("/health")
def health_check():

    return {

        "status": "healthy"

    }