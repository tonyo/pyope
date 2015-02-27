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

        ix = None

        prng = PRNG(coins)

        con, deltal = 57.56462733, 0.0078
        deltau, scale = 0.0034, 1.0e25

        # TODO Check validity of parameters.

        reject = True

        if nn1 >= nn2:
            n1, n2 = float(nn2), float(nn1)
        else:
            n1, n2 = float(nn1), float(nn2)

        tn = n1 + n2

        if kk + kk >= tn:
            k = tn - kk
        else:
            k = kk

        m = (k + 1.0) * (n1 + 1.0) / (tn + 2.0)

        if k - n2 < 0:
            minjx = 0
        else:
            minjx = k - n2

        if n1 < k:
            maxjx = n1
        else:
            maxjx = k

        # Degenerate distribution
        if minjx == maxjx:
            # no need to untangle TSL
            return int(math.floor(maxjx))

        # Inverse transformation
        elif m - minjx < 10:
            if k < n2:
                w = math.exp(
                    con + afc(n2) + afc(n1 + n2 - k) - afc(n2 - k) - afc(
                        n1 + n2))
            else:
                w = math.exp(
                    con + afc(n1) + afc(k) + afc(k - n2) - afc(n1 + n2))

            # TODO check!
            while True:
                p = w
                ix = minjx
                u = prng.draw() * scale

                finished = True
                while u > p:
                    u -= p
                    p = p * (n1 - ix) * (k - ix)
                    ix += 1
                    p = p / ix / (n2 - k + ix)
                    if ix > maxjx:
                        finished = False
                        break
                if finished:
                    break

        # Hypergeometrics-2 points-exponential tails
        else:

            s = math.sqrt((tn - k) * k * n1 * n2 / (tn - 1.0) / tn / tn)

            # Truncation centers cell boundaries at 0.5
            d = math.floor(1.5 * s) + 0.5
            xl = m - d + 0.5
            xr = m + d + 0.5
            a = afc(m) + afc(n1 - m) + afc(k - m) + afc(n2 - k + m)
            expon = a - afc(xl) - afc(n1 - xl) - afc(k - xl) - afc(n2 - k + xl)
            kl = math.exp(expon)
            kr = math.exp(a - afc(xr - 1) -
                          afc(n1 - xr + 1) - afc(k - xr + 1) -
                          afc(n2 - k + xr - 1))
            lamdl = -math.log(xl *
                              (n2 - k + xl) / (n1 - xl + 1) / (k - xl + 1))
            lamdr = -math.log(
                (n1 - xr + 1) * (k - xr + 1) / xr / (n2 - k + xr))

            p1 = 2 * d
            p2 = p1 + kl / lamdl
            p3 = p2 + kr / lamdr

            # LABEL 30
            while True:
                u = prng.draw() * p3
                v = prng.draw()

                # Rectangular region
                if u < p1:
                    ix = xl + u
                # Left tail region
                elif u <= p2:
                    ix = xl + math.log(v) / lamdl
                    if ix < minjx:
                        continue
                    v = v * (u - p1) * lamdl
                # Right tail region
                else:
                    ix = xr - math.log(v) / lamdr
                    if ix > maxjx:
                        continue
                    v = v * (u - p2) * lamdr

                if m < 100 or ix <= 50:
                    f = 1.0
                    if m < ix:
                        i = m + 1
                        while i < ix:  # <= ?
                            f = f * (n1 - i + 1.0) * (k - i + 1.0) / (
                                n2 - k + i) / i
                            i += 1
                    elif m > ix:
                        i = ix + 1
                        while i < m:  # <= ?
                            f = f * i * (n2 - k + i) / (n1 - i) / (
                                k - i)  # + 1 ?
                            i += 1
                    if v <= f:
                        reject = False
                else:
                    y = ix
                    y1 = y + 1.0
                    ym = y - m
                    yn = n1 - y + 1.0
                    yk = k - y + 1.0
                    nk = n2 - k + y1
                    r = -ym / y1
                    s2 = ym / yn
                    t = ym / yk
                    e = -ym / nk
                    g = yn * yk / (y1 * nk) - 1.0
                    dg = 1.0
                    if g < 0:
                        dg = 1.0 + g
                    gu = g * (1.0 + g * (-0.5 + g / 3.0))
                    gl = gu - 0.25 * (g * g * g * g) / dg
                    xm = m + 0.5
                    xn = n1 - m + 0.5
                    xk = k - m + 0.5
                    nm = n2 - k + xm

                    ub = y * gu - m * gl + deltau + xm * r * (1 + r * (-0.5 + r / 3)) + \
                        xn * s2 * (1.0 + s2 * (-0.5 + s2 / 3.0)) + \
                        xk * t * (1.0 + t * (-0.5 + t / 3.0)) + \
                        nm * e * (1.0 + e * (-0.5 + e / 3.0))

                    alv = math.log(v)

                    if alv > ub:
                        reject = True
                    else:
                        dr = xm * (r * r * r * r)
                        if r < 0:
                            dr /= (1.0 + r)
                        ds = xn * (s2 * s2 * s2 * s2)
                        if s2 < 0:
                            ds /= (1.0 + s2)
                        dt = xk * (t * t * t * t)
                        if t < 0:
                            dt /= (1.0 + t)
                        de = nm * (e * e * e * e)
                        if e < 0:
                            de /= (1.0 + e)

                        cand = ub - 0.25 * (dr + ds + dt + de) + (y + m) * (gl - gu) - deltal

                        if alv < cand:
                            reject = False
                        else:
                            cand = a - afc(ix) - afc(n1 - ix) - afc(k - ix) - afc(n2 - k + ix)
                            reject = alv > cand

                if not reject:
                    break

        if kk + kk >= tn:
            if nn1 > nn2:
                ix = kk - nn2 + ix
            else:
                ix = nn1 - ix

        else:
            if nn1 > nn2:
                ix = kk - ix

        jx = ix
        return int(math.floor(jx))
