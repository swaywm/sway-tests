def test_workspace_back_and_forth(sway):
    """
    Workspace switching with back and forth.
    """

    assert sway.workspace().name == "1"

    # since we start on workspace 1, start with back_and_forth, which shouldn't
    # change the workspace
    sway.cmd('workspace back_and_forth')
    assert sway.workspace().name == "1"

    sway.cmd('workspace 2')
    assert sway.workspace().name == "2"

    sway.cmd('workspace back_and_forth')
    assert sway.workspace().name == "1"

    sway.cmd('workspace 1')
    assert sway.workspace().name == "1"


def test_workspace_auto_back_and_forth(sway):
    """
    Workspace switching and auto back and forth.
    """

    sway.cmd('workspace_auto_back_and_forth yes')
    assert sway.workspace().name == "1"

    # don't change the workspace
    sway.cmd('workspace 1')
    assert sway.workspace().name == "1"

    sway.cmd('workspace 2')
    assert sway.workspace().name == "2"

    sway.cmd('workspace 2')
    assert sway.workspace().name == "1"

    # back_and_forth should still work
    sway.cmd('workspace back_and_forth')
    assert sway.workspace().name == "2"
