import pandas as pd

album_df = pd.read_excel("./album.xlsx")
photo_df = pd.read_excel("./photo.xlsx")
# photo_df = pd.read_excel("./photo.xlsx")
album_define_df = pd.read_excel("./album_define.xlsx")
# 稀有度對應權重
rarity_to_weight = {1: 1000, 2: 500, 3: 250}
errorCount = 0
for index_define, row_define in album_define_df.iterrows():
    # 欲檢查相簿名稱
    album_name = row_define['album_name']
    # 定義開放章節
    ch_open = row_define['ch_open']
    # 定義成套獎勵
    reward_type = row_define['reward_type']
    reward_value = row_define['reward_value']
    # 定義白藍彩數量
    rarity_white = row_define['white']
    rarity_blue = row_define['blue']
    rarity_rainbow = row_define['rainbow']
    # 定義 mask (name 包含 album_name)
    album_name_mask = album_df[album_df["name"].str.contains(album_name, na=False)]
    # 檢查 album_name 是否存在表中 by df長度
    if len(album_name_mask.index) != 1:
        print(f"{album_name} 重複或不存在")
    else:
        # 用相簿名稱取得 ID
        album_df_id = round(album_name_mask.iat[0, 0])
        album_df_name = album_name_mask.iat[0, 2]
        # 檢查 album 表開放章節
        album_ch_check = round(album_name_mask.iat[0, 6])
        if album_ch_check != ch_open:
            print(f"album {album_df_name} chapter_id 錯誤，表格資料 = {album_name_mask.iat[0, 6]}")
        # 檢查 album order 2023/8/16 改不顯示序號
        # album_order_by_name = album_df_name.split(".")[0]
        # if int(album_order_by_name) != round(album_name_mask.iat[0, 1]):
        #     print(f"album {album_df_name} order 錯誤，表格資料 = {album_name_mask.iat[0, 1]}")
        # 檢查成套獎勵
        if reward_type != album_name_mask.iat[0, 3]:
            print(f"album {album_df_name} reward_type 錯誤，表格資料 = {album_name_mask.iat[0, 3]}")
        if int(reward_value) != round(album_name_mask.iat[0, 5]):
            print(f"album {album_df_name} reward_value 錯誤，表格資料 = {album_name_mask.iat[0, 5]}")
        # photo 表資料 by album_df_id
        photo_by_album_df_id = photo_df[photo_df['album_id'] == album_df_id]
        # 檢查 photo 表是否存在對應相片
        if len(photo_by_album_df_id.index) == 0:
            print("{} 相片不存在".format(album_name))
        else:
            for index, row in photo_by_album_df_id.iterrows():
                # 比對權重是否符合稀有度
                if int(row["rarity"]) not in rarity_to_weight:
                    print(f"photo {row['id']} {row['name']} rarity or weight 錯誤，"
                          f"表格資料 rarity = {row['rarity']}, weight = {row['weight']}")
                else:
                    if int(row["weight"]) != rarity_to_weight[int(row["rarity"])]:
                        print(f"photo {row['id']} {row['name']} rarity or weight 錯誤，"
                              f"表格資料 rarity = {row['rarity']}, weight = {row['weight']}")
                # 比對開放章節
                if int(row["chapter_id"]) != ch_open:
                    print(f"photo {row['id']} {row['name']} chapter_id 錯誤，表格資料 = {row['chapter_id']}")
            # 檢查白藍彩數量
            count_by_rarity = photo_by_album_df_id.groupby('rarity')['id'].nunique()

            # photo 表沒有任一稀有度須補0
            while len(count_by_rarity) < 3:
                if 1 not in count_by_rarity:
                    count_by_rarity[1] = 0
                elif 2 not in count_by_rarity:
                    # insertZero = pd.Series([0], index=[2])
                    # count_by_rarity = pd.concat([count_by_rarity, insertZero])
                    count_by_rarity[2] = 0
                elif 3 not in count_by_rarity:
                    count_by_rarity[3] = 0
                # print(count_by_rarity)

            # print(count_by_rarity[3])
            if count_by_rarity[1] != int(rarity_white):
                print(f"photo {album_df_name} 白卡數量 錯誤，表格資料 = {count_by_rarity[1]} 張")
            if count_by_rarity[2] != int(rarity_blue):
                print(f"photo {album_df_name} 藍卡數量 錯誤，表格資料 = {count_by_rarity[2]} 張")
            if count_by_rarity[3] != int(rarity_rainbow):
                print(f"photo {album_df_name} 彩卡數量 錯誤，表格資料 = {count_by_rarity[3]} 張")
