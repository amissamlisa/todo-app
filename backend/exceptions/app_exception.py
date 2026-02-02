from typing import Any, Union
class AppException(Exception):
  def __init__(
    self,
    error_code: str,
    error_message: str,
    error: Union[Any, None] = None,
    status_code: int = 500,
    headers: dict | None = None,
  ):
    self.status_code = status_code
    self.error_code = error_code
    self.error_message = error_message
    self.error = error
    self.headers = headers
    super().__init__(self.error_message)