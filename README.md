# README

気にしている株の理論株価などを分析して、現状の株価と比較します。  
具体的には、EDINETで公開されている有価証券報告書を取得し、必要な項目を取り出して計算しています。

## 使い方

DockerfileをもとにDockerイメージを作成したあと、次のコマンドを実行してください。

```
docker run -it -v $(pwd)/due_deligence:/work --name due_deligence due_deligence_image
```

まず過去3年分のEDINETの情報を集めます。長くて1時間ほどかかります。

```
python script.py 3 2017-04-01 2020-03-31
```

上記の処理が終わったら、つぎに調査したい企業コードを指定することで調査結果を確認できます。
例は「9201 日本航空」です。

```
python script.py 2 9201
```

### より詳しい使い方

実行時の引数として、次のように指定することができます。

```
# python /work/script.py 検索開始日 検索終了日 企業コード
python /work/script.py 2020-01-01 2020-03-31 9201
```

また取り込む有価証券報告書の対象企業コードは、 `config.py` で指定します。

## その他

データベースのダンプ方法

```
# mysqldump -uroot -proot -h localhost -t db > mysqldump_all_data
# mysql -uroot -proot -h localhost db < mysqldump_all_data
```
