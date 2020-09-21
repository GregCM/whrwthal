from configparser import ConfigParser
import datetime as dt
import os
from tkinter import filedialog


def save(self, event=None):
    text = self.frame.text_widget.get('1.0', 'end')
    log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    wd = os.getcwd()
    try:
        os.chdir(self.fileLocation)
        self.config_obj.read('config.ini')
        self.save_directory = self.config_obj['PATH']['save']
        # Technical necessity in the case of accessing
        # settings from the menubar, before saving manually:
        if self.save_directory == '':
            raise KeyError

        with open('config.ini', 'w') as cfg:
            self.config_obj.write(cfg)

        os.chdir(self.save_directory)
        with open('%s.txt' % (log_time), 'w') as saved:
            # Save file found and amended
            saved.write(text)

    except (KeyError, FileNotFoundError):
        # Save file not found, saveas:
        self.saveas(self)

    finally:
        os.chdir(wd)


def saveas(self, event=None):
    text = self.frame.text_widget.get('1.0', 'end')
    dirName = filedialog.askdirectory(
               initialdir=self.homeDirectory, title="SaveAs")

    try:
        os.chdir(dirName)
    except OSError:
        return None
    log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open(log_time, 'w') as saved_as:
        saved_as.write(text)

    os.chdir(self.fileLocation)
    self.config_obj = ConfigParser()
    self.config_obj.read('config.ini')
    self.config_obj['PATH']['save'] = dirName
    with open('config.ini', 'w') as cfg:
        self.config_obj.write(cfg)


def browse(self, entry, cfg_key):
    new_path = filedialog.askdirectory()
    entry.delete(0, 'end')
    entry.insert('end', new_path)
    self.config_obj['PATH'][cfg_key] = new_path
    with open('config.ini', 'w') as cfg:
        self.config_obj.write(cfg)
