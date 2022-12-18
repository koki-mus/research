# 環境変数の準備
はじめに "src/.env" というファイルを作り

imgout={画像の出力先絶対パス}

root_dir={.reserch/のパス}

snaps_dir={スナップショットのパス}

## 例)
root_dir=C:/research/
を記述して下さい


./research/snap や /dataに変換前のデータ入れてますが、githubには重いのでアップしてません

# データ入力補助
src/writer.py を実行しながら、imgout/ohnolic/viewer*.htmlを開く。pキーでwriter.pyにpostし、任意のファイルに黄色いボックスの情報を書き加える。
エラーはまだ中途、リコネクション、ｘ、Ｏ点の情報も加えるつもり。


htmlの作成は。./imgout/ohnolicで
../../src/makeviewer2.pyを実行

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