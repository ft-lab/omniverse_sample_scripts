# kit-app-template

Omniverse Kitを使用したアプリを開発するには"kit-app-template"を使用します。  
Omniverseの開発向けのすべての入り口はこのローカルへのリポジトリのコピー(git clone)とビルドから始まります。  

https://github.com/NVIDIA-Omniverse/kit-app-template

## kit-app-templateを動かすのに必要な環境

* OS: Windows 11 または Ubuntu 22.04以降。
* RTXが動作するGPU
* コマンドラインで[git](https://git-scm.com/)を使えるようにする必要があります。

Windowsの場合はPowerShell、Ubuntuの場合はTerminalを使用しました。  


## ローカルにkit-app-templateをダウンロード (git clone)

```shell
git clone https://github.com/NVIDIA-Omniverse/kit-app-template.git
```

## テンプレートの作成

ここで、アプリケーションとして構築するための情報を指定します。  

Windows  
```shell
cd kit-app-template
.\repo.bat template new
```

Ubuntu  
```shell
cd kit-app-template
./repo.sh template new
```

これを実行した際に選択肢が何回か出てきますが、それらはkit-app-templateリポジトリの[README.md](https://github.com/NVIDIA-Omniverse/kit-app-template/blob/main/README.md)をご参照くださいませ。

ApplicationとしてUSD Exchange(Omniverse Kitの標準的な開発環境)をビルドするものとしました。  
なお、アプリケーション名は半角の小文字英字、アンダーバー、"."のみ使用できます。  

### 同じアプリ名で上書きしたい場合

新しいKitをGitHubリポジトリから取得して再度同じアプリ名でビルドを行いたい場合、
"source/extensions"から"[組織名].[アプリ名]_setup_extension"のディレクトリを削除してください。  

## ビルド

Windows  
```shell
.\repo.bat build
```

Ubuntu  
```shell
./repo.sh build
```

このビルドは時間がかかります。  

成功すると、"_build/windows-x86_64/release"(Linuxは"_build/linux-x86_64/release")に実行に必要な構成が出力されています。  

## 起動

Windows  
```shell  
.\repo.bat launch
```

Ubuntu  
```shell  
./repo.sh launch
```

これでUSD Composerが起動します。  
