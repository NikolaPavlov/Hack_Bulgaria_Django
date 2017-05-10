import pdfkit

from celery import Celery


output_file = 'result.pdf'
app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def convert_site_to_pdf(website):
    return pdfkit.from_url(website, output_file)
