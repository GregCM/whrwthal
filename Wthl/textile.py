def miniPreamble(self):
    cross = '''\n\n
-   \\              /  +
+    \\     _      /   -
-         | |         +
+         | |         -
-    _____| |_____    +
+   |_____   _____|   -
-         | |         +
+         | |         -
-         | |         +
+         | |         -
-         | |         +
+         | |         -
-         |_|         +
+ _______/   \\_______ -
'''

    version = '''
______________________

THE KING JAMES BIBLE
______________________

Please rightly divide and handle with prayer.
\n\n'''

    return ''.join([cross, version])


def preamble():
    cross = '''\n\n
-   \\              /  +
+    \\     _      /   -
-         | |         +
+         | |         -
-    _____| |_____    +
+   |_____   _____|   -
-         | |         +
+         | |         -
-         | |         +
+         | |         -
-         | |         +
+         | |         -
-         |_|         +
+ _______/   \\_______ -
'''

    version = '''
______________________

THE KING JAMES BIBLE
______________________

Please rightly divide and handle with prayer.
\n\n'''

    AppFormat = ''' The format: \n\n When queried "Where To?", a good
response would be one of the following...

To find a verse-to-verse passage --
"Book Chapter:Verse-Verse"
    EX: "Romans 5:8-10"

To find only one verse --
"Book Chapter:Verse"
    EX: "John 3:16"
To find full chapters --
"Book Chapter"
    EX: "Psalm 119"
To find full books --
"Book"
    EX: "Philemon"\n
______________________________________________________________\n
'''

    return ''.join([cross, version, AppFormat])


def update(self, text, just='left'):
    cls(self.frame)
    t = self.frame.text_widget
    t.configure(state='normal')
    t.insert('end', text)
    # Justification
    t.tag_add('just', '1.0', 'end')
    t.tag_config('just', justify=just)
    t.configure(state='disabled')


def cls(self):
    self.text_widget.configure(state='normal')
    self.text_widget.delete('1.0', 'end')
    self.text_widget.configure(state='disabled')
