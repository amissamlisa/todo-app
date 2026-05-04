def validate_password_byte_length(password: str, max_bytes: int = 72) -> None:
    if len(password.encode("utf-8")) > max_bytes:
        raise ValueError("パスワードは72バイト以内で入力してください")
