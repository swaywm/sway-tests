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

        # these should be unchanged
        assert view1.layout == 'splith'
        assert view2.layout == 'splith'

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
