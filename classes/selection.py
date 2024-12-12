class Selection:
    def __init__(self, map, site, side):
        self.map = map
        self.site = site
        self.side = side

    def set_map(self, map):
        self.map = map

    def set_site(self, site):
        self.site = site

    def set_side(self, side):
        self.side = side

    async def reset(self):
        self.map = ''
        self.site = ''
        self.side = '' 