import requests
from django.conf import settings


class AIServiceError(Exception):
    def __init__(self, message, status_code=502, detail=None):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail


def _post(path, payload):
    connect_timeout = getattr(settings, 'AI_SERVER_CONNECT_TIMEOUT', 5)
    read_timeout = getattr(settings, 'AI_SERVER_READ_TIMEOUT', 180)
    url = f"{settings.AI_SERVER_URL.rstrip('/')}{path}"

    try:
        resp = requests.post(url, json=payload, timeout=(connect_timeout, read_timeout))
    except requests.Timeout as exc:
        raise AIServiceError('AI 서버 응답 시간이 초과되었습니다.', status_code=504) from exc
    except requests.RequestException as exc:
        # 연결 자체가 안 되는 경우 (FastAPI 프로세스 중단·주소 오류) → 502
        raise AIServiceError(f'AI 서버에 연결할 수 없습니다: {exc}', status_code=502) from exc

    try:
        data = resp.json()
    except ValueError as exc:
        raise AIServiceError('AI 서버 응답이 JSON 형식이 아닙니다.', status_code=502) from exc

    if resp.status_code >= 400:
        detail = data.get('detail') if isinstance(data, dict) else data
        message = detail if isinstance(detail, str) else 'AI 서버 오류'
        # 계약서 기준: 422(입력검증)·503(KoBERT 문제)만 그대로 전달, 그 외 예상 못 한 코드는 502로 정규화
        normalized_status = resp.status_code if resp.status_code in (422, 503) else 502
        raise AIServiceError(message, status_code=normalized_status, detail=detail)

    return data


def analyze_events(text):
    """자연어 사건 탐지. Django는 결과를 저장하지 않고 그대로 프론트에 중계한다."""
    return _post('/v1/events/analyze', {'text': text})


def run_analysis(payload):
    """전체 주거 금융 분석. payload는 payload_builder.build_analysis_payload()로 생성한다."""
    return _post('/v1/analysis/run', payload)