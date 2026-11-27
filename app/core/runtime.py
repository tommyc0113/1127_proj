"""임시 뼈대 2/3: DB 조회 경로를 먼저 연결. 09절에서 최종 교체한다."""
from app.core.settings import load_settings
from app.db.connection import Database
from app.db.repository import Repository
from app.core.preflight import preflight
from app.agent import AgentService, make_model
from app.services.errors import ServiceError

class PendingRag:
    def run(self, question, query, category_code, k, meter):
        # 실제 RAG 구현은 아직 없다. 허위 결과를 반환하지 않는다.
        raise ServiceError('NOT_IMPLEMENTED', 'rag_pending')

class Runtime:
    def __init__(self):
        self.settings = load_settings()
        self.db = Database(self.settings)
        self.repo = Repository(self.db)
        self.model_factory = lambda: make_model(self.settings)
        self.pipeline = PendingRag()
        self.agent = AgentService(self.settings, self.repo,
                                  self.pipeline, self.model_factory)

    def health(self):
        # 기존 정답 Preflight를 그대로 실행한다. 아직 RAG 추론은 미검증이다.
        return preflight(self.settings, self.repo)

    def close(self):
        self.db.close()
