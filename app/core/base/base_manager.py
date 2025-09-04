from app.core.base.base_response import BaseResponse


class BaseManager:
    def base_success(self, payload=None):
        return BaseResponse.success(payload=payload)


    def base_error(self, message: str = None, payload=None):
        return BaseResponse.error(message=message, payload=payload)

