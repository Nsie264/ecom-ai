from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.api.dependencies.db import get_db
# from app.api.dependencies.auth import get_current_user # Bỏ comment nếu cần xác thực
# from app.models.user import User # Bỏ comment nếu cần User model
from app.api.schemas.product import (
    ProductListItem, 
    ProductSearchResult, 
    ProductResponse,
    ProductCreate, 
    ProductUpdate,
    CategorySimpleResponse, 
    ProductAdminSearchResult
)
from app.services.product_service import ProductService
# from app.services.category_service import CategoryService # Bỏ comment nếu cần CategoryService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_new_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user) # Bỏ qua xác thực
):
    """
    Tạo một sản phẩm mới.
    """
    product_service = ProductService(db)
    try:
        product = product_service.create_product(product_data=product_in)
    except ValueError as e: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    # Cần chuyển đổi product model sang ProductResponse schema
    # Giả sử ProductService.get_product_by_id trả về định dạng phù hợp hoặc có một hàm helper
    # Tạm thời trả về product model, cần điều chỉnh để phù hợp với ProductResponse
    # Hoặc gọi lại get_product_by_id để lấy đầy đủ thông tin theo schema
    detailed_product = product_service.get_product_by_id(product.product_id)
    if not detailed_product:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not retrieve created product details")
    return detailed_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_existing_product(
    product_in: ProductUpdate, # Sửa thứ tự tham số
    product_id: int = Path(..., title="The ID of the product to update", ge=1),
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user) # Bỏ qua xác thực
):
    """
    Cập nhật một sản phẩm đã có.
    """
    product_service = ProductService(db)
    
    # Kiểm tra sản phẩm có tồn tại không bằng cách gọi get_product_by_id
    # This initial check ensures we are trying to update a product that is currently findable (typically active).
    # If the goal is to allow updating an already inactive product, this check might need to be more lenient
    # or use a service method that finds products regardless of active status for the check.
    existing_product_details = product_service.get_product_by_id(product_id)
    if not existing_product_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or not active, cannot be updated")

    try:
        # product_service.update_product returns the ORM model instance
        updated_product_orm = product_service.update_product(product_id=product_id, product_data=product_in)
    except ValueError as e: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    if not updated_product_orm: 
        # This case implies an issue within product_service.update_product or repository.update_product
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update product in the repository")
    
    # Trả về thông tin chi tiết sản phẩm đã cập nhật.
    # Crucially, use allow_inactive=True (assuming ProductService.get_product_by_id is updated to support this)
    # to ensure we can fetch and return the product even if the update made it inactive.
    response_product_details = product_service.get_product_by_id(updated_product_orm.product_id, allow_inactive=True)
    
    if not response_product_details:
        # This would be an unexpected error if the product was just updated and allow_inactive=True is honored.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not retrieve complete product details after update.")
        
    return response_product_details

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_existing_product(
    product_id: int = Path(..., title="The ID of the product to delete", ge=1),
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user) # Bỏ qua xác thực
):
    """
    Xóa một sản phẩm (xóa mềm bằng cách đặt is_active=False).
    API này không yêu cầu quyền admin.
    """
    product_service = ProductService(db)
    
    # Kiểm tra sản phẩm có tồn tại và đang active không
    existing_product_details = product_service.get_product_by_id(product_id) # get_product_by_id đã kiểm tra is_active
    if not existing_product_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or already inactive")

    deleted_product = product_service.delete_product(product_id=product_id)
    if not deleted_product or deleted_product.is_active: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete product")
    return {"message": "Product deleted successfully (soft delete)", "product_id": product_id}

@router.get("/", response_model=ProductSearchResult)
async def search_products(
    search_query: Optional[str] = Query(None, description="Từ khóa tìm kiếm"),
    category_id: Optional[int] = Query(None, description="ID danh mục"),
    min_price: Optional[float] = Query(None, description="Giá tối thiểu"),
    max_price: Optional[float] = Query(None, description="Giá tối đa"),
    order_by: str = Query("created_at", description="Sắp xếp theo: name, price, created_at"),
    descending: bool = Query(True, description="Sắp xếp giảm dần"),
    page: int = Query(1, gt=0, description="Số trang"),
    page_size: int = Query(20, gt=0, le=100, description="Số sản phẩm mỗi trang"),
    db: Session = Depends(get_db),
    # current_user: Optional[User] = Depends(get_current_user) # Bỏ qua xác thực
):
    """
    Tìm kiếm sản phẩm với nhiều bộ lọc khác nhau.
    """
    product_service = ProductService(db)
    # user_id = current_user.user_id if current_user else None # Bỏ qua user_id
    user_id = None
    
    result = product_service.search_products(
        search_query=search_query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        order_by=order_by,
        descending=descending,
        page=page,
        page_size=page_size,
        user_id=user_id
    )
    
    return result

@router.get("/mananger", response_model=ProductAdminSearchResult)
async def search_products_mananger(
    search_query: Optional[str] = Query(None, description="Từ khóa tìm kiếm"),
    category_id: Optional[int] = Query(None, description="ID danh mục"),
    min_price: Optional[float] = Query(None, description="Giá tối thiểu"),
    max_price: Optional[float] = Query(None, description="Giá tối đa"),
    order_by: str = Query("created_at", description="Sắp xếp theo: name, price, created_at"),
    descending: bool = Query(True, description="Sắp xếp giảm dần"),
    page: int = Query(1, gt=0, description="Số trang"),
    page_size: int = Query(20, gt=0, le=100, description="Số sản phẩm mỗi trang"),
    db: Session = Depends(get_db),
    # current_user: Optional[User] = Depends(get_current_user) # Bỏ qua xác thực
):
    """
    Tìm kiếm sản phẩm với nhiều bộ lọc khác nhau.
    """
    product_service = ProductService(db)
    # user_id = current_user.user_id if current_user else None # Bỏ qua user_id
    user_id = None
    
    result = product_service.search_products_mananger(
        search_query=search_query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        order_by=order_by,
        descending=descending,
        page=page,
        page_size=page_size,
        user_id=user_id
    )
    
    return result


@router.get("/{product_id}", response_model=ProductResponse) 
async def get_product_details_by_id( # Đổi tên hàm để tránh trùng lặp
    product_id: int = Path(..., gt=0, description="ID của sản phẩm"),
    db: Session = Depends(get_db),
    # current_user: Optional[User] = Depends(get_current_user) # Bỏ qua xác thực
):
    """
    Lấy thông tin chi tiết của một sản phẩm.
    """
    product_service = ProductService(db)
    # user_id = current_user.user_id if current_user else None # Bỏ qua user_id
    user_id = None
    
    product = product_service.get_product_by_id(product_id, user_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sản phẩm không tồn tại hoặc không khả dụng"
        )
    
    return product

# Giữ lại hàm get_categories trả về danh sách phẳng
@router.get("/categories/", response_model=List[CategorySimpleResponse], summary="Get Flat List of Categories")
async def get_flat_categories_list(db: Session = Depends(get_db)):
    """
    Lấy danh sách tất cả danh mục sản phẩm (dạng phẳng).
    """
    product_service = ProductService(db)
    categories = product_service.get_categories() # Hàm này trả về list dict
    return categories


@router.get("/categories/tree", summary="Get Category Tree (Not Implemented Yet)") 
async def get_categories_tree(db: Session = Depends(get_db)):
    """
    Lấy danh sách danh mục theo cấu trúc cây.
    (Chức năng này chưa được triển khai đầy đủ, hiện tại có thể trả về lỗi hoặc danh sách phẳng.)
    """
    # product_service = ProductService(db)
    # # Hiện tại ProductService.get_categories() trả về list phẳng.
    # # Cần một service khác hoặc logic khác để build cây.
    # # Ví dụ: return category_service.get_category_tree() 
    # return product_service.get_categories() # Tạm thời trả về danh sách phẳng hoặc lỗi
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Get category tree is not implemented yet.")