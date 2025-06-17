from http.client import HTTPException
import json
from fastapi import APIRouter
from Zodex.work.models.work_model import TechCard, TechCardSchema

router = APIRouter()

# Add TechCard
@router.post("/api/v1/add-techcard")
async def add_techcard(body: TechCardSchema):
    savedata = TechCard(**body.dict())
    savedata.save()
    return {
        "message": "TechCard added successfully",
        "status": 200
    }

# Get All TechCards
@router.get("/api/v1/get-all-techcards")
async def get_all_techcards():
    all_data = TechCard.objects.all()
    return {
        "message": "All TechCards fetched",
        "data": json.loads(all_data.to_json()),
        "status": 200
    }

# Update TechCard by ID
@router.put("/api/v1/update-techcard/{techcard_id}")
async def update_techcard(techcard_id: str, body: TechCardSchema):
    try:
        techcard = TechCard.objects(id=techcard_id).first()
        if not techcard:
            raise HTTPException(status=404, detail="TechCard not found")

        techcard.update(
            set__image=body.image,
            set__techStack=body.techStack,
            set__title=body.title,
            set__link=body.link
        )

        updated = TechCard.objects(id=techcard_id).first()
        return {
            "message": "TechCard updated successfully",
            "data": json.loads(updated.to_json()),
            "status": 200
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status=500, detail=f"Error: {str(e)}")

# Delete all TechCards
@router.delete("/api/v1/delete-all-techcards")
def delete_all_techcards():
    TechCard.objects.all().delete()
    return {
        "message": "All TechCards deleted successfully",
        "status": 200
    }

# ✅ Delete a specific TechCard by ID
@router.delete("/api/v1/delete-techcard/{techcard_id}")
def delete_techcard_by_id(techcard_id: str):
    techcard = TechCard.objects(id=techcard_id).first()
    if not techcard:
        raise HTTPException(status=404, detail="TechCard not found")
    
    techcard.delete()
    return {
        "message": "TechCard deleted successfully",
        "status": 200
    }
