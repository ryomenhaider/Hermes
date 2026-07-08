from textual.widgets import Tree


class MainScreenTree(Tree):

    def __init__(self):
        super().__init__("Data Sources")

    def on_mount(self) -> None:
        root = self.root

        finance = root.add("Finance & Economics")

        macro = finance.add("Macroeconomic")
        markets = finance.add("Markets")
        corp = finance.add("Corporate Intelligence")

        macro.add_leaf("FRED", data="fred")
        macro.add_leaf("World Bank", data="world_bank")
        macro.add_leaf("IMF", data="imf")
        macro.add_leaf("ECB", data="ecb")
        macro.add_leaf("US Treasury", data="us_treasury")

        markets.add_leaf("Alpha Vantage", data="alpha_vantage")
        markets.add_leaf("CoinGecko", data="coingecko")
        markets.add_leaf("ExchangeRate.host", data="exchange_rate")
        markets.add_leaf("Financial Modeling Prep", data="fmp")

        corp.add_leaf("SEC EDGAR", data="sec_edgar")
        corp.add_leaf("OpenCorporates", data="open_corporates")
        corp.add_leaf("Open Ownership", data="open_ownership")
        corp.add_leaf("Companies House", data="companies_house")

        defense = root.add("Defense & Geopolitics")

        conflict = defense.add("Conflict Data")
        military = defense.add("Military Data")
        geo = defense.add("Geospatial")

        conflict.add_leaf("UCDP", data="ucdp")
        conflict.add_leaf("Correlates of War", data="cow")
        conflict.add_leaf("ICEWS", data="icews")
        conflict.add_leaf("GDELT", data="gdelt")
        conflict.add_leaf("Phoenix", data="phoenix")

        military.add_leaf("SIPRI Arms", data="sipri_arms")
        military.add_leaf(
            "SIPRI Military Expenditure",
            data="sipri_military",
        )
        military.add_leaf("NATO Data", data="nato")
        military.add_leaf("WMEAT", data="wmeat")

        geo.add_leaf("NASA FIRMS", data="firms")
        geo.add_leaf("NOAA", data="noaa")
        geo.add_leaf("USGS", data="usgs")
        geo.add_leaf("OpenStreetMap", data="osm")
        geo.add_leaf("Copernicus", data="copernicus")

    def on_tree_node_selected(
        self,
        event: Tree.NodeSelected,
    ) -> None:

        page = event.node.data

        if page:
            self.app.push_screen(page)