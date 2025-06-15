# Django Messaging App

This is a messaging application built with Django, designed to demonstrate the use of advanced ORM techniques, Django signals, custom model managers, threaded messaging, and view caching.

## Features

- **User-to-user messaging** with support for message editing and history
- **Threaded conversations** with recursive message replies
- **Real-time-like notifications** using Django signals
- **Message history tracking** on edit
- **Soft deletion** of user data with cascading cleanup of related models
- **Custom model manager** to filter unread messages
- **Optimized queries** with `select_related`, `prefetch_related`, and `.only()`
- **Basic view caching** using Django’s `cache_page` decorator



## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/alx-backend-python.git
   cd alx-backend-python/Django-signals_orm-0x04/messaging_app
   ```

2. **Create and activate a virtual environment**

```bash
    python -m venv .venv
    source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

3. **Install dependencies**

```bash
    pip install -r requirements.txt
```



4. **Apply migrations**
```bash
python manage.py migrate
```
5. **Create a superuser**
```bash
Copy code
python manage.py createsuperuser
```
6. Run the development server

```bash
Copy code
python manage.py runserver
```


## Authors
Vincent Dushime 

ALX Software Engineering Program

## License

This project is for educational purposes and part of the ALX Backend Specialization.