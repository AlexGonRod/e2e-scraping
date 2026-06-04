import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from models.smtp_mail_model import SmtpMailModel

mock_item = {"id":1, "contractingOrganization": {
      "id": "testid",
      "name": "testname"
    }}

def test_smtp_format_items_return_data():
    result = SmtpMailModel._format_item(mock_item)
    
    assert result["id"] == 1
    assert result["contractingOrganization"]["name"] == "testname"

def test_smtp_mail_return_empty_dict_if_not_instance():
    with pytest.raises(TypeError, match="Item must be a dict"):
      SmtpMailModel._format_item([])

def test_smtp_mail_raises_valueError_if_None_item():
    with pytest.raises(TypeError, match="Item must be a dict"):
      SmtpMailModel._format_item(item=None)
      
def test_smtp_mail_raises_valueError_if_empty_item():
    with pytest.raises(ValueError, match="Item is not provided to be formatted"):
      SmtpMailModel._format_item(item={})


def test_smtp_mail_return_data_with_contractingOrg_as_string():
    result = SmtpMailModel._format_item({"id":1, "contractingOrganization": "testname"})

    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["contractingOrganization"]