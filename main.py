import json

import requests

APILink = "https://sky.shiiyu.moe/api/v2/"


def main_text():
    text = open("main_text.txt", "r")
    print(text.read())


def api_status(link):
    try:
        request = requests.get(link)
        return request.status_code
    except:
        return 0


def api_json_get(link):
    try:
        request = requests.get(link)
        return request.json()
    except:
        return


def file_json_get(data, parameters):
    with open(data) as file:
        data = file.read()
    obj = json.loads(data)
    try:
        return str(obj[parameters])
    except:
        return '{"sellPrice": null, "buyPrice": null}'


if __name__ == '__main__':
    main_text()
    APIStatus = api_status(APILink)
    if APIStatus:
        print("API Status:", APIStatus)
        choose = input("1- Bazaar Sell\n2- NPC Sell\n3- Bazaar Item List\n0- Exit\n")
        # Bazaar Sell
        if choose == "1":
            bazaar_json = str(api_json_get(APILink + "bazaar"))
            bazaar_split = bazaar_json.split(sep=',')
            for i in range(len(bazaar_split)):
                if 'sellPrice' in bazaar_split[i]:
                    itemSellPrice = bazaar_split[i].split(':')
                    itemName_json = bazaar_split[i - 2].split(':')
                    itemName = itemName_json[1].replace('\'', '').removeprefix(' ')
                    npc_json = file_json_get("npcPrice.json", itemName).removeprefix('{').removesuffix('}').split(
                        sep=',')
                    npcBuyPrice = npc_json[1].split(sep=':')
                    try:
                        itemProfit = float(itemSellPrice[1]) - float(npcBuyPrice[1])
                        if itemProfit > 0:
                            print(itemName + ": " + str(itemProfit) + " $")
                    except:
                        pass
            print('Done!')
        # NPC Sell
        if choose == "2":
            bazaar_json = str(api_json_get(APILink + "bazaar"))
            bazaar_split = bazaar_json.split(sep=',')
            for i in range(len(bazaar_split)):
                if 'sellPrice' in bazaar_split[i]:
                    itemBuyPrice = bazaar_split[i-1].split(':')
                    itemName_json = bazaar_split[i - 2].split(':')
                    itemName = itemName_json[1].replace('\'', '').removeprefix(' ')
                    npc_json = file_json_get("npcPrice.json", itemName).removeprefix('{').removesuffix('}').split(
                        sep=',')
                    npcSellPrice = npc_json[0].split(sep=':')
                    try:
                        itemProfit = float(npcSellPrice[1]) - float(itemBuyPrice[1])
                        if itemProfit > 0:
                            print(itemName + ": " + str(itemProfit) + " $")
                    except:
                        pass
            print('Done!')
        # NPC Sell
        if choose == "2":
            pass
        # Bazaar Item List
        if choose == "3":
            itemList = open('BazaarItemList.txt', "w")
            bazaar_json = str(api_json_get(APILink + "bazaar"))
            bazaar_split = bazaar_json.split(sep=',')
            for i in range(len(bazaar_split)):
                if 'sellPrice' in bazaar_split[i]:
                    itemName = bazaar_split[i - 2].split(':')
                    itemList.write(itemName[1].replace('\'', '') + '\n')
            print('Done!')
            itemList.close()
        #
    else:
        print("Erreur de connection à l'API")
