    # E-commerce AI System - Frontend API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Base URL and Authentication](#base-url-and-authentication)
3. [API Endpoints](#api-endpoints)
   - [Authentication and User Management](#authentication-and-user-management)
   - [Products](#products)
   - [Cart](#cart)
   - [Orders](#orders)
   - [Recommendations](#recommendations)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Flutter Implementation Guidelines](#flutter-implementation-guidelines)

## Introduction

This document provides comprehensive documentation for frontend developers to implement a Flutter application that interacts with the E-commerce AI backend system. The backend is built with Python FastAPI and follows a monolithic architecture with MVC pattern.

The system consists of three main modules:

1. **Module 1: Product Recommendation Training System**
2. **Module 2: Online Shopping System**
3. **Module 3: Product Recommendation System**

This documentation covers all the necessary API endpoints and data models to implement these modules on the frontend.

## Base URL and Authentication

### Base URL

```
http://0.0.0.0:8001
```

In development environment, typically:

```
http://0.0.0.0:8001
```

### Authentication

The API uses JWT (JSON Web Token) authentication. Most endpoints require a valid JWT token obtained through the login process.

**How to include the token in requests:**

```
Authorization: Bearer {your_access_token}
```

## API Endpoints

### Authentication and User Management

#### Login

- **URL**: `/auth/login`
- **Method**: `POST`
- **Authentication**: None
- **Description**: Authenticate a user and get an access token
- **Request Body**:

```json
{
  "username": "user@example.com",
  "password": "yourpassword"
}
```

- **Response**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Register

- **URL**: `/auth/register`
- **Method**: `POST`
- **Authentication**: None
- **Description**: Register a new user
- **Request Body**:

```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "User Name"
}
```

- **Response**:

```json
{
  "user_id": 123,
  "email": "user@example.com",
  "full_name": "User Name",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00"
}
```

#### Get User Profile

- **URL**: `/auth/me`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Get the current user's profile information
- **Response**:

```json
{
  "user_id": 123,
  "email": "user@example.com",
  "full_name": "User Name",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00"
}
```

#### Update User Profile

- **URL**: `/auth/me`
- **Method**: `PUT`
- **Authentication**: Required
- **Description**: Update the current user's profile
- **Request Body**:

```json
{
  "full_name": "Updated Name",
  "password": "newpassword" // Optional
}
```

- **Response**:

```json
{
  "user_id": 123,
  "email": "user@example.com",
  "full_name": "Updated Name",
  "is_active": true,
  "created_at": "2023-01-01T12:00:00"
}
```

#### Get User Addresses

- **URL**: `/auth/addresses`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Get all addresses for the current user
- **Response**:

```json
[
  {
    "address_id": 1,
    "user_id": 123,
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "country": "USA",
    "postal_code": "12345",
    "phone": "123-456-7890",
    "is_default": true
  }
]
```

#### Add Address

- **URL**: `/auth/addresses`
- **Method**: `POST`
- **Authentication**: Required
- **Description**: Add a new address for the current user
- **Request Body**:

```json
{
  "street": "456 Oak St",
  "city": "Othertown",
  "state": "NY",
  "country": "USA",
  "postal_code": "54321",
  "phone": "098-765-4321",
  "is_default": false
}
```

- **Response**:

```json
{
  "address_id": 2,
  "user_id": 123,
  "street": "456 Oak St",
  "city": "Othertown",
  "state": "NY",
  "country": "USA",
  "postal_code": "54321",
  "phone": "098-765-4321",
  "is_default": false
}
```

#### Update Address

- **URL**: `/auth/addresses/{address_id}`
- **Method**: `PUT`
- **Authentication**: Required
- **Description**: Update an existing address
- **Path Parameters**:
  - `address_id`: ID of the address to update
- **Request Body**:

```json
{
  "street": "456 Updated St",
  "is_default": true
}
```

- **Response**:

```json
{
  "address_id": 2,
  "user_id": 123,
  "street": "456 Updated St",
  "city": "Othertown",
  "state": "NY",
  "country": "USA",
  "postal_code": "54321",
  "phone": "098-765-4321",
  "is_default": true
}
```

#### Delete Address

- **URL**: `/auth/addresses/{address_id}`
- **Method**: `DELETE`
- **Authentication**: Required
- **Description**: Delete an address
- **Path Parameters**:
  - `address_id`: ID of the address to delete
- **Response**:

```json
{
  "success": true,
  "message": "Address deleted successfully"
}
```

### Products

#### Search Products

- **URL**: `/products`
- **Method**: `GET`
- **Authentication**: Optional
- **Description**: Search and filter products
- **Query Parameters**:
  - `search_query`: (Optional) Text to search for in product names/descriptions
  - `category_id`: (Optional) Filter by category ID
  - `min_price`: (Optional) Minimum price filter
  - `max_price`: (Optional) Maximum price filter
  - `order_by`: (Optional) Field to sort by (default: "created_at")
  - `descending`: (Optional) Sort in descending order (default: true)
  - `page`: (Optional) Page number for pagination (default: 1)
  - `page_size`: (Optional) Number of results per page (default: 20, max: 100)
- **Response**:

```json
{
  "items": [
    {
      "product_id": 1,
      "name": "Product Name",
      "price": 99.99,
      "category_id": 5,
      "category_name": "Electronics",
      "image_url": "https://example.com/image.jpg"
    }
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  },
  "filters": {
    "categories": [{ "category_id": 5, "name": "Electronics", "count": 50 }],
    "price_range": { "min": 10.0, "max": 500.0 }
  }
}
```

#### Get Product Details

- **URL**: `/products/{product_id}`
- **Method**: `GET`
- **Authentication**: Optional
- **Description**: Get detailed information about a specific product
- **Path Parameters**:
  - `product_id`: ID of the product
- **Response**:

```json
{
  "product_id": 1,
  "name": "Product Name",
  "description": "Detailed product description",
  "price": 99.99,
  "category_id": 5,
  "category_name": "Electronics",
  "stock_quantity": 100,
  "attributes": {
    "color": "Black",
    "size": "Medium"
  },
  "is_active": true,
  "images": [
    {
      "image_id": 1,
      "product_id": 1,
      "image_url": "https://example.com/image1.jpg",
      "is_primary": true,
      "display_order": 1
    }
  ],
  "tags": ["Electronics", "Gadget"],
  "created_at": "2023-01-01T12:00:00",
  "updated_at": "2023-01-10T15:30:00"
}
```

#### Get Categories

- **URL**: `/products/categories`
- **Method**: `GET`
- **Authentication**: None
- **Description**: Get a list of all product categories
- **Response**:

```json
[
  {
    "category_id": 1,
    "name": "Electronics",
    "description": "Electronic devices and gadgets"
  },
  {
    "category_id": 2,
    "name": "Clothing",
    "description": "Fashion items and apparel"
  }
]
```

### Cart

#### Get Cart

- **URL**: `/cart`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Get the current user's shopping cart
- **Response**:

```json
{
  "items": [
    {
      "cart_item_id": 1,
      "product_id": 1,
      "name": "Product Name",
      "price": 99.99,
      "quantity": 2,
      "subtotal": 199.98,
      "image_url": "https://example.com/image.jpg",
      "stock_quantity": 100,
      "is_in_stock": true
    }
  ],
  "total_amount": 199.98,
  "item_count": 2
}
```

#### Add to Cart

- **URL**: `/cart/add`
- **Method**: `POST`
- **Authentication**: Required
- **Description**: Add an item to the cart
- **Request Body**:

```json
{
  "product_id": 1,
  "quantity": 2
}
```

- **Response**:

```json
{
  "success": true,
  "message": "Item added to cart",
  "cart": {
    "items": [...],
    "total_amount": 199.98,
    "item_count": 2
  }
}
```

#### Update Cart Item

- **URL**: `/cart/items/{cart_item_id}`
- **Method**: `PUT`
- **Authentication**: Required
- **Description**: Update the quantity of an item in the cart
- **Path Parameters**:
  - `cart_item_id`: ID of the cart item to update
- **Request Body**:

```json
{
  "quantity": 3
}
```

- **Response**:

```json
{
  "success": true,
  "message": "Cart item updated",
  "cart": {
    "items": [...],
    "total_amount": 299.97,
    "item_count": 3
  }
}
```

#### Remove from Cart

- **URL**: `/cart/items/{cart_item_id}`
- **Method**: `DELETE`
- **Authentication**: Required
- **Description**: Remove an item from the cart
- **Path Parameters**:
  - `cart_item_id`: ID of the cart item to remove
- **Response**:

```json
{
  "success": true,
  "message": "Item removed from cart",
  "cart": {
    "items": [],
    "total_amount": 0,
    "item_count": 0
  }
}
```

### Orders

#### Get Orders List

- **URL**: `/orders`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Get a paginated list of the user's orders
- **Query Parameters**:
  - `page`: (Optional) Page number (default: 1)
  - `page_size`: (Optional) Items per page (default: 10, max: 50)
- **Response**:

```json
{
  "items": [
    {
      "order_id": 1,
      "order_date": "2023-01-05T14:30:00",
      "status": "DELIVERED",
      "total_amount": 199.98,
      "payment_method": "COD",
      "item_count": 2,
      "shipping_address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "country": "USA",
        "postal_code": "12345"
      }
    }
  ],
  "pagination": {
    "total": 5,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
  }
}
```

#### Get Order Details

- **URL**: `/orders/{order_id}`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Get detailed information about a specific order
- **Path Parameters**:
  - `order_id`: ID of the order
- **Response**:

```json
{
  "success": true,
  "message": "Order details retrieved successfully",
  "order": {
    "order_id": 1,
    "user_id": 123,
    "order_date": "2023-01-05T14:30:00",
    "status": "DELIVERED",
    "total_amount": 199.98,
    "payment_method": "COD",
    "shipping_address": {
      "street": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "country": "USA",
      "postal_code": "12345"
    },
    "items": [
      {
        "order_item_id": 1,
        "product_id": 1,
        "product_name": "Product Name",
        "quantity": 2,
        "price_at_purchase": 99.99,
        "subtotal": 199.98,
        "image_url": "https://example.com/image.jpg"
      }
    ],
    "notes": "Please deliver in the morning",
    "created_at": "2023-01-05T14:30:00",
    "updated_at": "2023-01-05T14:30:00"
  }
}
```

#### Create Order

- **URL**: `/orders`
- **Method**: `POST`
- **Authentication**: Required
- **Description**: Create a new order from the user's cart
- **Request Body**:

```json
{
  "address_id": 1,
  "notes": "Please deliver in the morning"
}
```

- **Response**:

```json
{
  "success": true,
  "message": "Order created successfully",
  "order_id": 2,
  "total_amount": 299.97
}
```

#### Cancel Order

- **URL**: `/orders/{order_id}/cancel`
- **Method**: `POST`
- **Authentication**: Required
- **Description**: Cancel an existing order (only if it's in a cancellable state)
- **Path Parameters**:
  - `order_id`: ID of the order to cancel
- **Response**:

```json
{
  "success": true,
  "message": "Order cancelled successfully",
  "order_id": 2
}
```

### Recommendations

#### Get Similar Products

- **URL**: `/recommendations/similar/{product_id}`
- **Method**: `GET`
- **Authentication**: None
- **Description**: Get products similar to the specified product
- **Path Parameters**:
  - `product_id`: ID of the product to find similar items for
- **Query Parameters**:
  - `limit`: (Optional) Maximum number of similar products to return (default: 10, max: 50)
- **Response**:

```json
{
  "success": true,
  "product_id": 1,
  "product_name": "Product Name",
  "similar_products": [
    {
      "product_id": 2,
      "name": "Similar Product 1",
      "price": 89.99,
      "similarity_score": 0.92,
      "image_url": "https://example.com/image2.jpg"
    },
    {
      "product_id": 3,
      "name": "Similar Product 2",
      "price": 109.99,
      "similarity_score": 0.87,
      "image_url": "https://example.com/image3.jpg"
    }
  ]
}
```

#### Get Personalized Recommendations

- **URL**: `/recommendations/personalized`
- **Method**: `GET`
- **Authentication**: Required
- **Description**: Get personalized product recommendations for the current user
- **Query Parameters**:
  - `limit`: (Optional) Maximum number of recommendations to return (default: 20, max: 100)
- **Response**:

```json
{
  "success": true,
  "user_id": 123,
  "recommendations": [
    {
      "product_id": 5,
      "name": "Recommended Product 1",
      "price": 129.99,
      "recommendation_score": 0.95,
      "image_url": "https://example.com/image5.jpg"
    },
    {
      "product_id": 7,
      "name": "Recommended Product 2",
      "price": 79.99,
      "recommendation_score": 0.88,
      "image_url": "https://example.com/image7.jpg"
    }
  ],
  "recommendation_type": "personalized"
}
```

#### Start Training Job (Admin Only)

- **URL**: `/recommendations/training/run`
- **Method**: `POST`
- **Authentication**: Required (Admin only)
- **Description**: Manually trigger a recommendation model training job
- **Response**:

```json
{
  "success": true,
  "message": "Training job started successfully",
  "job_result": {
    "job_id": "training_job_20230105_143000",
    "status": "RUNNING",
    "start_time": "2023-01-05T14:30:00"
  }
}
```

#### Get Training History (Admin Only)

- **URL**: `/recommendations/training/history`
- **Method**: `GET`
- **Authentication**: Required (Admin only)
- **Description**: Get the history of recommendation model training jobs
- **Query Parameters**:
  - `page`: (Optional) Page number (default: 1)
  - `page_size`: (Optional) Items per page (default: 10, max: 50)
- **Response**:

```json
{
  "success": true,
  "history": [
    {
      "history_id": 1,
      "start_time": "2023-01-01T01:00:00",
      "end_time": "2023-01-01T01:15:27",
      "status": "SUCCESS",
      "triggered_by": "SCHEDULED",
      "message": "Training completed successfully",
      "duration_minutes": 15.45
    },
    {
      "history_id": 2,
      "start_time": "2023-01-02T01:00:00",
      "end_time": "2023-01-02T01:16:12",
      "status": "SUCCESS",
      "triggered_by": "MANUAL_ADMIN_123",
      "message": "Training completed successfully",
      "duration_minutes": 16.2
    }
  ],
  "pagination": {
    "total": 30,
    "page": 1,
    "page_size": 10,
    "total_pages": 3
  }
}
```

## Data Models

### User

```dart
class User {
  final int userId;
  final String email;
  final String fullName;
  final bool isActive;
  final DateTime createdAt;

  User({
    required this.userId,
    required this.email,
    required this.fullName,
    required this.isActive,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      userId: json['user_id'],
      email: json['email'],
      fullName: json['full_name'],
      isActive: json['is_active'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
```

### Address

```dart
class Address {
  final int addressId;
  final int userId;
  final String street;
  final String city;
  final String state;
  final String country;
  final String postalCode;
  final String phone;
  final bool isDefault;

  Address({
    required this.addressId,
    required this.userId,
    required this.street,
    required this.city,
    required this.state,
    required this.country,
    required this.postalCode,
    required this.phone,
    required this.isDefault,
  });

  factory Address.fromJson(Map<String, dynamic> json) {
    return Address(
      addressId: json['address_id'],
      userId: json['user_id'],
      street: json['street'],
      city: json['city'],
      state: json['state'],
      country: json['country'],
      postalCode: json['postal_code'],
      phone: json['phone'],
      isDefault: json['is_default'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'street': street,
      'city': city,
      'state': state,
      'country': country,
      'postal_code': postalCode,
      'phone': phone,
      'is_default': isDefault,
    };
  }
}
```

### Category

```dart
class Category {
  final int categoryId;
  final String name;
  final String? description;

  Category({
    required this.categoryId,
    required this.name,
    this.description,
  });

  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(
      categoryId: json['category_id'],
      name: json['name'],
      description: json['description'],
    );
  }
}
```

### Product

```dart
class Product {
  final int productId;
  final String name;
  final String description;
  final double price;
  final int categoryId;
  final String? categoryName;
  final int stockQuantity;
  final Map<String, dynamic>? attributes;
  final bool isActive;
  final List<ProductImage> images;
  final List<String> tags;
  final DateTime createdAt;
  final DateTime? updatedAt;

  Product({
    required this.productId,
    required this.name,
    required this.description,
    required this.price,
    required this.categoryId,
    this.categoryName,
    required this.stockQuantity,
    this.attributes,
    required this.isActive,
    required this.images,
    required this.tags,
    required this.createdAt,
    this.updatedAt,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      productId: json['product_id'],
      name: json['name'],
      description: json['description'],
      price: json['price'].toDouble(),
      categoryId: json['category_id'],
      categoryName: json['category_name'],
      stockQuantity: json['stock_quantity'],
      attributes: json['attributes'],
      isActive: json['is_active'],
      images: (json['images'] as List)
        .map((img) => ProductImage.fromJson(img))
        .toList(),
      tags: (json['tags'] as List).cast<String>(),
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null
        ? DateTime.parse(json['updated_at'])
        : null,
    );
  }
}
```

### ProductListItem

```dart
class ProductListItem {
  final int productId;
  final String name;
  final double price;
  final int categoryId;
  final String? categoryName;
  final String? imageUrl;

  ProductListItem({
    required this.productId,
    required this.name,
    required this.price,
    required this.categoryId,
    this.categoryName,
    this.imageUrl,
  });

  factory ProductListItem.fromJson(Map<String, dynamic> json) {
    return ProductListItem(
      productId: json['product_id'],
      name: json['name'],
      price: json['price'].toDouble(),
      categoryId: json['category_id'],
      categoryName: json['category_name'],
      imageUrl: json['image_url'],
    );
  }
}
```

### ProductImage

```dart
class ProductImage {
  final int imageId;
  final int productId;
  final String imageUrl;
  final bool isPrimary;
  final int displayOrder;

  ProductImage({
    required this.imageId,
    required this.productId,
    required this.imageUrl,
    required this.isPrimary,
    required this.displayOrder,
  });

  factory ProductImage.fromJson(Map<String, dynamic> json) {
    return ProductImage(
      imageId: json['image_id'],
      productId: json['product_id'],
      imageUrl: json['image_url'],
      isPrimary: json['is_primary'],
      displayOrder: json['display_order'],
    );
  }
}
```

### CartItem

```dart
class CartItem {
  final int cartItemId;
  final int productId;
  final String name;
  final double price;
  final int quantity;
  final double subtotal;
  final String? imageUrl;
  final int stockQuantity;
  final bool isInStock;

  CartItem({
    required this.cartItemId,
    required this.productId,
    required this.name,
    required this.price,
    required this.quantity,
    required this.subtotal,
    this.imageUrl,
    required this.stockQuantity,
    required this.isInStock,
  });

  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      cartItemId: json['cart_item_id'],
      productId: json['product_id'],
      name: json['name'],
      price: json['price'].toDouble(),
      quantity: json['quantity'],
      subtotal: json['subtotal'].toDouble(),
      imageUrl: json['image_url'],
      stockQuantity: json['stock_quantity'],
      isInStock: json['is_in_stock'],
    );
  }
}
```

### Cart

```dart
class Cart {
  final List<CartItem> items;
  final double totalAmount;
  final int itemCount;

  Cart({
    required this.items,
    required this.totalAmount,
    required this.itemCount,
  });

  factory Cart.fromJson(Map<String, dynamic> json) {
    return Cart(
      items: (json['items'] as List)
        .map((item) => CartItem.fromJson(item))
        .toList(),
      totalAmount: json['total_amount'].toDouble(),
      itemCount: json['item_count'],
    );
  }
}
```

### Order

```dart
class Order {
  final int orderId;
  final int userId;
  final DateTime orderDate;
  final String status;
  final double totalAmount;
  final String paymentMethod;
  final Map<String, dynamic> shippingAddress;
  final List<OrderItem> items;
  final String? notes;
  final DateTime createdAt;
  final DateTime? updatedAt;

  Order({
    required this.orderId,
    required this.userId,
    required this.orderDate,
    required this.status,
    required this.totalAmount,
    required this.paymentMethod,
    required this.shippingAddress,
    required this.items,
    this.notes,
    required this.createdAt,
    this.updatedAt,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      orderId: json['order_id'],
      userId: json['user_id'],
      orderDate: DateTime.parse(json['order_date']),
      status: json['status'],
      totalAmount: json['total_amount'].toDouble(),
      paymentMethod: json['payment_method'],
      shippingAddress: json['shipping_address'],
      items: (json['items'] as List)
        .map((item) => OrderItem.fromJson(item))
        .toList(),
      notes: json['notes'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null
        ? DateTime.parse(json['updated_at'])
        : null,
    );
  }
}
```

### OrderItem

```dart
class OrderItem {
  final int orderItemId;
  final int productId;
  final String productName;
  final int quantity;
  final double priceAtPurchase;
  final double subtotal;
  final String? imageUrl;

  OrderItem({
    required this.orderItemId,
    required this.productId,
    required this.productName,
    required this.quantity,
    required this.priceAtPurchase,
    required this.subtotal,
    this.imageUrl,
  });

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    return OrderItem(
      orderItemId: json['order_item_id'],
      productId: json['product_id'],
      productName: json['product_name'],
      quantity: json['quantity'],
      priceAtPurchase: json['price_at_purchase'].toDouble(),
      subtotal: json['subtotal'].toDouble(),
      imageUrl: json['image_url'],
    );
  }
}
```

### OrderListItem

```dart
class OrderListItem {
  final int orderId;
  final String orderDate;
  final String status;
  final double totalAmount;
  final String paymentMethod;
  final int itemCount;
  final Map<String, dynamic> shippingAddress;

  OrderListItem({
    required this.orderId,
    required this.orderDate,
    required this.status,
    required this.totalAmount,
    required this.paymentMethod,
    required this.itemCount,
    required this.shippingAddress,
  });

  factory OrderListItem.fromJson(Map<String, dynamic> json) {
    return OrderListItem(
      orderId: json['order_id'],
      orderDate: json['order_date'],
      status: json['status'],
      totalAmount: json['total_amount'].toDouble(),
      paymentMethod: json['payment_method'],
      itemCount: json['item_count'],
      shippingAddress: json['shipping_address'],
    );
  }
}
```

### SimilarProduct

```dart
class SimilarProduct {
  final int productId;
  final String name;
  final double price;
  final double similarityScore;
  final String? imageUrl;

  SimilarProduct({
    required this.productId,
    required this.name,
    required this.price,
    required this.similarityScore,
    this.imageUrl,
  });

  factory SimilarProduct.fromJson(Map<String, dynamic> json) {
    return SimilarProduct(
      productId: json['product_id'],
      name: json['name'],
      price: json['price'].toDouble(),
      similarityScore: json['similarity_score'].toDouble(),
      imageUrl: json['image_url'],
    );
  }
}
```

### RecommendedProduct

```dart
class RecommendedProduct {
  final int productId;
  final String name;
  final double price;
  final double? recommendationScore;
  final String? imageUrl;

  RecommendedProduct({
    required this.productId,
    required this.name,
    required this.price,
    this.recommendationScore,
    this.imageUrl,
  });

  factory RecommendedProduct.fromJson(Map<String, dynamic> json) {
    return RecommendedProduct(
      productId: json['product_id'],
      name: json['name'],
      price: json['price'].toDouble(),
      recommendationScore: json['recommendation_score']?.toDouble(),
      imageUrl: json['image_url'],
    );
  }
}
```

### TrainingHistoryItem

```dart
class TrainingHistoryItem {
  final int historyId;
  final String startTime;
  final String? endTime;
  final String status;
  final String triggeredBy;
  final String? message;
  final double? durationMinutes;

  TrainingHistoryItem({
    required this.historyId,
    required this.startTime,
    this.endTime,
    required this.status,
    required this.triggeredBy,
    this.message,
    this.durationMinutes,
  });

  factory TrainingHistoryItem.fromJson(Map<String, dynamic> json) {
    return TrainingHistoryItem(
      historyId: json['history_id'],
      startTime: json['start_time'],
      endTime: json['end_time'],
      status: json['status'],
      triggeredBy: json['triggered_by'],
      message: json['message'],
      durationMinutes: json['duration_minutes']?.toDouble(),
    );
  }
}
```

## Error Handling

The API follows a consistent error handling pattern:

### HTTP Status Codes

- `200 OK`: Successful operation
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication failed or token missing
- `403 Forbidden`: Insufficient permissions (e.g., non-admin user accessing admin endpoint)
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Request validation failed
- `500 Internal Server Error`: Server-side error

### Error Response Format

```json
{
  "detail": {
    "message": "Error message description",
    "code": "ERROR_CODE",
    "fields": {
      "field_name": "Error specific to this field"
    }
  }
}
```

## Flutter Implementation Guidelines

### Suggested Project Structure

```
lib/
├── config/
│   └── api_config.dart             # API base URL and headers config
├── models/                          # Data models
│   ├── user.dart
│   ├── product.dart
│   ├── cart.dart
│   ├── order.dart
│   └── recommendation.dart
├── services/                        # API services
│   ├── auth_service.dart
│   ├── product_service.dart
│   ├── cart_service.dart
│   ├── order_service.dart
│   └── recommendation_service.dart
├── controllers/                     # GetX controllers
│   ├── auth_controller.dart
│   ├── product_controller.dart
│   ├── cart_controller.dart
│   ├── order_controller.dart
│   └── recommendation_controller.dart
├── views/                           # UI screens and widgets
│   ├── auth/
│   │   ├── login_screen.dart
│   │   ├── register_screen.dart
│   │   └── profile_screen.dart
│   ├── products/
│   │   ├── product_list_screen.dart
│   │   ├── product_detail_screen.dart
│   │   └── widgets/
│   ├── cart/
│   │   └── cart_screen.dart
│   ├── checkout/
│   │   └── checkout_screen.dart
│   ├── orders/
│   │   ├── order_list_screen.dart
│   │   └── order_detail_screen.dart
│   ├── recommendations/
│   │   ├── recommended_products_widget.dart
│   │   └── similar_products_widget.dart
│   └── admin/
│       └── training_management_screen.dart
├── utils/                           # Utility functions
│   ├── http_client.dart             # HTTP client with auth interceptor
│   ├── error_handler.dart           # Global error handling
│   └── session_manager.dart         # Token storage and management
└── main.dart                        # App entry point
```

### API Service Implementation Example

Here's an example of how to implement the API service for products:

```dart
import 'package:dio/dio.dart';
import '../models/product.dart';
import '../utils/http_client.dart';

class ProductService {
  final HttpClient _httpClient;

  ProductService(this._httpClient);

  // Get all products with pagination and filtering
  Future<Map<String, dynamic>> getProducts({
    String? searchQuery,
    int? categoryId,
    double? minPrice,
    double? maxPrice,
    String orderBy = "created_at",
    bool descending = true,
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final Map<String, dynamic> queryParams = {
        if (searchQuery != null) 'search_query': searchQuery,
        if (categoryId != null) 'category_id': categoryId,
        if (minPrice != null) 'min_price': minPrice,
        if (maxPrice != null) 'max_price': maxPrice,
        'order_by': orderBy,
        'descending': descending,
        'page': page,
        'page_size': pageSize,
      };

      final response = await _httpClient.get('/products', queryParameters: queryParams);

      final products = (response.data['items'] as List)
          .map((item) => ProductListItem.fromJson(item))
          .toList();

      return {
        'products': products,
        'pagination': response.data['pagination'],
        'filters': response.data['filters'],
      };
    } catch (e) {
      rethrow;
    }
  }

  // Get product details
  Future<Product> getProductDetails(int productId) async {
    try {
      final response = await _httpClient.get('/products/$productId');
      return Product.fromJson(response.data);
    } catch (e) {
      rethrow;
    }
  }

  // Get all categories
  Future<List<Category>> getCategories() async {
    try {
      final response = await _httpClient.get('/products/categories');
      return (response.data as List)
          .map((item) => Category.fromJson(item))
          .toList();
    } catch (e) {
      rethrow;
    }
  }
}
```

### GetX Controller Implementation Example

Here's an example of a GetX controller for products:

```dart
import 'package:get/get.dart';
import '../models/product.dart';
import '../services/product_service.dart';

class ProductController extends GetxController {
  final ProductService _productService;

  ProductController(this._productService);

  // Observable variables
  var isLoading = false.obs;
  var products = <ProductListItem>[].obs;
  var pagination = {}.obs;
  var filters = {}.obs;
  var categories = <Category>[].obs;
  var selectedProduct = Rx<Product?>(null);

  @override
  void onInit() {
    super.onInit();
    fetchCategories();
  }

  Future<void> fetchProducts({
    String? searchQuery,
    int? categoryId,
    double? minPrice,
    double? maxPrice,
    String orderBy = "created_at",
    bool descending = true,
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      isLoading.value = true;

      final result = await _productService.getProducts(
        searchQuery: searchQuery,
        categoryId: categoryId,
        minPrice: minPrice,
        maxPrice: maxPrice,
        orderBy: orderBy,
        descending: descending,
        page: page,
        pageSize: pageSize,
      );

      products.value = result['products'];
      pagination.value = result['pagination'];
      filters.value = result['filters'];
    } catch (e) {
      Get.snackbar('Error', 'Failed to load products: ${e.toString()}');
    } finally {
      isLoading.value = false;
    }
  }

  Future<void> fetchProductDetails(int productId) async {
    try {
      isLoading.value = true;
      final product = await _productService.getProductDetails(productId);
      selectedProduct.value = product;
    } catch (e) {
      Get.snackbar('Error', 'Failed to load product details: ${e.toString()}');
    } finally {
      isLoading.value = false;
    }
  }

  Future<void> fetchCategories() async {
    try {
      final categoriesList = await _productService.getCategories();
      categories.value = categoriesList;
    } catch (e) {
      Get.snackbar('Error', 'Failed to load categories: ${e.toString()}');
    }
  }
}
```

### HTTP Client with Authentication

```dart
import 'package:dio/dio.dart';
import 'package:get_storage/get_storage.dart';

class HttpClient {
  late Dio _dio;
  final GetStorage _storage = GetStorage();

  HttpClient(String baseUrl) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 15),
    ));

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        // Add token to headers if available
        final token = _storage.read('access_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
      onError: (DioError error, handler) {
        // Handle 401 Unauthorized errors
        if (error.response?.statusCode == 401) {
          // Redirect to login
          // Get.offAllNamed('/login');
        }
        return handler.next(error);
      },
    ));
  }

  Future<Response> get(String path, {Map<String, dynamic>? queryParameters}) {
    return _dio.get(path, queryParameters: queryParameters);
  }

  Future<Response> post(String path, {dynamic data}) {
    return _dio.post(path, data: data);
  }

  Future<Response> put(String path, {dynamic data}) {
    return _dio.put(path, data: data);
  }

  Future<Response> delete(String path) {
    return _dio.delete(path);
  }
}
```

### Setup in main.dart

```dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';

import 'config/api_config.dart';
import 'utils/http_client.dart';
import 'services/auth_service.dart';
import 'services/product_service.dart';
import 'services/cart_service.dart';
import 'services/order_service.dart';
import 'services/recommendation_service.dart';
import 'controllers/auth_controller.dart';
import 'controllers/product_controller.dart';
import 'controllers/cart_controller.dart';
import 'controllers/order_controller.dart';
import 'controllers/recommendation_controller.dart';
// Import your views

void main() async {
  await GetStorage.init();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Initialize services and controllers
    final httpClient = HttpClient(ApiConfig.baseUrl);

    // Register services
    Get.put(AuthService(httpClient));
    Get.put(ProductService(httpClient));
    Get.put(CartService(httpClient));
    Get.put(OrderService(httpClient));
    Get.put(RecommendationService(httpClient));

    // Register controllers
    Get.put(AuthController(Get.find<AuthService>()));
    Get.put(ProductController(Get.find<ProductService>()));
    Get.put(CartController(Get.find<CartService>()));
    Get.put(OrderController(Get.find<OrderService>()));
    Get.put(RecommendationController(Get.find<RecommendationService>()));

    return GetMaterialApp(
      title: 'E-commerce AI App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      initialRoute: '/',
      getPages: [
        // Define your routes here
        // GetPage(name: '/', page: () => HomeScreen()),
        // ...
      ],
    );
  }
}
```
