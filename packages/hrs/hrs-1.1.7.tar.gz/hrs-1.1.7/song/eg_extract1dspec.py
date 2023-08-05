
"""
an example of extracting 1d spectra for SONG

"""

from song import extract
from song import measure_xdrift
from song import ccdproc_mod
import hrs

#%%

reload(extract)
reload(measure_xdrift)


#%%
%pylab qt
%matplotlib qt
%load_ext autoreload
%autoreload 2

#%%

# specify directory
dp = '/hydrogen/song/star_spec/20170102/night/raw/'

# scan fits files
t = measure_xdrift.scan_files(dp)

# measure cross-order drift
t2, fig = measure_xdrift.check_xdrift(t)



flat = extract.produce_master(t2, method='average', imagetp='FLAT', slc=slice(0, 10)).rot90(1)
bias = extract.produce_master(t2, method='average', imagetp='BIAS', slc=slice(0, 10)).rot90(1)
flat_bias = ccdproc_mod.subtract_bias(flat, bias)

star = extract.produce_master(t2, method='median', imagetp='STAR', slc=slice(0, 1)).rot90(1)
star_bias = ccdproc_mod.subtract_bias(star, bias)

extract.list_image(t, 'FLAT')

find_aps_param_dict = dict(start_col=1300, max_drift=12, max_apwidth=13, n_pix_goodap=200)
ap_comb = hrs.combine_apertures([flat_bias], n_jobs=1, find_aps_param_dict=find_aps_param_dict)
cheb_coefs, ap_uorder_interp = hrs.group_apertures(ap_comb, start_col=1024, order_dist=7)

imshow(flat)
imshow(star_bias)

plot(star_bias[:, 1026])


find_aps_param_dict = dict(start_col=200, max_drift=8, max_apwidth=12, n_pix_goodap=1000)
ap_comb = hrs.combine_apertures(flat_list, n_jobs=10, find_aps_param_dict=find_aps_param_dict)
cheb_coefs, ap_uorder_interp = group_apertures(ap_comb, start_col=1000, order_dist=10)
#%%
imshow(flat)
plot(ap_comb.T, 'k-')
plot(ap_uorder_interp.T, 'w-')
