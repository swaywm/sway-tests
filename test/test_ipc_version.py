def test_ipc_version(sway):
    version = sway.ipc.get_version()
    assert version.variant
    assert version.human_readable
    assert version.major >= 0
    assert version.minor >= 0
    assert version.patch >= 0
