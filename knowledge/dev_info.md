# Omniverseのスクリプトを追う手順

Omniverseのスクリプトでは大きく3つのアクセス先があるように思っています。      

* Pythonの既存モジュール (numpy/scipy/PILなど)
* USDへのアクセス
* Omniverseへのアクセス

## Pythonの既存モジュール

「Pythonの既存モジュール」は、一般的なPythonで追加できるモジュールです。      
Omniverseでは「[omni.kit.pip_archive](../pip_archive/readme.md)」のExtensionとしてまとまっています。     
これらは
```
import numpy

v1 = numpy.array([0.0, 1.0, 2.0])
v2 = numpy.array([1.2, 1.5, 2.3])

v3 = v1 + v2
print(v3)
```
のように一般的なPythonのプログラムと同じように使用できます。    


