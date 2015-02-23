# Kaggle-CLI
An unofficial Kaggle command line tool.

## Installation
```
$ pip install kaggle-cli
```

## Usage


### Submit
To submit an entry.

```
$ kg submit `entry` -u `username` -p `password` -c `competition` -m `message`
```

### Download
To download the data files, accepting the competition rules before your command.

```
$ kg download -u `username` -p `password` -c `competition`
```

### Config
To set config.

```
$ kg config -u `username` -p `password` -c `competition`
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
