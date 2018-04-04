from util.sway import Sway
import time

def test_split(sway: Sway):
    '''
    test that a nested split container opens and closes correctly without
    crashing
    '''

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
