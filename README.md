# Kaggle-CLI
An unofficial Kaggle command line tool.

## Installation
```
$ pip install kaggle-cli
```

## Usage
Please note that accepting the competition rules before your commands.


### Submit
To submit an entry.

```
$ kg submit `entry` -u `username` -p `password` -c `competition` -m `message`
```

### Download
To download the data files.

```
$ kg download -u `username` -p `password` -c `competition`
```

To download a specific data file.

```
$ kg download -u `username` -p `password` -c `competition` -f `train.zip`
```

### Dataset

To download a dataset.

```
$ kg download -u `username` -p `password` -o `owner` -d `dataset`
```

### Config
To set global config.

```
$ kg config -g -u `username` -p `password` -c `competition`
```

or local config:

```
$ kg config -u `username` -p `password` -c `competition`
```

Show working config:

```
$ kg config
```

## Example
```
$ kg submit sampleSubmission.csv -c titanic-gettingStarted -u USERNAME -p PASSWORD -m "Enter a brief description of this submission here."
```

or

```
$ kg config -c titanic-gettingStarted -u USERNAME -p PASSWORD
$ kg submit sampleSubmission.csv -m "Enter a brief description of this submission here."
```
