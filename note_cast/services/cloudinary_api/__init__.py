import cloudinary
from note_cast.core.settings import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)

notification_url = settings.CLOUDINARY_NOTIFICATION_URL
cloudinary_folder = settings.CLOUDINARY_FOLDER
asset_folder_path = lambda p_id, e_id : f"{cloudinary_folder}/{p_id}/{e_id}/"

