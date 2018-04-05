def test_move_left_from_center(sway):
    '''
    (container (view 1) (view 2 focus) (view 3))
    -> move left
    (container (view 2 focus) (view 1) (view 3))
    '''

    view1 = sway.open_window()
    view2 = sway.open_window()
    view3 = sway.open_window()

    view2.focus()
    view2.command('move left')

    tree = sway.ipc.get_tree()
    ws = tree.workspaces()[0]

    assert ws.nodes[0].id == view2.id
    assert ws.nodes[1].id == view1.id
    assert ws.nodes[2].id == view3.id

def test_move_right_from_center(sway):
    '''
    (container (view a) (view b focus) (view c))
    -> move right
    (container (view a) (view c) (view b focus))
    '''

    view1 = sway.open_window()
    view2 = sway.open_window()
    view3 = sway.open_window()

    view2.focus()
    view2.command('move right')

    tree = sway.ipc.get_tree()
    ws = tree.workspaces()[0]

    assert ws.nodes[0].id == view1.id
    assert ws.nodes[1].id == view3.id
    assert ws.nodes[2].id == view2.id
