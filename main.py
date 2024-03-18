from lib import *

def main():
    root = tk.Tk()
    root.resizable(False, False)
    app = Paint(root)
    root.mainloop()

if __name__ == "__main__":
    main()
