# -*- coding: utf-8 -*-
"""
Created on 2016/12/9 9:59

@version: python3.5
@author: qiding
"""

import os
import pandas as pd
import datetime

from log import my_log
import my_path


def get_account_path_mapping(intraday_record_path_root):
    file_list = os.listdir(intraday_record_path_root)
    file_acc_list = [path_ for path_ in file_list if path_.startswith('NO')]
    acc_list = [file_[2:] for file_ in file_acc_list]

    path_acc_list = [intraday_record_path_root+file_+'\\' for file_ in file_acc_list]

    mapping_dict = dict(zip(acc_list, path_acc_list))
    my_log.info('mapping dict: '+str(mapping_dict))
    return mapping_dict


def get_account_record(this_account, this_account_path):
    assert isinstance(this_account, str)
    file_path = this_account_path + this_account + 't0report.csv'
    my_log.info('get account data: {}'.format(str(this_account)))
    data = pd.read_csv(
        file_path,
        date_parser=lambda x: datetime.datetime.strptime(x.replace('/', '-'), '%Y-%m-%d'),
        parse_dates=['date']
    )
    data['trade_amount'] = data['total_earning'] / data['ret(d_trade_amt)']
    data_ = data.set_index('date')
    return data_


def main():
    intraday_ret_output_path = my_path.output_path_root + 'IntradayAccountSummary\\'
    # read data
    my_log.info('read data begin')
    account_path_mapping_dict = get_account_path_mapping(my_path.intraday_record_path_root)
    account_record_all = pd.DataFrame(pd.concat(
        list(map(get_account_record, account_path_mapping_dict.keys(), account_path_mapping_dict.values())),
        keys=account_path_mapping_dict.keys(),
        axis=1
    ))
    account_record_all.columns.names = ['account', 'stat_name']
    my_log.info('read data end')

    # aggregate data
    my_log.info('agg data begin')
    account_sum = account_record_all.sum(level='stat_name', axis=1)

    account_sum_w = account_sum.resample('1W', label='left', closed='left', loffset=datetime.timedelta(1)).mean()
    account_sum_m = account_sum.resample('1M', label='left', closed='left', loffset=datetime.timedelta(1)).mean()

    ret_d_pool_w = account_sum_w['total_earning'] / account_sum_w['pool_size'] * 252
    ret_d_trade_w = account_sum_w['total_earning'] / account_sum_w['trade_amount'] * 252
    ret_d_pool_m = account_sum_m['total_earning'] / account_sum_m['pool_size'] * 252
    ret_d_trade_m = account_sum_m['total_earning'] / account_sum_m['trade_amount'] * 252

    monthly_data = pd.concat(
        [ret_d_pool_m, ret_d_trade_m],
        keys=['ret_d_pool_ann_monthly', 'ret_d_trade_ann_monthly'],
        axis=1
    )
    weekly_data = pd.concat(
        [ret_d_pool_w, ret_d_trade_w],
        keys=['ret_d_pool_ann_weekly', 'ret_d_trade_ann_weekly'],
        axis=1
    )
    my_log.info('agg data end')

    # output data
    my_log.info('output data:\n{}\n{}\n{}'.format(
        intraday_ret_output_path + 'intraday_ret_monthly.csv',
        intraday_ret_output_path + 'intraday_ret_weekly.csv',
        intraday_ret_output_path + 'account_summuary_daily_details.csv'
    ))
    monthly_data.to_csv(intraday_ret_output_path + 'intraday_ret_monthly.csv')
    weekly_data.to_csv(intraday_ret_output_path + 'intraday_ret_weekly.csv')
    account_sum.to_csv(intraday_ret_output_path + 'account_summuary_daily_details.csv')

if __name__ == '__main__':
    main()

