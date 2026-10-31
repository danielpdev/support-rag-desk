import pytest
from app.core import Support


@pytest.fixture
def support(tmp_path):
    return Support("sqlite:///" + str(tmp_path / "support.sqlite"))


def test_scope_before_retrieval(support):
    a = support.ask("acme", "refund deadline")
    b = support.ask("beacon", "refund deadline")
    assert "30 days" in a["answer"] and "7 days" in b["answer"]
    assert {x["tenant"] for x in a["sources"]} == {"acme"}


def test_unknown_abstains_and_ticket_is_scoped(support):
    r = support.ask("acme", "jupiter orbital distance")
    assert r["abstain"] and len(support.tickets("acme")) == 1
    assert support.tickets("beacon") == []
    with pytest.raises(ValueError):
        support.ask("unknown", "refund")


def test_model_unknown_citation_escalates(support, monkeypatch):
    monkeypatch.setattr("app.core.rank", lambda q, d, m: [(d[0], 1)])
    monkeypatch.setattr(
        "app.local_model.generate",
        lambda *a, **k: {"text": '{"answer":"secret","citations":["other-tenant"],"abstain":false}'},
    )
    assert support.ask("acme", "refund", "local")["abstain"]
