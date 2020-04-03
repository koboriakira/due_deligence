# README

気にしている株の理論株価などを分析して、現状の株価と比較します。  
具体的には、EDINETで公開されている有価証券報告書を取得し、必要な項目を取り出して計算しています。

## 使い方

DockerfileをもとにDockerイメージを作成したあと、次のコマンドを実行してください。

```
docker run -it --rm -v $(pwd)/due_deligence:/work --name due_deligence due_deligence_image python /work/script.py
```

### より詳しい使い方

実行時の引数として、次のように指定することができます。

```
# python /work/script.py 検索開始日 検索終了日 企業コード
python /work/script.py 2020-01-01 2020-03-31 9201
```

また取り込む有価証券報告書の対象企業コードは、 `config.py` で指定します。
