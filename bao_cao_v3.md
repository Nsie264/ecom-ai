**(Thông tin trang bìa - Bạn tự điền theo mẫu)**

- Giảng viên hướng dẫn: \[Tên Giảng viên]
- Họ và tên sinh viên: \[Tên của bạn]
- Mã sinh viên: \[Mã SV của bạn]
- Lớp: \[Lớp của bạn]
- Nhóm: \[Nhóm của bạn]

**Hà Nội – \[Năm hiện tại]**

---

**1. Giới thiệu chung**

**1.1. Tổng quan về đề tài và mục tiêu**

Đề tài tập trung vào việc xây dựng một hệ thống thương mại điện tử (E-commerce) với điểm nhấn là khả năng gợi ý sản phẩm thông minh dựa trên hành vi và thông tin của người dùng. Mục tiêu chính bao gồm:

- Xây dựng nền tảng cho phép người dùng tìm kiếm, xem, và đặt mua sản phẩm trực tuyến (**Module 2**).
- Thu thập và quản lý hiệu quả dữ liệu hành vi người dùng (lịch sử xem, mua hàng - làm đầu vào cho **Module 1**).
- Phát triển hệ thống huấn luyện mô hình gợi ý sản phẩm ứng dụng thuật toán Machine Learning (**Module 1**), bao gồm khả năng kích hoạt thủ công và theo dõi lịch sử cho quản trị viên.
- Tích hợp và hiển thị các gợi ý sản phẩm cá nhân hóa để nâng cao trải nghiệm mua sắm (**Module 3**).

**1.2. Phạm vi và giới hạn của đề tài**

- **Phạm vi:**
  - Triển khai 03 module chính được trình bày chi tiết: Huấn luyện mô hình gợi ý (**Module 1**), Chức năng tìm chọn và đặt mua hàng online (**Module 2**), Hệ thống gợi ý sản phẩm (**Module 3**).
  - Xây dựng giao diện quản trị cơ bản trên Flutter cho phép kích hoạt và xem lịch sử huấn luyện (**Module 1**).
  - Xây dựng các chức năng hỗ trợ cần thiết cho 3 module trên (ví dụ: đăng ký/đăng nhập để có user_id).
  - Áp dụng kiến trúc Monolithic cho backend và mô hình **MVC với GetX** cho frontend/backend.
  - Sử dụng CSDL MySQL để lưu trữ toàn bộ dữ liệu liên quan đến 3 module và lịch sử huấn luyện. Danh mục sản phẩm được thiết kế dạng phẳng (không phân cấp).
- **Giới hạn:**
  - Hệ thống tập trung vào 3 module chính và giao diện admin cho Module 1. Không đi sâu vào các tính năng E-commerce mở rộng khác hoặc trang quản trị toàn diện, bao gồm cả quản lý sản phẩm/danh mục chi tiết phía admin.
  - Không hỗ trợ duyệt sản phẩm theo danh mục đa cấp.
  - Thuật toán gợi ý (**Module 1**, **Module 3**) tập trung vào Collaborative Filtering (Matrix Factorization).
  - Chưa tối ưu hóa sâu về hiệu năng cho quy mô cực lớn.

**1.3. Các công nghệ chính sử dụng**

- **Back-end:** Python (Sử dụng một framework web như Flask hoặc FastAPI), SQLAlchemy (ORM).
- **Front-end:** Flutter (Kiến trúc MVC, State Management: GetX).
- **Cơ sở dữ liệu:** MySQL.
- **Machine Learning (Module 1):** Pandas, NumPy, Scikit-learn, Surprise, Implicit (tùy chọn).
- **Scheduling (Module 1):** APScheduler.

**2. Giới thiệu hệ thống**

**2.1. Mô tả tổng quan**

Hệ thống là một ứng dụng thương mại điện tử (backend Python Monolithic, frontend Flutter) tập trung vào việc cung cấp trải nghiệm mua sắm cá nhân hóa thông qua gợi ý sản phẩm thông minh. Hệ thống cho phép người dùng thực hiện các thao tác mua sắm cốt lõi, đồng thời thu thập dữ liệu hành vi để huấn luyện và đưa ra các gợi ý phù hợp. Hệ thống cũng cung cấp giao diện quản trị cơ bản cho phép theo dõi và quản lý quá trình huấn luyện mô hình gợi ý.

**2.2. Các chức năng chính liên quan đến các module trình bày**

- **Module 2 (Tìm chọn và đặt mua hàng online):**
  - Duyệt sản phẩm theo danh mục (danh sách phẳng), tìm kiếm theo từ khóa.
  - Xem chi tiết thông tin sản phẩm.
  - Quản lý giỏ hàng (thêm, sửa số lượng, xóa).
  - Thực hiện quy trình đặt hàng (chọn địa chỉ, thanh toán COD, xác nhận).
- **Module 1 (Huấn luyện mô hình gợi ý sản phẩm):**
  - _(Backend)_ Tự động thu thập dữ liệu hành vi (xem, mua) từ hoạt động của người dùng trên **Module 2**.
  - _(Backend)_ Chạy định kỳ quy trình huấn luyện mô hình Matrix Factorization.
  - _(Backend)_ Lưu trữ kết quả gợi ý (sản phẩm tương tự, gợi ý cá nhân) vào CSDL MySQL.
  - _(Backend)_ Cung cấp API cho phép kích hoạt huấn luyện thủ công và lấy lịch sử huấn luyện.
  - _(Backend)_ Ghi lại lịch sử mỗi lần chạy huấn luyện (thời gian, trạng thái) vào CSDL.
  - _(Frontend - Admin)_ Giao diện cho phép Admin kích hoạt huấn luyện thủ công.
  - _(Frontend - Admin)_ Giao diện hiển thị danh sách lịch sử các lần chạy huấn luyện.
- **Module 3 (Gợi ý sản phẩm cho khách hàng):**
  - Hiển thị gợi ý "Sản phẩm tương tự" trên trang chi tiết sản phẩm (dựa trên kết quả **Module 1**).
  - Hiển thị gợi ý "Gợi ý cho bạn" trên trang chủ cho người dùng đã đăng nhập (dựa trên kết quả **Module 1**).
- **Chức năng hỗ trợ:**
  - Đăng ký/Đăng nhập (cho cả User và Admin): Cung cấp `user_id` và phân quyền. _(Dữ liệu sản phẩm/danh mục giả định đã có sẵn trong CSDL để hệ thống hoạt động)_.

**2.3. Vai trò và vị trí của các module được trình bày**

Ba module được chọn để trình bày chi tiết có mối liên hệ chặt chẽ:

- **Module 2 (Tìm chọn và đặt mua hàng online):** Là nền tảng cung cấp giao diện tương tác chính cho người dùng và tạo ra dữ liệu hành vi (xem, mua).
- **Module 1 (Huấn luyện mô hình gợi ý sản phẩm):** Xử lý dữ liệu từ **Module 2** để tạo ra "trí thông minh" cho hệ thống gợi ý. Cung cấp khả năng quản lý và theo dõi quá trình này cho Admin.
- **Module 3 (Gợi ý sản phẩm cho khách hàng):** Sử dụng kết quả từ **Module 1** để tăng cường trải nghiệm người dùng trên **Module 2**.

**2.4. Các đối tượng người dùng và quyền hạn (liên quan đến các module)**

- **Người dùng (Khách hàng):**
  - Chưa đăng nhập: Có thể duyệt, tìm kiếm, xem sản phẩm (**Module 2**).
  - Đã đăng nhập: Sử dụng đầy đủ **Module 2** (giỏ hàng server-side, đặt hàng), nhận gợi ý cá nhân hóa từ **Module 3**. Hành vi được ghi nhận cho **Module 1**.
- **Quản trị viên (Admin):**
  - Đăng nhập với quyền Admin.
  - Truy cập giao diện quản lý huấn luyện (**Module 1**): Kích hoạt huấn luyện thủ công, xem lịch sử huấn luyện.

**3. Thiết kế chung**

**3.1. Kiến trúc theo chiều dọc: Monolithic**
Hệ thống sử dụng kiến trúc Monolithic cho ứng dụng backend. Toàn bộ logic nghiệp vụ phía server được đóng gói và triển khai như một đơn vị duy nhất.

**3.2. Kiến trúc theo chiều ngang: Mô hình MVC (Áp dụng cho cả Frontend Flutter và Backend Python)**

- **Backend (Python - Flask/FastAPI):**
  - **Model:** Các lớp ORM (SQLAlchemy) đại diện cho các bảng CSDL (`User`, `Product`, `Order`...), các lớp Pydantic/Marshmallow để validate dữ liệu request/response (DTO).
  - **View:** Không có View truyền thống. Backend đóng vai trò là API server, trả về dữ liệu dạng JSON.
  - **Controller:** Các hàm xử lý request trong Flask/FastAPI, nhận request HTTP, gọi đến lớp Service để xử lý logic, và trả về response JSON.
  - **Service:** Các lớp chứa logic nghiệp vụ chính (ví dụ: `OrderService`, `RecommendationService`).
  - **Repository:** Các lớp chịu trách nhiệm tương tác trực tiếp với CSDL MySQL thông qua ORM (ví dụ: `ProductRepository`, `OrderRepository`).
- **Frontend (Flutter):**
  - **Model:** Các lớp Dart đại diện cho dữ liệu nhận từ API (ví dụ: `UserModel`, `ProductModel`). Bao gồm cả logic parse JSON.
  - **View:** Các Widget (StatelessWidget, StatefulWidget) xây dựng giao diện người dùng (`ProductListScreen`, `ProductCard`, `CartScreen`...). View lắng nghe và phản ứng với thay đổi state từ Controller.
  - **Controller:** Các lớp `GetxController` (ví dụ: `ProductController`, `CartController`) chứa state của màn hình/module (sử dụng `.obs` cho biến phản ứng), các phương thức xử lý logic nghiệp vụ phía client (ví dụ: `fetchProducts`, `addToCart`), và gọi đến các API Service để tương tác với backend.
  - **API Service:** Các lớp chịu trách nhiệm thực hiện các lời gọi HTTP đến API backend (ví dụ: `ProductApiService`, `OrderApiService`).
  - **State Management:** Sử dụng **GetX** để quản lý state (biến `.obs`), quản lý phụ thuộc (dependency injection với `Get.put`, `Get.find`), và điều hướng (`Get.to`, `Get.back`).

**3.3. Thiết kế thực thể**

Các lớp chính trong hệ thống:

- `User`: Đại diện cho người dùng (bao gồm cả khách hàng và admin).
  - Thuộc tính: user_id, name, email, password_hash, role, created_at, updated_at.
- `UserAddress`: Địa chỉ giao hàng của người dùng.
  - Thuộc tính: address_id, user_id, street, city, country, is_default.
- `Category`: Danh mục sản phẩm (dạng phẳng).
  - Thuộc tính: category_id, name, description.
- `Product`: Sản phẩm.
  - Thuộc tính: product_id, name, description, price, category_id, stock_quantity, attributes (JSON), created_at, updated_at.
- `ProductImage`: Ảnh của sản phẩm.
  - Thuộc tính: image_id, product_id, image_url, sort_order.
- `Tag`: Nhãn/Từ khóa mô tả sản phẩm.
  - Thuộc tính: tag_id, name.
- `ProductTag`: Bảng liên kết giữa Product và Tag (quan hệ N-N).
  - Thuộc tính: product_id, tag_id.
- `Order`: Đơn hàng của người dùng.
  - Thuộc tính: order_id, user_id, order_date, total_amount, status, shipping_address (JSON), payment_method, created_at, updated_at.
- `OrderItem`: Chi tiết một sản phẩm trong đơn hàng.
  - Thuộc tính: order_item_id, order_id, product_id, quantity, price_at_purchase, product_snapshot (JSON).
- `ViewHistory`: Lịch sử xem sản phẩm của người dùng.
  - Thuộc tính: view_id, user_id, product_id, view_timestamp.
- `SearchHistory`: Lịch sử tìm kiếm của người dùng.
  - Thuộc tính: search_id, user_id, query, search_timestamp.
- `Rating`: Đánh giá sản phẩm của người dùng.
  - Thuộc tính: rating_id, user_id, product_id, score, comment, rating_timestamp.
- `CartItem`: Một sản phẩm trong giỏ hàng của người dùng.
  - Thuộc tính: cart_item_id, user_id, product_id, quantity, added_at.
- `ProductSimilarity`: Lưu trữ độ tương đồng giữa các cặp sản phẩm.
  - Thuộc tính: product_id_a, product_id_b, similarity_score.
- `UserRecommendation`: Lưu trữ gợi ý sản phẩm cá nhân hóa cho người dùng.
  - Thuộc tính: user_id, product_id, recommendation_score, generated_at.
- `TrainingHistory`: Lưu trữ lịch sử các lần chạy huấn luyện mô hình.
  - Thuộc tính: history_id, start_time, end_time, status, triggered_by, message.

**Phân tích các mối quan hệ chính:**

- `User` có nhiều `UserAddress`, `Order`, `ViewHistory`, `SearchHistory`, `Rating`, `CartItem`, `UserRecommendation`.
- `Category` có nhiều `Product`.
- `Product` thuộc một `Category`. `Product` có nhiều `ProductImage`, `ViewHistory`, `Rating`, `CartItem`, `OrderItem`, `ProductTag`. `Product` liên quan đến các `ProductSimilarity` và `UserRecommendation`.
- `Tag` có nhiều `ProductTag`.
- `Order` thuộc một `User` và có nhiều `OrderItem`.
- `OrderItem` thuộc một `Order` và tham chiếu đến một `Product`.
- `ViewHistory`, `SearchHistory`, `Rating`, `CartItem`, `UserRecommendation` đều tham chiếu đến `User` và (ngoại trừ `SearchHistory`) tham chiếu đến `Product`.
- `ProductSimilarity` tham chiếu đến hai `Product`.

**\[ĐƯA VÀO BIỂU ĐỒ LỚP THỰC THỂ TỔNG QUAN Ở ĐÂY]**

**3.4. Thiết kế CSDL**

Các bảng chính trong cơ sở dữ liệu MySQL:

- **users**: `user_id` (PK), `name`, `email` (UNIQUE), `password_hash`, `role`, `created_at`, `updated_at`.
- **user_addresses**: `address_id` (PK), `user_id` (FK), `street`, `city`, `country`, `is_default`.
- **categories**: `category_id` (PK), `name`, `description`. _(Đã bỏ parent_category_id)_
- **products**: `product_id` (PK), `name`, `description`, `price`, `category_id` (FK), `stock_quantity`, `attributes` (JSON), `created_at`, `updated_at`.
- **product_images**: `image_id` (PK), `product_id` (FK), `image_url`, `sort_order`.
- **tags**: `tag_id` (PK), `name` (UNIQUE).
- **product_tags**: `product_id` (PK, FK), `tag_id` (PK, FK).
- **orders**: `order_id` (PK), `user_id` (FK), `order_date`, `total_amount`, `status`, `shipping_address` (JSON), `payment_method`, `created_at`, `updated_at`.
- **order_items**: `order_item_id` (PK), `order_id` (FK), `product_id` (FK), `quantity`, `price_at_purchase`, `product_snapshot` (JSON).
- **view_history**: `view_id` (PK), `user_id` (FK), `product_id` (FK), `view_timestamp`.
- **search_history**: `search_id` (PK), `user_id` (FK), `query`, `search_timestamp`.
- **ratings**: `rating_id` (PK), `user_id` (FK), `product_id` (FK), `score`, `comment`, `rating_timestamp`, UNIQUE(`user_id`, `product_id`).
- **cart_items**: `cart_item_id` (PK), `user_id` (FK), `product_id` (FK), `quantity`, `added_at`.
- **product_similarity**: `product_id_a` (PK, FK), `product_id_b` (PK, FK), `similarity_score`.
- **user_recommendations**: `user_id` (PK, FK), `product_id` (PK, FK), `recommendation_score`, `generated_at`.
- **training_history**: `history_id` (PK), `start_time`, `end_time`, `status`, `triggered_by`, `message`.

**\[ĐƯA VÀO BIỂU ĐỒ CƠ SỞ DỮ LIỆU CHI TIẾT (ERD) Ở ĐÂY - _Sử dụng danh sách bảng ở trên để vẽ, lưu ý bảng categories đã thay đổi_]**

---

**4. Module 1: Huấn luyện mô hình gợi ý sản phẩm**

**4.1. Hoạt động của module**

Module này chịu trách nhiệm phân tích dữ liệu hành vi người dùng trong quá khứ để xây dựng mô hình gợi ý. Quá trình này thường diễn ra ở backend và được thực hiện định kỳ (ví dụ: hàng đêm) để cập nhật mô hình với dữ liệu mới nhất.

- **Đầu vào:** Dữ liệu được đọc trực tiếp từ các bảng trong CSDL MySQL của ứng dụng:
  - `ratings`: Dữ liệu đánh giá sản phẩm của người dùng (user_id, product_id, score).
  - `view_history`: Lịch sử xem sản phẩm (user_id, product_id, view_timestamp). Có thể dùng để suy ra sở thích ngầm.
  - `order_items` và `orders`: Lịch sử mua hàng (user_id, product_id, quantity). Đây là tín hiệu mạnh về sở thích.
  - _(Tùy chọn)_ `products`: Dữ liệu thuộc tính sản phẩm (nếu kết hợp Content-based).
- **Thuật toán:** Sử dụng phương pháp **Collaborative Filtering** dựa trên **Matrix Factorization** (ví dụ: Singular Value Decomposition - SVD, Alternating Least Squares - ALS). Thuật toán này học các vector đặc trưng ẩn (latent factors) cho mỗi người dùng và mỗi sản phẩm từ ma trận tương tác user-item (ví dụ: ma trận rating hoặc ma trận mua hàng/xem hàng).
- **Xử lý:**
  1.  **Tải dữ liệu:** Truy vấn và tải dữ liệu tương tác từ các bảng MySQL liên quan.
  2.  **Tiền xử lý:** Làm sạch dữ liệu, loại bỏ nhiễu (nếu cần), chuyển đổi dữ liệu thành định dạng phù hợp cho thuật toán (ví dụ: ma trận user-item).
  3.  **Huấn luyện:** Áp dụng thuật toán Matrix Factorization để học user factors và item factors. Thư viện như `Surprise` hoặc `Implicit` trong Python có thể được sử dụng.
  4.  **Tính toán kết quả gợi ý:** Từ item factors, tính toán độ tương tự giữa các sản phẩm (ví dụ: cosine similarity). Từ user factors và item factors, dự đoán mức độ yêu thích/phù hợp của các sản phẩm chưa tương tác cho mỗi người dùng để tạo gợi ý top-N.
  5.  **Lưu kết quả:** Ghi các kết quả tính toán trước vào các bảng MySQL:
      - Độ tương tự sản phẩm -> `product_similarity` table.
      - Gợi ý top-N cho mỗi user -> `user_recommendations` table.
- **Kích hoạt:**
  - **Tự động:** Theo lịch trình (ví dụ: 1 giờ sáng mỗi ngày) sử dụng thư viện `APScheduler` tích hợp trong ứng dụng Python backend. Ghi `triggered_by = 'SCHEDULED'`.
  - **Thủ công (Admin):** Thông qua giao diện Admin trên Flutter, gọi API `POST /api/admin/training/run`. Ghi `triggered_by = 'MANUAL_ADMIN_ID'`.
- **Lịch sử huấn luyện:** Mỗi lần quá trình huấn luyện bắt đầu, một bản ghi mới được tạo trong bảng `training_history` với `status = 'RUNNING'`. Khi kết thúc, bản ghi được cập nhật với `end_time` và `status = 'SUCCESS'` hoặc `'FAILED'` (kèm `message` lỗi nếu có).
- **Logging:** Ghi log chi tiết các bước xử lý ra console/file.

**4.2. Thiết kế giao diện bên client**

- **Giao diện người dùng cuối (User):** Không có.
- **Giao diện quản trị viên (Admin - Flutter):**
  - **Màn hình Quản lý Huấn luyện (`TrainingManagementScreen`):**
    - Nút **"Chạy Huấn luyện Ngay"**: Kích hoạt quá trình huấn luyện thủ công. Hiển thị trạng thái loading/thông báo khi nhấn.
    - Khu vực **"Lịch sử Huấn luyện"**: Hiển thị danh sách các lần chạy huấn luyện gần đây nhất từ bảng `training_history`. Mỗi dòng hiển thị: `history_id`, `start_time`, `end_time`, `status`, `triggered_by`. Có thể có nút xem chi tiết log/message lỗi (nếu có).

_(Mô tả hình ảnh: Màn hình Flutter có tiêu đề "Quản lý Huấn luyện". Bên trên là một nút lớn "Chạy Huấn luyện Ngay". Bên dưới là một danh sách các mục, mỗi mục hiển thị thông tin một lần chạy huấn luyện: ID, Thời gian bắt đầu, Thời gian kết thúc, Trạng thái (SUCCESS/FAILED/RUNNING), Người kích hoạt (SCHEDULED/MANUAL).)_

**4.3. Thiết kế biểu đồ lớp chi tiết (Backend - Python Monolith & Flutter Admin)**
**Phân tích lớp theo tầng:**

- **Flutter (Admin UI):**
  - **View Layer:** `TrainingManagementScreen` (Hiển thị giao diện), Widgets (Button, List).
  - **Controller Layer (GetX):** `TrainingController` (extends `GetxController`, quản lý state với `.obs`, gọi API).
  - **Service Layer:** `AdminTrainingApiService` (Thực hiện gọi HTTP request đến Backend).
  - **Model Layer:** `TrainingHistoryModel` (Đại diện dữ liệu lịch sử).
- **Backend (Python):**
  - **Controller Layer:** `TrainingController` (Tiếp nhận HTTP request từ Admin UI).
  - **Service Layer:** `TrainingService_Or_Job` (Điều phối logic huấn luyện), `TrainingHistoryService` (Xử lý logic nghiệp vụ liên quan đến lịch sử).
  - **Engine/Algorithm Layer:** `DataPreprocessor`, `RecommendationModelTrainer` (Interface), `MatrixFactorizationTrainer` (Implementation), `ModelEvaluator`.
  - **Repository Layer:** `DataLoader_Repo`, `RecommendationResultWriter_Repo`, `TrainingHistoryRepository` (Truy cập CSDL).
  - **Scheduling Layer:** `TrainingScheduler` (Kích hoạt job định kỳ).
  - **Model/Entity Layer:** `TrainingHistory` (ORM class).

**\[ĐƯA VÀO BIỂU ĐỒ LỚP CHI TIẾT CHO MODULE HUẤN LUYỆN Ở ĐÂY]**

- **Phân tích ưu điểm Pattern:**
  - **Repository Pattern (Backend):** Tách biệt logic truy cập dữ liệu.
  - **Strategy Pattern (Backend - Tùy chọn):** Linh hoạt thay đổi thuật toán.
  - **GetX (Flutter):** Cung cấp giải pháp quản lý state đơn giản, hiệu năng tốt, tích hợp quản lý phụ thuộc và điều hướng, giúp giảm boilerplate code so với một số giải pháp khác. Kiến trúc MVC giúp phân tách rõ ràng giữa giao diện (View), logic xử lý và trạng thái (Controller), và dữ liệu (Model).

**4.4. Thiết kế biểu đồ tuần tự hoạt động**

**\[ĐƯA VÀO CÁC BIỂU ĐỒ TUẦN TỰ CHO MODULE 1 Ở ĐÂY (Scheduled Task, Admin Trigger, Admin View History)]**

---

**5. Module 2: Tìm chọn và đặt mua hàng online**

**5.1. Hoạt động của module**

Đây là module E-commerce cốt lõi, cung cấp các chức năng cơ bản cho phép người dùng duyệt, tìm kiếm, quản lý giỏ hàng và hoàn tất quy trình đặt hàng.

- **Tìm kiếm & Duyệt sản phẩm:**
  - Người dùng có thể nhập từ khóa vào thanh tìm kiếm hoặc chọn danh mục từ danh sách (danh sách phẳng).
  - Kết quả tìm kiếm/duyệt danh mục được hiển thị dưới dạng danh sách hoặc lưới sản phẩm.
  - Hỗ trợ **phân trang** để tải thêm sản phẩm khi người dùng cuộn xuống hoặc chuyển trang.
- **Xem chi tiết sản phẩm:**
  - Hiển thị đầy đủ thông tin: Tên, nhiều ảnh (dạng gallery/carousel), mô tả chi tiết, giá, các thuộc tính (size, màu sắc - nếu có), trạng thái còn hàng/hết hàng.
  - Nút "Thêm vào giỏ hàng".
  - Khu vực hiển thị sản phẩm gợi ý (từ **Module 3**).
- **Quản lý giỏ hàng:**
  - **Thêm vào giỏ:** Từ nút trên trang chi tiết hoặc trang danh sách.
  - **Xem giỏ hàng:** Truy cập màn hình giỏ hàng riêng. Hiển thị danh sách các sản phẩm đã thêm (ảnh, tên, giá, số lượng, thành tiền). Cho phép **thay đổi số lượng** hoặc **xóa sản phẩm** khỏi giỏ. Hiển thị tổng số lượng và tổng giá trị đơn hàng.
  - **Lưu trữ:** Giỏ hàng được lưu **phía server** (bảng `cart_items` trong MySQL) và liên kết với `user_id` của người dùng đã đăng nhập. Khi người dùng chưa đăng nhập, có thể lưu tạm ở client (Flutter `shared_preferences`) và đồng bộ lên server khi đăng nhập. _Thiết kế này giả định ưu tiên lưu server-side cho user đã đăng nhập._
- **Đặt hàng (Checkout):**
  - **Bước 1:** Từ màn hình giỏ hàng, nhấn nút "Thanh toán" / "Checkout".
  - **Bước 2:** Màn hình Checkout:
    - Hiển thị/Cho phép chọn/thêm mới **Địa chỉ giao hàng**. Dữ liệu địa chỉ đã lưu của người dùng được lấy từ bảng `user_addresses`.
    - Hiển thị/Cho phép chọn **Phương thức thanh toán**. Trong phạm vi đề tài, chỉ hỗ trợ **COD (Thanh toán khi nhận hàng)**.
    - Hiển thị **Tóm tắt đơn hàng** (sản phẩm, số lượng, giá, tổng tiền).
  - **Bước 3:** Nhấn nút **"Xác nhận đặt hàng"**.
  - **Xử lý phía Backend (trong một Database Transaction):**
    1.  Kiểm tra tính hợp lệ của giỏ hàng và địa chỉ.
    2.  Kiểm tra số lượng tồn kho (`stock_quantity`) của từng sản phẩm trong giỏ hàng. Nếu không đủ hàng, báo lỗi và hủy transaction.
    3.  Tạo một bản ghi mới trong bảng `orders` với thông tin người dùng, địa chỉ, tổng tiền, phương thức thanh toán (COD), trạng thái ban đầu (ví dụ: 'PENDING' hoặc 'PROCESSING').
    4.  Với mỗi sản phẩm trong giỏ hàng, tạo một bản ghi tương ứng trong bảng `order_items`, lưu `order_id`, `product_id`, `quantity`, `price_at_purchase`.
    5.  **Cập nhật (giảm) `stock_quantity`** trong bảng `products` cho từng sản phẩm đã đặt.
    6.  Xóa các sản phẩm tương ứng khỏi giỏ hàng của người dùng trong bảng `cart_items`.
    7.  Commit transaction.
    8.  Trả về thông báo thành công và thông tin đơn hàng vừa tạo cho client.
  - **Bước 4:** Hiển thị màn hình "Đặt hàng thành công" trên Flutter.

**5.2. Thiết kế giao diện bên client (Flutter)**

- **Màn hình Danh sách Sản phẩm (`ProductListScreen`):**
  - Thanh tìm kiếm (`SearchBar`).
  - Bộ lọc danh mục (tùy chọn, hiển thị danh sách phẳng).
  - Hiển thị sản phẩm dạng lưới hoặc danh sách (`ProductCard`), có cơ chế tải thêm (infinite scroll hoặc nút "Xem thêm").
- **Màn hình Chi tiết Sản phẩm (`ProductDetailScreen`):**
  - Carousel/Gallery ảnh sản phẩm.
  - Tên, giá, mô tả, thuộc tính (nếu có).
  - Nút "Thêm vào giỏ hàng".
  - Phần "Sản phẩm tương tự" (**Module 3**).
- **Màn hình Giỏ hàng (`CartScreen`):**
  - Danh sách các `CartItemWidget`. Mỗi item hiển thị ảnh, tên, giá, bộ điều chỉnh số lượng (+/-), nút xóa.
  - Hiển thị tổng số lượng, tổng tiền.
  - Nút "Tiếp tục mua sắm", "Tiến hành thanh toán".
- **Màn hình Thanh toán (`CheckoutScreen`):**
  - Khu vực chọn/thêm địa chỉ giao hàng (`AddressForm`, danh sách địa chỉ đã lưu).
  - Khu vực chọn phương thức thanh toán (`PaymentSelector` - chỉ có COD).
  - Khu vực tóm tắt đơn hàng (`OrderSummary`).
  - Nút "Xác nhận đặt hàng".
- **Màn hình Đặt hàng thành công (`OrderSuccessScreen`):**
  - Thông báo đặt hàng thành công.
  - Hiển thị mã đơn hàng.
  - Nút "Tiếp tục mua sắm" hoặc "Xem đơn hàng".

_(Mô tả hình ảnh: Một chuỗi các màn hình Flutter: màn hình danh sách sản phẩm với lưới ảnh, tên, giá; màn hình chi tiết với ảnh lớn, mô tả, nút thêm giỏ hàng; màn hình giỏ hàng với danh sách item, số lượng, tổng tiền; màn hình checkout với form địa chỉ, chọn COD, tóm tắt đơn hàng; màn hình báo thành công.)_

**5.3. Thiết kế biểu đồ lớp chi tiết**
**Phân tích lớp theo tầng:**

- **Flutter (Client UI):**
  - **View Layer:** Các Screens (`ProductListScreen`, `CartScreen`, `CheckoutScreen`...) và Widgets (`ProductCard`, `CartItemWidget`, `AddressForm`...).
  - **Controller Layer (GetX):** Các Controllers (`ProductController`, `CartController`, `OrderController`, `UserController`).
  - **Service Layer:** Các API Services (`ProductApiService`, `CartApiService`, `OrderApiService`, `UserApiService`).
  - **Model Layer:** Các lớp dữ liệu Dart (`ProductModel`, `CartItemModel`, `OrderModel`, `AddressModel`).
- **Backend (Python):**
  - **Controller Layer:** `ProductController`, `CartController`, `OrderController`, `UserController`.
  - **Service Layer:** `ProductService`, `CartService`, `OrderService`, `UserService`.
  - **Repository Layer:** `ProductRepository`, `CategoryRepository`, `CartRepository`, `OrderRepository`, `OrderItemRepository`, `UserRepository`, `UserAddressRepository`.
  - **Model/Entity Layer:** Các lớp ORM tương ứng với bảng CSDL (`Product`, `Order`, `CartItem`...).

**\[ĐƯA VÀO BIỂU ĐỒ LỚP CHI TIẾT CHO MODULE MUA HÀNG Ở ĐÂY]**

- **Phân tích ưu điểm Pattern:**
  - **Service Layer (Backend):** Tách biệt logic nghiệp vụ.
  - **Repository Pattern (Backend):** Đóng gói truy cập CSDL.
  - **MVC & GetX (Flutter):** Phân tách rõ ràng View, Controller (quản lý state và logic UI), Model. GetX giúp quản lý state và dependency injection gọn nhẹ, hiệu quả.

**5.4. Thiết kế biểu đồ tuần tự hoạt động**
**Kịch bản: Người dùng đặt hàng thành công**

**\[ĐƯA VÀO BIỂU ĐỒ TUẦN TỰ CHO KỊCH BẢN ĐẶT HÀNG Ở ĐÂY]**

---

**6. Module 3: Gợi ý sản phẩm cho khách hàng**

**6.1. Hoạt động của module**

Module này chịu trách nhiệm lấy các gợi ý đã được tính toán trước (bởi **Module 1**) và hiển thị chúng cho người dùng trên ứng dụng Flutter tại các vị trí phù hợp trong luồng mua sắm.

- **Nguồn dữ liệu:** Dữ liệu gợi ý được đọc trực tiếp từ các bảng trong CSDL MySQL đã được **Module 1** chuẩn bị:
  - `product_similarity`: Chứa thông tin về các sản phẩm tương tự nhau.
  - `user_recommendations`: Chứa danh sách sản phẩm được gợi ý riêng cho từng người dùng.
  - `products`: Dùng để lấy thông tin chi tiết (tên, ảnh, giá...) của các sản phẩm được gợi ý.
- **Logic gợi ý:**
  - **Khi người dùng xem trang chi tiết sản phẩm X:** Backend truy vấn bảng `product_similarity` để lấy danh sách ID các sản phẩm tương tự nhất với X (`product_id_b` khi `product_id_a` là X), sau đó truy vấn bảng `products` để lấy thông tin chi tiết của các ID đó.
  - **Khi người dùng (đã đăng nhập) truy cập trang chủ:** Backend truy vấn bảng `user_recommendations` để lấy danh sách ID các sản phẩm được gợi ý hàng đầu cho `user_id` hiện tại, sau đó truy vấn bảng `products` để lấy thông tin chi tiết.
- **Loại gợi ý hiển thị:**
  - "Sản phẩm tương tự": Hiển thị trên trang chi tiết sản phẩm.
  - "Gợi ý cho bạn": Hiển thị trên trang chủ (chỉ cho người dùng đã đăng nhập).
- **Tương tác:** Người dùng có thể nhấp vào một sản phẩm gợi ý để xem chi tiết sản phẩm đó.

**6.2. Thiết kế giao diện bên client (Flutter)**

- **Trên màn hình Chi tiết sản phẩm (`ProductDetailScreen`):**
  - Một khu vực (ví dụ: ở dưới phần mô tả sản phẩm) có tiêu đề "Sản phẩm tương tự".
  - Hiển thị một danh sách các sản phẩm gợi ý dưới dạng **Carousel cuộn ngang**.
  - Mỗi sản phẩm trong carousel hiển thị: **Ảnh đại diện**, **Tên sản phẩm**, **Giá bán**.
- **Trên màn hình Trang chủ (`HomeScreen`):**
  - Một khu vực (ví dụ: sau banner hoặc các mục nổi bật) có tiêu đề "Gợi ý cho bạn".
  - Hiển thị một **danh sách dọc hoặc lưới (grid)** các sản phẩm gợi ý cá nhân hóa.
  - Mỗi sản phẩm hiển thị: **Ảnh đại diện**, **Tên sản phẩm**, **Giá bán**.
  - Khu vực này chỉ hiển thị nếu người dùng đã đăng nhập.

_(Mô tả hình ảnh: Màn hình chi tiết sản phẩm có thêm một hàng ngang các sản phẩm khác cuộn được ở dưới cùng. Màn hình trang chủ có thêm một khu vực danh sách/lưới các sản phẩm với tiêu đề "Gợi ý cho bạn".)_

**6.3. Thiết kế biểu đồ lớp chi tiết**
**Phân tích lớp theo tầng:**

- **Flutter (Client UI):**
  - **View Layer:** `ProductDetailScreen`, `HomeScreen`, `RecommendationWidget`, `ProductCard`.
  - **Controller Layer (GetX):** `RecommendationController` (extends `GetxController`).
  - **Service Layer:** `RecommendationApiService`.
  - **Model Layer:** `ProductModel`.
- **Backend (Python):**
  - **Controller Layer:** `ProductController`, `RecommendationController`.
  - **Service Layer:** `RecommendationService`.
  - **Repository Layer:** `RecommendationRepository`, `ProductRepository`.
  - **Model/Entity Layer:** `Product`, `ProductSimilarity`, `UserRecommendation`.

**\[ĐƯA VÀO BIỂU ĐỒ LỚP CHI TIẾT CHO MODULE GỢI Ý Ở ĐÂY]**

- **Phân tích ưu điểm Pattern:**
  - **Service Layer (Backend):** Tách biệt logic kết hợp dữ liệu.
  - **Repository Pattern (Backend):** Đóng gói truy cập CSDL.
  - **MVC & GetX (Flutter):** Phân tách rõ ràng View, Controller, Model. GetX giúp quản lý state và dependency injection gọn nhẹ.
  - **Widget Tái sử dụng (Flutter):** `RecommendationWidget` có thể dùng lại.

**6.4. Thiết kế biểu đồ tuần tự hoạt động**
**Kịch bản: Người dùng mở trang chi tiết sản phẩm X**

**\[ĐƯA VÀO BIỂU ĐỒ TUẦN TỰ CHO KỊCH BẢN XEM GỢI Ý SẢN PHẨM TƯƠNG TỰ Ở ĐÂY]**

---

_(Kết thúc nội dung báo cáo. Bạn cần bổ sung các biểu đồ dạng hình ảnh (nếu muốn thay thế Mermaid) và định dạng lại theo yêu cầu)_
