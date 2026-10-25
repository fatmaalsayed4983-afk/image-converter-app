import os
import flet as ft
from PIL import Image

def main(page: ft.Page):
    page.title = "محول امتداد الصور - Flet Image Converter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 450
    page.window_height = 650

    selected_path_holder = {"path": None}

    # عناصر واجهة المستخدم
    selected_path_label = ft.Text("لم يتم اختيار صورة بعد", size=12, italic=True)
    status_label = ft.Text("", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN)
    
    # معاينة الصورة
    img_preview = ft.Image(src="", width=220, height=150, fit=ft.ImageFit.CONTAIN, visible=False)

    # قائمة اختيار الامتداد
    format_dropdown = ft.Dropdown(
        label="اختر الامتداد المراد التحويل إليه",
        value="PNG",
        options=[
            ft.dropdown.Option("PNG"),
            ft.dropdown.Option("JPG"),
            ft.dropdown.Option("JPEG"),
            ft.dropdown.Option("WEBP"),
            ft.dropdown.Option("BMP"),
            ft.dropdown.Option("ICO"),
            ft.dropdown.Option("TIFF"),
            ft.dropdown.Option("GIF"),
        ],
        width=280
    )

    # دالة اختيار الملف
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_info = e.files[0]
            selected_path_holder["path"] = file_info.path
            selected_path_label.value = f"الصورة المختارة: {file_info.name}"
            
            # عرض المعاينة
            img_preview.src = file_info.path
            img_preview.visible = True
            status_label.value = ""
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # دالة التحويل
    def start_conversion(e):
        path = selected_path_holder["path"]
        if not path:
            status_label.value = "يرجى اختيار صورة أولاً!"
            status_label.color = ft.colors.RED
            page.update()
            return

        target_ext = format_dropdown.value.lower()
        save_format = target_ext.upper()
        if save_format == "JPG":
            save_format = "JPEG"

        try:
            original_dir = os.path.dirname(path)
            output_dir = os.path.join(original_dir, "output")
            os.makedirs(output_dir, exist_ok=True)

            file_stem = os.path.splitext(os.path.basename(path))[0]
            output_filename = f"{file_stem}.{target_ext}"
            output_path = os.path.join(output_dir, output_filename)

            img_to_save = Image.open(path)

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

            status_label.value = f"تم الحفظ بنجاح في مجلد output:\n{output_filename}"
            status_label.color = ft.colors.GREEN
            page.update()
        except Exception as ex:
            status_label.value = f"خطأ أثناء التحويل: {str(ex)}"
            status_label.color = ft.colors.RED
            page.update()

    # تصميم الواجهة وترتيب العناصر
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("محول امتداد الصور", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ElevatedButton(
                    "1. اختر الصورة / Choose Photo",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)
                ),
                selected_path_label,
                img_preview,
                ft.Divider(),
                format_dropdown,
                ft.VerticalDivider(height=10),
                ft.ElevatedButton(
                    "3. بدء التحويل / Start Convert",
                    icon=ft.icons.CONVERT_TO_REMOTE_SFTP,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREEN_700,
                    on_click=start_conversion
                ),
                status_label
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )
    )

ft.app(target=main)
