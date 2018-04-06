def test_layout_change_split(sway):
    sway.open_window()
    sway.open_window()
    sway.cmd('splitv')
    sway.open_window()

    def assert_correct_layout(layout):
        split = sway.workspace().nodes[1]
        assert split.layout in ['splitv', 'splith']
        assert split.layout == layout

        view1 = split.nodes[0]
        view2 = split.nodes[1]

        if layout == 'splitv':
            assert view1.rect.x == view2.rect.x
            assert view1.rect.y < view2.rect.y

        elif layout == 'splith':
            assert view1.rect.y == view2.rect.y
            assert view1.rect.x < view2.rect.x

    assert_correct_layout('splitv')

    sway.cmd('layout splith')
    assert_correct_layout('splith')

    sway.cmd('layout toggle split')
    assert_correct_layout('splitv')

    sway.cmd('layout toggle split')
    assert_correct_layout('splith')

def test_change_workspace_child_layout(sway):
    ws = sway.ipc.get_tree().workspaces()[0]
    assert(ws.layout == 'splith')

    view1 = sway.open_window()
    view2 = sway.open_window()

    view1.command('layout splitv')

    ws = sway.ipc.get_tree().workspaces()[0]

    assert len(ws.nodes) == 1
    split = ws.nodes[0]

    assert split.layout == 'splitv'
    assert len(split.nodes) == 2

    # workspace layout should be unaffected
    assert(ws.layout == 'splith')

    view2.command('layout splith')

    ws = sway.ipc.get_tree().workspaces()[0]

    assert len(ws.nodes) == 1
    split = ws.nodes[0]

    assert split.layout == 'splith'
    assert len(split.nodes) == 2
