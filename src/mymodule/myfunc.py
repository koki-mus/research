import py_compile
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import os
from dotenv import load_dotenv
load_dotenv()


imgout = os.environ["imgout"]
root_dir = os.environ["root_dir"]
snaps_dir = os.environ["snaps_dir"]


def gen_snap_path(target, para, job):
    return f"{snaps_dir}{target}/{'{0:02d}'.format(job)}/{target}.{'{0:02d}'.format(para)}.{'{0:02d}'.format(job)}"
#データのロード
def load(filename, z=1):
    """
    little endianのデータの読み込み。z=1でz方向が一層だけのデータを
    z=3でz方向が3のデータを1層だけ読み込む
    """
    f = open(filename,mode='rb')
    #:525825でz方向の1個目だけ(xy平面一つ)とる。reshapeでx,yの整形
    if z == 1:
        print(np.fromfile(f, dtype='f',sep='').shape)
        data = np.fromfile(f, dtype='f',sep='').reshape(1025,513)
    elif z == 3:
        data = np.fromfile(f, dtype='f',sep='')[:525825].reshape(1025,513)
    f.close()
    return data

def load_bigendian(filename):
    """
    fort.111.0等のビッグエンディアンのデータをリトルエンディアンに変換し、
    必要な部分を抜き取る。
    """
    f = open(filename,mode='rb')
    #>fはbig endianのfloat型。:525825でz方向の1個目だけ(xy平面一つ)とる。reshapeでx,yの整形
    data = np.fromfile(f, dtype='>f',sep='')[:525825].reshape(1025,513)
    f.close()
    return data
#ヒートマップの生成と保存
def show(data: np.array, imgname=False, bar_range=None):
    plt.clf()
    if bar_range == None:
        sns.heatmap(data)
    else:
        sns.heatmap(data, vmin=bar_range[0], vmax=bar_range[1])

    if imgname:
        plt.savefig(f"{imgname}")


#畳み込み
def convolute(data: np.array, carnel: np.array, padding=0, stride=1):
    """
    畳み込み演算。
    """
    
    if padding:
        print("0パディングの処理未実装  padding=0で実行します")
        padding = 0
    
    c_width = carnel.shape[1]
    c_height = carnel.shape[0]

    result_width = int((data.shape[1] + 2*padding - carnel.shape[1]) / stride + 1)
    result_height = int((data.shape[0] + 2*padding - carnel.shape[0]) / stride + 1)
    print("result   Y,X:",result_height,result_width)
    print("original Y,X:",data.shape)
    def loop_calc():
        def calc(array):

            result = sum(array*carnel)
            result = sum(result.flat)
            return result
        orgX = 0
        orgY = 0
        convoluted = np.zeros((result_height, result_width))

        for resultY in range(result_height):
            for resultX in range(result_width):
                array = data[orgY : orgY + c_height, orgX : orgX + c_width]
                # a = convoluted[resultY]
                convoluted[resultY][resultX] = calc(array)
                orgX += stride

            orgX = 0
            orgY += stride
        return convoluted

    return loop_calc()

def ave_carnel(size:int):
    """
    畳み込みにおける平滑化のカーネル作成
    """
    ones = np.ones((size,size))
    res = ones / (size**2)
    return res

#離散データの微分
def diff(x, h):
    """
    精度低めの普通の微分。誤差:h**2
    """
    res = x[2:] - x[:-2]
    print(x[1:])
    print(x[:-1])
    return res/(2*h)
def diff4(x, h):
    """
    精度高めの微分・。誤差:h**4
    1回微分{-f(x+2h)+8f(x+h)-8f(x-h)+f(x-2h)}/12h
    xは時系列データ,hはデータ間の時間(second)
    ベクトル長が4短くなる
    """
    res = -x[4:] + 8*x[3:-1] - 8*x[1:-3] + x[:-4]
    return res/(12*h)


def diff4_x(data: np.ndarray, h:float):
    """
    diff4を使った行列の横方向偏微分
    """
    res = np.ndarray([])
    for vecx in data:
        if res.shape == tuple():
            res = diff4(vecx, h)
        else:
            res = np.append(res,diff4(vecx, h))
    return res.reshape(data.shape[0],data.shape[1]-4)
def diff4_y(data: np.ndarray, h:float):
    """
    diff4を使った行列の縦方向偏微分
    """
    data = data.T
    res = np.ndarray([])
    for vecy in data:
        if res.shape == tuple():
            res = diff4(vecy, h)
        else:
            res = np.append(res,diff4(vecy, h))
    return res.reshape(data.shape[0],data.shape[1]-4).T
def rot2d(vX:np.ndarray,vY:np.ndarray):
    """
    vX,vYよりローテーションを出す。出力はz方向のベクトル
    y方向については、vZ(zx平面)、vX(zx平面)の順で入力、x方向はvY(yz平面)、vZ(yz平面)の順で入力すると得られる。
    x､y､zそれぞれの出力であるスカラーの行列に対して、
    それぞれの方向の単位ベクトルを掛けて足せば3次元のローテーションが求まる
    """
    return diff4_x(vY,1)[2:-2,] - diff4_y(vX,1)[:,2:-2]

"""
rot2dの結果に対して単位ベクトルを掛けるやり方。
a = np.array([[0,1,2,3],[0,4,5,6],[0,7,8,9]])
e = np.array([1,0,0])
mylist = [[j *e for j in i ] for i in a]
"""
from scipy import interpolate
def array_interpolation(data:np.array,newxy, kind ='cubic'):
    oldy, oldx = data.shape
    X,Y = np.meshgrid(oldx,oldy)
    f = interpolate.interp2d(X, Y, data, kind=kind)
    znew = f(newxy[0], newxy[1])
    return znew