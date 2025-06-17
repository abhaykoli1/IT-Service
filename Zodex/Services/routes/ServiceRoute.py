from http.client import HTTPException
from Zodex.Services.models.ServiceModel import ServiceModel, ServiceTable
import json
from bson import ObjectId
from fastapi import FastAPI, APIRouter
from bson.errors import InvalidId

router= APIRouter()



@router.post("/api/v1/add-service")
async def addService(body : ServiceModel):
    serviceData = ServiceTable(**body.dict())
    serviceData.save()
    toJson = serviceData.to_json()
    fromJson = json.loads(toJson)
    return{
        "message" : "data added successfully",
        "status" : True,
        "data" :  fromJson
    }

@router.get("/api/v1/all-services")
async def serviceList():
    serviceListData = ServiceTable.objects.all()
    toJson = serviceListData.to_json()
    fromJson = json.loads(toJson)
    if(serviceListData): 
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

@router.get("/api/v1/get-Service/{_id}")
async def get_service(_id: str):
    query = _id.replace("-", " ")
    service = ServiceTable.objects(id=query).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return {
        "message": "Service data",
        "data": json.loads(service.to_json()),
        "status": 200
    }

@router.put("/api/v1/update-Service/{_id}")
async def update_service(_id: str, body: ServiceModel):
    query = _id.replace("-", " ")
    try:
        service = ServiceTable.objects(id=query).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        # Update the document using `modify`
        service.modify(
            icon=body.icon,
            title=body.title,
            description=body.description
        )
        service.reload()  # Reload to get updated data

        return {
            "message": "Service updated successfully",
            "data": json.loads(service.to_json())
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/api/v1/delete-all-services")
async def deleteServices():
   deleteServiceData = ServiceTable.objects.delete()
   if deleteServiceData == 0:
      return{
         "message" : "data Deleted Successfully",
         "status" : True,
         "data" : None
      }
   


@router.delete("/api/v1/delete-by-id/{_id}")
async def ServiceDeleteById(_id: str):
    try:
        # Validate ObjectId
        object_id = ObjectId(_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    item = ServiceTable.objects(id=object_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        item.delete()
        return {
            "message": "Service deleted successfully",
            "status": True,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting service: {str(e)}")