from fastapi import APIRouter


# router object
router = APIRouter(prefix="/api/v1",tags=["Health"])  #now url becomes /api/v1/health


# -----------------------------
# HEALTH CHECK
# -----------------------------

@router.get("/health")
def health_check():

    return {

        "status": "healthy"

    }