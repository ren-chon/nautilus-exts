import gi

gi.require_version('Adw', '1')
from gi.repository import Nautilus, GObject, Gtk, Adw, Gio, Gdk

gi_version_major = 3 if 30 <= gi.version_info[1] < 40 else 4
gi.require_versions({
    'Nautilus': '3.0' if gi_version_major == 3 else '4.0',
    'Gdk': '3.0' if gi_version_major == 3 else '4.0',
    'Gtk': '3.0' if gi_version_major == 3 else '4.0'
})

profiles = [
    {
        "name": "MPVPLAYDEFAULT",
        "label": "Play",
        "command": "mpv"
    },
    {
        "name": "MPVPLAYI965",
        "label": "Play with i965",
        "command": "mpv --hwdec=i965"
    },
    {
        "name": "MPVPLAYVAAPI",
        "label": "Play with VAAPI",
        "command": "mpv --hwdec=vaapi"
    },
    {
        "name": "MPVPLAY4K",
        "label": "Play with Safe Fast",
        "command": "mpv --hwdec=auto-safe --profile=fast"
    },
]


class MPVProfilesExt(GObject.GObject, Nautilus.MenuProvider):
    VALID_MIMETYPES = ('video/', 'image/', 'audio/')

    def __init__(self):
        GObject.GObject.__init__(self)

    def get_file_items(self, *args, **kwargs):
        files = args[0] if gi_version_major == 4 else args[1]
        if len(files) < 1:
            return []

        submenu = Nautilus.Menu()

        item = Nautilus.MenuItem(
            name='MPVProfilesExt::PlayMPVProfile',
            label='Open With MPV...',
        )
        item.set_submenu(submenu)

        for profile in profiles:
            item_two = Nautilus.MenuItem(
                name=f'MPVProfilesExt::{profile["name"]}',
                label=profile['label'],
                tip=profile['command'],
            )
            item_two.connect('activate',
                             lambda item, cmd=profile['command']: self.
                             on_profile_activated(cmd, files))
            submenu.append_item(item_two)

        return item,

    def on_profile_activated(self, command, file_paths):
        for file_path in file_paths:
            # `--force-window` to show a window for audio files,
            # otherwise it'll keep playing even after closing nautilus.

            # Or file_paths.get_location().get_uri() for URI (file://)
            full_command = command + " --force-window " + f"{file_path.get_location().get_uri()}"
            print(f"INFO: Executing command: {full_command}")

            import subprocess
            subprocess.Popen(full_command.split(), start_new_session=True)
