from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
app = FastAPI()
MONGO_DB_URL = 'mongodb://localhost:27017'
MONGO_DB_NAME = "FastAPI2"
appinsights_collection_name = "Appinsights"
application_collection_name = "Application"
process_collection_name = "Process"
class MongoDB:
    client: AsyncIOMotorClient = None
db = MongoDB()
async def get_database() -> AsyncIOMotorClient:
    return db.client[MONGO_DB_NAME]
async def connect_to_mongo():
    db.client = AsyncIOMotorClient(MONGO_DB_URL)
async def close_mongo_connection():
    db.client.close()
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)
class AppInsights(BaseModel):
    Appname: str
    ClientID: str
    Cluster: str
    ProcessName: str
class AppInsightsInDB(AppInsights):
    id: str
class Application(BaseModel):
    Appname: str
    Apptype: str
    Description: str
class ApplicationInDB(Application):
    id: str
class Process(BaseModel):
    ProcessName: str
    ProcessDescription: str
    Appname: str
class ProcessInDB(Process):
    id: str
@app.get("/appinsights", response_model=List[AppInsightsInDB])
async def get_appinsights():  # Modified
    await connect_to_mongo()
    db = await get_database()
    appinsights = await (db[appinsights_collection_name]
                         .find({}).to_list(None))
    return [AppInsightsInDB(**appinsights, id=str(appinsights["_id"]))
            for appinsights in appinsights]
@app.post("/appinsights", response_model=AppInsightsInDB)
async def create_appinsights(appinsights: AppInsights):
    db = await get_database()
    appinsights_dict = appinsights.dict()
    result = await (db[appinsights_collection_name]
                    .insert_one(appinsights_dict))
    created_appinsights = await (db[appinsights_collection_name]
                                 .find_one({"_id": result.inserted_id}))
    if created_appinsights:
        return AppInsightsInDB(**created_appinsights,
                               id=str(created_appinsights["_id"]))
    else:
        raise HTTPException(status_code=500,
                            detail="Failed to create AppInsights")
@app.put("/appinsights/{appinsights_id}", response_model=AppInsightsInDB)
async def update_appinsights(appinsights_id: str, appinsights: AppInsights):
    db = await get_database()
    appinsights_dict = appinsights.dict()
    result = await db[appinsights_collection_name].update_one(
        {"_id": ObjectId(appinsights_id)},
        {"$set": appinsights_dict}
    )
    if result.modified_count == 1:
        updated_appinsights = await (db[appinsights_collection_name]
        .find_one({"_id": ObjectId(appinsights_id)}))
        return AppInsightsInDB(**updated_appinsights,
                               id=str(updated_appinsights["_id"]))
    else:
        raise HTTPException(status_code=404, detail="AppInsights not found")
@app.delete("/appinsights/{appinsights_id}", response_model=dict)
async def delete_appinsights_by_id(appinsights_id: str):
    db = await get_database()
    existing_appinsights = await (db[appinsights_collection_name]
                                  .find_one({"_id": ObjectId(appinsights_id)}))
    if existing_appinsights is None:
        raise HTTPException(status_code=404,
                            detail="AppInsights not found")
    result = await (db[appinsights_collection_name]
                    .delete_one({"_id": ObjectId(appinsights_id)}))
    if result.deleted_count == 1:
        return {"message": f"AppInsights with ID '{appinsights_id}'deleted successfully"}
    else:
        raise HTTPException(status_code=500,
                            detail="An error occurred while deleting the AppInsights")
@app.get("/applications", response_model=List[ApplicationInDB])
async def get_applications():
    await connect_to_mongo()
    db = await get_database()
    applications = await (db[application_collection_name]
                          .find({}).to_list(None))
    return [ApplicationInDB(**application, id=str(application["_id"]))
            for application in applications]
@app.post("/applications", response_model=ApplicationInDB)
async def create_application(application: Application):
    db = await get_database()
    application_dict = application.dict()
    result = await (db[application_collection_name]
                    .insert_one(application_dict))
    created_application = await (db[application_collection_name]
                                 .find_one({"_id": result.inserted_id}))
    if created_application:
        return ApplicationInDB(**created_application,
                               id=str(created_application["_id"]))
    else:
        raise HTTPException(status_code=500,
                            detail="Failed to create Application")
@app.put("/applications/{application_id}", response_model=ApplicationInDB)
async def update_application(application_id: str, application: Application):
    db = await get_database()
    application_dict = application.dict()
    result = await db[application_collection_name].update_one(
        {"_id": ObjectId(application_id)},
        {"$set": application_dict}
    )
    if result.modified_count == 1:
        updated_application = await (db[application_collection_name]
        .find_one({"_id": ObjectId(application_id)}))
        return ApplicationInDB(**updated_application,
                               id=str(updated_application["_id"]))
    else:
        raise HTTPException(status_code=404,
                            detail="Application not found")
@app.delete("/applications/{application_id}", response_model=dict)
async def delete_application_by_id(application_id: str):
    db = await get_database()
    existing_application = await (db[application_collection_name]
                                  .find_one({"_id": ObjectId(application_id)}))
    if existing_application is None:
        raise HTTPException(status_code=404,
                            detail="Application not found")
    result = await (db[application_collection_name]
                    .delete_one({"_id": ObjectId(application_id)}))
    if result.deleted_count == 1:
        return {"message": f"Application with ID '{application_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=500,
                            detail="An error occurred while deleting the Application")
@app.get("/processes", response_model=List[ProcessInDB])
async def get_processes():
    await connect_to_mongo()
    db = await get_database()
    processes = await db[process_collection_name].find({}).to_list(None)
    return [ProcessInDB(**process, id=str(process["_id"])) for process in processes]
@app.post("/processes", response_model=ProcessInDB)
async def create_process(process: Process):
    db = await get_database()
    process_dict = process.dict()
    result = await db[process_collection_name].insert_one(process_dict)
    created_process = await (db[process_collection_name]
                             .find_one({"_id": result.inserted_id}))
    if created_process:
        return ProcessInDB(**created_process,
                           id=str(created_process["_id"]))
    else:
        raise HTTPException(status_code=500,
                            detail="Failed to create Process")
@app.put("/processes/{process_id}", response_model=ProcessInDB)
async def update_process(process_id: str, process: Process):
    db = await get_database()
    process_dict = process.dict()
    result = await db[process_collection_name].update_one(
        {"_id": ObjectId(process_id)},
        {"$set": process_dict}
    )
    if result.modified_count == 1:
        updated_process = await (db[process_collection_name]
                                 .find_one({"_id": ObjectId(process_id)}))
        return ProcessInDB(**updated_process,
                           id=str(updated_process["_id"]))
    else:
        raise HTTPException(status_code=404,
                            detail="Process not found")
@app.delete("/processes/{process_id}", response_model=dict)
async def delete_process_by_id(process_id: str):
    db = await get_database()
    existing_process = await (db[process_collection_name]
                              .find_one({"_id": ObjectId(process_id)}))
    if existing_process is None:
        raise HTTPException(status_code=404,
                            detail="Process not found")
    result = await (db[process_collection_name]
                    .delete_one({"_id": ObjectId(process_id)}))
    if result.deleted_count == 1:
        return {"message": f"Process with ID '{process_id}' deleted successfully"}
    else:
        raise HTTPException(status_code=500,
                            detail="An error occurred while deleting the Process")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
