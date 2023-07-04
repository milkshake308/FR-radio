from datetime import datetime
def log(*argv):
    datestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f")
    print(datestamp,*argv ,sep='\t')

