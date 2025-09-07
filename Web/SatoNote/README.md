# SatoNote

## 問題文
I had an LLM write this code, so there shouldn't be any vulnerabilities... 👈🤖✍️​​​​​​💻... 🧠➡️🗑️... 🚫🐛⁉️  
Can you outsmart the LLM and prove me wrong?  
**Note:** Please obtain the **flag locally** before trying it on the production environment.  
So find a the flag by exploring this service: `http://65.109.184.196:8000`  
Download the [**attachment!**](files/SatoNote_cabd1dbbbcb74be1ad37f7a59e47df63682a51a2.txz)  

## 難易度
**Hard**  

## 作問にあたって
短期間で高難易度の問題作成をお願いされたので、保管していたChromiumのバグ？仕様？を二つ使いました(報告済みでもある)。  

- Content-Security-Policyとして`base-uri 'none'`が設定されている場合でも、`<base href="[MY_SERVER]"><img src="/abcdef.png">`で`[MY_SERVER]/abcdef.png`にリクエストが飛んでしまう(Preload Scannerが原因？)  
- 既にHttpOnlyで存在しているCookieと同名のものが、`document.cookie = "=name=value";`とすることで重複して付与できてしまう(Nameless Cookie)  

どちらもFirefoxでは、脆弱性としてCVEが採番されています。  
コードは頭を使わずにLLMに書かせているので、非常に読み辛いと思っています🧠➡️🗑️。  
ちなみにsolver.pyもです。  

## 解法
Try Harder!  

## ASIS{Would_it_be_an_issue_if_I_use_a_0day_in_a_CTF?}