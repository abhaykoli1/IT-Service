from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from mongoengine import connect
import os
from fastapi.responses import RedirectResponse
import secrets


# Import routers
from Zodex.Counters.routes import CounterRoutes
from Zodex.Queries.routes import contact_router
from Zodex.Services.routes import ServiceRoute
from Zodex.Products.routes import ProductsRoute
from Zodex.blog_category.routes import blog_category_router
from Zodex.blogs.routes import blogs_routes
from Zodex.prices.routes import price_router
from Zodex.work.routes import work_router

# MongoDB connection
# connect('Zodexweb', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/Zodexweb")

def connect_to_mongo():
    try:
        mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/Zodexweb")
        connect('Zodexweb', host=mongo_uri)
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

connect_to_mongo()

# Disable default docs
app = FastAPI(docs_url=None, redoc_url=None)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth for docs
security = HTTPBasic()
USERNAME = "admin"
PASSWORD = "ipkoliki"

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Secure docs route
@app.get("/docs", include_in_schema=False)
async def get_documentation(username: str = Depends(verify_credentials)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Zodex API Docs")

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(verify_credentials)):
    return JSONResponse(get_openapi(title="Zodex API", version="1.0.0", routes=app.routes))

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/unauthorized")
    response.status_code = 401  # Forces re-prompt
    return response

@app.get("/unauthorized")
def unauthorized():
    return {"message": "You have been logged out. Please refresh and re-login."}

# Include routers
app.include_router(blogs_routes.router, tags=['Blogs'])
app.include_router(blog_category_router.router, tags=['Blog Category'])
app.include_router(work_router.router, tags=['Work'])
app.include_router(price_router.router, tags=['Price'])
app.include_router(CounterRoutes.router, tags=['Counters'])
app.include_router(ServiceRoute.router, tags=['Services'])
app.include_router(ProductsRoute.router, tags=['Products'])
app.include_router(contact_router.router, tags=["contact query"])

# Static assets
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

# Fallback for React frontend
@app.get("/{full_path:path}")
async def serve_react_app():
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found"}

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8080, reload=True)
