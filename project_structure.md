# Cấu trúc dự án eCommerce AI

```
ecom_AI/
├── bao_cao.md                           # Báo cáo thiết kế hệ thống
├── main.py                              # File chính để khởi động ứng dụng FastAPI
├── requirements.txt                     # Danh sách các thư viện cần thiết
├── app/                                 # Thư mục chính chứa mã nguồn ứng dụng
│   ├── api/                             # Xử lý API và endpoint
│   │   ├── api.py                       # Router chính đăng ký tất cả các endpoints
│   │   ├── dependencies/                # Dependencies cho API
│   │   │   ├── auth.py                  # Xác thực người dùng (hàm get_current_user, create_access_token)
│   │   │   └── db.py                    # Dependency để cung cấp database session
│   │   ├── endpoints/                   # Các endpoints API
│   │   │   ├── auth.py                  # API xác thực (đăng nhập, đăng ký, thông tin người dùng, địa chỉ)
│   │   │   ├── cart.py                  # API giỏ hàng
│   │   │   ├── orders.py                # API đơn hàng (tạo đơn, hủy đơn, xem lịch sử)
│   │   │   ├── products.py              # API sản phẩm (tìm kiếm, chi tiết, danh mục)
│   │   │   └── recommendations.py       # API gợi ý sản phẩm (gợi ý cá nhân, sản phẩm tương tự)
│   │   └── schemas/                     # Schemas để validate dữ liệu
│   │       ├── __init__.py              # Khởi tạo package
│   │       ├── cart.py                  # Schemas giỏ hàng (CartResponse, AddToCartRequest...)
│   │       ├── order.py                 # Schemas đơn hàng (OrderListResponse, CreateOrderRequest...)
│   │       ├── product.py               # Schemas sản phẩm (ProductResponse, ProductListItem...)
│   │       ├── recommendation.py        # Schemas gợi ý (SimilarProductsResult, PersonalizedRecommendationsResult...)
│   │       └── user.py                  # Schemas người dùng (UserResponse, AddressResponse, Token...)
│   ├── core/                            # Các thành phần core của ứng dụng
│   │   └── config.py                    # Cấu hình hệ thống (settings)
│   ├── db/                              # Kết nối và quản lý database
│   │   ├── base.py                      # Cấu hình kết nối database
│   │   └── init_db.py                   # Khởi tạo database, tạo admin
│   ├── models/                          # Models SQLAlchemy
│   │   ├── interaction.py               # Model tương tác người dùng (ViewHistory, CartItem, ProductRating...)
│   │   ├── order.py                     # Model đơn hàng (Order, OrderItem, OrderStatus, PaymentMethod)
│   │   ├── product.py                   # Model sản phẩm (Product, Category, ProductImage, Tag...)
│   │   ├── recommendation.py            # Model lưu kết quả gợi ý (UserRecommendation, ProductSimilarity)
│   │   └── user.py                      # Model người dùng (User, UserAddress)
│   ├── recommendations/                 # Module 1: Huấn luyện mô hình gợi ý
│   │   ├── repositories/                # Tầng truy cập dữ liệu cho gợi ý
│   │   │   └── recommendation_repository.py   # ProductSimilarityRepository, UserRecommendationRepository
│   │   └── training/                    # Các thành phần huấn luyện mô hình
│   │       ├── data_loader.py           # DataLoader - tải dữ liệu tương tác từ DB
│   │       ├── data_preprocessor.py     # DataPreprocessor - xử lý dữ liệu trước khi huấn luyện
│   │       ├── job.py                   # TrainingJob - điều phối quá trình huấn luyện
│   │       ├── model_trainer.py         # ModelTrainer - huấn luyện mô hình Collaborative Filtering
│   │       └── result_writer.py         # RecommendationResultWriter - lưu kết quả vào DB
│   ├── repositories/                    # Tầng truy cập dữ liệu cho Module 2,3
│   │   ├── __init__.py                  # Khởi tạo package
│   │   ├── interaction_repository.py    # ViewHistoryRepository, CartRepository, ProductRatingRepository
│   │   ├── order_repository.py          # OrderRepository, OrderItemRepository
│   │   ├── product_repository.py        # ProductRepository, CategoryRepository, TagRepository
│   │   ├── training_history_repository.py # TrainingHistoryRepository - quản lý lịch sử huấn luyện mô hình
│   │   └── user_repository.py           # UserRepository, UserAddressRepository
│   └── services/                        # Tầng logic nghiệp vụ
│       ├── cart_service.py              # CartService - xử lý giỏ hàng
│       ├── order_service.py             # OrderService - xử lý đơn hàng
│       ├── product_service.py           # ProductService - xử lý sản phẩm
│       ├── recommendation_service.py    # RecommendationService - xử lý gợi ý sản phẩm
│       └── user_service.py              # UserService - xử lý người dùng
└── tests/                               # Thư mục chứa tests
    ├── integration/                     # Tests tích hợp
    └── unit/                            # Unit tests
```

## Phân chia chức năng theo modules:

### Module 1: Huấn luyện mô hình gợi ý sản phẩm

- `app/recommendations/` - Chứa toàn bộ logic huấn luyện mô hình
  - `DataLoader` - Tải dữ liệu tương tác từ DB
  - `DataPreprocessor` - Chuẩn bị và làm sạch dữ liệu
  - `ModelTrainer` - Huấn luyện mô hình Matrix Factorization
  - `RecommendationResultWriter` - Lưu kết quả gợi ý
  - `TrainingJob` - Điều phối toàn bộ quy trình huấn luyện

### Module 2: Tìm chọn và đặt mua hàng online

- `app/models/product.py`, `app/models/order.py` - Định nghĩa cấu trúc dữ liệu
- `app/repositories/product_repository.py`, `app/repositories/order_repository.py` - Truy cập dữ liệu
- `app/services/product_service.py`, `app/services/cart_service.py`, `app/services/order_service.py` - Logic nghiệp vụ
- `app/api/endpoints/products.py`, `app/api/endpoints/cart.py`, `app/api/endpoints/orders.py` - API endpoints

### Module 3: Gợi ý sản phẩm cho khách hàng

- `app/models/recommendation.py` - Lưu trữ kết quả gợi ý
- `app/recommendations/repositories/recommendation_repository.py` - Truy cập dữ liệu gợi ý
- `app/services/recommendation_service.py` - Logic nghiệp vụ gợi ý
- `app/api/endpoints/recommendations.py` - API endpoints gợi ý

### Chức năng xác thực và quản lý người dùng

- `app/models/user.py` - Model người dùng và địa chỉ
- `app/repositories/user_repository.py` - Truy cập dữ liệu người dùng
- `app/services/user_service.py` - Logic nghiệp vụ người dùng
- `app/api/dependencies/auth.py` - Xác thực JWT
- `app/api/endpoints/auth.py` - API endpoints người dùng
