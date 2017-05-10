import sys
# from convert_task import convert_site_to_pdf
from tasks import convert_site_to_pdf


if sys.argv[1] == 'download':
    website = sys.argv[2]
    output_str = 'PDF for {} will be generated. Check with this UUID: {}'
    pdf = convert_site_to_pdf.delay(website)
    print(output_str.format(website, pdf.id))

elif sys.argv[1] == 'check':
    pass

else:
    print('''Available commands:
             download [website] ---> download website as pdf
             check [uuid] ---> check if file with uuid is available in the system''')
