P2Proxy
===============
規制うぜーと思って P2 使ってたんですが、
一部の Mac 用 2ch クライアントで P2 経由での書き込みができない場合があったのでとりあえずの対策として実装しました。  

正直いってバグだらけだったり未実装だらけだったりしますがとりあえず書き込めます。  
BathyScaphe で書き込んでみたら 「ＥＲＲＯＲ：アクセス規制中です！！」と表示されますが書き込めてますのでスレをリロードしてみてください。

注意
---
BBSPINK などは P2 経由でも書き込めないので諦めてください。  

あとエラー処理など無視してますので全然書き込めないときは現状どうしようもないです。  
そのうち改善していきたいと思っています。

環境
---
Mac 用です。  
Linux や BSDな どをお使いの方でも使えるとは思いますが設定などは自力でなんとかしてください。

必要なもの
--------

+ Python 2.7.4  
2.7.x ならなんでもいいかもしれませんが未確認

使い方
-----

### なにはともあれ
> pip install < requirement.txt  
> python p2proxy.py

### Mac (MountainLion) の設定
1. システム環境設定 > ネットワーク > お使いのネットワークを選択 > 詳細 > プロキシ
2. Web プロキシ（HTTP）にチェック
3. Web プロキシサーバに「127.0.0.1」:「8081」を入力
4. プロキシ設定を使用しないホストとドメイン に「p2.2ch.net」を追加
5. OK の後、適用

4 については safari 6.x のバグの存在ゆえに設定しなければならないところです。  
そのうち直ってくれるといいですね。。。

