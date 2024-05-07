## Go to `model` directory:
```cd model```

## Set credential:
```export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service/account```

## Launch the CLI on our trained model
```python launch.py --checkpoint dangvohiep/wikit5```

## If you want to further train the model yourself:

### Run:
```python train.py --from_checkpoint dangvohiep/wikit5 --config t5.yaml```

### Launch the CLI on your trained model:

After training, a checkpoint folder will be created as specified by 
`training/output_dir` in `model/configs/t5.yaml`. 

You can pass your new checkpoint in the following command to launch a new chat instance on top of your model:

```python launch.py --checkpoint <your-new-checkpoint>```

