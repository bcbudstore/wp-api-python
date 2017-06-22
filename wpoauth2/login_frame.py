# -*- coding: utf-8 -*-

"""
LoginFrame Class supporting token retrieval from client credentials.
"""

import Tkinter as tk
import tkMessageBox


class LoginFrame(tk.Frame):

    output = ''

    def __init__(self, master=None, form_caption=False, form_error_msg=False, x=False, y=False, **kw):
        """
        Initialize a new LoginFrame
        :param master:
        :param form_caption:
        :param form_error_msg:
        :param x:
        :param y:
        :param kw:
        """

        if master is None:
            master = tk.Tk()
        self.root = master
        self.root.wm_title("Sign-in Required")
        # self.root.withdraw()

        if not form_caption:
            form_caption = "Please sign in below"
        self.form_caption = form_caption
        # incomplete form dialog
        self.incomplete_error_title = "Username and Password required"
        self.incomplete_error_msg = "You must provide both a username and a password, please try again."
        self.form_error_msg = form_error_msg

        tk.Frame.__init__(self, master, **kw)

        self.create_widgets()
        self.root.bind("<Return>",
                       lambda username=self.entry_username.get(), password=self.entry_password.get(): self.submit(
                           username, password))
        self.root.focus_set()
        # self.center(tk.Toplevel(self))
        self.grid()

    def submit(self, username, password):
        """
        Credentials submit callback
        :param username:
        :param password:
        """
        if not (username and password):
            tkMessageBox.showerror(self.incomplete_error_title, self.incomplete_error_msg)
        else:
            self.output = username, password
            self.master.quit()

    def create_widgets(self):
        """
        Initialize form controls
        """
        self.lbl_caption = tk.Label(
            self,
            text=self.form_caption
        )
        self.lbl_caption.grid(row=1, column=1, columnspan=3, sticky="W", padx=5, pady=5)

        if self.form_error_msg:
            self.lbl_form_error_msg = tk.Label(
                self,
                text=self.form_error_msg,
                fg="red"
            )
            self.lbl_form_error_msg.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

        self.lbl_username = tk.Label(
            self,
            text="Username"
        )
        self.lbl_username.grid(row=2, column=1, sticky="E")

        self.entry_username = tk.Entry(
            self,
            width=20
        )
        self.entry_username.grid(row=2, column=2, padx=1, pady=5)

        self.lbl_password = tk.Label(
            self,
            text="Password"
        )
        self.lbl_password.grid(row=3, column=1, sticky="E")

        self.entry_password = tk.Entry(
            self,
            show="*",
            width=20,
        )
        self.entry_password.grid(row=3, column=2, padx=1, pady=5)

        self.btn_login = tk.Button(
            self,
            text="Sign-in",
            command=lambda: self.submit(self.entry_username.get(), self.entry_password.get())
        )
        self.btn_login.grid(row=2, rowspan=2, column=3, padx=5)

    def get_user_info(self):
        """
        The main entry point that Oauth2 will call
        when a grant refresh is required
        :return:
        """
        self.mainloop()
        return self.output

    # def key_press(self, event):
    #     # frame.focus_set()
    #     print event.keys()

    def center(self, toplevel):
        """
        Centers the frame in the toplevel element window
        :param toplevel:
        """
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def close_window(self):
        """
        Destroy this login frame
        """
        self.master.destroy()
