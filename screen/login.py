import flet as ft
from flet import (
    Container, Page, UserControl, Stack, Image, Text, Column, TextField, colors, FilledButton, OutlinedButton, Row
)


class LoginScreen(UserControl):
    def build(self):
        def on_cancel_clicked(self):
            pass

        def on_login_clicked(self):
            pass

        body = Container(
            content=Stack(
                [
                    Image("login_background.jpg", ),
                    Container(
                        Container(
                            Column(
                                [
                                    Text(
                                        "Login to MailBox",
                                        color=colors.BLACK,
                                        weight=ft.FontWeight.W_700,
                                        size=26,
                                    ),

                                    Container(
                                        Column(
                                            spacing=25,
                                            controls=[
                                                TextField(
                                                    border_radius=18,
                                                    border=ft.border.all(1, '#44f4f4f4'),
                                                    bgcolor='transparent',
                                                    prefix_icon=ft.icons.MAIL_ROUNDED,
                                                    label="Enter your email",
                                                ),

                                                TextField(
                                                    border_radius=18,
                                                    border=ft.border.all(1, '#44f4f4f4'),
                                                    bgcolor='transparent',
                                                    label='Enter your password',
                                                    prefix_icon=ft.icons.LOCK_ROUNDED,
                                                    suffix_icon=ft.icons.VISIBILITY_ROUNDED,
                                                    password=True,
                                                )
                                            ])
                                    ),

                                    Container(
                                        content=Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=30,
                                            controls=[
                                                FilledButton(
                                                    "Cancel",
                                                    on_click=on_cancel_clicked,
                                                    width=150,
                                                    height=50,
                                                ),

                                                OutlinedButton(
                                                    "Login",
                                                    on_click=on_login_clicked,
                                                    width=150,
                                                    height=50,
                                                )
                                            ])
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND
                            ),
                            width=400,
                            height=400,
                            border_radius=18,
                            blur=ft.Blur(10, 12, ft.BlurTileMode.MIRROR),
                            border=ft.border.all(1, colors.GREY_100),
                            alignment=ft.alignment.center,
                            padding=20,
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=150)
                    )
                ]
            )
        )

        return body


def main(page: Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_resizable = False
    page.vertical_alignment = ft.alignment.center
    page.horizontal_alignment = ft.alignment.center
    page.add(LoginScreen())


ft.app(
    target=main,
    assets_dir="D:/Mail/assets/"
)
