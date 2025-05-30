from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Schema cho thông tin sản phẩm tương tự
class SimilarProductResponse(BaseModel):
    product_id: int
    name: str
    price: float
    similarity_score: float
    image_url: Optional[str] = None

# Schema cho kết quả lấy sản phẩm tương tự
class SimilarProductsResult(BaseModel):
    success: bool
    message: Optional[str] = None
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    similar_products: List[SimilarProductResponse] = []

# Schema cho thông tin sản phẩm được gợi ý
class RecommendedProductResponse(BaseModel):
    product_id: int
    name: str
    price: float
    recommendation_score: Optional[float] = None
    image_url: Optional[str] = None

# Schema cho kết quả gợi ý sản phẩm cá nhân hóa
class PersonalizedRecommendationsResult(BaseModel):
    success: bool
    message: Optional[str] = None
    user_id: Optional[int] = None
    recommendations: List[RecommendedProductResponse] = []
    recommendation_type: str  # 'personalized', 'based_on_history', 'latest_products'
    based_on_product_id: Optional[int] = None
    based_on_product_name: Optional[str] = None

# Schema cho kết quả kích hoạt job huấn luyện
class TrainingJobResult(BaseModel):
    success: bool
    message: str
    job_result: Optional[Dict[str, Any]] = None

# Schema cho mỗi bản ghi lịch sử huấn luyện
class TrainingHistoryItem(BaseModel):
    history_id: int
    start_time: str
    end_time: Optional[str] = None
    status: str  # 'RUNNING', 'SUCCESS', 'FAILED'
    triggered_by: str  # 'SCHEDULED' hoặc ID của admin
    message: Optional[str] = None
    duration_minutes: Optional[float] = None

# Schema cho danh sách lịch sử huấn luyện
class TrainingHistoryResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    history: List[TrainingHistoryItem] = []
    total_count: int

# Schema cho chi tiết một job huấn luyện
class TrainingJobDetailResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    job: Optional[TrainingHistoryItem] = None
    metrics: Optional[Dict[str, Any]] = None  # Các thông số về model performance