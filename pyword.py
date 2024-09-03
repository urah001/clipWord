import tkinter as tk
import pyperclip
import threading


class ClipboardApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x200+100+100")  # Set initial position
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.wm_attributes("-topmost", True)  # Keep window on top
        self.root.configure(bg="lightgrey")

        # Title bar for dragging
        self.title_bar = tk.Frame(self.root, bg="darkgrey", relief=tk.FLAT, bd=0)
        self.title_bar.pack(fill=tk.X)

        # Title text
        self.title_label = tk.Label(self.title_bar, text="Clipboard History", bg="darkgrey", fg="white")
        self.title_label.pack(side=tk.LEFT, padx=5)

        # Close button
        self.close_button = tk.Button(self.title_bar, text="X", command=self.root.destroy, bg="red", fg="white", bd=0)
        self.close_button.pack(side=tk.RIGHT, padx=5)

        # Frame for clipboard content
        self.frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, bd=2)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Text area to display clipboard history
        self.text_area = tk.Text(self.frame, height=6, width=30, font=("Arial", 12), wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.config(state=tk.DISABLED)

        # Initialize clipboard history
        self.clipboard_history = []

        # Start clipboard monitoring
        self.update_clipboard()

        # Bind mouse events for dragging
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_motion)

    def update_clipboard(self):
        try:
            # Get the current clipboard content
            current_clipboard = pyperclip.paste()

            # Add to history if not already in it
            if current_clipboard and (not self.clipboard_history or current_clipboard != self.clipboard_history[-1]):
                self.clipboard_history.append(current_clipboard)

                # Update the text area
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, current_clipboard + "\n---\n")
                self.text_area.config(state=tk.DISABLED)
                self.text_area.yview(tk.END)  # Auto-scroll to the bottom
        except Exception as e:
            print(f"Error accessing clipboard: {e}")

        # Continue checking every second
        self.root.after(1000, self.update_clipboard)

    def start_move(self, event):
        """Initialize the start of a window move."""
        self.x = event.x
        self.y = event.y

    def on_motion(self, event):
        """Handle window movement."""
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")


def start_gui():
    root = tk.Tk()
    app = ClipboardApp(root)
    root.mainloop()


if __name__ == "__main__":
    threading.Thread(target=start_gui).start()
