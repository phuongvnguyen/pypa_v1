"""
This module is to clean the raw data
Authored: Phuong V. Nguyen
Dated: August 31th, 2021
"""
import sys
import os
import re
from pathlib import Path
import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import string
from string import punctuation
sys.path.insert(1, str(Path.home()))


def dob_cleaning(df, dob_col):
    """ Cleaning Date of Birth with format: 'DDMMYYY'
            - Remove DOB < 01/01/1945
            - Remove age < 10

        Args:
            df: DataFrame, containing PII data
            dob_col: DOB column

        Returns:
              df: The DataFrame with CustomerID and new DOB.
    """

    df = df[df[dob_col].notnull()]
    df[dob_col] = df[dob_col].apply(lambda x: x.strip())
    # df[dob_col] = df[dob_col].apply(lambda x: dt.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))  # convert str to date
    # df = df[df[dob_col] >= pd.to_datetime('1945-01-01')]  # remove dob < 01/01/1945
    # df = df[dt.date.today().year - df[dob_col].dt.year > 10]
    # df[dob_col] = df[dob_col].apply(lambda x: dt.datetime.strftime(x, '%d%m%Y'))
    df[dob_col] = df[dob_col].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d').strftime('%d%m%Y'))
    df = df[df[dob_col] >= '01011945']
    df = df[dt.date.today().year - df[dob_col].apply(lambda x: int(x[4:8])) > 10]

    return df[[df.columns[0], dob_col]]


def check_valid_national(df, national_col):
    """ Cleaning National ID with format:
            - 9 or 12 digits
            - Remove invalid number (^0{3} or ^123 or 9{9} or 1{9})

        Args:
            df : DataFrame, containing PII data
            national_col : National ID column

        Returns:
            df : The DataFrame with CustomerID and new National ID
    """

    df = df[df[national_col].notnull()]
    df[national_col] = df[national_col].apply(lambda x: x.strip())
    df = df[~df[national_col].str.contains('^0{3}|^123|9{9}|1{9}')]
    df[national_col] = df[national_col].apply(lambda x: re.sub('[^0-9]', '', str(x)))
    df = df[(df[national_col].str.len() == 9) | (df[national_col].str.len() == 12)]

    return df


def fix_duplicated_national(df, national_col):
    """ For those who have the same National_ID, take the one who have active ebank
        Args:
            df : DataFrame, containing valid national id
            national_col : National ID column

        Returns:
            df : The DataFrame with CustomerID and new National ID without duplication
    """

    id_count = df[national_col].value_counts().reset_index()
    id_count.columns = [national_col, 'COUNT']
    # id unique
    id_uniq = id_count[id_count['COUNT'] == 1]
    id_uniq_cus = df[df[national_col].isin(id_uniq[national_col])][['CUSID', national_col]]
    # id duplicated
    id_dup = id_count[id_count['COUNT'] > 1]
    id_dup_cus = df[df[national_col].isin(id_dup[national_col])]
    # for those duplicated id, choose customer who has active eb
    id_dup_active = id_dup_cus[id_dup_cus['EBANK_STATUS'] == 'ACTIVE']
    id_dup_active = id_dup_active.sort_values(['LAST_LOGIN_FMB'], ascending=False). \
        drop_duplicates([national_col], keep='first')[['CUSID', national_col]]

    return pd.concat([id_uniq_cus, id_dup_active])


def passport_cleaning(df, passport_col):
    """ Cleaning Passport with format:
            - Remove redundant space
            - Remove punctuation

        Args:
            df : DataFrame, containing PII data
            passport_col : National ID column

        Returns:
            df : The DataFrame with CustomerID and new National ID
    """

    df = df[df[passport_col].notnull()]
    df[passport_col] = df[passport_col].apply(lambda x: x.strip())
    df[passport_col] = df[passport_col].apply(lambda x: "".join(x.split()))
    df[passport_col] = df[passport_col].apply(lambda x: re.sub(r'[^\w\s]', '', x))

    return df[[df.columns[0], passport_col]]


def phone_cleaning(df, phone_col):
    """ Cleaning Phone with format:
        - 10 digits, start with 0
        - In case of old prefix, convert to new prefix
        - Remove invalid number (contains 0{10} or start with 01|02|04|06)
        - Remove whitespace at the beginning and end (both sides) of a string

        Args:
            df : DataFrame, containing PII data
            phone_col : Phone column

        Returns:
            df : The DataFrame with CustomerID and new National ID without duplication
    """

    # Dictionary to replace old prefix by new prefix
    phone_dict = {"0162": "032", "0163": "033", "0164": "034", "0165": "035", "0166": "036", "0167": "037",
                  "0168": "038", "0169": "039", "0120": "070", "0121": "079", "0122": "077", "0126": "076",
                  "0128": "078", "0123": "083", "0124": "084", "0125": "085", "0127": "081", "0129": "082",
                  "0186": "056", "0188": "058", "0199": "059"}

    df = df[df[phone_col].notnull()]
    df[phone_col] = df[phone_col].apply(lambda x: x.strip())
    df[phone_col] = df[phone_col].apply(lambda x: re.sub('[^0-9]', '', str(x)))  # remove non-digit character
    df[phone_col] = df[phone_col].apply(lambda x: x.lstrip("0"))  # remove all first 0
    df[phone_col] = df[phone_col].apply(lambda x: '0' + x)  # add 0
    df[phone_col] = df[phone_col].apply(
        lambda x: phone_dict[x[:4]] + x[4:]
        if len(x) == 11 and x[:4] in (phone_dict.keys()) else x)  # convert old prefix to new prefix
    df = df[~df[phone_col].str.contains('0{10}|^01|^02|^04|^06')]  # remove invalid number
    df = df[df[phone_col].str.len() == 10]  # only take 10-digits phone number (also exclude fixed/home phone number)

    return df[[df.columns[0], phone_col]]


def name_cleaning(df, name_col):
    """Cleaning Name with format:
        - Order: 'last name' then 'first name'
        - Only 1 space between words
        - Lowercase letters

    Args:
        df : DataFrame, containing PII data
        name_col : Name column

    Returns:
        df: The DataFrame with CustomerID and new Name.
    """

    df = df[~df[name_col].str.contains('khong su dung')]
    df[name_col] = df[name_col].apply(lambda x: x.strip())
    df[name_col] = df[name_col].apply(lambda x: re.sub(r'[^\w\s]', ' ', x).lower())
    df['len'] = df[name_col].apply(lambda x: len(x.split()))
    df = df[df['len'] > 1]
    df[name_col] = df[name_col].apply(lambda x: " ".join(x.split()))
    ori_name_lst = df[name_col]
    new_lst = []
    for x in ori_name_lst:
        # (1) Remove punctuation and replace by space, (2) lower case, and (3) split
        x = re.sub(r'[^\w\s]', ' ', x).lower().split()
        # Rejoin, keep only last name and first name
        if len(x) > 1:
            new_lst.append(x[0] + ' ' + x[len(x) - 1])
        else:
            new_lst.append(x)
    df['short_name'] = new_lst

    return df[[df.columns[0], name_col, 'short_name']]


def email_string_cleaning(df, email_col):
    """Cleaning email string: remove redundant punctuation, space

    Args:
        df: DataFrame containing PII
        email_col: Email column

    Returns:
        df: The DataFrame with CustomerID and new Email.
    """
    df = df[df[email_col].notnull()]
    df[email_col] = df[email_col].apply(lambda x: x.strip())
    df[email_col] = df[email_col].apply(lambda x: x.strip(string.punctuation))  # remove punctuation
    # df[email_col] = df[email_col].apply(lambda x: x.strip(punctuation))  # remove . at the end of string
    df[email_col] = df[email_col].apply(lambda x: "".join(x.split()))  # remove space
    df[email_col] = df[email_col].str.lower()
    df[email_col] = df[email_col].str.replace('@@', '@')
    df = df[~df[email_col].str.contains('^nobody@|^khongco@|^khongcoemail@|^kco@|^khongcomail@|kcomail@|'
                                        '^123@|^456@|^abc@|^xyz@')]

    return df[[df.columns[0], email_col]]


def check_valid_email(df, email_col):
    """Checking a valid email with format <name>@<domain> and right domain
     Args:
        df: DataFrame containing PII after cleaning string
        email_col: Email column

    Returns:
        df: The DataFrame with CustomerID and new Email.
    """
    regex_email = r"[^@\s]+@[^@\s]+\.[^@\s.]+$"
    df[email_col] = df[email_col].apply(lambda x: x if re.match(regex_email, x) is not None else None)
    df = df[df[email_col].notnull()]

    # fix wrong email domain (following email dictionary)
    email_dict = pd.read_csv('fix_email.csv')
    email_dict = email_dict.drop(columns=['IMPORT_DATE'])
    email_dict = email_dict.set_index('DOMAIN').T.to_dict('records')
    email_dict = email_dict[0]

    df['domain'] = df[email_col].apply(lambda x: x.split('@')[1])
    df['domain'] = df['domain'].apply(lambda x: email_dict[x] if x in email_dict.keys() else x)
    # df.loc[:,'domain'] = df.loc[:, 'domain'].map(email_dict)
    df['username'] = df[email_col].apply(lambda x: x.split('@')[0])
    df[email_col] = df['username'] + '@' + df['domain']

    return df[[df.columns[0], email_col]]


def tcb_hash(df):
    """Hash cleaned data using hashlib 'SHA256' and key '3W9G997Ie0f0hK9tH'

    Args:
        df : Cleaned PII DataFrame

    Returns:
        df : Hashed DataFrame
    """

    import hashlib
    # hash all columns except SEGMENT
    # for col in df.columns:
    for col in [x for x in df.columns if x != 'SEGMENT']:
        # print(col)
        df.loc[:, col] = df[col].astype('str')
        df.loc[:, col] = df[col].apply(lambda x:
                                       hashlib.sha256(x.encode('utf-8') +
                                                      '3W9G997Ie0f0hK9tH'.encode('utf-8')).hexdigest()
                                       if x not in ['None', 'nan'] else None)
        df.loc[:, col] = df[col].apply(lambda x: x.upper() if x is not None else None)
    return df