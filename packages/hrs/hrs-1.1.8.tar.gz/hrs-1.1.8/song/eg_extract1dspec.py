
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
#%pylab qt
#%matplotlib qt
#%load_ext autoreload
#%autoreload 2

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

find_aps_param_dict = dict(start_col=440, max_drift=8, max_apwidth=10,
                           n_pix_goodap=100, n_adj=10, n_smooth=1, n_sep=3, c=5)
ap_comb = hrs.combine_apertures([flat_bias], n_jobs=1, find_aps_param_dict=find_aps_param_dict)
cheb_coefs, ap_uorder_interp = hrs.group_apertures(ap_comb, start_col=1024, order_dist=7)

flat_bias_sl = hrs.substract_scattered_light(flat_bias, ap_uorder_interp, ap_width=10, shrink=.85)
flat1d = hrs.extract_1dspec(flat_bias_sl, ap_uorder_interp, ap_width=8)[0]

star_bias_sl = hrs.substract_scattered_light(star_bias, ap_uorder_interp, ap_width=10, shrink=.85)
star1d = hrs.extract_1dspec(star_bias_sl, ap_uorder_interp, ap_width=8)[0]


star1d_dblz = star1d/flat1d

for i in range(star1d_dblz.shape[0]):
    plot(star1d_dblz[i, :]/np.median(star1d_dblz[i, :])+i*1)


#%%
imshow(flat, interpolation='nearest')
plot(ap_comb.T, 'k-')
plot(ap_uorder_interp.T, 'w-')

