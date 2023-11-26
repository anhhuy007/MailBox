import flet as ft
import mail_content_view as MailContentView
import mail_compose_view as MailComposeSheet

class AppHeader(ft.UserControl):
    def build(self):
        self.iconTitle = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            width=100,
            controls=[
                ft.Icon(name=ft.icons.MAIL_ROUNDED, size=30),
                ft.Text(
                    "MailBox",
                    size=25,
                    weight=ft.FontWeight.BOLD
                )
            ]
        )

        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=1200,
            controls=[
                self.iconTitle,

                ft.TextField(
                    label="Find in mailbox",
                    width=500,
                    prefix_icon=ft.icons.SEARCH_OUTLINED,
                    border_radius=100,
                    content_padding=10
                ),

                ft.CircleAvatar(
                    foreground_image_url="https://sohanews.sohacdn.com/thumb_w/1000/160588918557773824/2021/9/14/photo1631588006082-16315880063578503538.jpg",
                    content=ft.Text("User")
                )
            ]
        )


class Mail(ft.UserControl):

    def __init__(self, sender: str, title: str, content: str, date: str):
        super().__init__()
        self.complete = False
        self.sender = sender
        self.title = title
        self.content = content
        self.date = date
        self.bs = MailContentView.MailContentView(sender, "", title, date, content)
        self.bs.open = False

    async def on_email_clicked(self, e):
        print("on click")
        self.bs.open = True
        await self.bs.update_async()

    def build(self):
        return ft.Container(
            bgcolor=ft.colors.GREY_100,
            padding=ft.padding.all(5),
            content=ft.Row(
                width=1050,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                margin=ft.margin.only(left=15),
                                content=ft.Checkbox(),
                                width=10
                            ),

                            ft.Container(
                                margin=ft.margin.only(left=50),
                                content=ft.Text(self.sender, width=180),
                            ),

                            ft.Container(
                                margin=ft.margin.only(left=15),
                                content=ft.Text(self.title, width=260),
                            ),

                            ft.Container(
                                margin=ft.margin.only(left=15),
                                content=ft.Text(self.content, width=360),
                            ),

                            ft.Container(
                                margin=ft.margin.only(left=15),
                                content=ft.Text(self.date, width=100),
                            ),
                        ]
                    )
                ]
            ),
            on_click=self.on_email_clicked
        )

    async def did_mount_async(self):
        self.page.overlay.append(self.bs)
        await self.page.update_async()

    # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    async def will_unmount_async(self):
        self.page.overlay.remove(self.bs)
        await self.page.update_async()

class InboxPage(ft.UserControl):
    def build(self):
        async def add_mail(self, mail):
            await self.mails.control.append(mail)

        mails = ft.Column(spacing=3)

        # default emails
        mail = Mail("anhhuy007@gmail.com", "Check mail", "Check this email please", "31/12/2023")
        mail2 = Mail("anhhuy007", "Checking for spacing and scaling", "Check this email without open it and then...",
                     "31/12/2023")
        mails.controls.append(mail)
        mails.controls.append(mail2)

        inbox_title = ft.Container(padding=ft.padding.only(top=10, left=5), content=ft.Row(width=1050, controls=[
            ft.Container(
                margin=ft.margin.only(left=15),
                width=10
            ),

            ft.Container(
                margin=ft.margin.only(left=50),
                content=ft.Text("Sender", width=180, weight=ft.FontWeight.BOLD),
            ),

            ft.Container(
                margin=ft.margin.only(left=15),
                content=ft.Text("Title", width=260, weight=ft.FontWeight.BOLD),
            ),

            ft.Container(
                margin=ft.margin.only(left=15),
                content=ft.Text("Content", width=360, weight=ft.FontWeight.BOLD),
            ),

            ft.Container(
                margin=ft.margin.only(left=15),
                content=ft.Text("Date", width=100, weight=ft.FontWeight.BOLD),
            )

        ]))

        return ft.Card(
            elevation=10,
            surface_tint_color=ft.colors.WHITE,
            content=ft.Column(
                controls=[
                    inbox_title,
                    ft.Container(
                        border_radius=10,
                        content=mails
                    )
                ]
            )
        )



def ComposeButton():
    class ComposeButton(ft.FloatingActionButton):
        def __init__(self):
            super().__init__()
            self.icon = ft.icons.CREATE
            self.text = "Compose"
            self.on_click = self.show_bs
            self.bs = MailComposeSheet.MailComposeView()

        def bs_dismissed(self, e):
            print("Dismissed!")

        async def show_bs(self, e):
            self.bs.open = True
            await self.bs.update_async()

        async def close_bs(self, e):
            self.bs.open = False
            await self.bs.update_async()

        # happens when example is added to the page (when user chooses the BottomSheet control from the grid)
        async def did_mount_async(self):
            self.page.overlay.append(self.bs)
            await self.page.update_async()

        # happens when example is removed from the page (when user chooses different control group on the navigation rail)
        async def will_unmount_async(self):
            self.page.overlay.remove(self.bs)
            await self.page.update_async()

    compose_button = ComposeButton()
    compose_button.width = 140

    return compose_button


class AppBody(ft.UserControl):
    def build(self):
        # AppBody attributes
        pages = [
            InboxPage(),
            ft.Container(content=ft.Text("Page 2")),
            ft.Container(content=ft.Text("Page 3")),
        ]

        page = ft.Container(content=pages[0], expand=True)

        # functions
        async def on_page_change(e):
            page.content = pages[e.control.selected_index]
            print("Current page: ", e.control.selected_index)
            await self.update_async()

        async def on_compose_click(self, e):
            pass

        # navigation rail
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            leading=ComposeButton(),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.INBOX_OUTLINED,
                    selected_icon=ft.icons.INBOX_ROUNDED,
                    label="Inbox",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SEND_OUTLINED,
                    selected_icon=ft.icons.SEND_ROUNDED,
                    label="Sent"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS_ROUNDED,
                    label="Setting"
                ),
            ],
            on_change=on_page_change
        )

        return ft.Row(
            expand=True,
            height=600,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                rail,
                ft.VerticalDivider(width=2, color=ft.colors.BLACK),
                page
            ],
        )


class MailApp(ft.UserControl):
    def build(self):
        return ft.Column(
            expand=True,
            controls=[
                AppHeader(),
                AppBody(),
            ]
        )


async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "MailBox"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf"
    }

    page.window_resizable = False

    page.theme = ft.Theme(font_family="Open Sans")
    await page.add_async(MailApp())


ft.app(main)
