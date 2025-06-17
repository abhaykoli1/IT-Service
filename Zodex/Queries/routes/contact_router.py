import json
from fastapi import APIRouter, HTTPException
from Zodex.Queries.models.contact_model import ContactQueryModel, ContactQueryTable

router = APIRouter()

@router.post("/api/v1/add-Contact-query")
async def add_contact_query(body: ContactQueryModel):

    print(body)
    try:
        contact = ContactQueryTable(**body.dict())
        contact.save()
        return {
            "message": "Contact added successfully",
            "status": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add contact: {str(e)}")


@router.get("/api/v1/get-all-Contact")
async def get_all_contact():
    try:
        data = ContactQueryTable.objects().order_by("-created_at")
        return {
            "message": "All contact queries fetched successfully",
            "data": json.loads(data.to_json()),
            "status": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch contacts: {str(e)}")
