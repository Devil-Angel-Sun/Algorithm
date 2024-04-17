import os
import argparse

path,_ = os.path.split(os.path.abspath(__file__))
def main(args):
    if args.form=='offline':
        print("Start offline forecast!")
        #docker不支持后台
        #os.system("nohup uwsgi {0}/config.ini --wsgi-file {0}/src/offline/api.py --callable app --touch-reload {0}/src/offline/ >run.log 2>&1 &".format(path))
        os.system("uwsgi {0}/config.ini --wsgi-file {0}/src/offline/api.py --callable app --touch-reload {0}/src/offline/".format(path))
    elif args.form=='online':
        print("Start online forecast!")
        os.system("python {0}/src/online/predict.py".format(path))
    else:
        print("forecast params wrong!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--form",
                      help="Select forcast methods:offline or online",
                      default='offline',
                      choices = ['offline','online']
                      )
    args = parser.parse_args()
    main(args)
