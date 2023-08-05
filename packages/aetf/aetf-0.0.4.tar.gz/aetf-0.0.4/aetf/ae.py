from markdown import markdown

#import packages
import tensorflow as tf
import pandas as pd
import numpy as np

class TheJoker(object):
    def joke(self):
        """doc for joke, lulz"""
        return "HAHA!"
joker = TheJoker()


class AutoEncoder(object):

    #initialize class variables
    def __init__(self):
        self._fit_min = 0
        self._fit_max = 0

    #remove constant columns
    def remove_const_cols(self, df):
        if not isinstance(df, pd.core.frame.DataFrame):
            raise TypeError("Argument should be a pandas DataFrame.")
        else:
            return df.loc[:,df.var()!=0]


    #parameters testing
    def get_kernel(self, kernel='rbf'):
        print kernel

    #encode the input
    def encode(self, X, activate = "sigmoid", hidden_layers = 1, hidden_units = [50]):
        """
        encode the data

        Parameters
        ----------
        input : A tensor
            The input tensor to encode. Must be compatible with TensorFlow

        activate : str, ["sigmoid","tanh"] , default: 'sigmoid'
            Specifies which activation function to used

        hidden_layers : int, default : 1
            Number of hidden layers in the network

        hidden_units : list with int elements, default : [50]
            Number of hidden units per layer


        Attributes
        ----------

        Returns
        -------
        code : A tensor
            Output of the encoding network a.k.a. the 'code'


        """

        if len(hidden_units) != hidden_layers:
            raise ValueError("Lenght mismatch: Hidden units should be provided per layer. Check your parameters: hidden_layers and hidden_units")
        if all(isinstance(item, int) for item in hidden_units):
            raise TypeError("The hidden units sizes are not of type %s" %int)
        




    #import aetf; print(aetf.import_data.__doc__)
    #import aetf; df = aetf.import_data("/home/nilesh/enc_lab.xlsx")
    def import_data(self,url):
        """
        imports the csv file from the location url
        parameters:
            url:: str :: the location of the file to be imported
        returns:
            pandas.DataFrame object
        #("lab_test_gauss_ldc_MG_CKD.csv")
        """
        if not url.endswith('.csv'):
            raise TypeError('Please enter a valid ".csv" file')
        else:
            df = pd.read_csv(url)
        return df

    def get_ae_data(self, df):
        """
        return the array in numpy.array format; [n_samples, n_inputs]

        """
        #remove the encounter_id column from the DataFrame
        if not isinstance(df, pd.core.frame.DataFrame):
            raise TypeError("Argument should be a pandas DataFrame.")
        else:
            return df[df.columns.tolist()[1:]].as_matrix()#np.array(df[df.columns.tolist()[1:]])

    def corrupt_input(self, array):
        """
        corrupt the original input with randomness/noise
        """
        if not isinstance(array, (np.ndarray)):
            raise TypeError("Function argument is not of <type 'numpy.ndarray'>")
        else:
            noise = 0.31416*np.random.random_sample((array.shape)) + 0.137
            X_noisy = np.add(array, noise)
        return X_noisy

    def fit_unit_scale(self, array):
        array = np.array(array)
        self._fit_min = array.min(axis=0)
        self._fit_max = array.max(axis=0)
        #X_unit_scaled = np.subtract(np.divide( np.subtract(array, self._fit_min), np.subtract(self._fit_max, self._fit_min)),np.array(0.5)[np.newaxis,np.newaxis])
        return np.divide( np.subtract(array, self._fit_min), np.subtract(self._fit_max, self._fit_min))#np.subtract(np.divide( np.subtract(array, self._fit_min), np.subtract(self._fit_max, self._fit_min)),np.array(0.5)[np.newaxis,np.newaxis])
    def transform_unit_scale(self, array):
        array = np.array(array)
        #X_transformed = np.subtract(np.divide( np.subtract(array, self._fit_min), np.subtract(self._fit_max, self._fit_min)),np.array(0.5)[np.newaxis,np.newaxis])
        if not (array.shape == np.array(self._fit_min).shape):#<==wrong logic
            raise NotImplementedError("Please fit your data first! See aetf.AutoEncode.fit_unit_scale(self, np_array)")
        else:
            return np.subtract(np.divide( np.subtract(array, self._fit_min), np.subtract(self._fit_max, self._fit_min)),np.array(0.5)[np.newaxis,np.newaxis])


auto_encode = AutoEncoder()


"""

        try:
            if (np.array(self._mean_scale).all()!=0) and (np.array(self._var_scale).all()!=0) and array.shape == :
                return np.divide( np.subtract(array, self._mean_scale), self._var_scale)
            else:
                raise ValueError("Your mean and variance seems to be zero. Have you first tried to fit the unit scale?\nSee: fit_unit_scale(np_array)")
        except ValueError:
            raise ValueError("Dimensions mismatch: a numpy.ndarray is expected")
"""









def refs_used():
    """Return references used"""
    return ("""
    http://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference
    http://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference
    http://stackoverflow.com/questions/9696495/python-when-is-a-variable-passed-by-reference-and-when-by-value
    http://www.adp-gmbh.ch/php/pass_by_reference.html
    http://docs.scala-lang.org/tutorials/tour/case-classes.html
    https://jeffknupp.com/blog/2012/11/13/is-python-callbyvalue-or-callbyreference-neither/
    http://www.jesshamrick.com/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/
    https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/
    https://www.programiz.com/python-programming/class


    """)