from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.api.dependencies.db import get_db
from app.api.dependencies.auth import get_current_user
from app.api.schemas.recommendation import (
    SimilarProductsResult, PersonalizedRecommendationsResult, TrainingJobResult,
    TrainingHistoryResponse, TrainingJobDetailResponse
)
from app.services.recommendation_service import RecommendationService
from app.models.user import User

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/similar/{product_id}", response_model=SimilarProductsResult)
async def get_similar_products(
    product_id: int = Path(..., gt=0),
    limit: int = Query(10, gt=0, le=50),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách sản phẩm tương tự với một sản phẩm cụ thể.
    Endpoint này hiển thị trên trang chi tiết sản phẩm.
    """
    recommendation_service = RecommendationService(db)
    result = recommendation_service.get_similar_products(
        product_id=product_id,
        limit=limit
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["message"]
        )
    
    return result

@router.get("/personalized", response_model=PersonalizedRecommendationsResult)
async def get_personalized_recommendations(
    limit: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy danh sách sản phẩm được gợi ý cá nhân hóa cho người dùng hiện tại.
    Endpoint này hiển thị trên trang chính hoặc trang gợi ý riêng.
    """
    recommendation_service = RecommendationService(db)
    result = recommendation_service.get_personalized_recommendations(
        user_id=current_user.user_id,
        limit=limit
    )
    
    return result

@router.post("/train", response_model=TrainingJobResult)
async def trigger_training_job(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Kích hoạt job huấn luyện mô hình gợi ý theo yêu cầu thủ công.

    """
    # Kiểm tra quyền admin (giả sử có trường is_admin trong model User)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền thực hiện hành động này"
        )
    
    recommendation_service = RecommendationService(db)
    result = recommendation_service.trigger_training_job(admin_id=str(current_user.user_id))
    
    return result

@router.get("/training-history", response_model=TrainingHistoryResponse)
async def get_training_history(
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy lịch sử các lần huấn luyện mô hình gợi ý.

    """
    # Kiểm tra quyền admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập thông tin này"
        )
    
    recommendation_service = RecommendationService(db)
    result = recommendation_service.get_training_history(limit=limit)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["message"]
        )
    
    # Đảm bảo response có trường total_count
    if "total_count" not in result:
        result["total_count"] = len(result["history"]) if "history" in result else 0
    
    return result

@router.get("/training-history/{history_id}", response_model=TrainingJobDetailResponse)
async def get_training_job_details(
    history_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy chi tiết của một bản ghi huấn luyện cụ thể.
    Chỉ admin mới có quyền thực hiện chức năng này.
    """
    # Kiểm tra quyền admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập thông tin này"
        )
    
    recommendation_service = RecommendationService(db)
    result = recommendation_service.get_training_job_details(history_id=history_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["message"]
        )
    
    return result