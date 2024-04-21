predict nutri score from image

参考
https://qiita.com/RyutoYoda/items/a51830dd75a2dac96d72

https://qiita.com/usaitoen/items/0184973e9de0ea9011ed


## Library
```
pip install -q -U google-generativeai
pip install pillow flask pandas
pip install mysql-connector-python
```

## Database
- mysqlをインストール
    - mac
        - https://qiita.com/fuwamaki/items/194c2a82bd6865f26045
    - ubuntu
        - https://qiita.com/houtarou/items/a44ce783d09201fc28f5
- sudo mysql -u root
- create database nutriscore;
- use nutriscore;
- source /...../create_table_id.sql
- source /...../create_table_record.sql

# RUN
- python app.py
