"""--format 미지원 서브커맨드(delete 등)에서 자동주입 거부 시 재시도 회귀 테스트."""
from atlassian_cli import mcp_server as server


def test_delete_retries_without_format(monkeypatch):
    calls = []

    def fake_run(args, creds=None):
        calls.append(list(args))
        if "--format" in args:
            # argparse가 미지원 인자 거부(실제 _run_cli가 exit2를 이렇게 반환)
            return "AUTH FAILURE (exit 2)\nerror: unrecognized arguments: --format json"
        return "Deleted page 123"

    monkeypatch.setattr(server, "_run_cli", fake_run)
    monkeypatch.setattr(server, "_is_write", lambda a: True)
    out = server.atlassian_cli(["confluence", "page", "delete", "123"], confirm_write=True)
    assert out == "Deleted page 123"
    # 1차: --format 주입, 2차: 원본(주입 없음)
    assert calls[0] == ["confluence", "page", "delete", "123", "--format", "json"]
    assert calls[1] == ["confluence", "page", "delete", "123"]


def test_read_keeps_format_no_retry(monkeypatch):
    calls = []

    def fake_run(args, creds=None):
        calls.append(list(args))
        return '{"id": "1"}'  # 정상

    monkeypatch.setattr(server, "_run_cli", fake_run)
    monkeypatch.setattr(server, "_is_write", lambda a: False)
    server.atlassian_cli(["confluence", "page", "get", "1"])
    assert len(calls) == 1  # 재시도 없음
    assert calls[0][-2:] == ["--format", "json"]


def test_non_format_error_no_retry(monkeypatch):
    """--format 무관 에러는 재시도하지 않는다(무한/불필요 재시도 방지)."""
    calls = []

    def fake_run(args, creds=None):
        calls.append(list(args))
        return "ERROR (exit 1)\nsome other failure"

    monkeypatch.setattr(server, "_run_cli", fake_run)
    monkeypatch.setattr(server, "_is_write", lambda a: True)
    server.atlassian_cli(["confluence", "page", "delete", "123"], confirm_write=True)
    assert len(calls) == 1  # 재시도 없음
