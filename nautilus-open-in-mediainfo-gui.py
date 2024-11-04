from gi.repository import Nautilus, GObject
import subprocess
import gi

gi_version_major = 3 if 30 <= gi.version_info[1] < 40 else 4
gi.require_versions({
    'Nautilus': '3.0' if gi_version_major == 3 else '4.0',
    'Gdk': '3.0' if gi_version_major == 3 else '4.0',
    'Gtk': '3.0' if gi_version_major == 3 else '4.0'
})


class MediaInfoExtension(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self):
        GObject.GObject.__init__(self)

    def get_file_items(self, *args, **kwargs):
        files = args[0] if gi_version_major == 4 else args[1]

        item_label = 'Open in MediaInfo'
        item_mediainfo = Nautilus.MenuItem(
            name='MediaInfoExtension::OpenWithMediaInfo',
            label=item_label,
            tip='View media information with MediaInfo')
        item_mediainfo.connect('activate', self.open_with_mediainfo, files)

        return item_mediainfo,

    def open_with_mediainfo(self, menu, files):
        if not self.check_mediainfo_installed():
            return

        file_paths = [file.get_location().get_path() for file in files]
        for file_path in file_paths:
            subprocess.Popen(['mediainfo-gui', file_path],
                             start_new_session=True)
            print(f"INFO: Opened {file_path.split('/')[-1]}")

    def check_mediainfo_installed(self):
        try:
            subprocess.check_output(['mediainfo', '--version'])
            return True
        except FileNotFoundError:
            return False
