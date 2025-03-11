# 相片獎勵比對

> 比對相簿表單與相片表單獎勵是否與企劃定義文件有出入

## 關聯文件

+ photo.xlsx (相片表)
+ album.xlsx (相簿表)
+ album_define.xlsx (企劃定義獎勵表)

## 套件

```
pip install pandas
pip install openpyxl (Excel 相依性套件)
```

## 流程

1. 讀取 album_define, photo, album
2. 以 album_define 為基準
   1. 檢查相簿使否存在
   1. 檢查 album 表開放章節
   2. 檢查 album 表成套獎勵
   3. 檢查 photo 表是否存在對應相片
   4. 比對 photo 表權重是否符合稀有度
   5. 比對 photo 表開放章節
   6. 檢查 photo 表各稀有度卡片數量
