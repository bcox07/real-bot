from classes.enums import Map

class Selection:
    def __init__(self):
        self.map = None
        self.site = None
        self.side = None

    def set_map(self, map: Map):
        self.map = map

    def set_site(self, site: str):
        self.site = site

    def set_side(self, side: str):
        self.side = side

    async def reset(self):
        self.map = None
        self.site = None
        self.side = None