import flet as ft
import os


def FilterPage():
    def getDirectoryList(current_directory: str):
        subdirectories = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]
        return subdirectories

    class FilterPage(ft.UserControl):
        def __init__(self):
            super().__init__()
            self.filter_option = ft.Dropdown()
            self.filter_option.options = getDirectoryList("D:\MailBox\Filter")

        def build(self):
            return ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Text(
                        "Filter",
                        size=25,
                        weight=ft.FontWeight.BOLD
                    ),
                    self.filter_option,
                    ft.OutlinedButton(
                        "Apply",
                        width=100,
                        height=40,
                    )
                ]
            )

    return FilterPage()
