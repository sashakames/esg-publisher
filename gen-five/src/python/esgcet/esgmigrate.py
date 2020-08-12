from ESGConfigParser import SectionParser


def run(args):
    DEFAULT_ESGINI = '/esg/config/esgcet'
    sp = SectionParser('config:cmip6')
    sp.parse(DEFAULT_ESGINI)



def main():

    args = {}

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    main()


