## 概要
Googleフォトのエクスポートしたファイルは撮影日時が画像のExifではなくJSONファイルにメタデータとして出力されているデータが多い  
それを一括でJSONファイルから `photoTakenTime` を読み取ってExifに埋め込むためのスクリプト  

変換結果は対象フォルダと同階層に `converted` として出力される

ちなみにエクスポートは以下から  
https://takeout.google.com/


## スクリプト

1. convert_all.py => 指定ディレクトリを再帰的にサブフォルダ含めて変換
2. convert.py => 指定フォルダのみを変換

## ex)

    python convert_all.py target/

|||
|---|---|
|第1引数|対象フォルダ|
