def test_focus_inactive_containers(sway):
    '''
    (view 1)
    (container (view 2) (view 3))
    '''
    view1 = sway.open_window('view1')
    view2 = sway.open_window('view2')
    sway.cmd('splitv')
    view3 = sway.open_window()
    view3.focus()

    ws = sway.ipc.get_tree().workspaces()[0]

    split = ws.nodes[1]

    assert len(ws.focus) == 2
    assert ws.focus[0] == split.id
    assert ws.focus[1] == view1.id
    assert len(split.focus) == 2
    assert split.focus[0] == view3.id
    assert split.focus[1] == view2.id
