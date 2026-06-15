import types
from atlassian_cli import mcp_server as server


def _set_ctx(request, headers):
    """HTTP 서빙 요청 시뮬: request_ctx에 request(헤더 보유) 설정."""
    from mcp.server.lowlevel.server import request_ctx
    rc = types.SimpleNamespace(request=types.SimpleNamespace(headers=headers))
    token = request_ctx.set(rc)
    request.addfinalizer(lambda: request_ctx.reset(token))


def test_delegate_creds_used_on_write(monkeypatch, request):
    captured = {}
    monkeypatch.setattr(server, "_run_cli", lambda args, creds=None: captured.update(args=args, creds=creds) or "OK")
    monkeypatch.setattr(server, "_is_write", lambda a: True)
    _set_ctx(request, {"x-atlassian-email": "u@medit.com", "x-atlassian-token": "utok"})
    server.atlassian_cli(["jira", "issue", "comment", "X-1", "--body", "hi"], confirm_write=True)
    assert captured["creds"] == {"email": "u@medit.com", "token": "utok"}


def test_delegate_creds_used_on_read(monkeypatch, request):
    """읽기도 요청자 본인 자격으로 실행(관련 없는 기본 계정 금지)."""
    captured = {}
    monkeypatch.setattr(server, "_run_cli", lambda args, creds=None: captured.update(creds=creds) or "OK")
    monkeypatch.setattr(server, "_is_write", lambda a: False)
    _set_ctx(request, {"x-atlassian-email": "u@medit.com", "x-atlassian-token": "utok"})
    server.atlassian_cli(["jira", "issue", "get", "X-1"])
    assert captured["creds"] == {"email": "u@medit.com", "token": "utok"}


def test_served_request_without_creds_refused(monkeypatch, request):
    """서빙(HTTP) 요청인데 유저 자격 없으면 기본 계정 폴백 없이 거부(_run_cli 미호출)."""
    called = {"run": False}
    monkeypatch.setattr(server, "_run_cli", lambda args, creds=None: called.update(run=True) or "OK")
    monkeypatch.setattr(server, "_is_write", lambda a: False)
    _set_ctx(request, {})  # 서빙 요청이나 atlassian 자격 헤더 없음
    out = server.atlassian_cli(["jira", "issue", "get", "X-1"])
    assert called["run"] is False
    assert "유저 자격 없음" in out


def test_local_stdio_without_creds_uses_default(monkeypatch):
    """로컬 stdio(서빙 아님)에선 자격 없어도 기본 config 사용(creds=None, 실행)."""
    captured = {}
    monkeypatch.setattr(server, "_run_cli", lambda args, creds=None: captured.update(creds=creds, run=True) or "OK")
    monkeypatch.setattr(server, "_is_write", lambda a: False)
    server.atlassian_cli(["jira", "issue", "get", "X-1"])  # request_ctx 미설정
    assert captured.get("run") is True
    assert captured["creds"] is None
