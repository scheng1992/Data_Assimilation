"""File to run elements of pipeline module from"""
from pipeline.settings.baseline import Baseline
from pipeline import TrainAE, ML_utils, GetData, SplitData
from pipeline.VarDA.batch_DA import BatchDA

import shutil

#global variables for DA and training:
EPOCHS = 1
ALL_DATA = False
SAVE = True

def main():

    settings = Baseline()
    #model = ML_utils.load_model_from_settings(settings)


    settings.BATCH_NORM = False
    settings.CHANGEOVER_DEFAULT = 0
    settings.REDUCED_SPACE = True
    settings.DEBUG = False
    settings.SHUFFLE_DATA = True #Set this =False for harder test and train set
    settings.FIELD_NAME = "Pressure"

    expdir = "experiments/train/baseline/test/"


    calc_DA_MAE = True
    num_epochs_cv = 0
    small_debug = True
    print_every = 1
    lr = 0.0001
    trainer = TrainAE(settings, expdir, calc_DA_MAE)
    expdir = trainer.expdir #get full path


    model = trainer.train(EPOCHS, learning_rate=lr, test_every=1, num_epochs_cv=num_epochs_cv,
                            print_every=print_every, small_debug=small_debug)



    #test loading
    model, settings = ML_utils.load_model_and_settings_from_dir(expdir)

    model.to(ML_utils.get_device()) #TODO

    settings.DEBUG = False
    x_fp = settings.get_X_fp(True) #force init X_FP

    #set control_states
    #Load data
    loader, splitter = GetData(), SplitData()
    X = loader.get_X(settings)

    train_X, test_X, u_c_std, X, mean, std = splitter.train_test_DA_split_maybe_normalize(X, settings)

    if ALL_DATA:
        control_states = X
    else:
        NUM_STATES = 5
        START = 100
        control_states = train_X[START:NUM_STATES + START]

    if SAVE:
        out_fp = expdir + "AE.csv"
    else:
        out_fp = None
    print(out_fp)

    batch_DA_AE = BatchDA(settings, control_states, csv_fp= out_fp, AEModel=model,
                        reconstruction=True, plot=False)

    res_AE = batch_DA_AE.run(print_every=10)
    print(res_AE)

    #Uncomment line below if you want to automatically delete expdir (useful during testing)
    if not SAVE:
        shutil.rmtree(expdir, ignore_errors=False, onerror=None)


if __name__ == "__main__":
    main()

