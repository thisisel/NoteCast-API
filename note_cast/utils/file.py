class FileUtils:

    @classmethod
    def get_random_filename(cls, ext: str = "mp3"):
        import secrets

        random_hex = secrets.token_hex(8)
        return f"{random_hex}.{ext}"

