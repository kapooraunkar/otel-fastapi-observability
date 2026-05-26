from fastapi import APIRouter


# router object
router = APIRouter()


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