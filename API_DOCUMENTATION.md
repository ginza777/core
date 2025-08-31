# Digital Products API Documentation

## Overview

The Digital Products API provides comprehensive endpoints for managing digital products, sellers, documents, and analytics. Built with Django REST Framework using generic class-based views for optimal CRUD operations.

## Base URL

```
http://localhost:8000/api/v1/
```

## Authentication

- **Read Operations**: No authentication required
- **Write Operations**: Session authentication required
- **Admin Operations**: Full authentication required

## API Endpoints

### 1. Sellers

#### List/Create Sellers
```http
GET/POST /api/v1/sellers/
```

**Query Parameters:**
- `search`: Search in fullname, email, phone, address
- `is_active`: Filter by active status (true/false)
- `ordering`: Order by fullname, created_at, updated_at
- `page`: Page number for pagination

**Example Response:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "201745",
            "fullname": "Exclusive qog'ozlar",
            "email": "exclusive@example.com",
            "phone": "+998901234567",
            "address": "Tashkent, Uzbekistan",
            "is_active": true,
            "created_at": "2025-08-30T04:30:00Z",
            "updated_at": "2025-08-30T04:30:00Z",
            "products_count": 2
        }
    ]
}
```

#### Get Seller Details
```http
GET /api/v1/sellers/{id}/
```

**Response includes:**
- Seller information
- Associated products
- Contact details

#### Seller Analytics
```http
GET /api/v1/sellers/{id}/analytics/
```

**Response includes:**
- Seller statistics
- Product performance metrics
- Content type distribution

### 2. Documents

#### List/Create Documents
```http
GET/POST /api/v1/documents/
```

**Query Parameters:**
- `content_type`: Filter by content type (file, video, audio, presentation)
- `file_type`: Filter by file extension
- `ordering`: Order by created_at, file_size, page_count

**Example Response:**
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "uuid-here",
            "page_count": 1,
            "file_size": "17.81 KB",
            "file_type": ".docx",
            "content_type": "file",
            "created_at": "2025-08-30T04:30:00Z",
            "updated_at": "2025-08-30T04:30:00Z"
        }
    ]
}
```

#### Get Document Details
```http
GET /api/v1/documents/{id}/
```

### 3. Products

#### List/Create Products
```http
GET/POST /api/v1/products/
```

**Query Parameters:**
- `search`: Search in title, description, tags, seller name
- `content_type`: Filter by content type
- `is_featured`: Filter featured products (true/false)
- `is_active`: Filter active products (true/false)
- `seller`: Filter by seller ID
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `has_discount`: Filter products with/without discount
- `ordering`: Order by title, price, views_count, created_at, discount

**Example Response:**
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 369803,
            "title": "Yashil iqtisodiyot strategiyalari",
            "slug": "taqdimotlar-iqtisodiyot-yashil-iqtisodiyot-strategiyalari",
            "seller_name": "Exclusive qog'ozlar",
            "price": "16500.00",
            "discount_price": "16500.00",
            "discount_percentage": 0.0,
            "poster_url": "https://example.com/poster.jpg",
            "views_count": 0,
            "content_type": "file",
            "is_featured": true,
            "is_active": true,
            "created_at": "2025-08-30T04:30:00Z"
        }
    ]
}
```

#### Get Product Details
```http
GET /api/v1/products/{id}/
```

**Response includes:**
- Complete product information
- Seller details
- Document information
- View analytics

#### Advanced Product Search
```http
GET /api/v1/products/search/
```

**Advanced Query Parameters:**
- `q`: General search query
- `content_type`: Content type filter
- `seller_id`: Seller ID filter
- `min_price`: Minimum price
- `max_price`: Maximum price
- `has_discount`: Discount filter
- `is_featured`: Featured filter

#### Product Analytics
```http
GET /api/v1/products/analytics/
```

**Response includes:**
- Overall statistics
- Content type distribution
- Top viewed products
- Recent products

### 4. Product Views

#### List/Create Product Views
```http
GET/POST /api/v1/product-views/
```

**Query Parameters:**
- `product`: Filter by product ID
- `ip_address`: Filter by IP address
- `search`: Search in product title, IP, session ID

#### Get Product View Details
```http
GET /api/v1/product-views/{id}/
```

## Request/Response Examples

### Creating a New Product

**Request:**
```http
POST /api/v1/products/
Content-Type: application/json

{
    "title": "New Digital Product",
    "seller_id": "201745",
    "document_id": "uuid-here",
    "price": "25000.00",
    "discount_price": "20000.00",
    "poster_url": "https://example.com/poster.jpg",
    "content_type": "file",
    "description": "Product description here",
    "tags": "digital, product, new"
}
```

**Response:**
```json
{
    "id": 369807,
    "title": "New Digital Product",
    "slug": "new-digital-product",
    "seller": {
        "id": "201745",
        "fullname": "Exclusive qog'ozlar"
    },
    "price": "25000.00",
    "discount_price": "20000.00",
    "discount": 20,
    "discount_percentage": 20.0,
    "is_on_sale": true,
    "final_price": "20000.00",
    "poster_url": "https://example.com/poster.jpg",
    "content_type": "file",
    "description": "Product description here",
    "tags": "digital, product, new",
    "is_featured": false,
    "is_active": true
}
```

### Updating a Product

**Request:**
```http
PUT /api/v1/products/369803/
Content-Type: application/json

{
    "price": "18000.00",
    "discount_price": "15000.00",
    "is_featured": true
}
```

### Filtering Products

**Request:**
```http
GET /api/v1/products/?content_type=file&min_price=10000&max_price=20000&has_discount=true&ordering=-created_at
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid data or validation errors
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

**Error Response Format:**
```json
{
    "error": "Error message here",
    "detail": "Detailed error information"
}
```

## Pagination

All list endpoints support pagination with the following response format:

```json
{
    "count": 100,
    "next": "http://localhost:8000/api/v1/products/?page=2",
    "previous": null,
    "results": [...]
}
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

## Caching

The API implements intelligent caching:
- **Sellers**: 15 minutes
- **Documents**: 10 minutes  
- **Products**: 5 minutes
- **Search**: 3 minutes

## Rate Limiting

Currently no rate limiting implemented. Consider implementing for production use.

## Testing the API

### Using Swagger UI

1. Navigate to: `http://localhost:8000/swagger/`
2. Interactive API documentation
3. Test endpoints directly from browser

### Using cURL

**Get all products:**
```bash
curl -X GET "http://localhost:8000/api/v1/products/" \
     -H "accept: application/json"
```

**Create a product:**
```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
     -H "Content-Type: application/json" \
     -H "X-CSRFToken: your-csrf-token" \
     -d '{
       "title": "Test Product",
       "seller_id": "201745",
       "document_id": "uuid-here",
       "price": "10000.00",
       "poster_url": "https://example.com/poster.jpg",
       "content_type": "file"
     }'
```

## Admin Interface

Access the enhanced admin interface at:
- **URL**: `http://localhost:8000/admin/`
- **Features**: 
  - Modern Jazzmin UI
  - Responsive design
  - Advanced filtering
  - Bulk operations
  - Analytics dashboard

## Development

### Running the Server
```bash
python3 manage.py runserver
```

### Creating Superuser
```bash
python3 manage.py createsuperuser
```

### Populating Sample Data
```bash
python3 manage.py populate_sample_data
```

### Running Tests
```bash
python3 manage.py test
```

## Production Considerations

1. **Security**: Implement proper authentication and authorization
2. **Rate Limiting**: Add rate limiting for API endpoints
3. **Caching**: Configure Redis/Memcached for better performance
4. **Monitoring**: Add logging and monitoring
5. **Documentation**: Keep API documentation updated
6. **Versioning**: Plan for API versioning strategy

## Support

For API support and questions:
- Email: contact@example.com
- Documentation: `/swagger/` or `/redoc/`
- Admin Interface: `/admin/`
