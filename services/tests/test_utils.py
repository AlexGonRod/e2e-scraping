from .test_utils import test_data_to_json


def func():
    obj = {"filename": "testjson", "data": [{"test": "test"}]}
    return obj


class TestClass:
    async def testSaveToJson(self):
        await test_data_to_json(func)
