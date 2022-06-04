# ------------------------------------------------------------------.
# 2点の緯度経度を指定したときの距離を計算.
# 参考 : https://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2stf.html
# ------------------------------------------------------------------.
import math

# --------------------------------------.
# Input Parameters.
# --------------------------------------.
# Latitude and longitude of the starting point.
in_lat1   = 35.680908
in_longi1 = 139.767348

# Latitude and longitude of the end point.
in_lat2   = 35.666436
in_longi2 = 139.758191

# -----------------------------------------.
# 前処理.
# -----------------------------------------.
# 赤道半径 (km).
R = 6378.137

# 極半径 (km).
R2 = 6356.752

# 扁平率 (ref : https://ja.wikipedia.org/wiki/%E5%9C%B0%E7%90%83).
# 「f = 1.0 - (R2 / R)」の計算になる.
# 「f = 1.0 / 298.257222101」のほうがより正確.
f = 1.0 / 298.257222101

# 度数をラジアンに変換.
lat1R   = in_lat1 * math.pi / 180.0
longi1R = in_longi1 * math.pi / 180.0
lat2R   = in_lat2 * math.pi / 180.0
longi2R = in_longi2 * math.pi / 180.0

l = longi2R - longi1R

l2 = l
if l > math.pi:
    l2 = l - math.pi * 2.0
elif l < -math.pi:
    l2 = l + math.pi * 2.0

L  = abs(l2)
L2 = math.pi - L

delta = 0.0
if l2 >= 0.0:
    depta = lat2R - lat1R
else:
    depta = lat1R - lat2R

sigma = lat1R + lat2R

if l2 >= 0.0:
    u1 = math.atan((1.0 - f) * math.tan(lat1R))
else:
    u1 = math.atan((1.0 - f) * math.tan(lat2R))

if l2 >= 0.0:
    u2 = math.atan((1.0 - f) * math.tan(lat2R))
else:
    u2 = math.atan((1.0 - f) * math.tan(lat1R))

sigma2 = u1 + u2
delta2 = u2 - u1

xi  = math.cos(sigma2 / 2.0)
xi2 = math.sin(sigma2 / 2.0)

eta  = math.sin(delta2 / 2.0)
eta2 = math.cos(delta2 / 2.0)

x = math.sin(u1) * math.sin(u2)
y = math.cos(u1) * math.cos(u2)

c = y * math.cos(L) + x
ep = f * (2.0 - f) / math.pow(1.0 - f, 2.0)

distanceV = 0.0     # 最終的な距離が返る(km).

# -----------------------------------------.
# ゾーンの判断、θの反復計算.
# -----------------------------------------.
t0 = 0.0
if c >= 0.0:
    # Zone(1).
    t0 = L * (1.0 + f * y)
elif c < 0.0 and c >= -math.cos((3.0 * math.pi / 180.0) * math.cos(u1)):
    # Zone(2).
    t0 = L2
else:
    # Zone(3).
    rr = 1.0 - (1.0/4.0) * f * (1.0 + f) * math.pow(math.sin(u1), 2.0)
    rr += (3.0/16.0) * f * f * math.pow(math.sin(u1), 4.0)
    rr = f * math.pi * math.pow(math.cos(u1), 2.0) * rr
    d1 = L2 * math.cos(u1) - rr
    d2 = abs(sigma2) + rr
    q = L2 / (f * math.pi)
    f1 = (1.0/4.0) * f * (1.0 + 0.5 * f)
    gam0 = q + f1 * q - f1 * math.pow(q, 3.0)

    if sigma != 0.0:
        A0 = math.atan(d1 / d2)
        B0 = math.asin(rr / math.sqrt(d1 * d1 + d2 * d2))

        v = A0 + B0
        j = gam0 / math.cos(u1)
        k = (1.0 + f1) * abs(sigma2) * (1.0 - f * y) / (f * math.pi * y)
        j1 = j / (1.0 + k * (1.0 / math.cos(v)))
        v2 = math.asin(j1)
        v3 = math.asin((math.cos(u1) / math.cos(u2)) * j1)

        t0 = math.tan((v2 + v3) / 2.0) * math.sin(abs(sigma2) / 2.0)
        t0 /= math.cos(delta2 / 2.0)
        t0 = 2.0 * math.atan(t0)

    else:
        if d1 > 0.0:
            t0 = L2
        elif d1 == 0.0:
            gam2 = math.pow(math.sin(u1), 2.0)
            n0 = math.sqrt(1.0 + ep * gam2) + 1.0
            n0 = (ep * gam2) / math.pow(n0, 2.0)
            A = (1.0 + n0) * (1.0 + (5.0/4.0) * n0 * n0)

            distanceV = (1.0 - f) * R * A * math.pi
        else:
            gV = gam0
            gam2 = 0.0
            while True:
                gam2 = 1.0 - gV * gV
                D = (1.0/4.0) * f * (1.0 + f) - (3.0/16.0) * f * f * gam2
                gV2 = q / (1.0 - D * gam2)
                if abs(gV2 - gV) < (1e-15):
                    break
            
            m = 1.0 - q * (1.0 / math.cos(u1))
            n = (D * gam2) / (1.0 - D * gam2)
            w = m - n + m * n

            n0 = math.sqrt(1.0 + ep * gam2) + 1.0
            n0 = (ep * gam2) / math.pow(n0, 2.0)
            A = (1.0 + n0) * (1.0 + (5.0/4.0) * n0 * n0)
            distanceV = (1.0 - f) * R * A * math.pi

if distanceV == 0.0:
    tV = t0

    while True:
        if c >= 0.0:
            g  = math.pow(eta, 2.0) * math.pow(math.cos(tV / 2.0), 2.0)
            g += math.pow(xi, 2.0) * math.pow(math.sin(tV / 2.0), 2.0)
            g = math.sqrt(g)

            h  = math.pow(eta2, 2.0) * math.pow(math.cos(tV / 2.0), 2.0)
            h += math.pow(xi2, 2.0) * math.pow(math.sin(tV / 2.0), 2.0)
            h = math.sqrt(h)

        else:
            g  = math.pow(eta, 2.0) * math.pow(math.sin(tV / 2.0), 2.0)
            g += math.pow(xi, 2.0) * math.pow(math.cos(tV / 2.0), 2.0)
            g = math.sqrt(g)

            h  = math.pow(eta2, 2.0) * math.pow(math.sin(tV / 2.0), 2.0)
            h += math.pow(xi2, 2.0) * math.pow(math.cos(tV / 2.0), 2.0)
            h = math.sqrt(h)

        sig = 2.0 * math.atan(g / h)
        J = 2.0 * g * h
        K = h * h - g * g
        gam = y * math.sin(tV) / J
        gam2 = 1.0 - gam * gam
        v  = gam2 * K - 2.0 * x
        v2 = v + x
        D = (1.0 / 4.0) * f * (1.0 + f) - (3.0 / 16.0) * f * f * gam2
        E = (1.0 - D * gam2) * f * gam * (sig + D * J * (v + D * K * (2.0 * v * v - gam2 * gam2)))

        if c >= 0.0:
            F = tV - L - E
        else:
            F = tV - L2 + E

        G  = f * gam * gam * (1.0 - 2.0 * D * gam2)
        G += f * v2 * (sig / J) * (1.0 - D * gam2 + 0.5 * f * gam * gam)
        G += (1.0 / 4.0) * f * f * v * v2

        tV = tV - F / (1.0 - G)

        # -----------------------------------------.
        # 測地線長の計算.
        # -----------------------------------------.
        if abs(F) < (1e-15):
            n0 = math.sqrt(1.0 + ep * gam2) + 1.0
            n0 = (ep * gam2) / math.pow(n0, 2.0)

            A = (1.0 + n0) * (1.0 + (5.0/4.0) * n0 * n0)
            B = ep * (1.0 - 3.0 * n0 * n0 / 8.0)
            B /= math.pow(math.sqrt(1.0 + ep * gam2) + 1.0, 2.0)

            s1 = (1.0/6.0) * B * v * (1.0 - 4.0 * K * K) * (3.0 * gam2 * gam2 - 4.0 * v * v)
            s2 = K * (gam2 * gam2 - 2.0 * v * v) - s1
            s3 = sig - B * J * (v - (1.0/4.0) * B * s2)
            distanceV = (1.0 - f) * R * A * s3
            break

print("Distance : " + str(distanceV * 1000.0) + " m ( " + str(distanceV) + " km )")

