from subprocess import Popen, PIPE, STDOUT
import os

def test_window_new_event(sway):
    env = os.environ.copy()
    if sway.variant == 'sway':
        if 'DISPLAY' in env:
            del env['DISPLAY']
        env['WAYLAND_DISPLAY'] = sway.display
    elif sway.variant == 'i3':
        if 'WAYLAND_DISPLAY' in env:
            del env['WAYLAND_DISPLAY']
        env['DISPLAY'] = sway.display

    title = 'test-window-event'
    proc = Popen(['test/util/gtk-window.py', '--title', title],
            env=env, stdout=PIPE, stderr=STDOUT)

    def on_window_new(ipc, e):
        global event
        if e.container.name == title:
            event = e
            sway.ipc.main_quit()

    sway.ipc.on('window::new', on_window_new)
    sway.ipc.main()

    assert event
    assert event.change == 'new'
    assert event.container
    assert event.container.name == title
