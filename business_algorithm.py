import cv2 as cv
import numpy as np
import os


class BusinessAlgorithm:
    def __init__(self):
        self.capacity_limit = 19
        self.armor_reference = 2700
        self.ninjin_reference = 7500
        self.sesame_oil_reference = 4000
        self.bell_reference = 4300
        self.pearl_reference = 5000
        self.jewelry_reference = 4300
        self.currency_reference = 3000
        self.luminous_pearl_reference = 8000
        self.armor_purchase = None
        self.ninjin_purchase = None
        self.sesame_oil_purchase = None
        self.bell_purchase = None
        self.pearl_purchase = None
        self.jewelry_purchase = None
        self.currency_purchase = None
        self.luminous_pearl_purchase = None

    # public:
    # 北俱芦洲买入计算
    def north_julu_buy_calculate(self, existing_check_amount, existing_capacity, armor_price, ninjin_price,
                                 sesame_oil_price, bell_price):
        # 输入:
        # existing_check_amount 现有的支票数量
        # existing_capacity 背包里已购买的商品数量
        # armor_price 衣甲价格
        # ninjin_price 人参价格
        # sesame_oil_price 香油价格
        # bell_price 铃铛价格
        # 输出:
        # best_earn 最佳预期能赚的价格
        # best_selection 最佳的选择商品(字符串)
        best_earn = None
        best_selection = None
        if armor_price < self.armor_reference:
            single_earn = self.single_buy_earn(existing_check_amount, existing_capacity, armor_price,
                                               self.armor_reference)
            if single_earn > 0:
                best_earn = single_earn
                best_selection = 'armor'
        if ninjin_price < self.ninjin_reference:
            single_earn = self.single_buy_earn(existing_check_amount, existing_capacity, ninjin_price,
                                               self.ninjin_reference)
            if single_earn > 0:
                if best_earn is None or single_earn > best_earn:
                    best_earn = single_earn
                    best_selection = 'ninjin'
        if sesame_oil_price < self.sesame_oil_reference:
            single_earn = self.single_buy_earn(existing_check_amount, existing_capacity, sesame_oil_price,
                                               self.sesame_oil_reference)
            if single_earn > 0:
                if best_earn is None or single_earn > best_earn:
                    best_earn = single_earn
                    best_selection = 'sesame_oil'
        if bell_price < self.bell_reference:
            single_earn = self.single_buy_earn(existing_check_amount, existing_capacity, bell_price,
                                               self.bell_reference)
            if single_earn > 0:
                if best_earn is None or single_earn > best_earn:
                    best_earn = single_earn
                    best_selection = 'bell'
        return best_earn, best_selection

    # 地府买入计算
    def nether_world_buy_calculate(self, existing_check_amount, existing_capacity, pearl_price, jewelry_price,
                                   currency_price, luminous_pearl_price):
        # 输入:
        # existing_check_amount 现有的支票数量
        # existing_capacity 背包里已购买的商品数量
        # pearl_price 珍珠价格
        # jewelry_price 首饰价格
        # currency_price 纸钱价格
        # luminous_pearl_price 夜明珠价格
        # 输出:
        # best_earn 最佳预期能赚的价格
        # best_selection 最佳的选择商品(字符串)
        best_earn = None
        best_selection = None
        if pearl_price < self.pearl_reference:
            single_earn = self.single_buy_earn(existing_check_amount, existing_capacity, pearl_price,
                                               self.pearl_reference)
            if single_earn > 0:
                best_earn = single_earn
                best_selection = 'pearl'

        if jewelry_price < self.jewelry_reference:
            single_earn = self.single_buy_earn(existing_check_amount, existing_capacity, jewelry_price,
                                               self.jewelry_reference)
            if single_earn > 0:
                if best_earn is None or single_earn > best_earn:
                    best_earn = single_earn
                    best_selection = 'jewelry'
        if currency_price < self.currency_reference:
            single_earn = self.single_buy_earn(existing_check_amount, existing_capacity, currency_price,
                                               self.currency_reference)
            if single_earn > 0:
                if best_earn is None or single_earn > best_earn:
                    best_earn = single_earn
                    best_selection = 'currency'
        if luminous_pearl_price < self.luminous_pearl_reference:
            single_earn = self.single_buy_earn(existing_check_amount, existing_capacity, luminous_pearl_price,
                                               self.luminous_pearl_reference)
            if single_earn > 0:
                if best_earn is None or single_earn > best_earn:
                    best_earn = single_earn
                    best_selection = 'luminous_pearl'
        return best_earn, best_selection

    # 北俱芦洲卖出计算
    def north_julu_sell_calculate(self, pearl_price, jewelry_price, currency_price, luminous_pearl_price):
        # 输入:
        # pearl_price 珍珠价格
        # jewelry_price 首饰价格
        # currency_price 纸钱价格
        # luminous_pearl_price 夜明珠价格
        # 输出:
        # sold_dict 需要卖出的商品和其能赚的金额的字典
        sold_dict = {"jewelry": None, 'pearl': None, 'currency': None, 'luminous_pearl': None}
        if pearl_price is not None and self.pearl_purchase is not None:
            if pearl_price > self.pearl_purchase:
                sold_dict['pearl'] = pearl_price - self.pearl_purchase
        if jewelry_price is not None and self.jewelry_purchase is not None:
            if jewelry_price > self.jewelry_purchase:
                sold_dict['jewelry'] = jewelry_price - self.jewelry_purchase
        if currency_price is not None and self.currency_purchase is not None:
            if currency_price > self.currency_purchase:
                sold_dict['currency'] = currency_price - self.currency_purchase
        if luminous_pearl_price is not None and self.luminous_pearl_purchase is not None:
            if luminous_pearl_price > self.luminous_pearl_purchase:
                sold_dict['luminous_pearl'] = luminous_pearl_price - self.luminous_pearl_purchase
        return sold_dict

    # 地府卖出计算
    def nether_world_sell(self, armor_price, ninjin_price, sesame_oil_price, bell_price):
        # 输入:
        # armor_price 衣甲价格
        # ninjin_price 人参价格
        # sesame_oil_price 香油价格
        # bell_price 铃铛价格
        # 输出:
        # sold_dict 需要卖出的商品和其能赚的金额的字典
        sold_dict = {"armor": None, 'ninjin': None, 'sesame_oil': None, 'bell': None}
        if armor_price is not None and self.armor_purchase is not None:
            if armor_price > self.armor_purchase:
                sold_dict['armor'] = armor_price - self.armor_purchase
        if ninjin_price is not None and self.ninjin_purchase is not None:
            if ninjin_price > self.ninjin_purchase:
                sold_dict['ninjin'] = ninjin_price - self.ninjin_purchase
        if sesame_oil_price is not None and self.sesame_oil_purchase is not None:
            if sesame_oil_price > self.sesame_oil_purchase:
                sold_dict['sesame_oil'] = sesame_oil_price - self.sesame_oil_purchase
        if bell_price is not None and self.bell_purchase is not None:
            if bell_price > self.bell_purchase:
                sold_dict['bell'] = bell_price - self.bell_purchase
        return sold_dict

    # 两个商人买入价格对比(北俱芦洲地府通用)
    @staticmethod
    def buy_contrast(best_earn1, best_selection1, best_earn2, best_selection2):
        # 输入:
        # best_earn1 商人1处预期能赚的价格
        # best_selection1 商人1处选择的商品
        # best_earn2 商人2处预期能赚的价格
        # best_selection2 商人2处选择的商品
        # 输出:
        # 同输入，进行对比后，只保留更优的商人的结果
        if best_earn1 is not None and best_earn2 is not None:
            if best_earn1 > best_earn2:
                best_earn2 = None
                best_selection2 = None
            else:
                best_earn1 = None
                best_selection1 = None
        return best_earn1, best_selection1, best_earn2, best_selection2

    # 是否等待商品价格更新再购买(北俱芦洲地府通用)
    @staticmethod
    def if_wait_for_next_buy(best_earn1, best_earn2):
        # 输入:
        # best_earn1 商人1处预期能赚的价格
        # best_earn2 商人2处预期能赚的价格
        # 输出:
        # 返回True表示进行等待，为False表示不等待更新，在本轮时间进行买入操作
        if best_earn1 is None and best_earn2 is None:
            return True
        else:
            return False

    # 买入操作(北俱芦洲和地府通用)
    def buy_action(self, best_selection, price):
        # 输入:
        # best_selection 选择的商品
        # price 商品的价格
        # 输出:
        # 无
        if best_selection is None:
            return
        if best_selection == "armor":
            self.armor_purchase = price
        elif best_selection == "ninjin":
            self.ninjin_purchase = price
        elif best_selection == "sesame_oil":
            self.sesame_oil_purchase = price
        elif best_selection == "bell":
            self.bell_purchase = price
        elif best_selection == "pearl":
            self.pearl_purchase = price
        elif best_selection == "jewelry":
            self.jewelry_purchase = price
        elif best_selection == "currency":
            self.currency_purchase = price
        elif best_selection == "luminous_pearl":
            self.luminous_pearl_purchase = price
        else:
            print("unknown selection item")

    # 两个商人卖出价格对比(北俱芦洲地府通用)
    @staticmethod
    def sell_contrast(sold_dict1, sold_dict2):
        # 输入:
        # sold_dict1 商人1处卖出商品及能赚金额的字典
        # sold_dict2 商人2处卖出商品及能赚金额的字典
        # 输出:
        # 同输入，进行对比后，只保留更优的商人的结果
        for key in sold_dict1.keys():
            if key in sold_dict2.keys():
                if sold_dict1[key] is not None and sold_dict2[key] is not None:
                    if sold_dict1[key] > sold_dict2[key]:
                        sold_dict2[key] = None
                    else:
                        sold_dict1[key] = None
        return sold_dict1, sold_dict2

    # 是否需要等待商品价格更新再卖出(北俱芦洲地府通用)
    def if_wait_for_next_sell(self, sold_dict1, sold_dict2):
        # 输入:
        # sold_dict1 商人1处卖出商品及能赚金额的字典
        # sold_dict2 商人2处卖出商品及能赚金额的字典
        # 输出:
        # 返回True表示进行等待，为False表示不等待更新，在本轮时间进行卖出操作
        if self.armor_purchase is not None:
            if 'armor' in sold_dict1.keys() and 'armor' in sold_dict2.keys():
                if sold_dict1['armor'] is None and sold_dict2['armor'] is None:
                    return True
        if self.ninjin_purchase is not None:
            if 'ninjin' in sold_dict1.keys() and 'ninjin' in sold_dict2.keys():
                if sold_dict1['ninjin'] is None and sold_dict2['ninjin'] is None:
                    return True
        if self.sesame_oil_purchase is not None:
            if 'sesame_oil' in sold_dict1.keys() and 'sesame_oil' in sold_dict2.keys():
                if sold_dict1['sesame_oil'] is None and sold_dict2['sesame_oil'] is None:
                    return True
        if self.bell_purchase is not None:
            if 'bell' in sold_dict1.keys() and 'bell' in sold_dict2.keys():
                if sold_dict1['bell'] is None and sold_dict2['bell'] is None:
                    return True
        if self.pearl_purchase is not None:
            if 'pearl' in sold_dict1.keys() and 'pearl' in sold_dict2.keys():
                if sold_dict1['pearl'] is None and sold_dict2['pearl'] is None:
                    return True
        if self.jewelry_purchase is not None:
            if 'jewelry' in sold_dict1.keys() and 'jewelry' in sold_dict2.keys():
                if sold_dict1['jewelry'] is None and sold_dict2['jewelry'] is None:
                    return True
        if self.currency_purchase is not None:
            if 'currency' in sold_dict1.keys() and 'currency' in sold_dict2.keys():
                if sold_dict1['currency'] is None and sold_dict2['currency'] is None:
                    return True
        if self.luminous_pearl_purchase is not None:
            if 'luminous_pearl' in sold_dict1.keys() and 'luminous_pearl' in sold_dict2.keys():
                if sold_dict1['luminous_pearl'] is None and sold_dict2['luminous_pearl'] is None:
                    return True
        return False

    # 卖出操作(北俱芦洲和地府通用)
    def sell_action(self, sold_dict):
        # 输入:
        # sold_dict 本交易的商人处卖出商品及能赚金额的字典
        # 输出:
        # 无
        for key in sold_dict.keys():
            if key == 'armor' and sold_dict[key] is not None:
                self.armor_purchase = None
            elif key == 'ninjin' and sold_dict[key] is not None:
                self.ninjin_purchase = None
            elif key == 'sesame_oil' and sold_dict[key] is not None:
                self.sesame_oil_purchase = None
            elif key == 'bell' and sold_dict[key] is not None:
                self.bell_purchase = None
            elif key == 'pearl' and sold_dict[key] is not None:
                self.pearl_purchase = None
            elif key == 'jewelry' and sold_dict[key] is not None:
                self.jewelry_purchase = None
            elif key == 'currency' and sold_dict[key] is not None:
                self.currency_purchase = None
            elif key == 'luminous_pearl' and sold_dict[key] is not None:
                self.luminous_pearl_purchase = None

    # private：
    # 计算单个商品商品买入会赚的价格
    def single_buy_earn(self, existing_check_amount, existing_capacity, price, reference):
        capacity = existing_check_amount//price
        if capacity > self.capacity_limit - existing_capacity:
            capacity = self.capacity_limit - existing_capacity
        single_earn = capacity * (reference - price)
        return single_earn
