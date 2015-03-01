# Fortran code was used as a reference: http://www.netlib.org/toms-2014-06-10/668

import math
import random
import itertools


class PRNG(object):
    def __init__(self, coins):
        self.coins = coins

    def draw(self):
        bits = list(itertools.islice(self.coins, 32))
        assert len(bits) == 32
        out = 0
        for b in bits:
            out = (out << 1) | b
        res = 1.0 * out / (2 ** 32 - 1)
        assert 0 <= res <= 1
        return res


# Calculates logarithm of i factorial: ln(i!)
# Uses Stirling's approximation to do so.
def afc(i):
    if i < 0:
        raise Exception('i should not be < 0')
    elif i == 0:
        return 0

    frac_12, frac_360 = 1.0 / 12.0, 1.0 / 360.0
    frac_pi = 0.5 * math.log(2 * math.pi)

    res = (i + 0.5) * math.log(i) - i + frac_12 / i - frac_360 / i / i / i + frac_pi
    return res


class HGD(object):
    # Random variates from the hypergeometric distribution.
    #
    # Returns the number of white balls drawn when kk balls
    # are drawn at random from an urn containing nn1 white
    # and nn2 black balls.
    # nn1 -- good
    # nn2 -- bad
    @staticmethod
    def rhyper(kk, nn1, nn2, coins):
        prng = PRNG(coins)
        if kk > 10:
            return HGD.hypergeometric_hrua(prng, nn1, nn2, kk)
        else:
            return HGD.hypergeometric_hyp(prng, nn1, nn2, kk)

    @staticmethod
    def hypergeometric_hyp(prng, good, bad, sample):
        d1 = bad + good - sample
        d2 = float(min(bad, good))

        Y = d2
        K = sample
        while Y > 0.0:
            U = prng.draw()
            Y -= int(math.floor(U + Y/(d1 + K)))
            K -= 1
            if K == 0:
                break
        Z = int(d2 - Y)
        if good > bad:
            Z = sample - Z
        return Z


    @staticmethod
    def hypergeometric_hrua(prng, good, bad, sample):
        D1 = 1.7155277699214135
        D2 = 0.8989161620588988
        # long mingoodbad, maxgoodbad, popsize, m, d9;
        # double d4, d5, d6, d7, d8, d10, d11;
        # long Z;
        # double T, W, X, Y;

        mingoodbad = min(good, bad)
        popsize = good + bad
        maxgoodbad = max(good, bad)
        m = min(sample, popsize - sample)
        d4 = float(mingoodbad) / popsize
        d5 = 1.0 - d4
        d6 = m*d4 + 0.5
        d7 = math.sqrt((popsize - m) * sample * d4 * d5 / (popsize-1) + 0.5)
        d8 = D1*d7 + D2
        d9 = int(math.floor(float(m+1) * (mingoodbad+1) / (popsize + 2)))
        d10 = HGD.loggam(d9+1) + HGD.loggam(mingoodbad-d9+1) + HGD.loggam(m-d9+1) + HGD.loggam(maxgoodbad-m+d9+1)
        d11 = min(min(m, mingoodbad) + 1.0, math.floor(d6 + 16 * d7))
        # 16 for 16-decimal-digit precision in D1 and D2

        while True:
            X = prng.draw()
            Y = prng.draw()
            W = d6 + d8 * (Y - 0.5) / X

            # fast rejection:
            if W < 0.0 or W >= d11:
                continue

            Z = int(math.floor(W))
            T = d10 - (HGD.loggam(Z+1) + HGD.loggam(mingoodbad-Z+1) + HGD.loggam(m-Z+1) + HGD.loggam(maxgoodbad-m+Z+1))

            # fast acceptance:
            if (X*(4.0-X)-3.0) <= T:
                break

            # fast rejection:
            if X*(X-T) >= 1:
                continue

            # acceptance:
            if 2.0 * math.log(X) <= T:
                break


        # this is a correction to HRUA* by Ivan Frohne in rv.py
        if good > bad:
            Z = m - Z

        # another fix from rv.py to allow sample to exceed popsize/2
        if m < sample:
            Z = good - Z

        return Z

    """
    /*
     * log-gamma function to support some of these distributions. The
     * algorithm comes from SPECFUN by Shanjie Zhang and Jianming Jin and their
     * book "Computation of Special Functions", 1996, John Wiley & Sons, Inc.
     */
"""
    @staticmethod
    def loggam(x):
        # double x0, x2, xp, gl, gl0;
        # long k, n;

        a = [8.333333333333333e-02, -2.777777777777778e-03,
             7.936507936507937e-04, -5.952380952380952e-04,
             8.417508417508418e-04, -1.917526917526918e-03,
             6.410256410256410e-03, -2.955065359477124e-02,
             1.796443723688307e-01, -1.39243221690590e+00]
        x *= 1.0
        x0 = x
        n = 0
        if x == 1.0 or x == 2.0:
            return 0.0

        elif x <= 7.0:
            n = int(7 - x)
            x0 = x + n
        x2 = 1.0 / (x0*x0)
        xp = 2 * math.pi
        gl0 = a[9]
        for k in range(8, -1, -1):
            gl0 *= x2
            gl0 += a[k]
        gl = gl0/x0 + 0.5 * math.log(xp) + (x0-0.5) * math.log(x0) - x0
        if x <= 7.0:
            for k in range(1, n + 1):
                gl -= math.log(x0-1.0)
                x0 -= 1.0
        return gl
