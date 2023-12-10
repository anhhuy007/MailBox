import flet as ft


import sys
# Add a directory to sys.path
sys.path.append('D:\\MMTseminar2\\MailBox\\screen\\model\\')
import smtp


def MailComposeView():
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
                    "codingAkerman@fit.hcmus.edu.vn",
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

        async def pick_files_result(self, e: ft.FilePickerResultEvent):
            print("On pick files result")
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

        async def did_mount_async(self):
            self.page.overlay.append(self.pick_file_dialog)
            self.page.overlay.append(self.selected_files)
            await self.page.update_async()

        # happens when example is removed from the page (when user chooses different control group on the navigation rail)
        async def will_unmount_async(self):
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
