import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ImageConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("محول امتداد الصور - GUI Image Converter")
        self.geometry("580x640")
        self.resizable(False, False)

        self.selected_image_path = None
        self.pil_image = None

        # Header
        self.title_label = ctk.CTkLabel(
            self,
            text="برنامج تحويل امتداد الصور\nImage Extension Converter",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(15, 10))

        # Step 1: Select Image
        self.step1_frame = ctk.CTkFrame(self)
        self.step1_frame.pack(fill="x", padx=20, pady=8)

        self.btn_select = ctk.CTkButton(
            self.step1_frame,
            text="1. اختر الصورة / Choose Photo",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.select_image
        )
        self.btn_select.pack(pady=10)

        self.lbl_file_path = ctk.CTkLabel(
            self.step1_frame,
            text="لم يتم اختيار صورة بعد",
            wraplength=480,
            font=ctk.CTkFont(size=12)
        )
        self.lbl_file_path.pack(pady=(0, 10))

        # Image Preview Box
        self.preview_frame = ctk.CTkFrame(self, width=320, height=200)
        self.preview_frame.pack(pady=10)
        self.preview_frame.pack_propagate(False)

        self.lbl_preview = ctk.CTkLabel(
            self.preview_frame,
            text="معاينة الصورة ستظهر هنا",
            font=ctk.CTkFont(size=12)
        )
        self.lbl_preview.pack(expand=True)

        # Step 2: Target Extension
        self.step2_frame = ctk.CTkFrame(self)
        self.step2_frame.pack(fill="x", padx=20, pady=8)

        self.lbl_ext_title = ctk.CTkLabel(
            self.step2_frame,
            text="2. اختر الامتداد المراد التحويل إليه / Select Target Format",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_ext_title.pack(pady=(8, 4))

        self.formats = ["PNG", "JPG", "JPEG", "WEBP", "BMP", "ICO", "TIFF", "GIF"]
        self.combo_ext = ctk.CTkOptionMenu(
            self.step2_frame,
            values=self.formats,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.combo_ext.set("PNG")
        self.combo_ext.pack(pady=(0, 10))

        # Step 3: Convert Button
        self.step3_frame = ctk.CTkFrame(self)
        self.step3_frame.pack(fill="x", padx=20, pady=8)

        self.btn_convert = ctk.CTkButton(
            self.step3_frame,
            text="3. بدء التحويل / Start Convert",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#27ae60",
            hover_color="#219150",
            command=self.start_conversion
        )
        self.btn_convert.pack(pady=12)

        # Status Message
        self.lbl_status = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#27ae60"
        )
        self.lbl_status.pack(pady=5)

    def select_image(self):
        file_types = [
            ("Image Files", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.gif *.ico"),
            ("All Files", "*.*")
        ]
        path = filedialog.askopenfilename(title="اختر الصورة / Choose Photo", filetypes=file_types)
        if path:
            self.selected_image_path = path
            self.lbl_file_path.configure(text=f"الصورة المختارة: {os.path.basename(path)}")
            self.lbl_status.configure(text="")
            self.load_preview(path)

    def load_preview(self, path):
        try:
            img = Image.open(path)
            self.pil_image = img.copy()

            max_size = (300, 180)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.lbl_preview.configure(image=ctk_img, text="")
            self.lbl_preview.image = ctk_img
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تحميل معاينة الصورة:\n{str(e)}")

    def start_conversion(self):
        if not self.selected_image_path or not self.pil_image:
            messagebox.showwarning("تنبيه", "يرجى اختيار صورة أولاً!")
            return

        target_ext = self.combo_ext.get().lower()
        save_format = target_ext.upper()
        if save_format == "JPG":
            save_format = "JPEG"

        try:
            original_dir = os.path.dirname(self.selected_image_path)
            output_dir = os.path.join(original_dir, "output")
            os.makedirs(output_dir, exist_ok=True)

            file_stem = os.path.splitext(os.path.basename(self.selected_image_path))[0]
            output_filename = f"{file_stem}.{target_ext}"
            output_path = os.path.join(output_dir, output_filename)

            img_to_save = Image.open(self.selected_image_path)

            if target_ext in ["jpg", "jpeg", "bmp"] and img_to_save.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img_to_save.size, (255, 255, 255))
                if img_to_save.mode == "P":
                    img_to_save = img_to_save.convert("RGBA")
                background.paste(img_to_save, mask=img_to_save.split()[3])
                img_to_save = background
            elif target_ext == "ico":
                img_to_save = img_to_save.convert("RGBA")
            elif img_to_save.mode != "RGB" and target_ext in ["jpg", "jpeg"]:
                img_to_save = img_to_save.convert("RGB")

            if save_format == "JPEG":
                img_to_save.save(output_path, format="JPEG", quality=95)
            elif save_format == "ICO":
                img_to_save.save(output_path, format="ICO", sizes=[(256, 256)])
            else:
                img_to_save.save(output_path, format=save_format)

            self.lbl_status.configure(text=f"تم التحويل والحفظ في مجلد output:\n{output_filename}")
            messagebox.showinfo("نجاح التحويل", f"تم حفظ الصورة بنجاح في:\n{output_path}")

        except Exception as e:
            messagebox.showerror("خطأ في التحويل", f"حدث خطأ أثناء حفظ الصورة:\n{str(e)}")

if __name__ == "__main__":
    app = ImageConverterApp()
    app.mainloop()
