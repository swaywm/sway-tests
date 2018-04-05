def test_split_close(sway):
    '''
    Test that a nested split container opens and closes correctly without
    crashing
    '''
    return
    sway.ipc.command('workspace 1')
    windows = [sway.open_window() for i in range(0, 2)]
    sway.ipc.command('splitv')
    sway.open_window()
    sway.ipc.command('splitv')
    sway.open_window()
    sway.ipc.command('focus parent')
    sway.ipc.command('focus parent')

    assert len(sway.focused().nodes) == 2
    assert len(sway.focused().nodes[1].nodes) == 2

    windows[1].close()

    ws = sway.focused().workspace()
    assert len(ws.nodes) == 2
    # TODO test that the layout updated correctly

def test_split_focus(sway):
    '''
    Test that focusing a split container in a direction focuses the focus
    inactive view of the split container.
    '''
    sway.ipc.command('workspace 2')
    win1 = sway.open_window()
    win2 = sway.open_window()
    win3 = sway.open_window()

    sway.ipc.command('focus left')
    sway.ipc.command('splitv')

    win4 = sway.open_window()

    # it should look like this
    '''---
    |  2  |
    |1 - 3|
    |  4  |
    ----'''

    tree = sway.ipc.get_tree()

    focused = tree.find_focused()

    assert focused.id == win4.id
    assert focused.parent.nodes[0].id == win2.id

    ws = focused.parent.parent
    assert ws.type == 'workspace'

    assert len(ws.nodes) == 3
    assert ws.nodes[0].id == win1.id
    assert ws.nodes[2].id == win3.id

    # focusing out of the split in a direction should work
    sway.ipc.command('focus right')

    assert sway.focused().id == win3.id

    # now test that focusing in a direction on the split container will focus
    # the focus-inactive child
    sway.ipc.command('focus left')

    assert sway.focused().id == win4.id

    sway.ipc.command('focus up')
    sway.ipc.command('focus right')
    sway.ipc.command('focus left')

    assert sway.focused().id == win2.id

    # test focus parent and focus child

    sway.ipc.command('focus parent')

    focused = sway.focused()

    assert focused.type == 'con'
    assert len(focused.nodes) == 2

    split_parent_id = focused.id

    sway.ipc.command('focus parent')

    focused = sway.focused()

    assert focused.type == 'workspace'
    assert len(focused.nodes) == 3

    sway.ipc.command('focus child')

    focused = sway.focused()

    assert focused.id == split_parent_id

    sway.ipc.command('focus child')

    focused = sway.focused()

    assert focused.id == win2.id
