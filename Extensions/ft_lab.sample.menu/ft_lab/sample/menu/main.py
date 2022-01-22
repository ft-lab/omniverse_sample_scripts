import omni.ext
import asyncio

import omni.kit.menu.utils
import omni.kit.undo
import omni.kit.commands
import omni.usd
from omni.kit.menu.utils import MenuItemDescription

class MenuExtension(omni.ext.IExt):
    # Menu list.
    _menu_list = None
    _sub_menu_list = None

    # Menu name.
    _menu_name = "MenuTest"

    # ------------------------------------------.
    # Initialize menu.
    # ------------------------------------------.
    def init_menu (self):
        async def _rebuild_menus():
            await omni.kit.app.get_app().next_update_async()
            omni.kit.menu.utils.rebuild_menus()

        def menu_select (mode):
            if mode == 0:
                print("Select MenuItem 1.")
            if mode == 1:
                print("Select MenuItem 2.")
            if mode == 2:
                print("Select MenuItem 3.")
            if mode == 10:
                print("Select Sub MenuItem 1.")
            if mode == 11:
                print("Select Sub MenuItem 2.")

        self._sub_menu_list = [
            MenuItemDescription(name="Sub MenuItem 1", onclick_fn=lambda: menu_select(10)),
            MenuItemDescription(name="Sub MenuItem 2", onclick_fn=lambda: menu_select(11)),
        ]

        self._menu_list = [
            MenuItemDescription(name="MenuItem 1", onclick_fn=lambda: menu_select(0)),
            MenuItemDescription(name="MenuItem 2", onclick_fn=lambda: menu_select(1)),
            MenuItemDescription(name="MenuItem 3", onclick_fn=lambda: menu_select(2)),
            MenuItemDescription(),
            MenuItemDescription(name="SubMenu", sub_menu=self._sub_menu_list),
        ]

        # Rebuild with additional menu items.
        omni.kit.menu.utils.add_menu_items(self._menu_list, self._menu_name)
        asyncio.ensure_future(_rebuild_menus())

    # ------------------------------------------.
    # Term menu.
    # It seems that the additional items in the top menu will not be removed.
    # ------------------------------------------.
    def term_menu (self):
        async def _rebuild_menus():
            await omni.kit.app.get_app().next_update_async()
            omni.kit.menu.utils.rebuild_menus()

        # Remove and rebuild the added menu items.
        omni.kit.menu.utils.remove_menu_items(self._menu_list, self._menu_name)
        asyncio.ensure_future(_rebuild_menus())

    # ------------------------------------------.

    def on_startup(self, ext_id):
        print("[ft_lab.sample.menu] MenuExtension startup")

        # Initialize menu.
        self.init_menu()

    def on_shutdown(self):
        print("[ft_lab.sample.menu] MenuExtension shutdown")

        # Term menu.
        self.term_menu()
