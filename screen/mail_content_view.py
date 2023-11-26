import flet as ft


def MailContentView(str_sender: str, str_to: str, str_title: str, str_date: str, str_content: str):
    class MailContentView(ft.BottomSheet):
        async def on_close(self, e):
            self.open = False
            await self.update_async()

        def __init__(self):
            super().__init__()

            header = ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        str_title,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        width=580,
                        max_lines=1
                    ),

                    ft.Container(
                        content=ft.Icon(ft.icons.CLOSE, size=20),
                        on_click=self.on_close
                    )
                ]
            )

            sender = ft.Container(
                padding=ft.padding.only(top=20, bottom=0),
                content=ft.Row(
                    controls=[
                        ft.Text("From: "),
                        ft.Text(str_sender, size=13)
                    ]
                )
            )

            to = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        ft.Text("To: "),
                        ft.Text(str_to, size=13)
                    ]
                )
            )

            date = ft.Container(
                padding=ft.padding.only(top=10, bottom=0),
                content=ft.Row(
                    controls=[
                        ft.Text("Date: "),
                        ft.Text(str_date, size=13)
                    ]
                )
            )

            content = ft.Container(
                padding=ft.padding.only(top=20, bottom=0),
                height=200,
                width=630,
                alignment=ft.alignment.top_left,
                content=ft.Row(
                    controls=[
                        ft.Text(str_content, size=13)
                    ]
                )
            )

            seen_and_attachment = ft.Container(
                padding=ft.padding.only(top=0),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([
                            ft.FilledButton(
                                "Mark as read",
                                icon=ft.icons.VISIBILITY_ROUNDED,
                            ),

                            ft.FilledButton(
                                "Download all attachments",
                                icon=ft.icons.DOWNLOAD_ROUNDED,
                            ),
                        ]),

                        ft.Row([
                            ft.Text("2 files attached"),

                            ft.Container(
                                content=ft.Icon(ft.icons.ATTACH_FILE)
                            )
                        ])
                    ]
                )
            )

            self.content = ft.Container(
                padding=ft.padding.only(left=20, right=20, top=10),
                height=500,
                width=1000,
                content=ft.Column(
                    spacing=0,
                    controls=[
                        header,
                        sender,
                        to,
                        date,
                        content,
                        seen_and_attachment,
                    ]
                )
            )

    mail_content_view = MailContentView()
    mail_content_view.open = True

    return mail_content_view
