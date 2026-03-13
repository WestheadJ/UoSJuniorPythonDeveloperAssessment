from fastapi import APIRouter
from ..schemas.customer import CustomerResponse
from ..services.customer_service import build_customer_response

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/{customer_id}/orders", response_model=CustomerResponse)
def get_customer_orders(customer_id: int):
    return build_customer_response(customer_id)
