class CloudinaryUploadException(Exception):
    """Exception raised for errors in cloudinary upload process.
    """

    def __init__(
        self,
        message="Error in cloudinary upload process",
        error: str= None,
    ):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'CLOUDINARY UPLOAD ERROR : {self.message} \n {self.error} : '
