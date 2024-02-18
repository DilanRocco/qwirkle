from tkinter import Tk, Label, Button, simpledialog, LEFT, Frame, TOP, NW

from PIL import ImageTk

from Q.Referee.observer_ui_callbacks import ObserverUICallback
from Q.Referee.scrollable_frame import ScrollFrame


class ObserverUI:

    def __init__(self, callback: ObserverUICallback):
        self.current_state = 0
        self.callback = callback

        self.root = Tk()
        self.o = ScrollFrame(self.root)
        self.button_frame = Frame(self.o.frame)
        self.next_button = Button(self.button_frame, text="Next", command=self.switch_next)
        self.next_button.pack(side=LEFT, anchor=NW)
        self.previous_button = Button(self.button_frame, text="Previous", command=self.switch_prev)
        self.previous_button.pack(side=LEFT, anchor=NW)
        self.save_button = Button(self.button_frame, text="Save", command=self.save)
        self.save_button.pack(side=LEFT, anchor=NW)
        self.button_frame.pack(anchor=NW)
        self.board_image = Label(self.o.frame)
        self.board_image.pack(side=TOP)

    def save(self):
        path = simpledialog.askstring(title="File Path Prompt",
                                      prompt="Enter the file path of this saved state")
        self.callback.save_j_state(self.current_state, path)

    def receive_new_image(self, filename: str):
        img = ImageTk.PhotoImage(file=filename)
        img.photo = img
        self.board_image.configure(image=img)
        self.o.update()

    def switch_prev(self):
        potential_new_state = self.current_state - 1
        prev_button_state = self.callback.hasState(potential_new_state)
        if prev_button_state:
            self.current_state -= 1
            self.callback.switch(self.current_state)
            self.next_button.configure(state="normal")
        else:
            self.previous_button.configure(state="disabled")

    def switch_next(self):
        potential_new_state = self.current_state + 1
        next_button_state = self.callback.hasState(potential_new_state)
        if next_button_state:
            self.current_state += 1
            self.callback.switch(self.current_state)
            self.previous_button.configure(state="normal")
        else:
            self.next_button.configure(state="disabled")

    def run(self):
        if self.callback.hasState(self.current_state):
            self.callback.switch(self.current_state)
            self.o.update()
            self.root.mainloop()
