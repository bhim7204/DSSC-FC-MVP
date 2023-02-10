
from config import config_global
import DSSC_FC_MVP_data_collect as dc
import DSSC_FC_MVP_storage as st


dc.data_collect(config_global.tickers)

st.store_mongo(config_global.data)