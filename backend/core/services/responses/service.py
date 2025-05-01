from backend.core.services.responses.repository import ResponseRepository


class ResponseService:

    def __init__(self, resp_repo: ResponseRepository):
        self.resp_repo = resp_repo
