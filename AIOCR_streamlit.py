import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import streamlit as st
from AIOCR_detect import AiocrDetect
st.title('OCRアプリ')

aiocr = AiocrDetect(st.secrets["subscription_key"], st.secrets["endpoint"])

st.sidebar.markdown("# 画像アップロード")
uploaded_file = st.sidebar.file_uploader(
    'Choose an image...', type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:   # ファイルアップロード後に動く
    st.sidebar.markdown("# 解析実行")
    btn = st.sidebar.button('Press here to send image')
    my_bar = st.sidebar.progress(0)
    img = Image.open(uploaded_file)
    img_path = os.path.join('img', uploaded_file.name)
    img.save(img_path)
    st_image = st.image(img, use_column_width=True)
    if btn:
        my_bar.progress(10)
        # AIOCR実行
        operation_id = aiocr.send_ocr_request(img_path)
        my_bar.progress(40)
        read_result = aiocr.wait_response(operation_id, 3)
        my_bar.progress(80)
        text_result = aiocr.get_ocr_results(read_result)

        # 描画
        draw = ImageDraw.Draw(img)
        for idx, line in enumerate(text_result.lines, start=1):
            result_text = line.text
            result_bb1 = line.bounding_box[0], line.bounding_box[1]
            result_bb2 = line.bounding_box[2], line.bounding_box[3]
            result_bb3 = line.bounding_box[4], line.bounding_box[5]
            result_bb4 = line.bounding_box[6], line.bounding_box[7]
            draw.polygon([result_bb1, result_bb2, result_bb3,
                        result_bb4], fill=None, outline='green')

            font = ImageFont.truetype(
                font='./resources/NotoSansJP-Regular.otf', size=20)
            text_w, text_h = draw.textsize(str(idx), font=font)
            result_textbox = line.bounding_box[0], line.bounding_box[1], line.bounding_box[0] + \
                text_w, line.bounding_box[1]+text_h
            draw.rectangle(result_textbox, fill='green')
            draw.text(result_bb1, str(idx), fill='white', font=font)

        # 画面イメージをOCR結果に上書き
        st_image.image(img)
        st.markdown('**認識された文字列**')
        for idx, line in enumerate(text_result.lines, start=1):
            st.markdown(f'{idx}. {line.text}')

        my_bar.progress(100)
