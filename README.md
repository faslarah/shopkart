# 🛒 ShopKart — Django E-Commerce Platform

A full-featured, production-ready e-commerce web application built with **Django**, featuring product management, session-based cart, Stripe payments, loyalty points, and Docker support.

---

## 🚀 Live Demo

> Deployed on [Render](https://openmall.onrender.com) *(may take a few seconds to wake up on free tier)*

---

## ✨ Features

### 🛍️ Store
- Product listing with categories, search, and filters
- Product detail page with image, description, brand, rating, and stock
- Featured and Bestseller product sections
- Discount percentage display (original price vs sale price)
- Product reviews and star ratings by authenticated users

### 🧺 Cart
- Session-based shopping cart (no login required to add items)
- Add, update quantity, and remove items
- Real-time cart total calculation

### 👤 User Accounts
- Register, Login, and Logout
- User profile with avatar, address, phone, city, state, and pincode
- Order history
- Wishlist — save products for later

### 📦 Orders
- Multi-step checkout with shipping address form
- Stripe payment integration (test & live mode)
- Order status tracking: `Pending → Processing → Shipped → Delivered → Cancelled`
- Email confirmation on order placement (via Gmail SMTP)

### 🎁 Loyalty Points System
- Earn points on every purchase (fully configurable via admin)
- Redeem points for discounts at checkout
- Admin-controlled loyalty settings (points per ₹ spent, redemption rate, minimum points)

### 🧑‍💼 Admin Dashboard
- Custom dashboard for managing products, categories, orders, and users
- Sales analytics and order management

### ⚙️ DevOps
- **Docker** + **Docker Compose** for containerized deployment
- **Celery** + **Redis** for background task processing (e.g., email sending)
- **Cloudinary** for cloud image storage (production)
- **WhiteNoise** for static file serving
- **Gunicorn** as the production WSGI server
- Deployable to **Render**, **Railway**, or any cloud platform

---

## 🗂️ Project Structure

```
shopkart/
│
├── ecommerce/          # Main Django project config (settings, urls, celery)
├── store/              # Products, Categories, Reviews
├── cart/               # Session-based Cart logic
├── orders/             # Order model, checkout, Stripe payment
├── accounts/           # User Profile, Wishlist, Loyalty Points
├── dashboard/          # Admin analytics dashboard
│
├── templates/          # All HTML templates
├── static/             # CSS, JS, and image assets
├── media/              # Uploaded product/category images (local dev)
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── build.sh
└── manage.py
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.9, Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Payments | Stripe |
| Task Queue | Celery + Redis |
| Image Storage | Cloudinary (prod) / Local (dev) |
| Static Files | WhiteNoise |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Forms | Django Crispy Forms + Bootstrap5 |
| Containerization | Docker, Docker Compose |
| Deployment | Render / Gunicorn |

---

## ⚡ Getting Started (Local Development)

### Prerequisites
- Python 3.9+
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/faslarah/shopkart.git
cd shopkart
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

# Stripe (use test keys for development)
STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxx

# Email (optional for local dev)
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Cloudinary (optional for local dev — leave blank to use local storage)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

> 💡 **For local development**, you can leave Cloudinary fields blank. Product images will be stored in the local `media/` folder.

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open 👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Admin Panel 👉 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🐳 Run with Docker

Make sure Docker Desktop is running, then:

```bash
docker-compose up --build
```

Open 👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 💳 Stripe Test Card

Use this card number to test payments locally:

| Field | Value |
|---|---|
| Card Number | `4242 4242 4242 4242` |
| Expiry | Any future date (e.g. `12/34`) |
| CVC | Any 3 digits (e.g. `123`) |

---

## 📸 Screenshots

> *(Add screenshots of the homepage, product page, cart, and checkout here)*

---

## 📋 Environment Variables Reference

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Django secret key | ✅ Yes |
| `DEBUG` | Set `True` for dev, `False` for prod | ✅ Yes |
| `STRIPE_PUBLIC_KEY` | Stripe publishable key | ✅ For payments |
| `STRIPE_SECRET_KEY` | Stripe secret key | ✅ For payments |
| `EMAIL_HOST_USER` | Gmail address for sending emails | Optional |
| `EMAIL_HOST_PASSWORD` | Gmail App Password | Optional |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Optional (prod) |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Optional (prod) |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Optional (prod) |
| `CELERY_BROKER_URL` | Redis URL for Celery | Optional |

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Fasla Rah**
- GitHub: [@faslarah](https://github.com/faslarah)

---

> Built with ❤️ using Django
