from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from arelle import ModelManager
from arelle import Cntlr
import os, time, glob

"""
データベースのモデル定義と基本設定
"""
DATABASE_URL = "sqlite:///company_data.db"
Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    edinet_code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    OperatingProfitLoss = Column(Integer, nullable=False)

"""
データベースのエンジンとセッションをセットアップする関数
"""
def setup_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

"""
8章で使用した、10社の企業情報を抽出する関数
"""
def make_edinet_company_info_list(xbrl_files):
    edinet_company_info_list = []
    for index, xbrl_file in enumerate(xbrl_files):
        company_data = {"EDINETCODE": "", "企業名": "", "営業利益(IFRS)": ""}
        
        ctrl = Cntlr.Cntlr()
        model_manager = ModelManager.initialize(ctrl)
        model_xbrl = model_manager.load(xbrl_file)
        print("XBRLファイルを読み込んでいます", ":", index + 1, "/", len(xbrl_files))

        for fact in model_xbrl.facts:
            if fact.concept.qname.localName == 'EDINETCodeDEI':
                company_data["EDINETCODE"] = fact.value
            elif fact.concept.qname.localName == 'FilerNameInJapaneseDEI':
                company_data["企業名"] = fact.value
            elif fact.concept.qname.localName == 'OperatingProfitLossIFRS' and fact.contextID == 'CurrentYearDuration':
                company_data["営業利益(IFRS)"] = fact.value

        edinet_company_info_list.append([
            company_data["EDINETCODE"],
            company_data["企業名"],
            company_data["営業利益(IFRS)"],
        ])
    print(edinet_company_info_list)
    return edinet_company_info_list

"""
企業データをデータベースに生成する関数
"""
def create_company_data(session, company_list):
    for company_info in company_list:
        time.sleep(2)
        print("企業データを登録しています", ":", company_info[1])
        new_company = Company(
            edinet_code=company_info[0],
            name=company_info[1],
            OperatingProfitLoss=int(company_info[2]) if company_info[2] else 0
        )
        session.add(new_company)
        session.commit()

# データを読み込む関数
def read_company():
    session = setup_database()
    # テーブルに存在するデータをすべて取得
    companies = session.query(Company).all()
    for company in companies:
        print(f"EDINET Code: {company.edinet_code}, Name: {company.name}, Operating Profit Loss: {company.OperatingProfitLoss}")
    session.close()
    
# データを更新する関数
def update_company(edinet_code, new_name=None, new_profit_loss=None):
    session = setup_database()
    # edinet_codeに任意のEDINETコードを指定することでその行だけ更新
    company = session.query(Company).filter(Company.edinet_code == edinet_code).first()
    if company:
        if new_name:
            company.name = new_name
        if new_profit_loss is not None:
            company.OperatingProfitLoss = new_profit_loss
        session.commit()
        print(f"データを更新しました: {company.edinet_code}")
    else:
        print("指定された企業が見つかりません")
    session.close()
    
# データを削除する関数
def delete_company(edinet_code):
    session = setup_database()
    # edinet_codeに任意のEDINETコードを指定することでその行だけ削除
    company = session.query(Company).filter(Company.edinet_code == edinet_code).first()
    if company:
        session.delete(company)
        session.commit()
        print(f"データを削除しました: {company.edinet_code}")
    else:
        print("削除する企業が見つかりません")
    session.close()

"""
メイン処理: XBRLファイルを解析し、データベースに登録する関数
"""
def main():
    session = setup_database()
    xbrl_files = glob.glob(r'C:\\Users\\ryoun\\test_xbrl_book\\XBRL_file\\Xbrl_Search_20250307_111123\\S100TR7I\\XBRL\\PublicDoc\\*.xbrl')
    edinet_company_info_list = make_edinet_company_info_list(xbrl_files)
    create_company_data(session, edinet_company_info_list)
    session.close()

if __name__ == "__main__":
    main()
