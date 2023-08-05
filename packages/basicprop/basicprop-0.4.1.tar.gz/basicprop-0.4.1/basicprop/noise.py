import numpy as np

def set_uniform_noise(inp, lo, hi, p_val):
    """ Set specific pixels (p_val) to noise.
    """

    r = np.random.randint(lo, hi, inp.shape)
    mask = (inp == p_val)
    outp = np.choose(mask, [inp, r])
    return outp

def add_uniform_noise(inp, lo, hi, p_val=None):
    """ Add noise to input image.
    """

    r = np.random.randint(lo, hi, inp.shape)
    if p_val is not None:
        mask = (inp == p_val)
        zeros = np.zeros((inp.shape))
        outp = inp + np.choose(mask, [zeros, r])
    else:
        outp = inp + r

    return outp
