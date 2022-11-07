# object_fit_images
## セットアップ
```
docker-compose build
```
# 利用方法
1. ディレクトリ`input`に対象の写真を入れたフォルダを設置
2. 全体画像はファイル名の頭に`whole`を入れる
3. 以下コマンドを実行
```
make run dir={対象のフォルダ名}
```