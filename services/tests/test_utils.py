import json
from pathlib import Path

from services.utils import save_data_to_json


class fakeTest():
    filename = "test_filename.json"
    @save_data_to_json
    def fetch(self):
        return {"key": "value"}


def test_decorator_SaveToJson(tmp_path):
    model = fakeTest()
    model.filename = str(tmp_path / "test_output.json")

    data = model.fetch()
    assert data == {"key": "value"}
    saved = json.loads(Path(model.filename).read_text())
    assert saved == {"key": "value"}

def test_jason_does_not_exist(tmp_path):
    model = fakeTest()
    result = model.fetch()
    assert result == {"key": "value"}
    saved = json.loads(Path(model.filename).read_text())
    assert saved == {"key": "value"}
