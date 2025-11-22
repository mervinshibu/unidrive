upload_responses = {
    200: {
        "description": "File uploaded successfully",
        "content": {
            "application/json": {
                "example": {
                    "id": "f3a9c640-8b1d-4a6d-a50c-61a9f3a07a3b",
                    "message": "File uploaded successfully"
                }
            }
        }
    },
    400: {
        "description": "No file uploaded",
        "content": {
            "application/json": {
                "example": {
                    "error": "No file found in the request"
                }
            }
        }
    },
    413: {
        "description": "File too large (max 20MB)",
        "content": {
            "application/json": {
                "example": {
                    "error": "File exceeds maximum allowed size of 20MB"
                }
            }
        }
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {
                    "error": "Failed to upload file due to a server error"
                }
            }
        }
    },
}

get_all_files_responses = {
    200: {
        "description": "List of all uploaded files",
        "content": {
            "application/json": {
                "example": [
                    [
                        {
                            "size": 5992843,
                            "s3_key": "87e4f50c-9e2f-4b66-9ee2-de2a562a3949_MENU (2).pdf",
                            "id": "87e4f50c-9e2f-4b66-9ee2-de2a562a3949",
                            "mime_type": "application/pdf",
                            "filename": "MENU (2).pdf",
                            "uploaded_at": "2025-11-21T18:05:43.246495"
                        },
                        {
                            "size": 19465965,
                            "s3_key": "fa901890-08de-45d6-8e07-1ea3d9767a0f_Sky Kisses Earth.mp3",
                            "id": "fa901890-08de-45d6-8e07-1ea3d9767a0f",
                            "mime_type": "audio/mpeg",
                            "filename": "Sky Kisses Earth.mp3",
                            "uploaded_at": "2025-11-21T18:09:11.757382"
                        }
                    ]
                ]
            }
        }
    }
}

get_file_responses = {
    200: {
        "description": "File retrieved successfully",
        "content": {
            "application/octet-stream": {
                "example": "Binary data of the file"
            }
        }
    },
    404: {
        "description": "File not found",
        "content": {
            "application/json": {
                "example": {
                    "message": "File with File ID does not exist"
                }
            }
        }
    }
}

delete_file_responses = {
    200: {
        "description": "File deleted successfully",
        "content": {
            "application/json": {
                "example": {
                    "message": "File deleted successfully"
                }
            }
        }
    },
    404: {
        "description": "File not found",
        "content": {
            "application/json": {
                "example": {
                    "message": "File with File ID does not exist"
                }
            }
        }
    }
}