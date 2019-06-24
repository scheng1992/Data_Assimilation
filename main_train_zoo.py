"""File to run elements of pipeline module from"""
from pipeline import config
from pipeline import TrainAE
from pipeline.AEs.CAE_configs import ARCHITECTURES as architectures

def main():
    activations = ["lrelu", "relu"]
    chann_sf = [1, 0.5] #scaling factors for final channel
    EPOCHS = 25
    expdir_base = "experiments/CAE_zoo/"
    exp_idx = 0 #experiment index (for logging)
    for archi in architectures:
        settings = archi()
        #use half latent dimension
        final_channel = settings.CHANNELS[-1]
        for activ in activations:
            settings.ACTIVATION = activ
            for sf in chann_sf:
                chan = int(final_channel * sf)
                if chan < 1:
                    chan = 1
                settings.CHANNELS[-1] = chan

                expdir = expdir_base + exp_idx
                trainer = TrainAE(settings, expdir)
                model = trainer.train(EPOCHS)
                exp_idx += 1



if __name__ == "__main__":
    main()