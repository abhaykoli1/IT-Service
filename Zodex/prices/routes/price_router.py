from fastapi import APIRouter
import json
from fastapi import HTTPException  # ✅ use FastAPI's exception

from Zodex.prices.models.price_model import Feature, PricingPlan, PricingPlanSchema


router = APIRouter()

@router.post("/api/v1/add-pricing-plan")
async def add_pricing_plan(body: PricingPlanSchema):
    save_data = PricingPlan(**body.dict())
    save_data.save()
    return {
        "message": "Pricing plan added successfully",
        "status": 200
    }

@router.get("/api/v1/get-all-pricing-plans")
async def get_all_pricing_plans():
    all_data = PricingPlan.objects.all()
    return {
        "message": "All pricing plans fetched",
        "data": json.loads(all_data.to_json()),
        "status": 200
    }

@router.put("/api/v1/update-pricing-plan/{plan_id}")
async def update_pricing_plan(plan_id: str, body: PricingPlanSchema):
    try:
        plan = PricingPlan.objects(id=plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Pricing plan not found")

        # Convert feature schemas to MongoEngine Feature objects
        mongo_features = [Feature(label=feat.label, included=feat.included) for feat in body.features]

        # Modify and save
        plan.update(
            title=body.title,
            price=body.price,
            monthly=body.monthly,
            description=body.description,
            discount=body.discount,
            features=mongo_features
        )

        updated_plan = PricingPlan.objects(id=plan_id).first()  # refetch updated
        return {
            "message": "Pricing plan updated",
            "data": json.loads(updated_plan.to_json()),
            "status": 200
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/api/v1/delete-all-pricing-plans")
async def delete_all_pricing_plans():
    PricingPlan.objects.all().delete()
    return {
        "message": "All pricing plans deleted successfully",
        "status": 200
    }


# ✅ New: Delete plan by ID
@router.delete("/api/v1/delete-pricing-plan/{plan_id}")
async def delete_pricing_plan(plan_id: str):
    plan = PricingPlan.objects(id=plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Pricing plan not found")
    
    plan.delete()
    return {
        "message": "Pricing plan deleted successfully",
        "status": 200
    }
