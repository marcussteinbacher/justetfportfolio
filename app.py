import streamlit as st 
from utils import get_all_etfs, Etf, EtfPortfolio

# Session state
if "etfs" not in st.session_state:
    st.session_state.etfs = []
if "all_etfs" not in st.session_state:
    st.session_state.all_etfs = get_all_etfs()


# Functions
def add_etf(isin,amnt,is_shares):
    if not amnt:
        st.warning("Please enter a valid amount!")
        return
    
    if is_shares:
        new_etf = Etf(isin, shares=amnt)
    else:
        new_etf = Etf(isin, value=amnt)
    
    # New ETF
    if isin not in [etf.isin for etf in st.session_state.etfs]:
        st.session_state.etfs.append(new_etf)
    # ETF already in state
    else:
        st.session_state.etfs = [etf+new_etf if etf.isin == new_etf.isin else etf for etf in st.session_state.etfs]


def remove_etf(isin):
    st.session_state.etfs = [etf for etf in st.session_state.etfs if etf.isin != isin]
    st.rerun()

st.header("JustETF Portfolio Holdings")
st.markdown("Build a portfolio of ETFs listed on [justETF](https://www.justetf.com/) and analyze the aggregated country, sector, and holdings exposure.")

with st.form("input",enter_to_submit=False):
    etf_input = st.selectbox("Select ETF", st.session_state.all_etfs["display"])
    
    with st.container(horizontal=True,vertical_alignment="center"):
        amnt_input = st.number_input("Amount", min_value=0., value=1.,step=0.01)
        is_shares = st.radio("Amount", [True,False], format_func=lambda x: "Shares" if x else "EUR", label_visibility="hidden")
    
    isin = st.session_state.all_etfs.loc[st.session_state.all_etfs["display"] == etf_input]["isin"].values[0]
    
    #if isin in [etf.isin for etf in st.session_state.etfs]:
    #    st.warning("ETF already in portfolio! Position will be updated.")

    submit_btn = st.form_submit_button("Add",key="submit_btn")

    if submit_btn:
        with st.spinner():
            add_etf(isin,amnt_input,is_shares)


st.markdown("## Overview", help="In case a position is added with the `Shares` option, the position's `value` (EUR) is automatically calculated from the last fetched quote price.")

portfolio = EtfPortfolio(st.session_state.etfs)
for etf in portfolio.etfs:
    with st.container(horizontal=True,vertical_alignment="center"):
        st.write(etf)
        st.space("stretch")
        if st.button("Remove",type="primary",key=f"del_btn_{etf.isin}"):
            remove_etf(etf.isin)

with st.container(horizontal=True):
    st.write("Total Value", round(portfolio.value,2))
    st.write("Total TER", round(portfolio.ter,2))

st.markdown("## Weights", help="Portfolio weights are automatically calculated based on the `value` (EUR) of each position.")

st.write(portfolio.get_weights(scale=100))

st.markdown("## Exposure", help="The total exposure is calculated from the `weight` and the individual exposure of each position. If no value is reported by justetf, it defaults to `Unknown`. The aggregated `Holdings` are calculated from the top 10 holdings of each position, only.")

ctry_tab, sect_tab, hld_tabs = st.tabs(["Countries","Sectors","Holdings"])

with ctry_tab:
    st.write(portfolio.get_countries())
with sect_tab:
    st.write(portfolio.get_sectors())
with hld_tabs:
    st.write(portfolio.get_holdings())