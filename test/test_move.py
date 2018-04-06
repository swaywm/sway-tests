def test_move_left_from_center(sway):
    '''
    (container (view 1) (view 2 focus) (view 3))
    -> move left
    (container (view 2 focus) (view 1) (view 3))
    '''

    view1 = sway.open_window('view1')
    view2 = sway.open_window('view2')
    view3 = sway.open_window('view3')

    view2.focus()
    view2.command('move left')

    tree = sway.ipc.get_tree()
    ws = tree.workspaces()[0]

    assert ws.nodes[0].id == view2.id
    assert ws.nodes[1].id == view1.id
    assert ws.nodes[2].id == view3.id

def test_move_right_from_center(sway):
    '''
    (container (view 1) (view 2 focus) (view 3))
    -> move right
    (container (view 1) (view 3) (view 2 focus))
    '''

    view1 = sway.open_window('view1')
    view2 = sway.open_window('view2')
    view3 = sway.open_window('view3')

    view2.focus()
    view2.command('move right')

    tree = sway.ipc.get_tree()
    ws = tree.workspaces()[0]

    assert ws.nodes[0].id == view1.id
    assert ws.nodes[1].id == view3.id
    assert ws.nodes[2].id == view2.id

def test_move(sway):
    '''
    (container L_VERT (view 1))
    (container L_HORIZ
      (view 2) (view 3 focus))
    -> move up
    (container L_VERT
      (view 1) (view 3 focus))
    (container L_HORIZ (view 2))
    '''

    view1 = sway.open_window('view1')
    view2 = sway.open_window('view2')
    view1.command('splitv')
    view3 = sway.open_window('view3')
    view3.focus()

    sway.ipc.command('move up')

def test_move_into_split(sway):
    '''
    (view 1 focus)
    (container (view2) (view3 focus-inactive) (view4))
    (view 5)
    -> move right
    (container (view2) (view3) (view1 focus) (view4))
    (view 5)
    '''
    view1 = sway.open_window('view1')
    view2 = sway.open_window('view2')
    view5 = sway.open_window('view5')
    view2.focus()
    view2.command('splitv')
    view3 = sway.open_window('view3')
    view4 = sway.open_window('view4')

    view3.focus()
    view1.focus()
    sway.ipc.command('move right')

    tree = sway.ipc.get_tree()
    ws = tree.workspaces()[0]

    assert len(ws.nodes) == 2

    assert ws.nodes[1].id == view5.id
    split = ws.nodes[0].nodes
    assert len(split) == 4
    assert split[0].id == view2.id
    assert split[1].id == view3.id
    assert split[2].id == view1.id
    assert split[3].id == view4.id
    assert split[2].focused

def test_move_out_of_split(sway):
    '''
    (view1) (container (view2) (view3 focus))
    -> move right
    (view1) ((container) (view2)) ((view3 focus)
    '''
    view1 = sway.open_window('view1')
    view2 = sway.open_window('view2')
    view2.command('splitv')
    view3 = sway.open_window('view3')

    sway.ipc.command('move right')

    tree = sway.ipc.get_tree()
    ws = tree.workspaces()[0]

    assert len(ws.nodes) == 3
    assert ws.nodes[0].id == view1.id

    split = ws.nodes[1]
    assert len(split.nodes) == 1
    assert split.nodes[0].id == view2.id

    assert ws.nodes[2].id == view3.id
    assert ws.nodes[2].focused

def test_move_out_of_split_flattening(sway):
    '''
    # when moving out of a split that leaves no children left within the
    # container, the container should flatten.
    (view1) (container (view2 focus))
    -> move left
    (view1) (view2 focus)
    '''
    view1 = sway.open_window('view1')
    view2 = sway.open_window('view2')
    view2.command('splith')
    sway.ipc.command('move left')

    tree = sway.ipc.get_tree()
    ws = tree.workspaces()[0]

    assert len(ws.nodes) == 2

    assert ws.nodes[0].id == view1.id
    assert ws.nodes[1].id == view2.id

def test_move_changes_workspace_layout(sway):
    '''
    (workspace HORIZ (view1) (view2 focus))
    -> move down
    (workspace VERT (view2 focus) (view1))
    '''
    ws = sway.workspace()

    assert ws.layout == 'splith'
    assert ws.type == 'workspace'
    assert ws.name == '1'

    view1 = sway.open_window('view1')
    view2 = sway.open_window('view2')

    view2.focus()
    sway.cmd('move down')

    ws = sway.workspace()

    assert len(ws.nodes) == 2
    assert ws.layout == 'splitv'
    assert ws.type == 'workspace'
    assert ws.name == '1'
