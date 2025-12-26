"""
 _    _           _        __  __           _          _   _                 _           
| |  | |         | |      |  \/  |         | |        | | (_)               | |          
| |__| | ___  ___| |_ ___ | \  / | ___  ___| |__   ___| |_ _  ___  _ __  ___| |_ ___  _ __ 
|  __  |/ _ \/ __| __/ _ \| |\/| |/ _ \/ __| '_ \ / _ \ __| |/ _ \| '_ \/ __| __/ _ \| '__|
| |  | |  __/\__ \ || (_) | |  | |  __/\__ \ | | |  __/ |_| | (_) | | | \__ \ || (_) | |   
|_|  |_|\___||___/\__\___/|_|  |_|\___||___/_| |_|\___|\__|_|\___/|_| |_|___/\__\___/|_|   

Hostel Management System 🏨 — ASGI configuration

Design / Topic: Hostel Management System
Project: Hostel Management System
Version: 0.1.0
Author: Your Name

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Project metadata / stylish header
PROJECT_TITLE = "Hostel Management System"
PROJECT_VERSION = "0.1.0"
PROJECT_AUTHOR = "Your Name"
PROJECT_EMOJI = "🏨"


def project_banner() -> str:
    """Return a compact project banner used for logs or quick identification."""
    return f"{PROJECT_EMOJI} {PROJECT_TITLE} — v{PROJECT_VERSION} by {PROJECT_AUTHOR}"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_asgi_application()
