from pydantic import BaseModel
from supabase_auth import datetime

class User(BaseModel):
    uid: str
    full_name: str
    created_at: datetime = datetime.now()
    photo_url: str
    status: bool = True
    email: str
    info_message: str = ""
    last_request: datetime = datetime.now()