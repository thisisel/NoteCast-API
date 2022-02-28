
import cloudinary
from note_cast.core.settings import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)

import cloudinary.api

notification_url = settings.CLOUDINARY_NOTIFICATION_URL


