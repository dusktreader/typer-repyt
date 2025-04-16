from pytest import CaptureFixture

from typer_attach.main import main


def test_raise(capsys: CaptureFixture[str]):
    main()
    assert "Ritchie Blackmore" in capsys.readouterr().out
