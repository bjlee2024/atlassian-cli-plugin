import types
from atlassian_cli import mcp_server as server


def _set_ctx(request, headers):
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


def test_no_delegate_on_read(monkeypatch, request):
    captured = {}
    monkeypatch.setattr(server, "_run_cli", lambda args, creds=None: captured.update(creds=creds) or "OK")
    monkeypatch.setattr(server, "_is_write", lambda a: False)
    _set_ctx(request, {"x-atlassian-email": "u@medit.com", "x-atlassian-token": "utok"})
    server.atlassian_cli(["jira", "issue", "get", "X-1"])
    assert captured["creds"] is None


def test_write_without_headers_uses_service_account(monkeypatch):
    captured = {}
    monkeypatch.setattr(server, "_run_cli", lambda args, creds=None: captured.update(creds=creds) or "OK")
    monkeypatch.setattr(server, "_is_write", lambda a: True)
    server.atlassian_cli(["jira", "issue", "comment", "X-1", "--body", "hi"], confirm_write=True)
    assert captured["creds"] is None
