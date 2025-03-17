from arelle import ModelManager
from arelle import Cntlr
import os
import glob
import re
from bs4 import BeautifulSoup

"""
取得する項目をリストとして格納するための関数
"""
def make_edinet_company_info_list(xbrl_files):
    edinet_company_info_list = []
    for index, xbrl_file in enumerate(xbrl_files):
        company_data = {
            "EDINETCODE": "",
            "企業名": "",
            "事業等のリスク": "",
        }

        ctrl = Cntlr.Cntlr()
        model_manager = ModelManager.initialize(ctrl)

        model_xbrl = model_manager.load(xbrl_file)
        print("XBRLファイルを読み込んでいます", ":", index + 1, "/", len(xbrl_files))

        # 実データを探して取得
        for fact in model_xbrl.facts:

            #  EDINETコードを探す
            if fact.concept.qname.localName == 'EDINETCodeDEI':
                company_data["EDINETCODE"] = fact.value

            # 企業名を探す
            elif fact.concept.qname.localName == 'FilerNameInJapaneseDEI':
                company_data["企業名"] = fact.value

            # 事業等のリスクを探す
            elif fact.concept.qname.localName == 'BusinessRisksTextBlock': 
                if fact.contextID == 'FilingDateInstant':
                    company_data["事業等のリスク"] = fact.value										
                    """
                    BeautifulSoupとreモジュールを使用してデータクレンジングをする
                    """
                    soup = BeautifulSoup(company_data["事業等のリスク"], "html.parser")
                    company_data["事業等のリスク"] = soup.get_text()

                    company_data["事業等のリスク"] = re.sub(r'\s', '', company_data["事業等のリスク"]).strip()

        # 見つけたデータをリストに入れる
        edinet_company_info_list.append([
            company_data["EDINETCODE"],
            company_data["企業名"],
            company_data["事業等のリスク"],
        ])

    return edinet_company_info_list

"""
元データのパスを指定し、すべての処理を実行する関数
"""
def main():
	# あなたのXBRLファイルのパスを指定(ただコピーしても動きません)
    xbrl_files = glob.glob(r'C:\\Users\\ryoun\\test_xbrl_book\\XBRL_file\\*\\*\\XBRL\\PublicDoc\\*.xbrl')

    company_info = make_edinet_company_info_list(xbrl_files)
    for info in company_info:
        print(info)

    print("extract finish")

if __name__ == "__main__":
    main()