# ------------------------------------------------------------------.
# 緯度経度を平面直角座標に変換し、Omniverse(USD)のY-Up/cmに変換.
# 参考 : https://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2xyf.html
#
# ただし、日本地図上での計算になる点に注意.
# ------------------------------------------------------------------.
import math

# --------------------------------------.
# Input Parameters.
# --------------------------------------.
# Latitude and longitude.
in_lat   = 35.680908
in_longi = 139.767348

# ---------------------------------------------------------.
# 平面直角座標系の原点の緯度と経度を取得.
# 参考 : https://www.gsi.go.jp/LAW/heimencho.html
# 東京都の場合は9を指定.
# ---------------------------------------------------------.
def getOriginLatAndLongi (index : int = 9):
    latV0   = 0.0
    longiV0 = 0.0

    # I.
    if index == 1:
        latV0   = 33.0
        longiV0 = 129.5
    # II.
    elif index == 2:
        latV0   = 33.0
        longiV0 = 131.0
    # III.
    elif index == 3:
        latV0   = 36.0
        longiV0 = 131.16666666
    # IV.
    elif index == 4:
        latV0   = 33.0
        longiV0 = 133.5
    # V.
    elif index == 5:
        latV0   = 36.0
        longiV0 = 134.33333333
    # VI.
    elif index == 6:
        latV0   = 36.0
        longiV0 = 136.0
    # VII.
    elif index == 7:
        latV0   = 36.0
        longiV0 = 137.16666666
    # VIII.
    elif index == 8:
        latV0   = 36.0
        longiV0 = 138.5
    # IX.       // 東京都（デフォルト）.
    elif index == 9:
        latV0   = 36.0
        longiV0 = 139.83333333
    # X.
    elif index == 10:
        latV0   = 40.0
        longiV0 = 140.83333333
    # XI.
    elif index == 11:
        latV0   = 44.0
        longiV0 = 140.25
    # XII.
    elif index == 12:
        latV0   = 44.0
        longiV0 = 142.25
    # XIII.
    elif index == 13:
        latV0   = 44.0
        longiV0 = 144.25
    # XIV.
    elif index == 14:
        latV0   = 26.0
        longiV0 = 142.0
    # XV.
    elif index == 15:
        latV0   = 26.0
        longiV0 = 127.5
    # XVI.
    elif index == 16:
        latV0   = 26.0
        longiV0 = 124.0
    # XVII.
    elif index == 17:
        latV0   = 26.0
        longiV0 = 131.0
    # XVIII.
    elif index == 18:
        latV0   = 20.0
        longiV0 = 136.0
    # XIX.
    elif index == 19:
        latV0   = 26.0
        longiV0 = 154.0

    return latV0, longiV0

# ---------------------------------------------.
# 緯度経度を平面直角座標に変換.
# @param[in] latV        緯度 (10進数の度数指定).
# @param[in] longiV      経度 (10進数の度数指定).
# @param[in] originIndex 平面直角座標系の原点の番号.
#                         https://www.gsi.go.jp/LAW/heimencho.html
# @return x, y (m単位)
# ---------------------------------------------.
def calcLatLongToHeimenChokaku (latV : float, longiV : float, originIndex : int = 9):
    # 赤道半径 (km) = 楕円体の長半径.
    R = 6378.137

    # 極半径 (km).
    R2 = 6356.752

    # 逆扁平率.
    F = 298.257222101

    # 平面直角座標系のX軸上における縮尺係数.
    m0 = 0.9999

    # 平面直角座標系の原点の緯度と経度.
    # https://www.gsi.go.jp/LAW/heimencho.html
    # 地域によってこれは変わる。東京の場合はIX(9)番目のものを使用.
    latV0, longiV0 = getOriginLatAndLongi(originIndex)

    # 度数をラジアンに変換.
    lat0R   = latV0 * math.pi / 180.0
    longi0R = longiV0 * math.pi / 180.0
    latR    = latV * math.pi / 180.0
    longiR  = longiV * math.pi / 180.0

    n = 1.0 / (2.0 * F - 1.0)

    A0 = 1.0 + (n**2) / 4.0 + (n**4) / 64.0
    A1 = (-3.0 / 2.0) * (n - (n**3) / 8.0 - (n**5) / 64.0)
    A2 = (15.0 / 16.0) * ((n**2) - (n**4) / 4.0)
    A3 = (-35.0/ 48.0) * ((n**3) - (5.0 / 16.0) * (n**5))
    A4 = (315.0 / 512.0) * (n**4)
    A5 = (-693.0/1280.0) * (n**5)
    A_Array = [A0, A1, A2, A3 , A4, A5]

    a1 = (1.0 / 2.0) * n - (2.0 / 3.0) * (n**2) + (5.0 / 16.0) * (n**3) + (41.0 / 180.0) * (n**4) - (127.0 / 288.0) * (n**5)
    a2 = (13.0 / 48.0) * (n**2) - (3.0 / 5.0) * (n**3) + (557.0 / 1440.0) * (n**4) + (281.0 / 630.0) * (n**5)
    a3 = (61.0 / 240.0) * (n**3) - (103.0 / 140.0) * (n**4) + (15061.0 / 26880.0) * (n**5)
    a4 = (49561.0 / 161280.0) * (n**4) - (179.0 / 168.0) * (n**5)
    a5 = (34729.0 / 80640.0) * (n**5)
    a_Array = [0.0, a1, a2, a3, a4, a5]

    A_ = ((m0 * R) / (1.0 + n)) * A0

    v = 0.0
    for i in range(5):
        v += A_Array[i + 1] * math.sin(2.0 * (float)(i + 1) * lat0R)
    S_ = ((m0 * R) / (1.0 + n)) * (A0 * lat0R + v)

    lambdaC = math.cos(longiR - longi0R)
    lambdaS = math.sin(longiR - longi0R)

    t = math.sinh(math.atanh(math.sin(latR)) - ((2.0 * math.sqrt(n)) / (1.0 + n)) * math.atanh(((2.0 * math.sqrt(n)) / (1.0 + n)) * math.sin(latR)))
    t_ = math.sqrt(1.0 + t * t)

    xi2  = math.atan(t / lambdaC)
    eta2 = math.atanh(lambdaS / t_)

    v = 0.0
    for i in range(5):
        v += a_Array[i + 1] * math.sin(2.0 * (float)(i + 1) * xi2) * math.cosh(2.0 * (float)(i + 1) * eta2)
    x = A_ * (xi2 + v) - S_

    v = 0.0
    for i in range(5):
        v += a_Array[i + 1] * math.cos(2.0 * (float)(i + 1) * xi2) * math.sinh(2.0 * (float)(i + 1) * eta2)
    y = A_ * (eta2 + v)

    # kmからmに変換して返す.
    return (x * 1000.0), (y * 1000.0)

# ----------------------------------------------------------.

# 緯度経度から平面直角座標に変換（単位 m）.
originIndex = 9     # Tokyo.
x,y = calcLatLongToHeimenChokaku(in_lat, in_longi, originIndex)
print("Latitude  = " + str(in_lat))
print("Longitude = " + str(in_longi))
print("  X = " + str(x) + " (m)")
print("  Y = " + str(y) + " (m)")

# Omniverse(USD)のY-up/右手座標系/cmに変換.
x2 = y * 100.0
z2 = -x * 100.0
print("[ Omniverse ] (Y-up/right hand/cm)")
print("   x = " + str(x2) + " (cm)")
print("   z = " + str(z2) + " (cm)")

