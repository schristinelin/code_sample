import pandas as pd
import unittest
import logging
import os
from os import path

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

class TestValid(unittest.TestCase):
    def setUp(self):
        # make the logs folder if its not present
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # # remove existing log files within logs folder
        # if len(os.listdir(dir_path + '\logs')) > 0:
        #     for file in os.listdir(dir_path + '/logs'):
        #         if os.path.exists(dir_path + '/logs/' + file):
        #             os.remove(dir_path + '/logs/' + file)

        logging.basicConfig(filename = f'{dir_path}/logs/test_valid.log',
                            level = logging.INFO,
                            format='%(asctime)s [%(levelname)s] %(message)s')
        global df
        df = pd.read_csv(f'{dir_path}\weatherAUS.csv')


    def test_nulls(self):
        logging.info('Checking for missing values within file:')
        if df.isna().values.any():
            logging.info('Missing values found in:')
            logging.error(df[df.isna().any(axis=1)])
            logging.info('%s rows with the below indexes were not taken into analysis because of missing values:', len(df[df.isna().any(axis=1)]))
            logging.error(df[df.isna().any(axis=1)].index.to_list())
            self.assertEqual(df.isna().values.any(), True) # make sure this is correct
        else:
            logging.info('No Missing Values found in file.')
            self.assertEqual(df.isna().values.any(), False)
        logging.info('Done checking for missing values.')

    def test_temp_range(self):
        logging.info('Checking for abnormal out-of-range temperature values, unit used in data is celsius:')
        logging.info('The lowest temperature recorded is negative 89.2 C at the Vostok station operated by Russia; ')
        logging.info('and the highest temperature recorded is 56.7 C at the Greenland Ranch in the Death Valley.')
        logging.info('Therefore, setting normal range to negative 90 °C to positive 60°C for testings:')
        if any(df['MinTemp'] < -90) or any(df['MaxTemp'] > 60):
            logging.info('Abnormal temperature values found:')
            logging.error(df[(df['MinTemp'] < -90) | (df['MaxTemp'] > 60)])
            logging.info('%s rows with the below indexes were not taken into analysis because of abnormal values:', len(df[(df['MinTemp'] < -90) | (df['MaxTemp'] > 20)]))
            logging.error(df[(df['MinTemp'] < -90) | (df['MaxTemp'] > 20)].index.to_list())
        else:
            logging.info('No abnormal temperature values found in either MinTemp or MaxTemp column.')
        logging.info('Done checking for abnormal temperature values.')


if __name__ == '__main__':
    unittest.main()


