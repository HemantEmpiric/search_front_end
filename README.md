# Restaurant Search Application

A Django-based web application for searching and discovering restaurants with advanced filtering capabilities, caching, and detailed restaurant information.

## 🍽️ Features

- **Advanced Search**: Search restaurants by name, cuisine, address, and neighbourhood
- **Restaurant Details**: Comprehensive restaurant information including ratings, price ranges, and vibes
- **Caching System**: Built-in caching for improved search performance
- **Sample Data**: Populate the database with sample restaurant data for testing
- **Responsive Design**: Modern, user-friendly interface
- **Operating Hours**: Detailed operating hours for each day of the week
- **Image Galleries**: Multiple images per restaurant

## 🏗️ Project Structure

```
mainSearch/
├── basicSearch/           # Main Django app
│   ├── models.py         # Restaurant data model
│   ├── views.py          # API endpoints and views
│   ├── urls.py           # URL routing
│   ├── admin.py          # Django admin configuration
│   └── templates/        # HTML templates
│       └── basicSearch/
│           ├── index.html
│           └── restaurant_detail.html
├── mainSearch/           # Django project settings
│   ├── settings.py       # Project configuration
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI application
├── db.sqlite3            # SQLite database
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip3 (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Navigate to the project directory**
   ```bash
   cd /home/empiric/Desktop/Search
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv env
   ```

3. **Activate the virtual environment**
   ```bash
   source env/bin/activate  # On Linux/Mac
   # OR
   env\Scripts\activate     # On Windows
   ```

4. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   cd mainSearch
   python3 manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python3 manage.py createsuperuser
   ```

7. **Populate sample data**
   ```bash
   python3 manage.py runserver
   ```
   Then visit: `http://localhost:8000/populate/`

8. **Start the development server**
   ```bash
   python3 manage.py runserver
   ```

9. **Access the application**
   - Main search page: `http://localhost:8000/`
   - Admin interface: `http://localhost:8000/admin/`

## 📊 Data Model

### Restaurant Model

The application uses a comprehensive `Restaurant` model with the following fields:

- **Basic Info**: name, address, neighbourhood, cuisine
- **Location**: latitude, longitude, place_id
- **Contact**: phone, website, reservation_url, menu_url
- **Social Media**: Instagram, Facebook, Twitter, TikTok URLs
- **Business Info**: rating, price_range, reservation_partner
- **Features**: vibes (atmosphere tags), operating_hours, images
- **Metadata**: created_at, updated_at

### Vibes Categories

The application supports various atmosphere tags:
- `aesthetic`, `bar`, `brunch`, `business`, `casual`
- `chic`, `cozy`, `date`, `fancy`, `finedining`
- `intimate`, `lively`, `luxury`, `romantic`, `view`
- And many more...

## 🔌 API Endpoints

### Search API

**GET** `/search/`
- **Purpose**: Search restaurants with caching
- **Parameters**: 
  - `q` (string): Search query
- **Response**: JSON with restaurant results
- **Caching**: 5-minute cache for improved performance

**Example Request:**
```bash
curl "http://localhost:8000/search/?q=pizza"
```

**Example Response:**
```json
{
  "success": true,
  "results": [
    {
      "id": "uuid-here",
      "name": "Pizza Palace",
      "cuisine": "Italian",
      "address": "123 Main St, Downtown, City",
      "neighbourhood": "Downtown",
      "rating": 4.5,
      "price_range": "$$",
      "vibes": ["casual", "family-friendly", "lively"],
      "reservation_partner": "OpenTable",
      "main_image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800"
    }
  ],
  "count": 1,
  "cached": false
}
```

### Restaurant Detail

**GET** `/restaurant/<uuid:restaurant_id>/`
- **Purpose**: Get detailed information about a specific restaurant
- **Parameters**: restaurant_id (UUID)
- **Response**: HTML page with restaurant details

### Cache Management

**GET** `/cache/clear/`
- **Purpose**: Clear all search cache entries
- **Response**: JSON with cache clearing status

**GET** `/cache/stats/`
- **Purpose**: Get cache statistics
- **Response**: JSON with cache information

### Data Population

**GET** `/populate/`
- **Purpose**: Populate database with sample restaurant data
- **Response**: Success message or "Sample data already exists!"

## 🎨 Frontend Features

### Search Interface
- Real-time search with AJAX
- Responsive design for mobile and desktop
- Search suggestions and autocomplete
- Filter by cuisine, neighbourhood, and vibes

### Restaurant Cards
- Beautiful image galleries
- Rating display with stars
- Price range indicators
- Quick access to reservations and menus
- Social media links

### Restaurant Detail Pages
- Comprehensive restaurant information
- Operating hours display
- Image carousel
- Contact information
- Social media integration

## 🛠️ Development

### Adding New Features

1. **Create new models** in `basicSearch/models.py`
2. **Add views** in `basicSearch/views.py`
3. **Update URLs** in `basicSearch/urls.py`
4. **Create templates** in `basicSearch/templates/basicSearch/`
5. **Run migrations** for model changes

### Database Operations

```bash
# Create new migration
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate

# Reset database (WARNING: deletes all data)
python3 manage.py flush
```

## 📦 Dependencies

### Core Dependencies

The application uses the following Python packages:

- **Django 5.2.5**: Web framework
- **asgiref 3.9.1**: ASGI utilities
- **sqlparse 0.5.3**: SQL parsing utilities
- **typing-extensions 4.15.0**: Type hints support

### Installation

All dependencies are listed in `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

### Adding New Dependencies

When adding new packages:

1. Install the package: `pip3 install package-name`
2. Update requirements.txt: `pip3 freeze > requirements.txt`
3. Commit both changes to version control

## 🔧 Configuration

### Settings

Key settings in `mainSearch/settings.py`:

- **Database**: SQLite (default) - can be changed to PostgreSQL/MySQL
- **Cache**: Local memory cache with 5-minute timeout
- **Debug**: Enabled for development
- **Secret Key**: Change for production deployment

### Environment Variables

For production, consider using environment variables for:
- `SECRET_KEY`
- `DEBUG`
- `DATABASE_URL`
- `ALLOWED_HOSTS`

## 📝 License

This project is private and available under the [MIT License](LICENSE).


