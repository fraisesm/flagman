class Signature:
    def __init__(
        self,
        document_id: int,
        user_id: int,
        phone_signature: str,
        confirmation_channel: str,
    ):
        self.document_id = document_id
        self.user_id = user_id
        self.phone_signature = phone_signature
        self.confirmation_channel = confirmation_channel