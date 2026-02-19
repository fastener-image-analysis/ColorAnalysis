import streamlit as st
from analysis_core import analyze_image_core

st.set_page_config(page_title='Fastener Color Analysis', layout='wide')

st.title('Fastener Color Analysis')

uploaded = st.file_uploader('Upload an Image', type=['jpg', 'jpeg', 'png'])

if uploaded:
    st.image(uploaded, caption='Uploaded Image', use_column_width=True)
    if st.button('Run Analysis'):
        with st.spinner('Analyzing Image...'):
            df, fig, annotated_buf = analyze_image_core(
                image_input = uploaded,
                output_dir = None,
                return_fig = True
            )
        st.subheader('Processing Visualization')
        st.pyplot(fig)
        st.subheader('Per-Part Metrics')
        st.dataframe(df)
        st.download_button(
            'Download Metrics CSV',
            df.to_csv(index=False).encode(),
            'metrics.csv',
            'text/csv'
        )

        st.download_button(
            'Download Visualization',
            annotated_buf,
            'visualization.jpg',
            'image/jpeg'
        )
