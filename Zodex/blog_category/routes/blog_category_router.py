from fastapi import APIRouter, HTTPException
from bson import ObjectId
import json

from Zodex.blog_category.models.blog_category_model import CategoryModel, CategoryTable

router = APIRouter()


@router.post("/api/v1/add-category")
def add_category(body: CategoryModel):
    cat = CategoryTable(**body.dict())
    cat.save()
    return {"message": "Category added", "status": 200}


@router.get("/api/v1/get-all-categories")
def get_all_categories():
    categories = CategoryTable.objects.all()
    return {
        "message": "All categories",
        "data": json.loads(categories.to_json()),
        "status": 200
    }


@router.delete("/api/v1/delete-category/{category_id}")
def delete_category_by_id(category_id: str):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    category = CategoryTable.objects(id=ObjectId(category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.delete()
    return {
        "message": "Category deleted successfully",
        "status": 200
    }
