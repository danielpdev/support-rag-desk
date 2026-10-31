import os
import pytest
from app.core import Support
from app.db import Base


@pytest.mark.skipif(
    not os.getenv("POSTGRES_TEST_URL"), reason="Set POSTGRES_TEST_URL to a dedicated test database"
)
def test_postgresql_transactional_scenario():
    s = Support(os.environ["POSTGRES_TEST_URL"])
    try:
        a = s.ask("acme", "refund deadline")
        b = s.ask("beacon", "refund deadline")
        assert "30 days" in a["answer"] and "7 days" in b["answer"]
    finally:
        Base.metadata.drop_all(s.engine)
        s.engine.dispose()
