def test_focus_direction(sway):
    windows = [sway.open_window() for i in range(0, 3)]
    root = sway.ipc.get_tree()
    containers = [root.find_by_id(w.id) for w in windows]

    assert sway.focused().id == containers[2].id

    containers[1].command('focus')
    assert sway.focused().id == containers[1].id

    sway.ipc.command('focus left')
    assert sway.focused().id == containers[0].id

    # test wrapping
    sway.ipc.command('focus left')
    assert sway.focused().id == containers[2].id

    sway.ipc.command('focus left')
    assert sway.focused().id == containers[1].id

    sway.ipc.command('focus right')
    assert sway.focused().id == containers[2].id
