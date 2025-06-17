from http.client import HTTPException
import json
from fastapi import APIRouter

from Zodex.Counters.models.Counters import CountersModel, CountersTable



router = APIRouter()

@router.post("/api/v1/add-counters")
async def addCounters(body: CountersModel):
    savedata = CountersTable(**body.dict())
    savedata.save()
    
    return {
        "message": "Counters Added",
        "status":200
    }


@router.get("/api/v1/get-all-counters")
async def getAllCounters():
    findata = CountersTable.objects.all()
    return {
        "message": "all Counters",
        "data": json.loads(findata.to_json()),
        "status": 200
    }

@router.put("/api/v1/update-counters/{counter_id}")
async def updateCounter(counter_id: str, body: CountersModel):
    query = counter_id.replace("-", " ")
    try:
        counter = CountersTable.objects(id=query).first()
        if not counter:
            raise HTTPException(status_code=404, detail="Counter not found")  
        counter.modify(
            build=body.build,
            identity=body.identity,
            growth=body.growth,
        )   
        counter.reload()  

        return {
            "message": "Counter updated successfully",
            "data": json.loads(counter.to_json())
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



@router.delete("/api/v1/deleteCounters")
def delete_all_samples():
    deleted = CountersTable.objects.all().delete()
    return {
        "message": f"Deleted  successfully",
        "status": 200
    }