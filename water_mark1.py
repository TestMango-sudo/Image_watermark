from tkinter import *
from tkinter import filedialog as fd
from tkinter.colorchooser import askcolor
import tkinter.messagebox
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageTk
import matplotlib
from matplotlib import font_manager
import os


# --------- Variables for Watermark and Image -----------------
img_main = ""
file_main = ""
opacity_main = (255,)
font_size_main = 60
height_main = 0
width_main = 0
rotation_main = 0
color_main = (255, 255, 255)
font_main = "arial"
original_height = 0
original_width = 0


# ---------- Creating Main Functions ------------------------

def select_file():
    global file_main
    try:
        filename = fd.askopenfilename(filetypes=[("jpeg", ".jpg .jpeg"),
                                                 ("png", ".png"),
                                                 ("bitmap", "bmp"),
                                                 ("gif", ".gif")])
        show_image(filename)
        file_main = filename
    except AttributeError:
        pass


def show_image(filename):
    global height_main, width_main, original_height, original_width
    img = (Image.open(filename))
    width, height = img.size[0], img.size[1]
    r_img = resize(img)
    panel.configure(image=r_img)
    panel.image = r_img
    image_size.config(text=f"Image size {height}/{width} (height/width)", bg="#000000", fg="#fafafa",
                      font=("Arial", 8))
    height_main = height / 2
    width_main = width / 2
    original_height = height
    original_width = width
    change_x_y()

def resize(img):
    size = img.size
    f_size = (700, 600)
    factor = min(float(f_size[1]) / size[1], float(f_size[0]) / size[0])
    width = int(size[0] * factor)
    height = int(size[1] * factor)
    r_img = img.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(r_img)


def watermark():
    global img_main, file_main, font_size_main
    try:
        with Image.open(file_main).convert("RGBA") as base:
            # make a blank image for the text, initialized to transparent text color
            txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
            # get a font
            fnt = ImageFont.truetype(font_main, font_size_main)
            # get a drawing context
            d = ImageDraw.Draw(txt)
            # draw text
            fill = color_main + (opacity_main,)
            d.text((width_main, height_main), f"{wmark_entry.get()}", font=fnt, fill=fill)
            rotated_txt = txt.rotate(rotation_main)
            out = Image.alpha_composite(base, rotated_txt)

            marked_img = out.convert("RGBA")
            w_img = resize(marked_img)
            panel.configure(image=w_img)
            panel.image = w_img
            
            img_main = marked_img
    except FileNotFoundError:
        tkinter.messagebox.showerror("Error", "No such file.")
    except PIL.UnidentifiedImageError:
        tkinter.messagebox.showerror("Error", "Wrong file extension.")
    except AttributeError:
        pass


def save(marked_img):
    path = fd.asksaveasfilename(confirmoverwrite=True, defaultextension="png",
                                filetypes=[("jpeg", ".jpg"),
                                           ("png", ".png"),
                                           ("bitmap", "bmp"),
                                           ("gif", ".gif")])
    if path is not None:
        if os.path.splitext(path)[1] == ".jpg":
            image = marked_img.convert("RGB")
            image.save(path)
            tkinter.messagebox.showinfo("Success", "Image got watermarked and saved.")

#  ----------------- Watermark Appearance Functions --------------


def color():
    global color_main
    colors = askcolor(title="Tkinter Color Chooser")
    new_color = colors[0]
    color_button.configure(bg=colors[1])
    color_main = new_color
    watermark()


def opacity(value):
    global opacity_main
    opacity_main = int(value)
    watermark()


def font_size(value):
    global font_size_main
    font_size_main = int(value)
    watermark()


def font_change(new_font):
    global font_main
    font_main = new_font
    watermark()


def x_pos(value):
    global width_main
    width_main = int(value)
    watermark()


def y_pos(value):
    global height_main
    height_main = int(value)
    watermark()


def rotate(value):
    global rotation_main
    rotation_main = int(value)
    watermark()


def change_x_y():
    position_label_x = Label(text="X Position:", bg="#451952", fg="white", font="Arial")
    position_label_y = Label(text="Y Position:", bg="#451952", fg="white", font="Arial")
    position_label_x.grid(row=10, column=5, sticky="w", padx=(10, 0), pady=(20, 20))
    position_label_y.grid(row=10, column=6, sticky="w", padx=(10, 0), pady=(20, 20))

    x_select = Scale(window, from_=0, to=original_width, fg="white", bg="#451952", length=120, highlightthickness=0,
                     orient=HORIZONTAL, command=x_pos)
    x_select.set(f"{original_width / 2}")
    y_select = Scale(window, from_=0, to=original_height, fg="white", bg="#451952", length=120, highlightthickness=0,
                     orient=HORIZONTAL, command=y_pos)
    y_select.set(f"{original_height / 2}")
    x_select.grid(row=11, column=5, sticky="w", padx=(10, 0), pady=(0, 30))
    y_select.grid(row=11, column=6, sticky="w", padx=(10, 0), pady=(0, 30))
# ----------- Creating a GUI -------------------
window = Tk()
window.title("Watermark Magic Version 1.0")
window.minsize(height=100, width=500)
window.config(padx=0, pady=10, bg="#451952")
window.iconbitmap("images/logo.ico")

# ----------- Grid logo and image layout--------
logo = Image.open("images/logo1.png")
logo_img = ImageTk.PhotoImage(logo)
logo_img1 = Label(window, image=logo_img, borderwidth=0)
logo_img1.image = logo_img
logo_img1.grid(row=0, column=0, rowspan=2, padx=(25, 5))
blank_photo = Image.new(mode="RGBA", size=(700, 600), color="white")
image1 = ImageTk.PhotoImage(blank_photo)
panel = Label(window, image=image1)
panel.image = image1  # keep a reference
panel.grid(column=0, row=2, rowspan=10, columnspan=4, padx=(25, 0), pady=20, sticky="ews")


# ----------- Image Size Label -----------------
image_size = Label(text=f"Image size {height_main}/{width_main} (height/width)", bg="#451952", fg="white",
                   font=("Arial", 8))
image_size.grid(column=1, row=12, sticky="w", padx=(0, 20), pady=(20, 0))
show_image("images/blank_image.png")

# ----------- Watermark Text -------------------
wmark = Label(text="Watermark Text:", width=12, bg="#451952", fg="white", font="Arial")
wmark.grid(column=5, row=0, sticky="w", padx=(10, 0), pady=(25,5))
wmark_entry = Entry(width=42, bg="white", fg="black")
wmark_entry.grid(column=5, row=1, columnspan=3, padx=(10, 0), pady=(0, 30), sticky="w")
wmark_entry.get()

# ------------ Watermark Color ---------------------
color_label = Label(text="   Color:", bg="#451952", fg="white", font="Arial")
color_label.grid(column=6, row=12, sticky="w", padx=0, pady=5)
color_button = Button(text="      ", bg="#fafafa", fg="#fafafa", command=color, width=16)
color_button.grid(column=5, row=12, sticky="w", padx=(10, 10), pady=5)

# ------------ Watermark Opacity ------------------
opacity_label = Label(text="Opacity:", bg="#451952", font="Arial", fg="white")
opacity_label.grid(column=5, row=4, sticky="nws", padx=(10, 0), pady=0)
opacity = Scale(window, from_=0, to=255, orient=HORIZONTAL, bg="#451952", fg="white", length=260, highlightthickness=0,
                command=opacity)
opacity.set(255)
opacity.grid(column=5, columnspan=3, row=5, ipadx=20, sticky="w", padx=(10, 15), pady=(0, 20))

# ------------- Watermark Font Size ----------------
font_label = Label(text="Font size:", bg="#451952", fg="white", font="Arial")
font_label.grid(column=5, row=8, sticky="w", padx=(10, 0), pady=0)
default_font_size = StringVar(window)
default_font_size.set("60")
font_sizer = Scale(window, from_=0, to=360, fg="white", bg="#451952", length=260, highlightthickness=0,
                   orient=HORIZONTAL, command=font_size)
font_sizer.grid(row=9, column=5, columnspan=2, sticky="ew", padx=(10, 0), pady=(0, 20))
font_sizer.set("12")

# -------------- Watermark Font Type ---------------
font_list = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
final_font_list = []
formatted_font_list = [x.split("\\")[-1] for x in font_list]
for font in formatted_font_list:
    if ".otf" not in font:
        final_font_list.append(font.replace(".ttf", "").replace(".TTF", "").replace(".ttc", ""))
font = StringVar(window)
font.set("arial")
font_type_label = Label(text="Font:", bg="#451952", font="Arial", fg="white")
font_type_label.grid(row=2, column=5, sticky="nws", pady=(0, 0), padx=(10, 0))
font_type = OptionMenu(window, font, *final_font_list, command=font_change)
font_type.grid(row=3, column=5, columnspan=2, sticky="ew", padx=(10, 0), pady=(0, 30))

# Buttons
load_button = Button(text="Load Image", highlightthickness=0, font=("Arial", 12, "bold"),
                     fg="white", bg="#8E7AB5", height=2, width=15, command=select_file)
load_button.grid(row=0, column=1, sticky="w", padx=(10, 5))

apply_changes = Button(text="Apply Changes", fg="white", bg="#8E7AB5", font=("Arial", 12, "bold"),
                       height=2, width=25, command=watermark)
apply_changes.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(10, 43))

save_img = Button(text="Save Current Image", fg="white", bg="#8E7AB5", height=2, width=15,
                  font=("Arial", 12, "bold"), command=lambda: save(img_main))
save_img.grid(row=0, column=2, sticky="w", padx=(0, 40))

# erase_button = Button(text="Erase last Change", highlightthickness=0, font=("Arial", 12, "bold"),
#                       fg="white", bg="#8E7AB5", height=2, width=15)
# erase_button.grid(row=1, column=3, sticky="w", padx=(0, 40))

# -------------- Watermark Location Settings -----------------
change_x_y()


# Watermark Angle
angle_label = Label(text="Watermark Rotation", bg="#451952", fg="white", font="Arial")
angle_label.grid(row=6, column=5, sticky="w", padx=(10, 0), pady=0)
rotate_select = Scale(window, from_=0, to=360, fg="white", bg="#451952", length=260, highlightthickness=0,
                      orient=HORIZONTAL, command=rotate)
rotate_select.grid(row=7, column=5, columnspan=2, padx=(10, 0), sticky="ew", pady=(0, 20))

# -------------- Application Loop -----------------
window.mainloop()
