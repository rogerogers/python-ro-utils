from ro_utils.debug import pprint


def test_pprint(capsys):
    data = {"name": "test", "items": [1, 2, 3]}
    pprint(data)
    captured = capsys.readouterr()
    assert "'name': 'test'" in captured.out
    assert "[1, 2, 3]" in captured.out
