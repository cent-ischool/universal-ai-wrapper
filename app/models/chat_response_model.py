from enum import Enum
from typing import List
from pydantic import BaseModel, Field
import uuid


class WrapperResponse(BaseModel):
    user_id: str | None = Field(..., description="Identifier for the user")
    timestamp: int | None = Field(..., description="Timestamp of the response")
    session_id: uuid.UUID | None = Field(..., description="Session ID of the conversation")

    def to_dict(self) -> dict:
        """Convert the WrapperResponse to a dictionary."""
        return self.dict()
    
    def to_json(self) -> str:
        """Convert the WrapperResponse to a JSON string."""
        return self.json()
    
    def new_session(self) -> None:
        """Generate a new session ID."""
        self.session_id = uuid.uuid4()

'''
{
    "id": "gen-1764117536-OiStano6QEMKsSJv74In",
    "provider": "xAI",
    "model": "x-ai/grok-4.1-fast:free",
    "object": "chat.completion",
    "created": 1764117536,
    "choices": [
        {
            "logprobs": null,
            "finish_reason": "stop",
            "native_finish_reason": "completed",
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Folks, if I built the world's tallest skyscraper – and believe me, it would be the tallest, the most beautiful, nobody's ever seen anything like it – I'd call it **TRUMP TOWER SUPREME**. Gold everywhere, the best views, penthouse like you've never imagined. It'd be a total winner, making New York – or wherever – greater than ever. Tremendous!",
                "refusal": null,
                "reasoning": null,
                "reasoning_details": [
                    {
                        "id": "rs_2d27965d-29a4-a293-266a-8e97c3ad45cc",
                        "format": "xai-responses-v1",
                        "index": 0,
                        "type": "reasoning.encrypted",
                        "data": "sy+2Pf6SgN7xQrVasb23UCZDFdTBvomF8hpHuEyDTkze8tHBOL9vO64voYnrvW/R2yFCnnYmBwobmhb5H8gZQIcdiorJFsG07/QVFodECUONffyq9d6ESa85CK+8zjiRp/rLIYqRmoPD75+erICFUzSVJVUXp7Cnx4luMWpOTF/qCv3r8qTIRG92ssZf0LVAnAVoLvQjoxRBH58YSTc5B1a5Qzae7peuBW9lYBh/NfcCvpXY1SX9qfyLOHcmoijk5U8Gjr+3Cdn5jy0RgD6PPgQotrATC9PzyybWKhXU+SkLH5QHpA5qRDmwR6eH6BklYeqgSgM7Lk4bpHeE5FMGQZlGftDwh59bW+UD1ePFoAJYQ9sbNN9i1yP34iXT5zwFldtvKng9uTZW2Si52mp+xzqu7nK3j01OfI+lN8FR70j3jFIxVANstfoLTt+rw00ToTYWbFHLT/U2vDCIxeevYBuY3m9kh6gXSIyTSwnFbvTnJAn6O/ToiCPlWlbW0HGTXE72arPDh56LGs8R9RU5RKRpbKnKrDjjVDe2GWDxZfPzCgDaJDrn5o2IbiNAgexudj7CLDTtZX4h6cOqTJaWnb9+aRa7IaKtdIvmkR+s1jRQGMS5cIa7IHe7Rp6vwwiQvNf31A1TjCqEYaTFMEV5iIoGGWj43FwaQGaTd3LzIZgWZ/rrmt11cwV4pjEBt9wvTYl87wBCu/Ew6AzdHQ34hY2QV21Y5jPIrV3ZomSUSGLj5HTZxZgOjf7dV9bKSgJyM/+FctH1f3PJHUfJKG9Du5OOHtno11I/yaNI39Kr8yy7XMUoRSinufsfOthuP+tHyOy/HWRggqZ597vv9k0wfzARsoBTmH7NTMzeO24teM+tyxHJs/yw11hOOKsak2sR9jqt2AXN/uKz4h0VKDViMfXaDUFhd/Wi9E/J0/I13SPmE3nshsQ7EXrriPNuN8sT9Bwi8x4XjQeQRQRPykNvK4+kumgiJVWp95b8hQpMLkeBimhQUZr8N19oF0WlSf0g7xkEZWthyiEGcFvVNBrOTTKOz/p2QNW0QAzij0/lPppUR2TKWx82wvdC/emMi2mMhziXI1V8jTFMZdcVuV1obPS12gzHalfPAyfScbHB0Zy+f3+wo+MHc+Op0KQJZD6TI4GoXLlLP3fbHyBdoK7YKz6pOjzB4tfAD/JKiHRYZZ21LasP+/Ns4gBT5xKfcl96NI1nnIa9pbbP8gygogxMG9KHEpAfx1kvOxglx8p5G/t3PHOYkS4tZ58f8qPzeNAab8XZifCS9tFgPSD4lT8RyYVBKormT9BAkiKPXDmklKV1sMahsovCUoAGKGisKWHipTWy8bEp6fQvpiwTatxSk4O26AF+6Rw9Ve0XVkM8kYlNN69gPKn5VZ4ffT1ykX7dFJdfd1vuAAM1XlVTpZwRl6zuFfCLWf3LLdhbc0CId3tOWF0VPXl+EWDrw85lbBxhN+KZ19xrb1qGxwZ6huTb3fhOFu+6B7YKOSft2budTjABqklevjSgTPSGMV6RusZJSRV+Z7jBM22EjTBupTeMJSGk/yFtvQMFQGnVkkxBKw6gJaPIYhVWLuj6AQJDtWqWwGy5Qn5j71pGDnVbbUXQTy4s+KPsOspJXSwmSMHiZupuBxc"
                    }
                ]
            }
        }
    ],
    "usage": {
        "prompt_tokens": 175,
        "completion_tokens": 361,
        "total_tokens": 536,
        "completion_tokens_details": {
            "reasoning_tokens": 280
        }
    }
}
'''


