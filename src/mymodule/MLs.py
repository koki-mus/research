import numpy as np 
import os
import random 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report
import glob 
from mymodule import myfunc as mf
from dotenv import load_dotenv
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import LinearSVC 
import xgboost as xgb 
from sklearn.svm import SVC 
from sklearn.neighbors import KNeighborsClassifier 
load_dotenv()
root_dir = os.environ["root_dir"]

#selfついてるのとついてないのとでバグあるかも
#labelのcsvにリコネクションしてるかどうかを0,1で表す列がいる。
#その列がない場合にはあとJUDGE_COLUMNが使えなくなるので、列を作ってからMLに突っ込む
class ML:
    def __init__(self, ALTIMAGE0, ALTIMAGE1, LABEL_SOURCE, JUDGE_COLUMN, IMGSHAPE, DO_PCA = False, dilute = False) -> None:
        self.ALTIMAGES0 = root_dir + ALTIMAGE0
        self.ALTIMAGES1 = root_dir + +ALTIMAGE1
        self.LABEL_SOURCE = LABEL_SOURCE#
        self.JUDGE_CCOLUMN = JUDGE_COLUMN#is_reconnecting列(0,1)
        self.IMGSHAPE = IMGSHAPE#出来れば画像サイズはすべて同じで合ってほしい。違うサイズが混じる場合は最も多いサイズを指定すること
        self.DO_PCA = DO_PCA
        # def compress(array, LEVEL=1):
        #     return mf.convolute(array,mf.ave_carnel(LEVEL), stride = LEVEL)
        # temp = compress(mf.load())
        # IMGSHAPE = temp.shape
        labelcsvs = glob.glob(root_dir+LABEL_SOURCE)############
        columns = ["path",JUDGE_COLUMN]###############
        df = pd.DataFrame(columns=columns)
        for labelcsv in labelcsvs:
            dftmp = pd.read_csv(labelcsv, index_col=0)[columns]
            df = pd.concat([df,dftmp])
        self.PATH0 = list(df[df[JUDGE_COLUMN] == 0]["path"])
        self.PATH0 = list(map(lambda path : root_dir+path, self.PATH0))
        self.PATH1 = list(df[df[JUDGE_COLUMN] == 1]["path"])
        self.PATH1 = list(map(lambda path : root_dir+path, self.PATH1))
        self.split_testtrain()
        if dilute:
            self.dilute()
        self.load_data()
        self.exePCA()
    def size_dir(self, path):
        return len(glob.glob(path))
    def split_testtrain(self):#############別の方法も実装するかも
        self.PATH0TRAIN, self.PATH0TEST = train_test_split(self.PATH0, test_size=0.6, shuffle=True, stratify=self.Path0)
        self.PATH1TRAIN, self.PATH1TEST = train_test_split(self.PATH1, test_size=0.6, shuffle=True, stratify=self.Path1)
    def dilute(self):
        #ランダムな領域の切り取りを行う関数
        def random_crop(imagearay, size=0.8):
            height, width, _ = imagearay.shape
            crop_size = int(min(height, width) * size)

            top = np.random.randint(0, height - crop_size)
            left = np.random.randint(0, width - crop_size)
            bottom = top + crop_size
            right = left + crop_size
            imagearay = imagearay[top:bottom, left:right,:]
            #motonosaizunimoosu
            return imagearay
        def altarray_save(item, temp_output_dir):
            img = mf.load(item, z=3)
            file_name = os.path.basename(item)
            img_flip = np.flipud(img) # 画像の上下反転
            np.save(temp_output_dir + "flip_" + file_name , img_flip) # 画像保存
            img_mirror = np.fliplr(img) # 画像の左右反転
            np.save(temp_output_dir + "mirr_" + file_name , img_mirror) # 画像保存
            img_T = img.T # 画像の上下左右反転
            np.save(temp_output_dir + "trns_" + file_name , img_T) # 画像保存
            # img_crop = random_crop(img) # 画像の切り取り
            # img_crop = img_crop.resize((256, 256)) # 元のサイズに戻す
            # img_crop.save(temp_output_dir + file_name + "_crop.png") # 画像保存
        
        #リコネクションがない画像ファイルのパスのリストを取得
        files = self.PATH0TRAIN
        #出力ディレクトリのパス
        temp_output_dir = self.ALTIMAGES0
        for item in files:
            altarray_save(item,temp_output_dir)
        #リコネクションがある画像ファイルのパスのリストを取得
        files = self.PATH1TRAIN
        #出力ディレクトリのパス
        temp_output_dir = self.ALTIMAGES1
        for item in files:
            altarray_save(item,temp_output_dir)
    def load_data(self):
        # 訓練データ
        self.ALLTARINDATA0 = glob.glob(self.ALTIMAGES0+"*") + self.PATH0TRAIN
        self.ALLTARINDATA1 = glob.glob(self.ALTIMAGES1+"*") + self.PATH1TRAIN
        num_of_data_clear = len(self.ALLTARINDATA0) # リコネクションがない画像の枚数
        num_of_data_cloudy = len(self.ALLTARINDATA1) # リコネクションがある画像の枚数
        num_of_data_total = num_of_data_clear + num_of_data_cloudy # 学習データの全枚数

        N_col = self.IMGSHAPE[0]*self.IMGSHAPE[1]*1 # 行列の列数
        self.X_train = np.zeros((num_of_data_total, N_col)) # 学習データ格納のためゼロ行列生成
        self.y_train = np.zeros((num_of_data_total)) # 学習データに対するラベルを格納するためのゼロ行列生成
        self.path_train = list("" for i in range(num_of_data_total)) # 学習データに対するpathを格納するためのゼロ行列生成

        # リコネクションがない画像を行列に読み込む
        path_list = self.ALLTARINDATA0
        i_count = 0

        def load_regularize(item):#自動でやらない
            type = item[-4:]
            # print(item)
            if type == ".npy":
                im = np.load(item)
            elif type == ".npz":
                print("npz doesnot supported")
                return
            elif type == ".jpg":
                im = Image.open(item).convert('L')
                im =im.resize(self.IMGSHAPE) # 画像のサイズ変更
                im = np.ravel(np.array(im)) # 画像を配列に変換
                # im = im_array/255. # 正規化 
            else:
                im = mf.load(item, z=3)
            # img_resize = compress(im)
            img_resize = mf.resize(im, self.IMGSHAPE)
            return ((img_resize - min(img_resize.flat)) / max(img_resize.flat)).flat # 正規化

        for item in path_list:
            self.X_train[i_count,:] = load_regularize(item)
            self.y_train[i_count] = 0 # リコネクションがないことを表すラベル
            self.path_train[i_count] = item
            i_count += 1

        # リコネクションがある画像を行列に読み込む
        path_list = self.ALLTARINDATA1

        for item in path_list:
            self.X_train[i_count,:] = load_regularize(item)
            self.y_train[i_count] = 1 # リコネクションがあることを表すラベル
            self.path_train[i_count] = item
            i_count += 1
        

        # テストデータ
        num_of_data_clear = len(self.PATH0TEST) # リコネクションがない画像の枚数
        num_of_data_cloudy = len(self.PATH1TEST) # リコネクションがある画像の枚数
        num_of_data_total = num_of_data_clear + num_of_data_cloudy # テストデータの全枚数
        
        N_col = self.IMGSHAPE[0]*self.IMGSHAPE[1]*1 # 行列の列数(RGBなら*3)
        self.X_test = np.zeros((num_of_data_total, N_col)) # テストデータ格納のためゼロ行列生成
        self.y_test = np.zeros(num_of_data_total) # テストデータに対するラベルを格納するためのゼロ行列生成
        self.path_test = list("" for i in range(num_of_data_total)) # テストデータに対するpathを格納するためのゼロ行列生成
        
        # リコネクションがない画像を行列に読み込む
        path_list = self.PATH0TEST 
        i_count = 0
        for item in path_list:
        
            self.X_test[i_count,:] = load_regularize(item)
            self.y_test[i_count] = 0 # リコネクションがないことを表すラベル
            self.path_test[i_count] = item
            i_count += 1
        
        # リコネクションがある画像を行列に読み込む
        path_list = self.PATH1TEST
        
        for item in path_list:
            self.X_test[i_count,:] = load_regularize(item)
            self.y_test[i_count] = 1 # リコネクションがあることを表すラベル
            self.path_test[i_count] = item
            i_count += 1 
    def exePCA(self):
        if self.DO_PCA:
            N_dim =  100 #100列に落とし込む

            pca = PCA(n_components=N_dim, random_state=0)

            self.X_train_pca = pca.fit_transform(self.X_train)
            self.X_test_pca = pca.transform(self.X_test)

            print('累積寄与率: {0}'.format(sum(pca.explained_variance_ratio_)))
        else:
            self.X_train_pca = self.X_train
            self.X_test_pca = self.X_test
            print("PCA 非実施")
    
##################################

    def linearSVC(self):
        model = LinearSVC(C=0.3, random_state=0) # インスタンスを生成
        model.fit(self.X_train_pca, self.y_train) # モデルの学習
        # 学習データに対する精度
        print("Train :", model.score(self.X_train_pca,  self.y_train)) 
        # テストデータに対する精度
        print("Test :", model.score(self.X_test_pca, self.y_test)) 
        print(model.predict(self.X_test))
        pred = model.predict(self.X_test)
        # svmres = pd.DataFrame(np.array([self.path_test, self.y_test, model.predict(X_test_pca)]).T, columns=["path", "y", "predict"])
        svmres = pd.DataFrame(np.array([self.path_test, self.y_test, pred]).T, columns=["path", "y", "predict"])###################
        print(classification_report(self.y_test, pred))
        return model
    def kneighbors(self):
        n_neighbors = int(np.sqrt(6000))  # kの設定
        model = KNeighborsClassifier(n_neighbors = n_neighbors)  
        model.fit(self.X_train_pca, self.y_train) # モデルの学習
        # 精度
        print("Train :", model.score(self.X_train_pca, self.y_train))
        print("Test :", model.score(self.X_test_pca, self.y_test))
        return model
    def rbfSVC(self):
        model = SVC(C=0.3, kernel='rbf', random_state=0) # インスタンスを生成 
        model.fit(self.X_train_pca, self.y_train) # モデルの学習
        # 精度
        print("Train :", model.score(self.X_train_pca,  self.y_train))
        print("Test :", model.score(self.X_test_pca, self.y_test))
        return model
    def XGBoost(self):
        model = xgb.XGBClassifier(n_estimators=80, max_depth=4, gamma=3) # インスタンスの生成
        model.fit(self.X_train_pca, self.y_train) # モデルの学習
        # 精度
        print("Train :", model.score(self.X_train_pca,  self.y_train))
        print("Test :", model.score(self.X_test_pca, self.y_test))
        return model

