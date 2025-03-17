from arelle import ModelManager
from arelle import Cntlr
import os
import glob

"""
取得する項目をリストとして保管するための関数
"""
def make_edinet_company_info_list(xbrl_files):
    edinet_company_info_list = []
    """
    XBRLファイルを複数社すべて読み込む処理
    """
    for index, xbrl_file in enumerate(xbrl_files):
        company_data = {
            "EDINETCODE": "",
            "企業名": "",
            "営業利益(IFRS)": "",
        }

        ctrl = Cntlr.Cntlr()
        model_manager = ModelManager.initialize(ctrl)

        model_xbrl = model_manager.load(xbrl_file)
        print("XBRLファイルを読み込んでいます", ":", index + 1, "/", len(xbrl_files))

        # 実データを探して取得
        for fact in model_xbrl.facts:

            # EDINETコードを探す
            if fact.concept.qname.localName == 'EDINETCodeDEI':
                company_data["EDINETCODE"] = fact.value

            # 企業名を探す
            elif fact.concept.qname.localName == 'FilerNameInJapaneseDEI':
                company_data["企業名"] = fact.value

            # 営業利益(IFRS)を探す
            elif fact.concept.qname.localName == 'OperatingProfitLossIFRS': 
                if fact.contextID == 'CurrentYearDuration':
                    company_data["営業利益(IFRS)"] = fact.value

        # 見つけたデータをリストに入れる
        edinet_company_info_list.append([
            company_data["EDINETCODE"],
            company_data["企業名"],
            company_data["営業利益(IFRS)"],
        ])
    
    return edinet_company_info_list

"""
元データのパスを指定し、すべての処理を実行する関数
"""
def main():
    """
    main()で指定したXBRLファイルパスを正規表現で指定
    あなたのXBRLファイルのパスを指定(ただコピーしても動きません)
    """
    xbrl_files = glob.glob(r'C:\\Users\\ryoun\\test_xbrl_book\\XBRL_file\\*\\*\\XBRL\\PublicDoc\\*.xbrl')

    company_info = make_edinet_company_info_list(xbrl_files)
    for info in company_info:
        print(info)

    print("extract finish")

if __name__ == "__main__":
    main()
