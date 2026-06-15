"""confluence space mine: 현재 인증 사용자의 본인 개인 스페이스를 결정론적으로 해소."""
import types

from atlassian_cli.confluence import spaces


class _FakeConf:
    def __init__(self):
        self.queried_key = None

    def get(self, path):
        assert path == "rest/api/user/current"
        return {"accountId": "712020:ce29-2396-abcd"}

    def get_space(self, key):
        self.queried_key = key
        return {"key": key, "name": "me", "type": "personal"}


def test_space_mine_resolves_own_personal_space(monkeypatch):
    fake = _FakeConf()
    monkeypatch.setattr(spaces, "get_confluence", lambda: fake)
    args = types.SimpleNamespace(space_cmd="mine", format="json")
    spaces.handle_space(args)
    # accountId의 ':'·'-' 제거 후 '~' 접두 = 본인 개인 스페이스 키(추측 아님)
    assert fake.queried_key == "~712020ce292396abcd"


def test_space_mine_no_account_errors(monkeypatch):
    class _NoAcct(_FakeConf):
        def get(self, path):
            return {}
    monkeypatch.setattr(spaces, "get_confluence", lambda: _NoAcct())
    args = types.SimpleNamespace(space_cmd="mine", format="json")
    try:
        spaces.handle_space(args)
    except SystemExit:
        pass  # output_error → exit
