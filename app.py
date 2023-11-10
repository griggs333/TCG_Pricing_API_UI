import gradio as gr
import pandas as pd
import requests
import io
import os

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Upload Input CSV File")
            file_upload = gr.File(label='Input CSV Upload', type='binary')
            response_txt = gr.Text(visible=False)
            # sub_btn = gr.Button(value="Submit")
        with gr.Column():
            gr.Markdown("## Download Output CSV File")
            file_out = gr.File(label="Output CSV Download")

    with gr.Row():
        with gr.Column():
            gr.Markdown("## API Result")
            init_headers = ["TCGplayer Id","Product Line","Set Name","Product Name","Title","Number","Rarity","Condition","TCG Market Price","TCG Direct Low","TCG Low Price With Shipping","TCG Low Price","Total Quantity","Add to Quantity","TCG Marketplace Price","Photo URL","TCG Marketplace Price New","%diff","$diff"]
            col_types = ["number", "str", "str", "str", "str", "number", "str", "number", "number", "number", "number", "number", "number", "number", "number", "str", "number", "number", "number"]
            df_out = gr.Dataframe(type="pandas", interactive=False,  visible=True, headers=init_headers, datatype=col_types)


    def get_csv(csvFile):
        url = "https://lxgv3ow729.execute-api.us-east-1.amazonaws.com/TCG_Pricing"
        payload = csvFile
        headers = {
            'Content-Type': 'text/csv'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text

    def data_trans(csv_txt):
        df = pd.read_csv(io.StringIO(csv_txt))

        # File Write
        if os.path.exists("Archive/TCGcsv.csv"):
            os.remove("Archive/TCGcsv.csv")
        csvOut = df.to_csv('TCGcsv.csv', index=True)

        df2 = df.drop(columns=["Title", "Photo URL"])
        columns_to_dollars = ["TCG Market Price", "TCG Direct Low", "TCG Low Price With Shipping", "TCG Low Price", "TCG Marketplace Price", "TCG Marketplace Price New", "$diff"]
        for column in columns_to_dollars:
            df2[column] = df2[column].apply(lambda x: "${:.2f}".format(x))

        df2["%diff"] = df2["%diff"].apply(lambda x: "{:.2f}%".format(x))

        return df2, "TCGcsv.csv"

    file_upload.upload(get_csv, inputs=[file_upload], outputs=response_txt).then(data_trans, inputs=response_txt, outputs=[df_out, file_out])
    # sub_btn.click(get_csv, inputs=[file_upload], outputs=response_txt).then(data_trans, inputs=response_txt, outputs=df_out)
    # file_out.select()

    demo.launch()