import numpy.random as rand

# TODO remove it, but make portable?
MAX_INT = 2**32

def sample_hgd(in_range, out_range, nsample, seed):
    seed = int(seed % MAX_INT)
    rand.seed(seed)
    in_size = in_range.size()
    out_size = out_range.size()
    assert in_size > 0 and out_size > 0
    assert in_size <= out_size
    assert out_range.contains(nsample)

    # 1-based index of nsample in out_range
    nsample_index = nsample - out_range.start + 1
    if in_size == out_size:
        # Input and output domains have equal size
        return in_range.start + nsample_index - 1

    in_sample_num = rand.hypergeometric(in_size, out_size - in_size, nsample_index)
    if in_sample_num == 0:
        return in_range.start
    elif in_sample_num == in_size:
        return in_range.end
    else:
        in_sample = in_range.start + in_sample_num
        assert in_range.contains(in_sample)
        return in_sample


