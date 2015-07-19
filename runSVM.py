from sklearn import svm
from optparse import OptionParser
from sklearn.datasets import fetch_mldata

def main():
    usage = '%prog [options]'
    parser = OptionParser(usage)
    parser.add_option("-C",type="float",default=0.01)
    parser.add_option("--degree",type="int",default=1)
    parser.add_option("--path",type="string",default=os.getcwd(),\
        help="path to experiment directory")
    (options, args) = parser.parse_args()
    run(C=options.C,degree=options.degree)

def run(C,degree):
    job = {"C":C,"degree":degree}
    data_set = fetch_mldata('yahoo-web-directory-topics')
    train_set = (data_set['data'][:1000],data_set['target'][:1000])
    validation_set = (data_set['data'][1000:],data_set['target'][1000:])
    learner = svm.SVC(kernel='poly',**job)
    learner.fit(*train_set)
    accuracy = learner.score(*validation_set)
    f = open('%s/results/Accuracy_C_%s_degree_%s.txt'%(codePath,str(job["C"]),\
                                                    str(job["degree"])),'w')
    f.write(str(accuracy))
    f.close()

if __name__=='__main__':
    main()
