import justetf_scraping as justetf
from justetf_scraping.etf_profile import List, AllocationItem, ElementTree, BeautifulSoup, _parse_percentage
import copy
import streamlit as st


# Patch for justetf_scraping
def parse_allocation_from_ajax_new(xml_response: str, table_id: str, name_testid: str, pct_testid: str
) -> List[AllocationItem]:

    allocations = []

    try:
        root = ElementTree.fromstring(xml_response)
        components = root.findall("component")
        for component in components:
            soup = BeautifulSoup(component.text, "html.parser")
            table = soup.find("table",attrs={"data-testid":"etf-holdings_countries_table"}) or soup.find("table",attrs={"data-testid":"etf-holdings_sectors_table"})
            if table:
                rows = soup.find_all("tr", attrs={"data-testid": True})
                for row in rows:
                    name_elem = row.find("td", attrs={"data-testid": name_testid})
                    pct_elem = row.find("span", attrs={"data-testid": pct_testid})
                    if name_elem and pct_elem:
                        name = name_elem.get_text(strip=True)
                        pct = _parse_percentage(pct_elem.get_text(strip=True))
                        if name and pct is not None:
                            allocations.append(
                                AllocationItem(name=name, percentage=pct)
                            )
    except Exception as e:
        print(f"Error parsing allocation data: {e}")

    return allocations

# Monkey patch
justetf.etf_profile._parse_allocation_from_ajax = parse_allocation_from_ajax_new

@st.cache_data(show_spinner="Fetching available ETFs...")
def get_all_etfs():
    df = justetf.load_overview()
    df.loc[:,"isin"] = df.index
    df.loc[:,"display"] = df["name"]+" ("+df["isin"]+")"
    return df


class Etf:
    _fetch_kwargs = {
        "include_gettex":False, 
        "expand_allocations":False
        }

    def __init__(self, isin:str, shares:int|None=None,value:float|None=None,**kwargs):
        if not shares and not value:
            raise ValueError("Either shares or value must be provided!")
        self._fetch_kwargs.update({k:v for k,v in kwargs.items() if k in self._fetch_kwargs.keys()})
        self.overview = self._account_for_non_reported(justetf.get_etf_overview(isin, **self._fetch_kwargs))
        self.isin = isin
        self.shares = shares
        self.value = value if value else justetf.load_live_quote(isin).last * shares
        self.ter = self.overview["ter"] if self.overview["ter"] is not None else 0

    def _account_for_non_reported(self, overview):
        if len(overview["top_holdings"])==0:
            overview["top_holdings"] = [{"name":"Unknown","percentage":100}]
        if len(overview["countries"])==0:
            overview["countries"] = [{"name":"Unknown","percentage":100}]
        if len(overview["sectors"])==0:
            overview["sectors"] = [{"name":"Unknown","percentage":100}]
        return overview
    

    def __mul__(self, weight:float):
        """
        Scales the exposure for easy summation in a portfolio of multiple ETs.
        """
        obj = copy.deepcopy(self)

        for holding in obj.overview["top_holdings"]:
            holding["percentage"] *= weight
        for country in obj.overview["countries"]:
            country["percentage"] *= weight
        for sector in obj.overview["sectors"]:
            sector["percentage"] *= weight
        #obj.ter *= weight
        #obj.value *= weight
        
        return obj
    
    def __add__(self, other):
        if not self.isin == other.isin:
            raise ValueError("Cannot add different ETFs!")
        
        return Etf(self.isin, shares=self.shares + other.shares,value=self.value + other.value)

    def __repr__(self) -> str:
        if not self.shares:
            return f"ETF({self.overview['name']}: {round(self.value,2)}€ @ {self.ter}% p.a.)"
        else:
            return f"ETF({self.overview['name']}: {round(self.value,2)}€ ({int(self.shares)} pcs.) @ {self.ter}% p.a.)"


class EtfPortfolio:
    def __init__(self, etfs:list[Etf]):
        self.value = sum([etf.value for etf in etfs])
        self.weights = [etf.value / self.value for etf in etfs]
        self.etfs = [etf * weight for etf,weight in zip(etfs,self.weights)]
        self.ter = sum([etf.ter * weight for etf,weight in zip(self.etfs,self.weights)])

    def _get_accumulation(self,key:str)->dict:
        d = {}
        for etf in self.etfs: # exposure already scaled with weight
            for entry in etf.overview[key]:
                if entry["name"] in d:
                    d[entry["name"]] += entry["percentage"]
                else:
                    d[entry["name"]] = entry["percentage"]
        return dict(sorted(d.items(),key=lambda x: x[1],reverse=True))
    
    def get_weights(self,scale=1):
        return dict(zip([etf.overview["name"] for etf in self.etfs], [weight*scale for weight in self.weights]))

    def get_countries(self):
        return self._get_accumulation("countries")

    def get_sectors(self):
        return self._get_accumulation("sectors")

    def get_holdings(self):
        return self._get_accumulation("top_holdings")

if __name__ == "__main__":
    get_all_etfs()