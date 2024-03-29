import flet as ft

import sys
import os

# Add a directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "model\\"))  
import smtp


def MailComposeView(user_email: str):
    class MailCompose_View(ft.BottomSheet):

        async def on_close(self, e):
            self.open = False
            await self.update_async()

        def check_valid_info(self):
            print("Value: ", self.textfield_title.value)

            return self.textfield_to != ""

        async def send_mail_clicked(self, e):
            if self.check_valid_info():
                # check sent mail information
                print("OK data")
                print(f"self.to: {self.textfield_title.value}")
                print(f"self.to: {self.textfield_content.value}")
                print(f"self.to: {self.textfield_to.value}")
                print(f"self.to: {self.textfield_cc.value}")
                print(f"self.to: {self.textfield_bcc.value}")

                # send email
                client = smtp.SMTPCLIENT(
                    user_email,
                    self.textfield_to.value,
                    self.textfield_cc.value,
                    self.textfield_bcc.value,
                    self.textfield_title.value,
                    self.textfield_content.value,
                    self.files_path
                )
                client.send_mail()

                # clear mail information
                self.textfield_title.value = ""
                self.textfield_content.value = ""
                self.textfield_cc.value = ""
                self.textfield_bcc.value = ""
                self.textfield_to.value = ""

                await self.update_async()
                await self.on_close(e)

        async def on_click_event(self, e):
            print("On pick files")
            await self.pick_file_dialog.pick_files_async(allow_multiple=True)
            await self.update_async()

        async def on_open_dialog(self, e):
            self.page.dialog = self.file_size_overflow_dialog
            self.file_size_overflow_dialog.open = True
            await self.file_size_overflow_dialog.update_async()

        async def pick_files_result(self, e: ft.FilePickerResultEvent):
            print("On pick files result")

            if e.files is None:
                self.selected_files.value = "No attachment"
                await self.selected_files.update_async()
                await self.update_async()
                print("No file picked")
                return

            # check file size <= 3mb
            total_size = 0
            for file in e.files:
                total_size += file.size

            if total_size > 3 * 1024 * 1024:
                print("File size overflow")
                # display announcement dialog
                await self.on_open_dialog(e)
                return

            self.selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "No attachment"
            )
            print(f"Files: {e.files}")

            # clear previous files path
            self.files_path = ""

            # get files path
            for file in e.files:
                self.files_path += file.path + ", "

            # remove last comma
            self.files_path = self.files_path[:-2]

            print(f"Files path: {self.files_path}")

            await self.selected_files.update_async()
            await self.update_async()

        async def did_mount_async(self):
            self.page.overlay.append(self.pick_file_dialog)
            self.page.overlay.append(self.selected_files)
            self.page.overlay.append(self.file_size_overflow_dialog)
            await self.page.update_async()

        # happens when example is removed from the page (when user chooses different control group on the navigation rail)
        async def will_unmount_async(self):
            self.selected_files.value = ""
            await self.page.overlay.remove(self.file_size_overflow_dialog)
            await self.page.overlay.remove(self.pick_file_dialog)
            await self.page.overlay.remove(self.content)
            await self.page.update_async()

        def __init__(self):
            super().__init__()

            self.textfield_to = ft.TextField(
                hint_text="To",
                height=25,
                width=640,
                border_color='transparent',
                text_size=13,
            )
            self.textfield_cc = ft.TextField(
                hint_text="CC",
                height=25,
                width=640,
                border_color='transparent',
                text_size=13,
            )
            self.textfield_bcc = ft.TextField(
                hint_text="BCC",
                height=25,
                width=640,
                border_color='transparent',
                text_size=13,
            )
            self.textfield_title = ft.TextField(
                hint_text="Title",
                height=25,
                width=640,
                border_color='transparent',
                text_size=13,
            )
            self.textfield_content = ft.TextField(
                hint_text="Content",
                height=200,
                width=630,
                border_color='transparent',
                text_size=13,
                multiline=True,
                max_length=1000
            )

            async def close_dlg(e):
                self.file_size_overflow_dialog.open = False
                await self.file_size_overflow_dialog.update_async()

            self.file_size_overflow_dialog = ft.AlertDialog(
                title=ft.Container(
                    width=300,
                    content=ft.Text(
                        value='Announcement',
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                content=ft.Text('File size must be less than 3MB!'),
                modal=False,
                on_dismiss=lambda e: print("Dialog dismissed!"),
                actions=[
                    ft.TextButton("Close", on_click=close_dlg),
                ],
            )
            self.pick_file_dialog = ft.FilePicker(on_result=self.pick_files_result)
            self.selected_files = ft.Text(value="No attachment", max_lines=1, width=300,
                                          overflow=ft.TextOverflow.ELLIPSIS, text_align=ft.TextAlign.RIGHT)

            # array of files path
            self.files_path = ""

            header = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "New email",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Container(
                        content=ft.Icon(ft.icons.CLOSE, size=20),
                        on_click=self.on_close
                    )
                ]
            )

            to = ft.Container(
                padding=ft.padding.only(top=20, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_to
                    ]
                )
            )

            cc = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_cc
                    ]
                )
            )

            bcc = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_bcc
                    ]
                )
            )

            title = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_title
                    ]
                )
            )

            content = ft.Container(
                padding=ft.padding.only(top=0, bottom=0),
                content=ft.Row(
                    controls=[
                        self.textfield_content
                    ]
                )
            )

            send_and_attach = ft.Container(
                padding=ft.padding.only(top=0),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.FilledButton(
                            "Send",
                            icon=ft.icons.SEND_ROUNDED,
                            on_click=self.send_mail_clicked
                        ),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    self.selected_files,
                                    ft.ElevatedButton(
                                        "Pick files",
                                        icon=ft.icons.UPLOAD_FILE,
                                        on_click=self.on_click_event
                                    ),
                                ])
                        )
                    ]
                )
            )

            self.content = ft.Container(
                padding=ft.padding.only(left=20, right=20, top=10, bottom=5),
                height=450,
                width=1000,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=0,
                    controls=[
                        ft.Column(
                            spacing=0,
                            controls=[
                                header,
                                to,
                                ft.Divider(thickness=1, height=1),
                                cc,
                                ft.Divider(thickness=1, height=1),
                                bcc,
                                ft.Divider(thickness=1, height=1),
                                title,
                                ft.Divider(thickness=1, height=1),
                                content,
                            ]
                        ),
                        send_and_attach,
                    ]
                )
            )

    mail_compose_view = MailCompose_View()
    mail_compose_view.is_scroll_controlled = True

    return mail_compose_view
