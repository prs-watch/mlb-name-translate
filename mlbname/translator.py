import pandas as pd
import requests
import pickle
import os

# consts
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICKLE_PATH = f"{APP_ROOT}/pickle/names.pickle"

def __gen_name_df(url):
    """Private function to generate DataFrame from wiki page.

    Args:
        url (str): Wiki's url

    Returns:
        pandas.DataFrame: DataFrame that will be converted into name dictionary.
    """
    res = requests.get(url)
    try:
        data = pd.read_html(res.content, header=0)[2]
        data = data.rename(columns={"選手名(日本語)": "jp_name", "選手名(英語)":"en_name"})
        data = data.drop("初年", axis=1)
        data = data.drop("最終年", axis=1)
        data = data.drop("特記事項", axis=1)
        data = data[~(data["en_name"].str.contains("[編集]"))]
        return data
    except:
        return None

def __trans_df_into_dict(data):
    """Converte DataFrame to dictionary.

    Args:
        data (pandas.DataFrame): DataFrame.

    Returns:
        dict: Name dictionary.
    """
    data["en_name_f"] = data["en_name"].str.split(" ", expand=True)[0]
    data["en_name_l"] = data["en_name"].str.split(" ", expand=True)[1]
    data["jp_name_f"] = data["jp_name"].str.split("・", expand=True)[0]
    data["jp_name_l"] = data["jp_name"].str.split("・", expand=True)[1]
    fullname_dict = dict(zip(data["en_name"], data["jp_name"]))
    fname_dict = dict(zip(data["en_name_f"], data["jp_name_f"]))
    lname_dict = dict(zip(data["en_name_l"], data["jp_name_l"]))
    return fullname_dict, fname_dict, lname_dict

def __get_names(do_update):
    """Get name dictionary.

    Args:
        do_update (boolean): If True, English-Japansese dictionary will be updated.

    Returns:
        tuple: Name dictionaries.
    """
    # use pickle data if update is not requested.
    if not do_update and os.path.exists(PICKLE_PATH):
        print("Load pickled dictionary..")
        with open(f"{APP_ROOT}/pickle/names.pickle", "rb") as f:
            return pickle.load(f)
    # create new dictionary.
    start_char = ord('A')
    end_char = ord('Z')
    chars = range(start_char, end_char + 1)
    df = pd.DataFrame()
    print("Generate name dictionary..")
    for char in chars:
        alph = chr(char)
        url = f"https://ja.wikipedia.org/wiki/メジャーリーグベースボールの選手一覧_{alph}"

        print(f"{alph}..")
        df = pd.concat([df, __gen_name_df(url)])
    names = __trans_df_into_dict(df)

    with open(PICKLE_PATH, "wb") as f:
        print("Save dictionary..")
        pickle.dump(names, f)
    return names

def __translate(target, do_update):
    """Translate name into Japanese.

    Args:
        target (str): Name that you want to translate into Japanese.
        do_update (boolean): If True, English-Japansese dictionary will be updated.

    Returns:
        str: Translated name.
    """
    print(f"Translate {target}..")
    names = __get_names(do_update)
    fullnames = names[0]
    if target in fullnames:
        return fullnames[target]
    else:
        firstnames = names[1]
        lastnames = names[2]
        target_first = target.split(" ")[0]
        target_last = target.split(" ")[1]
        if (target_first in firstnames) and (target_last in lastnames):
            return firstnames[target_first] + "・" + lastnames[target_last]
        # If translation fails, return ordinal name.
        return target

def translate(target, do_update):
    """Execute translating.

    Args:
        target (str): Name that you want to translate into Japanese.
        do_update (boolean): If True, English-Japansese dictionary will be updated.

    Returns:
        str: Translated name.
    """
    return __translate(target, do_update)