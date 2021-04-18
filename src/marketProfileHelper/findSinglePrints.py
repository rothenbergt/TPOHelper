# The purpose of this file is to find single prints for a given day

from market_profile import MarketProfile
import pandas_datareader as data
es = data.get_data_yahoo('ES=F', '2021-4-12', '2021-4-16')

mp = MarketProfile(es)
mp_slice = mp[es.index.min():es.index.max()]

val = str(mp_slice.value_area[0])
vah = str(mp_slice.value_area[1])

print("The weekly VAH is: " + vah)
print("The weekly VAL is: " + val)


