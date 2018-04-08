def test_focus_inactive_containers(sway):
    '''
    (workspace
        (view1)
        (container (view2) (view3))
    )
    (workspace
        (view4)
    )
    '''
    sway.cmd('workspace 1')
    view1 = sway.open_window('view1')
    view2 = sway.open_window('view2')
    sway.cmd('splitv')

    # first check if the split container is added to the top of the focus stack
    # right after the split command happens
    ws = sway.ipc.get_tree().workspaces()[0]
    assert len(ws.nodes) == len(ws.focus)
    split = ws.nodes[1]
    assert len(split.nodes) == 1
    assert split.nodes[0].id == view2.id
    assert len(split.nodes) == len(split.focus)
    assert split.focus[0] == view2.id

    view3 = sway.open_window()

    # start with view3 focused
    view3.focus()

    ws = sway.ipc.get_tree().workspaces()[0]
    split = ws.nodes[1]

    assert len(ws.nodes) == len(ws.focus)
    assert ws.focus[0] == split.id
    assert ws.focus[1] == view1.id
    assert len(split.focus) == len(split.nodes)
    assert split.focus[0] == view3.id
    assert split.focus[1] == view2.id

    # now focus view1 and the workspace focus stack should upate but the split
    # focus stack shouldn't change.
    view1.focus()

    ws = sway.ipc.get_tree().workspaces()[0]
    split = ws.nodes[1]

    assert len(ws.nodes) == len(ws.focus)
    assert ws.focus[0] == view1.id
    assert ws.focus[1] == split.id
    assert len(split.focus) == len(split.nodes)
    assert split.focus[0] == view3.id
    assert split.focus[1] == view2.id

    # check to make sure it works with a container focused instead of a view
    split.command('focus')

    ws = sway.ipc.get_tree().workspaces()[0]
    split = ws.nodes[1]

    assert split.focused
    assert len(ws.nodes) == len(ws.focus)
    assert ws.focus[0] == split.id
    assert ws.focus[1] == view1.id
    assert len(split.focus) == len(split.nodes)
    assert split.focus[0] == view3.id
    assert split.focus[1] == view2.id

    # test to make sure focus stack works at the output level
    sway.cmd('workspace 2')
    view4 = sway.open_window()

    tree = sway.ipc.get_tree()
    ws1 = tree.workspaces()[0]
    ws2 = tree.workspaces()[1]
    assert(ws1.parent == ws2.parent)
    output_content = ws1.parent

    assert len(output_content.nodes) == len(output_content.focus)
    assert output_content.focus[0] == ws2.id
    assert output_content.focus[1] == ws1.id

    sway.cmd('workspace 1')
    tree = sway.ipc.get_tree()
    ws1 = tree.workspaces()[0]
    ws2 = tree.workspaces()[1]
    assert(ws1.parent == ws2.parent)
    output_content = ws1.parent

    assert len(output_content.nodes) == len(output_content.focus)
    assert output_content.focus[0] == ws1.id
    assert output_content.focus[1] == ws2.id
