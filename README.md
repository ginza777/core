# Digital Products Management System

A comprehensive Django-based system for managing digital products, sellers, and analytics.

## Project Structure

```
core/
├── manage.py              # Django's command-line utility
├── core_project/          # Project configuration directory
│   ├── __init__.py        # Python package marker
│   ├── settings.py        # Project settings and configuration
│   ├── urls.py           # URL declarations for the project
│   ├── wsgi.py           # WSGI application entry point
│   └── asgi.py           # ASGI application entry point
├── products/              # Products app
│   ├── models.py          # Data models
│   ├── admin.py           # Admin interface
│   ├── serializers.py     # API serializers
│   ├── api_views.py       # API views
│   └── urls.py            # App URL patterns
├── requirements.txt        # Python dependencies
├── API_DOCUMENTATION.md   # API documentation
└── README.md              # This file
```

## Features

### 🏪 **Product Management**
- **Digital Products**: Support for files, videos, audio, presentations, courses, and e-books
- **Pricing System**: Regular price, discount price, and automatic discount calculation
- **Content Types**: Multiple content type support with file information
- **SEO Friendly**: Automatic slug generation and meta information

### 👥 **Seller Management**
- **Seller Profiles**: Complete seller information with contact details
- **Product Association**: Track products by seller
- **Status Management**: Active/inactive seller status

### 📊 **Analytics & Tracking**
- **View Analytics**: Track product views with IP addresses and user agents
- **Performance Metrics**: View counts and engagement tracking
- **Session Tracking**: User session management for analytics

### 🎨 **Admin Interface**
- **Responsive Design**: Modern, mobile-friendly admin interface
- **Advanced Filtering**: Multiple filter options for easy data management
- **Bulk Actions**: Mass operations for products (feature, activate, deactivate)
- **Inline Editing**: Quick edit capabilities in list views
- **Search & Sort**: Advanced search and sorting functionality

## Models Structure

### 1. **Seller Model**
```python
- id: Unique seller identifier
- fullname: Seller's full name
- email: Contact email
- phone: Contact phone number
- address: Physical address
- is_active: Account status
- created_at/updated_at: Timestamps
```

### 2. **Document Model**
```python
- id: UUID primary key
- page_count: Number of pages
- file_size: File size in human-readable format
- file_type: File extension (.pdf, .docx, etc.)
- content_type: Type of content (file, video, audio, presentation)
- content_duration: Duration for media files
- short_content_url: Preview URL
```

### 3. **Product Model**
```python
- id: Unique product identifier
- title: Product name
- slug: SEO-friendly URL slug
- seller: Foreign key to Seller
- price: Original price
- discount_price: Discounted price
- discount: Discount percentage (auto-calculated)
- poster_url: Product image/thumbnail
- content_type: Product category
- document: One-to-one relationship with Document
- description: Product description
- tags: Searchable tags
- is_featured: Featured product flag
- is_active: Product availability
```

### 4. **ProductView Model**
```python
- product: Foreign key to Product
- ip_address: Visitor's IP address
- user_agent: Browser/client information
- referrer: Traffic source
- viewed_at: View timestamp
- session_id: User session identifier
```

## Installation & Setup

### 1. **Clone and Install Dependencies**
```bash
git clone <repository-url>
cd core
pip install -r requirements.txt
```

### 2. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. **Create Superuser**
```bash
python manage.py createsuperuser
```

### 4. **Populate Sample Data (Optional)**
```bash
python manage.py populate_sample_data
```

### 5. **Run Development Server**
```bash
python manage.py runserver
```

### 6. **Static File Management**
```bash
# Collect static files (required for WhiteNoise)
python manage.py collectstatic

# Clear static files cache
python manage.py collectstatic --clear
```

## Admin Interface Access

1. Navigate to `http://localhost:8000/admin/`
2. Login with your superuser credentials
3. Access the following admin sections:
   - **Sellers**: Manage seller accounts and information
   - **Documents**: Handle file metadata and content information
   - **Products**: Manage digital products, pricing, and features
   - **Product Views**: Monitor analytics and user engagement

## Admin Features

### **Product Management**
- ✅ List view with all product information
- ✅ Inline editing for quick updates
- ✅ Bulk actions for multiple products
- ✅ Advanced filtering and search
- ✅ Automatic discount calculation
- ✅ Featured product management

### **Seller Management**
- ✅ Seller profile management
- ✅ Product count tracking
- ✅ Contact information management
- ✅ Status control

### **Document Management**
- ✅ File metadata management
- ✅ Content type categorization
- ✅ Size and page count tracking
- ✅ Media duration support

### **Analytics Dashboard**
- ✅ View tracking with detailed information
- ✅ IP address and user agent logging
- ✅ Referrer tracking
- ✅ Session management

## Sample Data

The system includes sample data for testing:
- **3 Sellers**: Different seller profiles with contact information
- **4 Documents**: Various content types (docx, pdf, pptx, mp4)
- **4 Products**: Sample products with different pricing and features

## Customization

### **Adding New Content Types**
1. Update `CONTENT_TYPE_CHOICES` in models
2. Add new fields as needed
3. Run migrations

### **Extending Models**
- Add new fields to existing models
- Create new related models
- Customize admin interface

### **Admin Customization**
- Modify list displays
- Add custom filters
- Create custom actions
- Customize field sets

## API Endpoints

The system is designed to easily integrate with REST APIs:
- Product listing and details
- Seller information
- Analytics data
- Search and filtering

## Performance Features

- **Database Indexing**: Optimized queries with proper indexes
- **Select Related**: Efficient database queries
- **Pagination**: Admin list pagination for large datasets
- **Static File Optimization**: WhiteNoise for efficient static file serving
- **Caching Ready**: Prepared for Redis/Memcached integration

## Security Features

- **Admin Authentication**: Django's built-in security
- **Permission Control**: Granular admin permissions
- **Data Validation**: Form and model validation
- **SQL Injection Protection**: Django ORM security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

---

**Built with Django** - A high-level Python web framework that encourages rapid development and clean, pragmatic design.
