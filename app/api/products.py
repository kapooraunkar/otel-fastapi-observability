from fastapi import APIRouter


# router object
router = APIRouter(prefix="/api/v1",tags=["Products"])  #now  url becomes /api/v1/users


# -----------------------------
# PRODUCTS ENDPOINT
# -----------------------------

@router.get("/products")
def get_products():

    return {

        "products": [

            "Laptop",
            "Phone",
            "Keyboard"

        ]

    }