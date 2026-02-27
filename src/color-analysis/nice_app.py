from nicegui import ui
from io import BytesIO
import base64
import asyncio
import analysis_core
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

async def handle_upload(e):
    filename = e.file.name
    ui.notify(f'Processing image {filename}')

    img_bytes = BytesIO(e.file._path.read_bytes())

    df, fig, annotated_buf = analysis_core.analyze_image_core_single(
        image_input=img_bytes,
        output_dir=None,
        return_fig=True
    )

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')

    await asyncio.sleep(0)

    result_area.clear()
    with result_area:
        ui.table.from_pandas(df)
        ui.image(f'data:image/png;base64,{img_b64}').classes('max-w-full')

with ui.row():
    ui.upload(on_upload=handle_upload, auto_upload=True).classes('max-w-full')

result_area = ui.column()

ui.run(reload=False)