# -*- coding: utf-8 -*-

"""
A LoginFrame Responsible for retrieving the
data necessary to request a new OAuth2 token.
"""

from Tkinter import *
from tkFont import *
import tkMessageBox
from pprint import *


class LoginFrame(Frame):

    def __init__(self, master=None, form_caption=None, form_blurb=None, error_text=None, autosize=False, width=0, height=0):
        """
        Initialize a new LoginFrame
        :param master:
        :param form_blurb:
        :param error_text:
        :param x:
        :param y:
        :param kw:
        """
        if master is None:
            self.master = Tk()
        else:
            self.master = master
        self.master.wm_title("Authorization Required - Please Login to Proceed")

        #####
        # Parent Init and Grid config
        #####
        Frame.__init__(self, master=self.master, border=2, relief=GROOVE)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        #####
        # Configure own grid
        self.grid(column=0, row=0, sticky=W+E+N+S)
        # Expand to fill on resize
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.center(self.master)

        ########
        # Calculate Frame Dimensions
        ########
        if autosize:
            width = Tk().winfo_screenwidth() * .75
            height = Tk().winfo_screenheight() * .75
        elif width and height:
            width = abs(width)
            height = abs(height)
        self.master.geometry('{}x{}'.format(int(width), (int(height))))

        #######
        #Fonts
        #######
        self.font_caption = Font(size=22, weight=BOLD)
        self.font_blurb = Font(size=12)
        self.font_field_labels = Font(size=14, weight=NORMAL, underline=1)
        self.font_entry_fields = Font(size=20, weight=NORMAL)
        self.font_button_submit = Font(size=14)

        # Incomplete login form feedback
        self.incomplete_error_title = "Incomplete Form"
        self.incomplete_error_msg = "Username and password are both required, please try again."

        # Top Caption text
        if form_caption is None:
            form_caption = "Authorization Required!"
        self.form_caption = form_caption

        # Blurb Label text (one or two sentences)
        if form_blurb is None:
            form_blurb = "System access is restricted to authorized users.\nPlease enter your " \
                         "username and password below to authenticate with the server."
        self.form_blurb = form_blurb

        # Error text to display from the last form submission
        self.form_error_msg = error_text

        ###########################################################
        #########    Widgets Initialization and Layout    #########
        ###########################################################
        # Outer container Frame
        self.frame_outer = Frame(self, border=3, relief=GROOVE)
        # self.frame_outer.config(bg="blue")
        self.frame_outer.grid(row=0, column=0, padx=4, pady=4, sticky=W+E+N+S)

        # FrameOuter column conf
        self.frame_outer.grid_columnconfigure(0, weight=1)
        # self.frame_outer.grid_columnconfigure(1, weight=1)
        # self.frame_outer.grid_columnconfigure(2, weight=1)

        # FrameOuter row conf
        self.frame_outer.grid_rowconfigure(0, weight=2)
        self.frame_outer.grid_rowconfigure(1, weight=1)
        self.frame_outer.grid_rowconfigure(2, weight=3)

        #######
        # Field container Frame
        #######
        self.frame_field_container = Frame(self.frame_outer, border=1, relief=GROOVE)
        self.frame_field_container.grid(row=2, column=0, padx=10, pady=(4,4), sticky=E+W)

        # Outer ->
        # FieldContainer Frame row config
        self.frame_field_container.grid_rowconfigure(0, weight=1)
        self.frame_field_container.grid_rowconfigure(1, weight=1)

        self.frame_field_container.grid_rowconfigure(2, weight=1)

        # FieldContainer Frame column config
        self.frame_field_container.grid_columnconfigure(0, weight=1)
        self.frame_field_container.grid_columnconfigure(1, weight=3)
        self.frame_field_container.grid_columnconfigure(2, weight=2)


        #####
        # Header Label
        self.lbl_caption = Label(self.frame_outer, font=self.font_caption, text=self.form_caption, anchor=W)
        self.lbl_caption.grid(row=0, column=0, sticky=W+E, padx=4, pady=(16,4))

        #####
        # Form blurb Label
        self.lbl_blurb = Label(self.frame_outer, font=self.font_blurb, text=self.form_blurb, justify=LEFT, anchor=W)
        self.lbl_blurb.grid(row=1, column=0, sticky=W+E, padx=5, pady=(4, 6))

        ####
        # Error Message Display Label
        # if self.form_error_msg is not None:
        self.lbl_form_error_msg = Label(self.frame_outer, fg="red", text="")
        self.lbl_form_error_msg.grid(row=2, column=0, columnspan=1, padx=8, pady=5, sticky=S+E+W)

        label_padx = (6,4)
        label_pady = (2,2)
        button_padx = (4,10)
        button_pady = (6,6)

        #####
        # Username Label
        self.lbl_username = Label(self.frame_field_container, font=self.font_field_labels, text="Username", anchor=W)
        self.lbl_username.grid(row=0, column=0, padx=label_padx, sticky=W+E+N+S)
        # Username Entry field
        self.entry_username = Entry(self.frame_field_container, width=12, font=self.font_entry_fields)
        self.entry_username.grid(row=0, column=1, padx=(4,4), pady=label_pady, sticky=W+E+N+S)

        #####
        # Password label
        self.lbl_password = Label(self.frame_field_container, font=self.font_field_labels, text="Password", anchor=W)
        self.lbl_password.grid(row=1, column=0, padx=label_padx, pady=label_pady, sticky=W+E+N+S)
        # Password Entry field
        self.entry_password = Entry(self.frame_field_container, width=12, font=self.font_entry_fields, show="*")
        self.entry_password.grid(row=1, column=1, padx=(4, 4), pady=label_pady, sticky=W+E+N+S)

        #####
        # Submit Button
        self.btn_submit = Button(
            self.frame_field_container,
            font=self.font_button_submit,
            text="Submit",
            command=lambda : self.submit(self, self.entry_username.get(), self.entry_password.get())
        )
        self.btn_submit.grid(row=0, column=2, rowspan=2, padx=button_padx, pady=button_pady, sticky=W+E+N+S)

        # Bind submit logic to the Enter key
        self.master.bind("<Return>", lambda e: self.submit(e, self.entry_username.get(), self.entry_password.get()))
        self.master.focus_set()

        # Intercept attempts to close the window
        self.master.protocol(
            'WM_DELETE_WINDOW',
            lambda: self.submit(self, self.entry_username.get(), self.entry_password.get())
        )

    def submit(self, event, username, password):
        """
        Credentials submit callback
        :param username:
        :param password:
        """
        if len(username) > 0 and len(password) > 0:
            self.output = username, password
            self.close_window()
        else:
            self.lbl_form_error_msg.config({"text": self.incomplete_error_msg})
            tkMessageBox.showerror(self.incomplete_error_title, self.incomplete_error_msg)

    def get_user_info(self):
        """
        The main entry point that Oauth2 will call
        when a grant refresh is required
        :return:
        """
        self.mainloop()
        return self.output

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
        Destroy the Frame
        """
        self.destroy()
        self.master.quit()
        self.master.destroy()


def main():  # run mainnloop
    root = Tk()
    app = LoginFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
