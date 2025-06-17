from http.client import HTTPException
import json
from bson import ObjectId
from fastapi import FastAPI ,APIRouter

from Zodex.Products.models.ProductsModel import ProductModel, ProductTable


router= APIRouter()

@router.post("/api/v1/AddProduct")
async def addProduct(body : ProductModel):
    ProductData = ProductTable(**body.dict())
    ProductData.save()
    toJson = ProductData.to_json()
    fromJson = json.loads(toJson)
    return{
        "message" : "data added successfully",
        "status" : True,
        "data" :  fromJson
    }
    
@router.get("/api/v1/ProductList")
async def ProductList():
    ProductListData = ProductTable.objects.all()
    toJson = ProductListData.to_json()
    fromJson = json.loads(toJson)
    if(ProductListData): 
      return{
        "message" : "Data Fetched Successfully",
        "status" : True,
        "data" : fromJson,
    }
    else:
       return{
          "message" : "Data Not Found",
          "status" : False,
          "data": None
       }
       
       
@router.get("/api/v1/get-Product/{_id}")
async def get_product(_id: str):
    query = _id.replace("-", " ")
    product = ProductTable.objects(id=query).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "message": "Product data",
        "data": json.loads(product.to_json()),
        "status": 200
    }

@router.put("/api/v1/update-Product/{_id}")
async def update_product(_id: str, body: ProductModel):
    query = _id.replace("-", " ")
    try:
        product = ProductTable.objects(id=query).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Update the document using `modify`
        product.modify(
            image=body.image,
            title=body.title,
            type=body.type,
        )
        product.reload()  # Reload to get updated data

        return {
            "message": "Product updated successfully",
            "data": json.loads(product.to_json())
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

  
@router.delete("/api/v1/DeleteAllProducts")
async def deleteProducts():
   deleteProductData = ProductTable.objects.delete()
   if deleteProductData == 0:
      return{
         "message" : "data Deleted Successfully",
         "status" : True,
         "data" : None
      }
   
@router.delete("/api/v1/DeleteAProduct/{_id}")
async def ServiceDeleteById(_id : str):
    object_id = ObjectId(_id)
    item = ProductTable.objects(id=object_id).first()
    item.delete()
    
    return {
        "message": "Data Deleted Successfully",
        "status": True,
    }