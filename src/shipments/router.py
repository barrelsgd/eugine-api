from fastapi import APIRouter
from . import service

router = APIRouter(prefix="/shipments", tags=["shipments"])

@router.get("/shipment")
def get_shipment():
    return service.get_shipment()
