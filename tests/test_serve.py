from atlassian_cli import mcp_server as server


def test_serve_http_sets_transport_and_port(monkeypatch):
    called = {}
    monkeypatch.setattr(server.mcp, "run", lambda **kw: called.update(kw))
    server._serve(["--http", "--port", "8811"])
    assert called.get("transport") == "streamable-http"
    assert server.mcp.settings.port == 8811
    assert server.mcp.settings.host == "127.0.0.1"


def test_serve_stdio_default(monkeypatch):
    called = {}
    monkeypatch.setattr(server.mcp, "run", lambda **kw: called.update(kw))
    server._serve([])
    assert "transport" not in called
