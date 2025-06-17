from fastapi import APIRouter, HTTPException
from bson import ObjectId
from Zodex.blog_category.models.blog_category_model import CategoryTable
from Zodex.blogs.models.blogs_model import BlogModel, BlogTable
from mongoengine import Document, StringField
import json
from bson.errors import InvalidId


router = APIRouter()


def is_valid_object_id(id_str: str) -> bool:
    return ObjectId.is_valid(id_str)


@router.post("/api/v1/add-blog")
async def add_blog(body: BlogModel):
    if not is_valid_object_id(body.category):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    category = CategoryTable.objects(id=ObjectId(body.category)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    data = BlogTable(**body.dict(exclude={"category"}), category=category)
    data.save()

    return {
        "message": "Blog added successfully",
        "status": True,
        "data": json.loads(data.to_json())
    }


@router.get("/api/v1/all-blogs")
async def get_all_blogs():
    try:
        blogs = BlogTable.objects.all() 
        blog_list = []

        for blog in blogs:
            blog_dict = blog.to_mongo().to_dict()
            blog_dict["_id"] = str(blog.id)
            blog_dict["created_at"] = blog.created_at
            blog_dict["updated_at"] = blog.updated_at

            # Dereference the category object
            if blog.category:
                blog_dict["category"] = {
                    "id": str(blog.category.id),
                    "name": blog.category.name
                }
            else:
                blog_dict["category"] = None

            blog_list.append(blog_dict)

        return {
            "message": "Blogs fetched successfully",
            "data": blog_list,
            "status": 200
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching blogs: {str(e)}")

@router.get("/api/v1/get-Blog/{seo_title}")
async def get_blog_by_seo_title(seo_title: str):
    query = seo_title.replace("-", " ")
    data = BlogTable.objects(seo_title=query).first()
    if not data:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {
        "message": "Blog found",
        "status": True,
        "data": json.loads(data.to_json())
    }


@router.get("/api/v1/get-Blog-by-id/{blog_id}")
async def get_blog_by_id(blog_id: str):
    if not is_valid_object_id(blog_id):
        raise HTTPException(status_code=400, detail="Invalid blog ID")

    data = BlogTable.objects(id=ObjectId(blog_id)).first()
    if not data:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {
        "message": "Blog found",
        "status": True,
        "data": json.loads(data.to_json())
    }


@router.delete("/api/v1/delete-blog/{blog_id}")
async def delete_blog(blog_id: str):
    if not is_valid_object_id(blog_id):
        raise HTTPException(status_code=400, detail="Invalid blog ID")

    data = BlogTable.objects(id=ObjectId(blog_id)).first()
    if not data:
        raise HTTPException(status_code=404, detail="Blog not found")

    try:
        data.delete()
        return {
            "message": "Blog deleted successfully",
            "status": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting blog: {str(e)}")

@router.put("/api/v1/update-Blog/{blog_id}")
async def update_blog(blog_id: str, body: BlogModel):
    if not is_valid_object_id(blog_id):
        raise HTTPException(status_code=400, detail="Invalid blog ID")

    blog = BlogTable.objects(id=ObjectId(blog_id)).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # Validate category before update
    if not is_valid_object_id(body.category):
        raise HTTPException(status_code=400, detail="Invalid category ID")
    category = CategoryTable.objects(id=ObjectId(body.category)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    blog.update(**body.dict(exclude={"category"}), category=category)
    updated = BlogTable.objects(id=ObjectId(blog_id)).first()
    return {
        "message": "Blog updated successfully",
        "status": True,
        "data": json.loads(updated.to_json())
    }

@router.delete("/api/v1/delete-all-blogs")
def delete_all_blogs():
    BlogTable.objects.all().delete()
    return {
        "message": "All Blogs deleted successfully",
        "status": 200
    }