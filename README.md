# 環境変数の準備
はじめに ".env" というファイルを作り

bigendian_data={データの絶対パス}

imgout={データの出力先絶対パス}

root_dir={pythonプログラムのルートにしたいパス}

snaps_dir={スナップショットのパス}

## 例)

imgout=C:/research/imgout/

bigendian_data=C:/research/bigendian_data/

root_dir=C:/research/

snaps_dir=C:/research/Snapshots/

を記述して下さい


./research/snap や /dataに変換前のデータ入れてますが、githubには重いのでアップしてません

# ディレクトリ構造
research/

    ├cln/  c言語のツール
    ├data/  元データ
    ├imgout/  画像の出力先
    ├snap/  元データと分解後のデータ
    |   ├density/
    |   |     ├00/
    |   |     ├01/
    .   .     .
    .   .     .
    |   |     └14/
    |   ├enstrophy/
    |   |     ├00/
    |   |     ├01/
    .   .     .
    .   .     .
    |   |     └14/
    |   ├magfieldx/
    .   .
    .   .
    |   └velocityz
    ├src/  ipynbやモジュール
    ├.env 環境変数のファイル
    ├README.md
    ├.gitignore
    └.git