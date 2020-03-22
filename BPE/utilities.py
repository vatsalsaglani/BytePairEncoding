import pickle


def save_pickle(filepath, object):

    with open(filepath, 'wb') as fp:
        pickle.dump(object, fp)


def load_pickle(filepath):

    with open(filepath, 'rb') as fp:
        return pickle.load(fp)