from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from mongoengine import connect
import secrets
import os

# Routers
from Zodex.Counters.routes import CounterRoutes
from Zodex.Queries.routes import contact_router
from Zodex.Services.routes import ServiceRoute
from Zodex.Products.routes import ProductsRoute
from Zodex.blog_category.routes import blog_category_router
from Zodex.blogs.routes import blogs_routes
from Zodex.prices.routes import price_router
from Zodex.work.routes import work_router

#   New Upadate
# Initialize FastAPI (disable default docs)
app = FastAPI(docs_url=None, redoc_url=None)

# Connect to MongoDB
def connect_to_mongo():
    try:
        mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/Zodexweb")
        connect('Zodexweb', host=mongo_uri)
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

connect_to_mongo()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic Auth for docs
security = HTTPBasic()
USERNAME = "admin"
PASSWORD = "ipkoliki"

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if not (secrets.compare_digest(credentials.username, USERNAME) and
            secrets.compare_digest(credentials.password, PASSWORD)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Secure Swagger docs
@app.get("/docs", include_in_schema=False)
async def get_documentation(username: str = Depends(verify_credentials)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Zodex API Docs")

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(verify_credentials)):
    return JSONResponse(get_openapi(title="Zodex API", version="1.0.0", routes=app.routes))

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/unauthorized")
    response.status_code = 401
    return response

@app.get("/unauthorized")
def unauthorized():
    return {"message": "You have been logged out. Please refresh and re-login."}

# API Routers
app.include_router(blogs_routes.router, tags=["Blogs"])
app.include_router(blog_category_router.router, tags=["Blog Category"])
app.include_router(work_router.router, tags=["Work"])
app.include_router(price_router.router, tags=["Price"])
app.include_router(CounterRoutes.router, tags=["Counters"])
app.include_router(ServiceRoute.router, tags=["Services"])
app.include_router(ProductsRoute.router, tags=["Products"])
app.include_router(contact_router.router, tags=["Contact Query"])

# Serve static assets (e.g. /assets/logo.svg)
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

# Fallback to serve React/HTML frontend
@app.get("/")
def serve_root():
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "index.html not found"}

# Wildcard fallback (optional - can break API if not careful)
@app.get("/{full_path:path}")
def fallback_static(full_path: str):
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Resource not found"}


# Only used for local dev
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


# Live
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Use $PORT for Render, fallback to 8080
    uvicorn.run("main:app", host="0.0.0.0", port=port)


